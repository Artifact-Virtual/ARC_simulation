import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import json
import os
import time
import pandas as pd
import numpy as np

DATA_DIR = "simulation_data"
STATE_PATH = os.path.join(DATA_DIR, "latest.json")
CONTROL_PATH = os.path.join(DATA_DIR, "control.json")

st.set_page_config(layout="wide", page_title="ARC Network Dashboard")
st.title("🔮 Artifact Virtual: Multi-ARC Network Simulation")

# Auto-refresh functionality
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False

def get_current_control():
    try:
        with open(CONTROL_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {"play": False, "speed": 0.5}

def read_state():
    try:
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return None

def write_control(play, speed):
    with open(CONTROL_PATH, "w") as f:
        json.dump({"play": play, "speed": speed}, f)

def write_reset_command():
    """Send reset command to daemon"""
    reset_path = os.path.join(DATA_DIR, "reset.json")
    with open(reset_path, "w") as f:
        json.dump({"reset": True, "timestamp": time.time()}, f)

# Enhanced UI controls
st.sidebar.header("🎮 Network Controls")
col1, col2 = st.sidebar.columns([1, 1])
with col1:
    play = st.button("▶️ Play", use_container_width=True)
    reset = st.button("🔄 Reset", type="secondary", use_container_width=True)
with col2:
    pause = st.button("⏸️ Pause", use_container_width=True)

speed = st.sidebar.slider("⚡ Speed (seconds per step)", 0.05, 2.0, 0.5, 0.05)

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh Dashboard", value=st.session_state.auto_refresh)
st.session_state.auto_refresh = auto_refresh

# Handle control actions
if play:
    write_control(True, speed)
    st.session_state.auto_refresh = True
if pause:
    write_control(False, speed)
    st.session_state.auto_refresh = False
if reset:
    write_reset_command()
    write_control(False, speed)
    st.session_state.auto_refresh = False
    st.success("🔄 Reset command sent to daemon!")

# Get current state
current_control = get_current_control()
is_playing = current_control.get("play", False)
state = read_state()

# Status display
if state and 'network_state' in state:
    network_state = state['network_state']
    
    # Top metrics
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        st.metric("📅 Step", state.get('step', 'N/A'))
    with col2:
        status_icon = "▶️" if is_playing else "⏸️"
        st.metric("🎯 Status", f"{status_icon} {'Playing' if is_playing else 'Paused'}")
    with col3:
        era_icon = "⚡" if state.get('crisis_mode', False) else "🕊️"
        st.metric("🏛️ Era", f"{era_icon} {state.get('era', 0)}")
    with col4:
        total_arcs = len(network_state.get('arcs', []))
        st.metric("🌐 ARCs", total_arcs)

    # Crisis indicators
    if state.get('crisis_indicators'):
        st.error("⚠️ **Crisis Detected**")
        for indicator in state['crisis_indicators']:
            st.write(f"🔥 {indicator}")
    
    # Main dashboard layout
    tab1, tab2, tab3, tab4 = st.tabs(["🌐 Network Mesh", "⛓️ ARC States", "⚡ FUEL Economy", "🤖 Agents"])
    
    with tab1:
        st.header("🌐 Multi-ARC Network Topology")
        
        # Create network graph
        G = nx.Graph()
        arcs = network_state.get('arcs', [])
        
        # Add ARC nodes
        for i, arc in enumerate(arcs):
            G.add_node(f"ARC-{i}", type="arc", blocks=arc.get('total_blocks', 0))
        
        # Add FUEL mainnet
        G.add_node("FUEL-Mainnet", type="fuel", 
                   liquidity=network_state.get('fuel_mainnet', {}).get('liquidity', 0))
        
        # Add connections (ARCs connected to mainnet, and cross-ARC connections)
        for i in range(len(arcs)):
            G.add_edge(f"ARC-{i}", "FUEL-Mainnet")
            # Add some cross-ARC connections
            for j in range(i+1, min(i+3, len(arcs))):
                if j < len(arcs):
                    G.add_edge(f"ARC-{i}", f"ARC-{j}")
        
        # Plot network
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        pos = nx.spring_layout(G, seed=42, k=3, iterations=50)
        
        # Draw nodes with different colors
        arc_nodes = [n for n in G.nodes() if n.startswith('ARC')]
        fuel_nodes = [n for n in G.nodes() if n.startswith('FUEL')]
        
        nx.draw_networkx_nodes(G, pos, nodelist=arc_nodes, 
                               node_color='lightblue', node_size=1500, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=fuel_nodes, 
                               node_color='gold', node_size=2000, ax=ax)
        nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
        nx.draw_networkx_labels(G, pos, ax=ax)
        
        ax.set_title("Network Topology: ARCs + FUEL Mainnet")
        ax.axis('off')
        st.pyplot(fig)
    
    with tab2:
        st.header("⛓️ ARC Blockchain States")
        
        # Display each ARC's state
        for i, arc in enumerate(arcs):
            with st.expander(f"🔗 ARC-{i} Details", expanded=i==0):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("Recent Blocks")
                    blocks = arc.get('blocks', [])
                    if blocks:
                        df_blocks = pd.DataFrame(blocks[-10:])  # Last 10 blocks
                        st.dataframe(df_blocks, use_container_width=True)
                    else:
                        st.info("No blocks available")
                
                with col2:
                    st.subheader("Block Statistics")
                    total_blocks = arc.get('total_blocks', 0)
                    st.metric("Total Blocks", total_blocks)
                    
                    if blocks:
                        valid_blocks = sum(1 for b in blocks if b.get('status') == 'valid')
                        invalid_blocks = len(blocks) - valid_blocks
                        st.metric("Valid Blocks", valid_blocks)
                        st.metric("Invalid Blocks", invalid_blocks)
                
                # Events
                events = arc.get('events', [])
                if events:
                    st.subheader("Recent Events")
                    for event in events[-5:]:
                        st.write(f"📝 {event}")
    
    with tab3:
        st.header("⚡ FUEL Economy Dashboard")
        
        # FUEL Mainnet stats
        fuel_mainnet = network_state.get('fuel_mainnet', {})
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            liquidity = fuel_mainnet.get('liquidity', 0)
            st.metric("💰 Mainnet Liquidity", f"${liquidity:,.0f}")
        with col2:
            price = fuel_mainnet.get('price', 1.0)
            st.metric("💲 FUEL Price", f"${price:.2f}")
        with col3:
            bridges = fuel_mainnet.get('total_bridges', 0)
            st.metric("🌉 Total Bridges", bridges)
        
        # Subnet liquidity chart
        fuel_subnets = network_state.get('fuel_subnets', [])
        if fuel_subnets:
            subnet_data = []
            for subnet in fuel_subnets:
                subnet_data.append({
                    'ARC': f"ARC-{subnet.get('arc_id', '?')}",
                    'Liquidity': subnet.get('liquidity', 0),
                    'Utilization': subnet.get('utilization', 0) * 100
                })
            
            df_subnets = pd.DataFrame(subnet_data)
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            
            # Liquidity bar chart
            ax1.bar(df_subnets['ARC'], df_subnets['Liquidity'])
            ax1.set_title('Subnet Liquidity')
            ax1.set_ylabel('FUEL Amount')
            ax1.tick_params(axis='x', rotation=45)
            
            # Utilization chart
            ax2.bar(df_subnets['ARC'], df_subnets['Utilization'])
            ax2.set_title('Subnet Utilization %')
            ax2.set_ylabel('Utilization %')
            ax2.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            st.pyplot(fig)
    
    with tab4:
        st.header("🤖 Agent Network Activity")
        
        agents = network_state.get('agents', [])
        if agents:
            # Agent type distribution
            agent_types = {}
            for agent in agents:
                agent_type = agent.get('type', 'unknown')
                agent_types[agent_type] = agent_types.get(agent_type, 0) + 1
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Agent Distribution")
                for agent_type, count in agent_types.items():
                    st.metric(f"{agent_type.title()}s", count)
            
            with col2:
                st.subheader("Agent Details")
                df_agents = pd.DataFrame(agents)
                st.dataframe(df_agents, use_container_width=True)
        else:
            st.info("No agent data available")

else:
    st.info("⏳ Waiting for simulation data from daemon...")
    st.write("Make sure the simulation is running with the new multi-ARC architecture.")

# Auto-refresh at the end
def should_auto_refresh():
    return st.session_state.auto_refresh and is_playing

if should_auto_refresh():
    time.sleep(2)
    st.rerun()
