#!/bin/bash
# Comprehensive startup script for the constitution simulation system

set -e  # Exit on any error

echo "🚀 Starting Constitution Simulation System..."
echo "================================================"

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down system..."
    
    # Kill background processes
    pkill -f "python demon.py" 2>/dev/null || true
    pkill -f "streamlit run" 2>/dev/null || true
    
    # Stop systemd service if running
    # systemctl --user stop demon.service 2>/dev/null || true
    
    # Deactivate virtual environment
    if [ "$VENV_ACTIVE" -eq 1 ]; then
        deactivate 2>/dev/null || true
        echo "✅ Virtual environment deactivated"
    fi
    
    echo "✅ System shutdown complete"
    exit 0
}

# Set up cleanup trap
trap cleanup EXIT INT TERM

# Step 1: Activate virtual environment
echo "📦 Activating virtual environment..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
    VENV_ACTIVE=1
    echo "✅ Virtual environment activated"
else
    echo "❌ No .venv directory found. Please run setup.sh first."
    exit 1
fi

# Step 2: Ensure simulation_data directory exists
echo "📁 Setting up data directory..."
mkdir -p simulation_data
echo "✅ Data directory ready"

# Step 3: Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "python demon.py" 2>/dev/null || true
pkill -f "streamlit run" 2>/dev/null || true
# systemctl --user stop demon.service 2>/dev/null || true
sleep 2
echo "✅ Cleanup complete"

# Step 4: Start the simulation daemon in background
echo "⚙️  Starting simulation daemon..."
python demon.py &
DAEMON_PID=$!
sleep 3

# Check if daemon started successfully
if ps -p $DAEMON_PID > /dev/null; then
    echo "✅ Simulation daemon started (PID: $DAEMON_PID)"
else
    echo "❌ Failed to start daemon"
    exit 1
fi

# Step 5: Verify data generation
echo "📊 Verifying data generation..."
sleep 5
if [ -f "simulation_data/latest.json" ]; then
    STEP=$(cat simulation_data/latest.json | jq -r '.step' 2>/dev/null || echo "unknown")
    echo "✅ Data generation confirmed (Step: $STEP)"
else
    echo "❌ No simulation data found"
    exit 1
fi

# Step 6: Start Streamlit dashboard
echo "🖥️  Starting web dashboard..."
echo "📍 Dashboard will be available at: http://localhost:8501"
echo "🎮 Use the sidebar controls to Play/Pause the simulation"
echo "🔄 Enable 'Auto-refresh Dashboard' for live animations"
echo ""
echo "Press Ctrl+C to stop the entire system"
echo "================================================"

# Start Streamlit (this will block until user interrupts)
streamlit run visualization/dashboard.py --server.port 8501 --server.address 0.0.0.0
