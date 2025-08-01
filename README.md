# Constitutional Intelligence System
![Simulation](https://img.shields.io/badge/Simulation-darkblue.svg)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20%2B-ff4b4b.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/your-repo/constitutional_simulation/ci.yml?branch=main)](https://github.com/your-repo/constitutional_simulation/actions)

A dynamic simulation of emergent governance where constitutional law (ARC), AI governance (ADAM Protocol), and economic systems (FUEL) interact as a living, evolving entity. Watch as rules adapt, agents compete, and constitutional patterns emerge from the interplay of law, intelligence, and economics.

## System Overview

This simulation models three interconnected layers:

- **ARC (Constitutional Layer)**: A blockchain of constitutional blocks with evolving validation rules
- **ADAM Protocol (AI Governance)**: Intelligent rule evolution based on ethical observations and guilt tracking
- **FUEL (Economic Substrate)**: Competitive agents in a resource-constrained environment

## Quick Start

### Launch the Interactive Dashboard

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Launch the dashboard:**
    ```bash
    PYTHONPATH=. streamlit run visualization/dashboard.py
    ```

3. **Access the interface:**
    Open your browser to `http://localhost:8501`

### Run Headless Simulation

For console-based monitoring:
```bash
python main.py
```

## Dashboard Features

### Real-Time System Monitoring
- **System Health Metrics**: Track total blocks, living agents, and average FUEL levels
- **Event Logging**: See constitutional events, rule violations, and economic crises
- **Agent Status**: Monitor individual agent survival and resource levels

### Interactive Visualizations
- **Constitutional Chain**: Visual representation of blocks with rule type highlighting
- **FUEL Flow Dynamics**: Agent resource histories with status color coding
- **ADAM Protocol Analysis**: Rule scores and guilt tracking

### Controls
- **Run Continuously**: Auto-stepping simulation with real-time updates
- **Step Once**: Manual progression for detailed observation
- **Reset System**: Start fresh with new initial conditions

## System Dynamics

### Constitutional Evolution (ARC)
- Genesis block establishes foundational law ("Do no harm")
- Regular blocks validated against 7 rotating rules
- Rules evolve based on ADAM Protocol feedback
- Strict rules create visual markers (red borders in visualization)

### AI Governance (ADAM)
- Observes constitutional chain for ethical violations
- Tracks rule scores and guilt accumulation
- Triggers rule evolution when thresholds are exceeded
- Implements quadratic voting for rule prioritization

### Economic Simulation (FUEL)
- 8 competing agents with limited resources
- Agents work, consume, trade, and can die from resource depletion
- Economic stress feeds back into constitutional rule evolution
- Visual status tracking (green=alive, red=dead)

## Emergent Behaviors to Observe

### Constitutional Patterns
- **Rule Strictness Cycles**: Watch rules become stricter then relax based on system stress
- **Validation Failures**: Blocks rejected due to evolving constitutional standards
- **Genesis Influence**: How foundational law propagates through the system

### Economic Dynamics
- **Agent Competition**: Resource competition leading to survival/death cycles
- **Economic Crises**: Mass agent deaths triggering constitutional responses
- **Resource Redistribution**: Trading behaviors and wealth concentration

### Governance Intelligence
- **Guilt Accumulation**: ADAM detecting patterns of rule violations
- **Rule Evolution**: Intelligent adaptation to changing system conditions
- **Ethical Learning**: Constitutional law evolving based on observed outcomes

## Customization

### Tuning Parameters
- Modify agent count in `FuelSimulator(n_agents=8)`
- Adjust rule sensitivity in ADAM Protocol
- Change constitutional validation logic in ARC

### Adding New Rules
- Implement custom validation functions in `arc_simulation/arc_sim.py`
- Define new ethical criteria in `adam_simulation/adam_sim.py`
- Create economic events in `fuel_simulation/fuel_sim.py`

### Visual Enhancements
- Customize colors and styling in `visualization/dashboard.py`
- Add new metrics and charts
- Implement custom event logging

## Project Structure

```
constitutional_simulation/
├── arc_simulation/          # Constitutional blockchain layer
├── adam_simulation/         # AI governance and rule evolution
├── fuel_simulation/         # Economic agent competition
├── shared/                  # Common utilities and context loop
├── visualization/           # Interactive dashboard
├── docs/                    # Documentation
└── main.py                 # Headless simulation runner
```

## Understanding the Visualizations

### Constitutional Chain Plot
- **Colors**: Genesis (red), Regular (teal), Unknown (gray)
- **Borders**: Red borders indicate strict rule enforcement
- **Height**: All blocks shown at unit height for pattern recognition

### FUEL Flow Chart
- **Line Colors**: Green = living agents, Red = dead agents
- **Transparency**: Reduced alpha for dead agents
- **Timeline**: X-axis shows simulation steps

### System Metrics
- **Total Blocks**: Constitutional chain length
- **Living Agents**: Current survivor count
- **Average FUEL**: Economic health indicator

## Advanced Features

### Event System
The dashboard tracks and displays:
- Constitutional rule changes
- Agent deaths and resource crises
- ADAM Protocol decisions
- System state transitions

### Cross-System Feedback
- Economic stress influences rule strictness
- Constitutional changes affect agent behavior
- ADAM observations drive both legal and economic policy

### Emergent Complexity
Watch for:
- Constitutional eras with distinct rule patterns
- Economic boom/bust cycles
- AI governance learning and adaptation
- System-wide phase transitions

## Development

### Adding New Simulation Layers
1. Create new module in project root
2. Implement simulation logic with `.step()` method
3. Add to `LiveContextLoop` in `shared/context.py`
4. Update dashboard visualization

### Implementing New Visualizations
1. Add chart logic to `visualization/dashboard.py`
2. Use matplotlib for static plots
3. Leverage Streamlit components for interactivity
4. Follow color scheme and styling conventions

### Contributing to System Dynamics
1. Enhance cross-layer interactions in `shared/context.py`
2. Add complexity to individual simulation modules
3. Implement new event types and logging
4. Create feedback mechanisms between layers

This living constitutional system demonstrates how governance, intelligence, and economics can create emergent complexity through simple rules and interactions. Using this system we can experiment with different parameters and observe how small changes can lead to dramatically different constitutional evolution patterns.

