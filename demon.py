import time
import json
import os
import numpy as np
from shared.context import LiveContextLoop

DATA_DIR = "simulation_data"
STATE_PATH = os.path.join(DATA_DIR, "latest.json")
CONTROL_PATH = os.path.join(DATA_DIR, "control.json")
RESET_PATH = os.path.join(DATA_DIR, "reset.json")

os.makedirs(DATA_DIR, exist_ok=True)

def read_control():
    try:
        with open(CONTROL_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {"play": True, "speed": 0.5}

def check_reset():
    """Check if a reset command has been issued"""
    try:
        if os.path.exists(RESET_PATH):
            with open(RESET_PATH, "r") as f:
                reset_data = json.load(f)
            # Remove the reset file after reading
            os.remove(RESET_PATH)
            return True
    except Exception:
        pass
    return False

def write_state(state):
    # Convert numpy arrays and sets to lists for JSON serialization
    def convert_for_json(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(item) for item in obj]
        else:
            return obj
    
    json_state = convert_for_json(state)
    
    with open(STATE_PATH, "w") as f:
        json.dump(json_state, f)
    # Clean up any other files in DATA_DIR except latest.json and control.json
    for fname in os.listdir(DATA_DIR):
        if fname not in ("latest.json", "control.json"):
            try:
                os.remove(os.path.join(DATA_DIR, fname))
            except Exception:
                pass

def main():
    print("🔄 Starting daemon initialization...")
    
    # Pass classes, not instances, to LiveContextLoop
    from arc_simulation.arc_sim import ArcSimulator
    from adam_simulation.adam_sim import AdamAgent
    from fuel_simulation.fuel_sim import FuelSimulator
    
    print("📦 Creating FuelSimulator...")
    fuel = FuelSimulator(n_agents=8)
    print("⚙️ Creating LiveContextLoop...")
    loop = LiveContextLoop(ArcSimulator, AdamAgent, fuel)
    print("✅ Daemon initialization complete!")
    
    step_count = 0
    while True:
        step_count += 1
        
        # Check for reset command first
        if check_reset():
            print("🔄 Reset command received - reinitializing simulation...")
            # Reinitialize all components
            fuel = FuelSimulator(n_agents=8)
            loop = LiveContextLoop(ArcSimulator, AdamAgent, fuel)
            print("✅ Simulation reset complete")
        
        control = read_control()
        
        if control.get("play", True):
            try:
                loop.step()
                if loop.logs:
                    write_state(loop.logs[-1])
            except Exception as e:
                print(f"❌ Error during step: {e}")
                import traceback
                traceback.print_exc()
        
        time.sleep(float(control.get("speed", 0.5)))

if __name__ == "__main__":
    main()
