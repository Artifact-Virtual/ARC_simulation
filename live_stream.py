import streamlit as st
import sys
sys.path.append('.')

from arc_network.network import ArcNetwork
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(
    page_title="AV Multi-ARC Professional Stream",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better visuals
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f1f2e, #2d3748);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 0.5rem 0;
    }
    .arc-status {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.2rem;
    }
    .live-indicator {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .paused-mode {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with enhanced tracking
if 'network' not in st.session_state:
    st.session_state.network = ArcNetwork(n_arcs=5, n_agents=15)
    st.session_state.step_count = 0
    st.session_state.running = False
    st.session_state.history = []
    st.session_state.subnet_bridge_threshold = 500  # FUEL tokens to bridge
    st.session_state.analytics_data = {
        'block_creation_rate': [],
        'agent_performance': [],
        'fuel_flows': [],
        'network_health': []
    }

# Professional Header
st.markdown("""
<div class="main-header">
    <h1>🔴 ARTIFACT VIRTUAL MULTI-ARC PROFESSIONAL ANALYTICS STREAM</h1>
    <p>Real-time blockchain simulation with advanced analytics and FUEL token economics</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Control Panel
with st.sidebar:
    st.header("🎛️ Professional Controls")
    
    # Main controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start", type="primary", use_container_width=True):
            st.session_state.running = True
    with col2:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.running = False
    
    if st.button("🔄 Reset Network", use_container_width=True):
        st.session_state.network = ArcNetwork(n_arcs=5, n_agents=15)
        st.session_state.step_count = 0
        st.session_state.running = False
        st.session_state.history = []
        st.session_state.analytics_data = {
            'block_creation_rate': [],
            'agent_performance': [],
            'fuel_flows': [],
            'network_health': []
        }
    
    # Stream settings
    st.subheader("⚙️ Stream Settings")
    stream_speed = st.slider("Update Interval (sec)", 0.1, 3.0, 0.8, 0.1)
    
    # FUEL Economics Settings
    st.subheader("⚡ FUEL Economics")
    bridge_threshold = st.slider("Subnet Bridge Threshold (FUEL)", 100, 1000, 500, 50)
    st.session_state.subnet_bridge_threshold = bridge_threshold
    
    # Analytics Settings
    st.subheader("📊 Analytics Settings")
    history_window = st.slider("History Window (steps)", 10, 100, 50, 5)
    show_predictions = st.checkbox("Show Forecaster Predictions", True)
    show_disputes = st.checkbox("Show Block Disputes", True)
    
    # Live Status
    st.subheader("📡 System Status")
    if st.session_state.running:
        st.markdown('<div class="live-indicator">🔴 STREAMING LIVE</div>', unsafe_allow_html=True)
        st.metric("Active Step", st.session_state.step_count)
    else:
        st.info("⏸️ PAUSED")
        st.metric("Current Step", st.session_state.step_count)
    
    # Performance metrics
    if len(st.session_state.history) > 1:
        avg_duration = np.mean([h.get('duration', 0) for h in st.session_state.history[-10:]])
        st.metric("Avg Step Time", f"{avg_duration:.3f}s")
    
    # Network health indicator
    if st.session_state.step_count > 0:
        current_state = st.session_state.network.get_state()
        total_blocks = sum(len(arc['blocks']) for arc in current_state['arcs'])
        total_valid = sum(sum(1 for block in arc['blocks'] if block['valid']) for arc in current_state['arcs'])
        health = (total_valid / total_blocks * 100) if total_blocks > 0 else 100
        
        if health >= 90:
            st.success(f"🟢 Network: {health:.1f}%")
        elif health >= 80:
            st.warning(f"🟡 Network: {health:.1f}%")
        else:
            st.error(f"🔴 Network: {health:.1f}%")

# Main Dashboard Area
if st.session_state.step_count > 0:
    current_state = st.session_state.network.get_state()
    
    # Enhanced metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_blocks = sum(len(arc['blocks']) for arc in current_state['arcs'])
    total_agents = len(current_state['agents'])
    total_events = len(current_state['messages']['events'])
    mainnet_fuel = current_state['fuel_mainnet']['liquidity']
    
    # Calculate total subnet FUEL tokens (not dollars)
    total_subnet_fuel = sum(subnet['liquidity'] for subnet in current_state['fuel_subnets'])
    
    with col1:
        st.metric("🔗 Network Blocks", total_blocks, 
                 delta=len(st.session_state.history[-1]['arcs'][0]['blocks']) if st.session_state.history else None)
    with col2:
        st.metric("🤖 Active Agents", total_agents)
    with col3:
        st.metric("📡 Live Events", total_events)
    with col4:
        st.metric("💰 FUEL Mainnet", f"${mainnet_fuel:,.0f}")
    with col5:
        st.metric("⚡ Subnet FUEL", f"{total_subnet_fuel:,.0f} tokens")
    
    # Main content based on mode
    if st.session_state.running:
        # LIVE MODE - Full real-time dashboard
        st.markdown("### 🔴 LIVE ANALYTICS DASHBOARD")
        
        # Tab structure for organized data
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔗 ARC Network Status",
            "⚡ FUEL Token Economics", 
            "🤖 Agent Performance",
            "📡 Cross-ARC Events",
            "📊 Advanced Analytics"
        ])
        
        with tab1:
            # Enhanced ARC display
            st.subheader("🏗️ ARC Network Architecture")
            arc_cols = st.columns(len(current_state['arcs']))
            
            for i, arc_state in enumerate(current_state['arcs']):
                with arc_cols[i]:
                    st.markdown(f"""
                    <div class="arc-status">
                        <h4>ARC-{arc_state['arc_id']}</h4>
                        <p><strong>Blocks:</strong> {len(arc_state['blocks'])}</p>
                        <p><strong>Rules:</strong> {len(arc_state['rules'])}</p>
                        <p><strong>Validators:</strong> {len([a for a in current_state['agents'] if a['arc'] == arc_state['arc_id'] and a['type'] == 'validator'])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Recent blocks with details
                    if arc_state['blocks']:
                        st.write("**Recent Blocks:**")
                        for block in arc_state['blocks'][-3:]:
                            status = "🔲" if block['valid'] else "❌"
                            dispute = "⚔️" if block.get('disputed', False) else ""
                            st.write(f"`{status} #{block['index']}` {block['content'][:20]}... {dispute}")
            
            # Network topology visualization
            if len(st.session_state.history) > 5:
                st.subheader("📈 Block Creation Rate")
                history_df = pd.DataFrame([
                    {
                        'Step': h['step'],
                        'Total Blocks': sum(len(arc['blocks']) for arc in h['arcs']),
                        'Valid Blocks': sum(sum(1 for block in arc['blocks'] if block['valid']) for arc in h['arcs'])
                    }
                    for h in st.session_state.history[-history_window:]
                ])
                
                fig = px.line(history_df, x='Step', y=['Total Blocks', 'Valid Blocks'], 
                             title="Network Block Growth")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Enhanced FUEL economics
            st.subheader("⚡ FUEL Token Economics Dashboard")
            
            # FUEL distribution chart
            fuel_data = []
            fuel_data.append({"Location": "Mainnet", "Amount": mainnet_fuel, "Type": "USD"})
            
            for subnet in current_state['fuel_subnets']:
                fuel_data.append({
                    "Location": f"ARC-{subnet['arc_id']} Subnet",
                    "Amount": subnet['liquidity'],
                    "Type": "FUEL Tokens"
                })
            
            fuel_df = pd.DataFrame(fuel_data)
            
            # Separate charts for USD and FUEL tokens
            col1, col2 = st.columns(2)
            
            with col1:
                mainnet_df = fuel_df[fuel_df['Type'] == 'USD']
                if not mainnet_df.empty:
                    fig_mainnet = px.pie(mainnet_df, values='Amount', names='Location',
                                       title="💰 Mainnet USD Liquidity")
                    st.plotly_chart(fig_mainnet, use_container_width=True)
            
            with col2:
                subnet_df = fuel_df[fuel_df['Type'] == 'FUEL Tokens']
                if not subnet_df.empty:
                    fig_subnet = px.bar(subnet_df, x='Location', y='Amount',
                                      title="⚡ Subnet FUEL Token Balances")
                    st.plotly_chart(fig_subnet, use_container_width=True)
            
            # Bridge threshold monitoring
            st.subheader("🌉 Bridge Monitoring")
            bridge_cols = st.columns(len(current_state['fuel_subnets']))
            
            for i, subnet in enumerate(current_state['fuel_subnets']):
                with bridge_cols[i]:
                    progress = subnet['liquidity'] / bridge_threshold
                    st.metric(f"ARC-{subnet['arc_id']}", f"{subnet['liquidity']} FUEL")
                    st.progress(min(progress, 1.0))
                    
                    if subnet['liquidity'] >= bridge_threshold:
                        st.success("🌉 Ready to Bridge!")
                    else:
                        remaining = bridge_threshold - subnet['liquidity']
                        st.info(f"Need {remaining} more FUEL")
        
        with tab3:
            # Enhanced agent analytics
            st.subheader("🤖 Agent Performance Analytics")
            
            # Agent type breakdown with performance metrics
            validators = [a for a in current_state['agents'] if a['type'] == 'validator']
            forecasters = [a for a in current_state['agents'] if a['type'] == 'forecaster']
            operators = [a for a in current_state['agents'] if a['type'] == 'operator']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### ⚖️ Validators")
                if validators:
                    val_df = pd.DataFrame(validators)
                    fig = px.bar(val_df, x='arc', y='earnings', 
                               title="Validator Earnings by ARC")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Top performer
                    top_validator = max(validators, key=lambda x: x['earnings'])
                    st.success(f"🏆 Top: ARC-{top_validator['arc']} (${top_validator['earnings']})")
            
            with col2:
                st.markdown("#### 🔮 Forecasters")
                if forecasters:
                    fore_df = pd.DataFrame(forecasters)
                    fig = px.scatter(fore_df, x='arc', y='score', size='score',
                                   title="Forecaster Accuracy by ARC")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Most accurate
                    top_forecaster = max(forecasters, key=lambda x: x['score'])
                    st.success(f"🎯 Best: ARC-{top_forecaster['arc']} ({top_forecaster['score']} correct)")
            
            with col3:
                st.markdown("#### ⚙️ Operators")
                if operators:
                    op_df = pd.DataFrame(operators)
                    fig = px.bar(op_df, x='arc', y='jobs_done',
                               title="Operator Jobs by ARC")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Most productive
                    top_operator = max(operators, key=lambda x: x['jobs_done'])
                    st.success(f"🔧 Busiest: ARC-{top_operator['arc']} ({top_operator['jobs_done']} jobs)")
        
        with tab4:
            # Enhanced event monitoring
            st.subheader("📡 Cross-ARC Event Monitor")
            
            events = current_state['messages']['events']
            if events:
                # Event timeline
                event_data = []
                for i, event in enumerate(events[-10:]):  # Last 10 events
                    event_data.append({
                        'Event_ID': i,
                        'Type': event.get('type', 'Unknown'),
                        'Details': str(event)[:50] + "...",
                        'Timestamp': time.time() - (len(events) - i)
                    })
                
                event_df = pd.DataFrame(event_data)
                
                # Event type distribution
                event_counts = event_df['Type'].value_counts()
                fig = px.pie(values=event_counts.values, names=event_counts.index,
                           title="Event Type Distribution")
                st.plotly_chart(fig, use_container_width=True)
                
                # Recent events list
                st.markdown("#### 🚨 Recent Events")
                for event in events[-5:]:
                    event_type = event.get('type', 'Unknown')
                    if event_type == 'block_challenge':
                        st.warning(f"⚔️ Challenge: ARC-{event.get('from_arc')} → ARC-{event.get('target_arc')}")
                    elif event_type == 'fuel_bridge_complete':
                        st.success(f"🌉 Bridge: ARC-{event.get('arc')} +{event.get('amount'):,} FUEL")
                    else:
                        st.info(f"📨 {event_type}: {str(event)[:80]}...")
            else:
                st.info("🔲 No active cross-ARC events")
        
        with tab5:
            # Advanced analytics and insights
            st.subheader("📊 Advanced Network Analytics")
            
            if len(st.session_state.history) > 10:
                # Network health trends
                health_data = []
                for h in st.session_state.history[-history_window:]:
                    total_b = sum(len(arc['blocks']) for arc in h['arcs'])
                    valid_b = sum(sum(1 for block in arc['blocks'] if block['valid']) for arc in h['arcs'])
                    health_data.append({
                        'Step': h['step'],
                        'Health': (valid_b / total_b * 100) if total_b > 0 else 100,
                        'Blocks': total_b,
                        'Events': len(h['messages']['events'])
                    })
                
                health_df = pd.DataFrame(health_data)
                
                # Multi-metric dashboard
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Network Health %', 'Block Growth', 'Event Activity', 'Health vs Events'),
                    specs=[[{"secondary_y": False}, {"secondary_y": False}],
                           [{"secondary_y": False}, {"secondary_y": False}]]
                )
                
                # Health trend
                fig.add_trace(
                    go.Scatter(x=health_df['Step'], y=health_df['Health'], name="Health %"),
                    row=1, col=1
                )
                
                # Block growth
                fig.add_trace(
                    go.Scatter(x=health_df['Step'], y=health_df['Blocks'], name="Total Blocks"),
                    row=1, col=2
                )
                
                # Event activity
                fig.add_trace(
                    go.Scatter(x=health_df['Step'], y=health_df['Events'], name="Events"),
                    row=2, col=1
                )
                
                # Health vs Events correlation
                fig.add_trace(
                    go.Scatter(x=health_df['Events'], y=health_df['Health'], 
                             mode='markers', name="Health vs Events"),
                    row=2, col=2
                )
                
                fig.update_layout(height=600, title_text="Advanced Network Analytics")
                st.plotly_chart(fig, use_container_width=True)
                
                # Key insights
                st.markdown("#### 🧠 AI Insights")
                avg_health = health_df['Health'].mean()
                health_trend = health_df['Health'].diff().mean()
                
                if avg_health >= 95:
                    st.success(f"🟢 Excellent network health: {avg_health:.1f}% average")
                elif avg_health >= 85:
                    st.warning(f"🟡 Good network health: {avg_health:.1f}% average")
                else:
                    st.error(f"🔴 Network under stress: {avg_health:.1f}% average")
                
                if health_trend > 0:
                    st.info("📈 Network health is improving")
                elif health_trend < -0.5:
                    st.warning("📉 Network health is declining")
                else:
                    st.info("➡️ Network health is stable")
    
    else:
        # PAUSED MODE - Full detailed analysis for research
        st.markdown("""
        <div class="paused-mode">
            <h3>⏸️ RESEARCH MODE - DETAILED ANALYSIS</h3>
            <p>Stream paused for detailed analysis. All data remains accessible for research.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Full detailed view when paused (for research)
        research_tab1, research_tab2, research_tab3 = st.tabs([
            "🔬 Detailed Network State",
            "📋 Complete Agent Analysis", 
            "🧪 Research Data Export"
        ])
        
        with research_tab1:
            st.subheader("🔬 Complete Network State Analysis")
            
            # Detailed ARC analysis
            for arc_state in current_state['arcs']:
                with st.expander(f"📊 ARC-{arc_state['arc_id']} Complete Analysis", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Network Metrics:**")
                        st.json({
                            "total_blocks": len(arc_state['blocks']),
                            "valid_blocks": sum(1 for b in arc_state['blocks'] if b['valid']),
                            "disputed_blocks": sum(1 for b in arc_state['blocks'] if b.get('disputed', False)),
                            "active_rules": arc_state['rules']
                        })
                    
                    with col2:
                        st.write("**Block Details:**")
                        if arc_state['blocks']:
                            block_df = pd.DataFrame(arc_state['blocks'][-10:])  # Last 10 blocks
                            st.dataframe(block_df, use_container_width=True)
        
        with research_tab2:
            st.subheader("📋 Complete Agent Performance Analysis")
            
            # Detailed agent breakdowns
            all_agents_df = pd.DataFrame(current_state['agents'])
            
            # Performance by type
            for agent_type in ['validator', 'forecaster', 'operator']:
                type_agents = all_agents_df[all_agents_df['type'] == agent_type]
                if not type_agents.empty:
                    st.write(f"**{agent_type.title()} Detailed Analysis:**")
                    st.dataframe(type_agents, use_container_width=True)
                    
                    # Performance statistics
                    if agent_type == 'validator':
                        st.metric("Total Earnings", f"${type_agents['earnings'].sum()}")
                        st.metric("Average Earnings", f"${type_agents['earnings'].mean():.2f}")
                    elif agent_type == 'forecaster':
                        st.metric("Total Predictions", type_agents['score'].sum())
                        st.metric("Average Accuracy", f"{type_agents['score'].mean():.2f}")
                    elif agent_type == 'operator':
                        st.metric("Total Jobs", type_agents['jobs_done'].sum())
                        st.metric("Average Productivity", f"{type_agents['jobs_done'].mean():.2f}")
        
        with research_tab3:
            st.subheader("🧪 Research Data Export")
            
            # Downloadable research data
            if st.button("📊 Generate Research Report"):
                research_data = {
                    "simulation_step": st.session_state.step_count,
                    "network_state": current_state,
                    "history_summary": {
                        "total_steps": len(st.session_state.history),
                        "avg_health": np.mean([
                            sum(sum(1 for block in arc['blocks'] if block['valid']) for arc in h['arcs']) / 
                            max(1, sum(len(arc['blocks']) for arc in h['arcs'])) * 100
                            for h in st.session_state.history[-20:]
                        ]) if st.session_state.history else 0
                    }
                }
                
                st.json(research_data)
                st.download_button(
                    "💾 Download Research Data (JSON)",
                    data=pd.Series(research_data).to_json(),
                    file_name=f"arc_simulation_research_step_{st.session_state.step_count}.json",
                    mime="application/json"
                )

else:
    # Initial state
    st.info("🚀 Professional Multi-ARC Analytics Stream Ready")
    st.markdown("### 🎯 Features:")
    st.markdown("""
    - **🔴 Live Streaming**: Real-time network monitoring with professional analytics
    - **⏸️ Research Mode**: Detailed analysis when paused - perfect for studying network behavior
    - **⚡ FUEL Token Economics**: Proper subnet token tracking with bridge thresholds
    - **📊 Advanced Analytics**: Multi-dimensional performance tracking and AI insights
    - **🎛️ Professional Controls**: Fine-tuned parameters for research and analysis
    - **💾 Data Export**: Download research data for external analysis
    """)
    
    st.markdown("Click **▶️ Start** in the sidebar to begin the professional simulation stream.")

# Live streaming execution
if st.session_state.running:
    start_time = time.time()
    
    # Run simulation step
    st.session_state.network.step()
    st.session_state.step_count += 1
    
    # Record performance
    step_duration = time.time() - start_time
    
    # Get state and add to history
    state = st.session_state.network.get_state()
    st.session_state.history.append({
        'step': st.session_state.step_count,
        'timestamp': time.time(),
        'duration': step_duration,
        **state
    })
    
    # Limit history size for performance
    if len(st.session_state.history) > 200:
        st.session_state.history = st.session_state.history[-100:]
    
    # Auto-refresh
    time.sleep(stream_speed)
    st.rerun()
