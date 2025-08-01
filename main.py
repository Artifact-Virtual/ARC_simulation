import sys
sys.path.append('.')

from arc_network.network import ArcNetwork
import time
import json

def print_detailed_state(state, step_count):
    """Print comprehensive simulation state with all details"""
    # Clear screen for better readability
    import os
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"{'='*80}")
    print(f"🌐 ARTIFACT VIRTUAL MULTI-ARC NETWORK - STEP {step_count}")
    print(f"{'='*80}")
    
    # 1. DETAILED ARC STATES
    print(f"\n🔗 ARC BLOCKCHAIN STATES:")
    print("-" * 50)
    for i, arc_state in enumerate(state['arcs']):
        print(f"\n  📊 ARC-{arc_state['arc_id']} Status:")
        print(f"     • Total Blocks: {len(arc_state['blocks'])}")
        print(f"     • Active Rules: {', '.join(arc_state['rules'])}")
        
        # Show recent blocks with details
        if arc_state['blocks']:
            print(f"     • Recent Blocks:")
            for block in arc_state['blocks'][-3:]:  # Last 3 blocks
                status_icon = "🔲" if block['valid'] else "❌"
                dispute_icon = "⚔️" if block.get('disputed', False) else ""
                print(f"       {status_icon} Block #{block['index']}: {block['content']} {dispute_icon}")
    
    # 2. ADAM PROTOCOL STATES
    print(f"\n🏛️ ADAM PROTOCOL STATES:")
    print("-" * 50)
    for i, adam_state in enumerate(state['adams']):
        print(f"  🤖 ADAM-{adam_state['arc_id']}:")
        print(f"     • Policy: {adam_state['policy']}")
        print(f"     • Council Events: {len(adam_state['council_log'])}")
        if adam_state['council_log']:
            latest_council = adam_state['council_log'][-1]
            print(f"     • Latest Council: {latest_council['reason']}")
    
    # 3. FUEL ECONOMY DETAILS
    print(f"\n⚡ FUEL ECONOMY STATUS:")
    print("-" * 50)
    mainnet_state = state['fuel_mainnet']
    print(f"  💰 Mainnet: ${mainnet_state['liquidity']:,.0f} @ ${mainnet_state['price']:.2f}")
    print(f"  🌉 Total Bridges: {len(mainnet_state['bridges'])}")
    
    if mainnet_state['bridges']:
        print(f"     • Recent Bridges:")
        for bridge in mainnet_state['bridges'][-3:]:
            print(f"       → ARC-{bridge['arc']}: ${bridge['amount']:,}")
    
    print(f"\n  🏪 Subnet States:")
    total_subnet_liquidity = 0
    for subnet_state in state['fuel_subnets']:
        total_subnet_liquidity += subnet_state['liquidity']
        print(f"     • ARC-{subnet_state['arc_id']}: ${subnet_state['liquidity']:,.0f}")
    
    print(f"  📈 Total Network Liquidity: ${mainnet_state['liquidity'] + total_subnet_liquidity:,.0f}")
    
    # 4. DETAILED AGENT ACTIVITIES
    print(f"\n🤖 AGENT NETWORK ACTIVITY:")
    print("-" * 50)
    
    # Group agents by type
    validators = [a for a in state['agents'] if a['type'] == 'validator']
    forecasters = [a for a in state['agents'] if a['type'] == 'forecaster']
    operators = [a for a in state['agents'] if a['type'] == 'operator']
    
    print(f"  ⚖️ Validators ({len(validators)}):")
    total_validator_earnings = sum(v['earnings'] for v in validators)
    for validator in validators:
        print(f"     • ARC-{validator['arc']} Validator: ${validator['earnings']} earned")
    print(f"     💰 Total Validator Earnings: ${total_validator_earnings}")
    
    print(f"\n  🔮 Forecasters ({len(forecasters)}):")
    total_forecaster_score = sum(f['score'] for f in forecasters)
    for forecaster in forecasters:
        print(f"     • ARC-{forecaster['arc']} Forecaster: {forecaster['score']} correct predictions")
    print(f"     🎯 Total Predictions: {total_forecaster_score}")
    
    print(f"\n  ⚙️ Operators ({len(operators)}):")
    total_jobs = sum(o['jobs_done'] for o in operators)
    for operator in operators:
        print(f"     • ARC-{operator['arc']} Operator: {operator['jobs_done']} jobs completed")
    print(f"     🔧 Total Jobs: {total_jobs}")
    
    # 5. CROSS-ARC MESSAGING & EVENTS
    print(f"\n📡 CROSS-ARC MESSAGING:")
    print("-" * 50)
    events = state['messages']['events']
    if events:
        print(f"  🚨 Active Events ({len(events)}):")
        for event in events:
            if event.get('type') == 'block_challenge':
                print(f"     ⚔️ Block Challenge: ARC-{event.get('from_arc')} → ARC-{event.get('target_arc')}")
            elif event.get('type') == 'fuel_bridge_complete':
                print(f"     🌉 Bridge Complete: ARC-{event.get('arc')} received ${event.get('amount'):,}")
            else:
                print(f"     📨 {event.get('type', 'Unknown')}: {str(event)[:60]}...")
    else:
        print(f"  🔲 No active cross-ARC events")
    
    # 6. NETWORK STATISTICS & TRENDS
    print(f"\n📊 NETWORK STATISTICS:")
    print("-" * 50)
    
    total_blocks = sum(len(arc['blocks']) for arc in state['arcs'])
    total_valid_blocks = sum(sum(1 for block in arc['blocks'] if block['valid']) for arc in state['arcs'])
    total_disputed_blocks = sum(sum(1 for block in arc['blocks'] if block.get('disputed', False)) for arc in state['arcs'])
    
    print(f"  🔗 Total Blocks: {total_blocks}")
    print(f"  🔲 Valid Blocks: {total_valid_blocks} ({(total_valid_blocks/total_blocks*100):.1f}%)")
    if total_disputed_blocks > 0:
        print(f"  ⚔️ Disputed Blocks: {total_disputed_blocks} ({(total_disputed_blocks/total_blocks*100):.1f}%)")
    
    network_health = "🟢 HEALTHY"
    if total_disputed_blocks > total_blocks * 0.1:  # >10% disputed
        network_health = "🟡 STRESSED"
    if total_disputed_blocks > total_blocks * 0.2:  # >20% disputed
        network_health = "🔴 CRISIS"
    
    print(f"  🩺 Network Health: {network_health}")
    
    # Economic indicators
    liquidity_ratio = total_subnet_liquidity / mainnet_state['liquidity'] if mainnet_state['liquidity'] > 0 else 0
    print(f"  💎 Liquidity Distribution: {liquidity_ratio:.2%} in subnets")
    
    print(f"\n{'='*80}")

# Create the new multi-ARC network
network = ArcNetwork(n_arcs=5, n_agents=15)

print("🚀 STARTING ARTIFACT VIRTUAL MULTI-ARC SIMULATION")
print(f"📡 Network initialized with {len(network.arcs)} ARCs and {len(network.agent_registry.agents)} agents")
print(f"💰 Initial FUEL: $1,000,000 mainnet + {len(network.fuel_subnets)} subnets @ $100,000 each")

step_count = 0
print("🚀 Starting simulation... Press 'q' + Enter to quit, 'p' + Enter to pause, or just Enter to continue")

while True:
    try:
        network.step()
        step_count += 1
        
        # Get comprehensive state
        state = network.get_state()
        
        # Print detailed state information
        print_detailed_state(state, step_count)
        
        # Interactive controls
        print("\n" + "="*80)
        print("Controls: [Enter] Continue | [p] Pause | [q] Quit")
        print("="*80)
        
        # Non-blocking input with timeout (auto-continue after 3 seconds)
        import select
        import sys
        
        print("Auto-continuing in 3 seconds...", end="", flush=True)
        
        # Check if input is available
        if select.select([sys.stdin], [], [], 3):
            user_input = input().strip().lower()
            if user_input == 'q':
                break
            elif user_input == 'p':
                input("⏸️ Paused. Press Enter to continue...")
        else:
            print(" ⏭️ Continuing...")
        
    except KeyboardInterrupt:
        print(f"\n🛑 Simulation stopped after {step_count} steps.")
        break
    except Exception as e:
        print(f"❌ Error in step {step_count}: {e}")
        import traceback
        traceback.print_exc()
        break
