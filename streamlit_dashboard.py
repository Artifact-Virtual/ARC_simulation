import streamlit as st
import sys
sys.path.append('.')

from arc_network.network import ArcNetwork
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Page config
st.set_page_config(
    page_title="Artifact Virtual Multi-ARC Network",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'network' not in st.session_state:
    st.session_state.network = ArcNetwork(n_arcs=5, n_agents=15)
    st.session_state.step_count = 0
    st.session_state.history = []
    st.session_state.auto_run = False
    # Auto-start with first step
    st.session_state.network.step()
    st.session_state.step_count += 1
    initial_state = st.session_state.network.get_state()
    st.session_state.history.append({
        'step': st.session_state.step_count,
        'timestamp': time.time(),
        **initial_state
    })

# Title and description
st.title("🌐 Artifact Virtual Multi-ARC Network")
st.markdown("Real-time visualization of the multi-ARC blockchain simulation with FUEL economy and agent activities")

# Sidebar controls
st.sidebar.header("🎛️ Simulation Controls")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("▶️ Step", type="primary"):
        st.session_state.network.step()
        st.session_state.step_count += 1
        state = st.session_state.network.get_state()
        st.session_state.history.append({
            'step': st.session_state.step_count,
            'timestamp': time.time(),
            **state
        })

with col2:
    if st.button("🔄 Reset"):
        st.session_state.network = ArcNetwork(n_arcs=5, n_agents=15)
        st.session_state.step_count = 0
        st.session_state.history = []

# Auto-run toggle
st.session_state.auto_run = st.sidebar.checkbox("🔁 Auto-run", value=st.session_state.auto_run)

# Auto-run interval
auto_interval = st.sidebar.slider("Auto-run Interval (seconds)", 0.5, 5.0, 2.0, 0.5)

if st.session_state.auto_run:
    # Auto-refresh - run one step and immediately refresh
    placeholder = st.empty()
    with placeholder.container():
        st.info(f"🔄 Auto-running... Next step in {auto_interval} seconds")
    
    time.sleep(auto_interval)
    
    # Run exactly one step
    st.session_state.network.step()
    st.session_state.step_count += 1
    state = st.session_state.network.get_state()
    st.session_state.history.append({
        'step': st.session_state.step_count,
        'timestamp': time.time(),
        **state
    })
    
    # Force immediate refresh
    st.rerun()

# Display current step
st.sidebar.metric("📊 Current Step", st.session_state.step_count)

# Real-time status indicator
if st.session_state.auto_run:
    st.sidebar.success("🔴 LIVE - Auto-running")
else:
    st.sidebar.info("⏸️ Manual Mode")

# Performance metrics
if len(st.session_state.history) > 1:
    last_step_time = st.session_state.history[-1]['timestamp']
    prev_step_time = st.session_state.history[-2]['timestamp']
    step_duration = last_step_time - prev_step_time
    st.sidebar.metric("⏱️ Last Step Duration", f"{step_duration:.2f}s")

# Get current state
if st.session_state.step_count > 0:
    current_state = st.session_state.network.get_state()
    
    # Show current simulation status
    st.success(f"🔥 Simulation Running - Step {st.session_state.step_count} | Network Health: {len(current_state['arcs'])} ARCs Active")
    
    # Main dashboard layout
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔗 ARC Network", 
        "⚡ FUEL Economy", 
        "🤖 Agent Activity", 
        "📡 Cross-ARC Events", 
        "📊 Network Analytics"
    ])
    
    with tab1:
        st.header("🔗 ARC Blockchain States")
        
        # ARC overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_blocks = sum(len(arc['blocks']) for arc in current_state['arcs'])
        total_valid = sum(sum(1 for block in arc['blocks'] if block['valid']) for arc in current_state['arcs'])
        total_disputed = sum(sum(1 for block in arc['blocks'] if block.get('disputed', False)) for arc in current_state['arcs'])
        
        with col1:
            st.metric("Total Blocks", total_blocks)
        with col2:
            st.metric("Valid Blocks", total_valid)
        with col3:
            st.metric("Disputed Blocks", total_disputed)
        with col4:
            health = "🟢 Healthy"
            if total_blocks > 0:
                dispute_rate = total_disputed / total_blocks
                if dispute_rate > 0.2:
                    health = "🔴 Crisis"
                elif dispute_rate > 0.1:
                    health = "🟡 Stressed"
            st.metric("Network Health", health)
        
        # Individual ARC details
        for i, arc_state in enumerate(current_state['arcs']):
            with st.expander(f"📊 ARC-{arc_state['arc_id']} Details", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Basic Info:**")
                    st.write(f"• Blocks: {len(arc_state['blocks'])}")
                    st.write(f"• Rules: {', '.join(arc_state['rules'])}")
                
                with col2:
                    if arc_state['blocks']:
                        st.write("**Recent Blocks:**")
                        for block in arc_state['blocks'][-3:]:
                            status = "🔲" if block['valid'] else "❌"
                            dispute = "⚔️" if block.get('disputed', False) else ""
                            st.write(f"{status} Block #{block['index']}: {block['content']} {dispute}")
    
    with tab2:
        st.header("⚡ FUEL Economy Dashboard")
        
        # FUEL metrics
        mainnet = current_state['fuel_mainnet']
        total_subnet_liquidity = sum(subnet['liquidity'] for subnet in current_state['fuel_subnets'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Mainnet Liquidity", f"${mainnet['liquidity']:,.0f}")
        with col2:
            st.metric("💱 FUEL Price", f"${mainnet['price']:.2f}")
        with col3:
            st.metric("🌉 Total Bridges", len(mainnet['bridges']))
        with col4:
            st.metric("🏪 Subnet Liquidity", f"${total_subnet_liquidity:,.0f}")
        
        # Liquidity distribution chart
        if current_state['fuel_subnets']:
            subnet_data = []
            for subnet in current_state['fuel_subnets']:
                subnet_data.append({
                    'ARC': f"ARC-{subnet['arc_id']}",
                    'Liquidity': subnet['liquidity']
                })
            
            df_subnets = pd.DataFrame(subnet_data)
            fig = px.bar(df_subnets, x='ARC', y='Liquidity', 
                        title="💰 FUEL Subnet Liquidity Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent bridges
        if mainnet['bridges']:
            st.subheader("🌉 Recent Bridge Activities")
            bridge_data = []
            for bridge in mainnet['bridges'][-10:]:  # Last 10 bridges
                bridge_data.append({
                    'ARC': f"ARC-{bridge['arc']}",
                    'Amount': bridge['amount']
                })
            
            df_bridges = pd.DataFrame(bridge_data)
            fig = px.line(df_bridges, x=df_bridges.index, y='Amount', 
                         color='ARC', title="Bridge Transfer Amounts Over Time")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("🤖 Agent Network Activity")
        
        # Agent type breakdown
        agents = current_state['agents']
        validators = [a for a in agents if a['type'] == 'validator']
        forecasters = [a for a in agents if a['type'] == 'forecaster']
        operators = [a for a in agents if a['type'] == 'operator']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("⚖️ Validators")
            total_earnings = sum(v['earnings'] for v in validators)
            st.metric("Total Earnings", f"${total_earnings}")
            
            for validator in validators:
                st.write(f"ARC-{validator['arc']}: ${validator['earnings']}")
        
        with col2:
            st.subheader("🔮 Forecasters")
            total_predictions = sum(f['score'] for f in forecasters)
            st.metric("Total Correct Predictions", total_predictions)
            
            for forecaster in forecasters:
                st.write(f"ARC-{forecaster['arc']}: {forecaster['score']} correct")
        
        with col3:
            st.subheader("⚙️ Operators")
            total_jobs = sum(o['jobs_done'] for o in operators)
            st.metric("Total Jobs Completed", total_jobs)
            
            for operator in operators:
                st.write(f"ARC-{operator['arc']}: {operator['jobs_done']} jobs")
        
        # Agent performance chart
        if len(st.session_state.history) > 1:
            st.subheader("📈 Agent Performance Over Time")
            
            history_data = []
            for entry in st.session_state.history[-20:]:  # Last 20 steps
                step_validators = [a for a in entry['agents'] if a['type'] == 'validator']
                step_forecasters = [a for a in entry['agents'] if a['type'] == 'forecaster']
                step_operators = [a for a in entry['agents'] if a['type'] == 'operator']
                
                history_data.append({
                    'Step': entry['step'],
                    'Validator Earnings': sum(v['earnings'] for v in step_validators),
                    'Forecaster Score': sum(f['score'] for f in step_forecasters),
                    'Operator Jobs': sum(o['jobs_done'] for o in step_operators)
                })
            
            df_history = pd.DataFrame(history_data)
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Scatter(x=df_history['Step'], y=df_history['Validator Earnings'], name="Validator Earnings"),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=df_history['Step'], y=df_history['Forecaster Score'], name="Forecaster Score"),
                secondary_y=True,
            )
            fig.add_trace(
                go.Scatter(x=df_history['Step'], y=df_history['Operator Jobs'], name="Operator Jobs"),
                secondary_y=True,
            )
            
            fig.update_yaxes(title_text="Earnings ($)", secondary_y=False)
            fig.update_yaxes(title_text="Score/Jobs", secondary_y=True)
            fig.update_layout(title_text="Agent Performance Trends")
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("📡 Cross-ARC Messaging & Events")
        
        events = current_state['messages']['events']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🚨 Active Events", len(events))
        
        if events:
            st.subheader("Current Events")
            for i, event in enumerate(events):
                event_type = event.get('type', 'Unknown')
                
                if event_type == 'block_challenge':
                    st.warning(f"⚔️ Block Challenge: ARC-{event.get('from_arc')} → ARC-{event.get('target_arc')}")
                elif event_type == 'fuel_bridge_complete':
                    st.success(f"🌉 Bridge Complete: ARC-{event.get('arc')} received ${event.get('amount'):,}")
                else:
                    st.info(f"📨 {event_type}: {str(event)[:100]}...")
        else:
            st.success("🔲 No active cross-ARC events")
    
    with tab5:
        st.header("📊 Network Analytics & Trends")
        
        if len(st.session_state.history) > 5:
            # Network growth over time
            network_data = []
            for entry in st.session_state.history:
                total_blocks = sum(len(arc['blocks']) for arc in entry['arcs'])
                total_liquidity = entry['fuel_mainnet']['liquidity'] + sum(subnet['liquidity'] for subnet in entry['fuel_subnets'])
                total_events = len(entry['messages']['events'])
                
                network_data.append({
                    'Step': entry['step'],
                    'Total Blocks': total_blocks,
                    'Total Liquidity': total_liquidity,
                    'Active Events': total_events
                })
            
            df_network = pd.DataFrame(network_data)
            
            # Multi-metric chart
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Network Blocks Over Time', 'Total Liquidity', 
                              'Cross-ARC Events', 'Network Health'),
                specs=[[{"secondary_y": True}, {"secondary_y": True}],
                       [{"secondary_y": True}, {"secondary_y": True}]]
            )
            
            # Blocks chart
            fig.add_trace(
                go.Scatter(x=df_network['Step'], y=df_network['Total Blocks'], 
                          name="Total Blocks", line=dict(color='blue')),
                row=1, col=1
            )
            
            # Liquidity chart
            fig.add_trace(
                go.Scatter(x=df_network['Step'], y=df_network['Total Liquidity'], 
                          name="Total Liquidity", line=dict(color='green')),
                row=1, col=2
            )
            
            # Events chart
            fig.add_trace(
                go.Scatter(x=df_network['Step'], y=df_network['Active Events'], 
                          name="Active Events", line=dict(color='red')),
                row=2, col=1
            )
            
            fig.update_layout(height=600, title_text="Network Analytics Dashboard")
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary statistics
            st.subheader("📈 Network Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_blocks_per_step = df_network['Total Blocks'].diff().mean()
                st.metric("Avg Blocks/Step", f"{avg_blocks_per_step:.1f}")
            
            with col2:
                liquidity_change = ((df_network['Total Liquidity'].iloc[-1] - df_network['Total Liquidity'].iloc[0]) 
                                  / df_network['Total Liquidity'].iloc[0] * 100)
                st.metric("Liquidity Change", f"{liquidity_change:+.1f}%")
            
            with col3:
                avg_events = df_network['Active Events'].mean()
                st.metric("Avg Events/Step", f"{avg_events:.1f}")
            
            with col4:
                current_step = df_network['Step'].iloc[-1]
                st.metric("Simulation Duration", f"{current_step} steps")
        
        else:
            st.info("📊 Run more steps to see analytics trends...")

else:
    st.info("🚀 Click 'Step' to start the simulation!")

# Footer
st.markdown("---")
st.markdown("🌐 **Artifact Virtual Multi-ARC Network** - Real-time blockchain simulation with FUEL economy")
