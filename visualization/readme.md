# Visualization Dashboard

## Overview
Streamlit dashboard for real-time visualization and control of the ARC, ADAM, and FUEL simulation. Displays system state, events, crisis/era, and agent/block statistics with enhanced color and event feedback.

## Features
- Live simulation control: step or continuous mode
- Era and crisis highlighting
- Event log aggregation and display
- FUEL agent status and death visualization
- ARC block status and rule visualization (valid/invalid, strict rules)
- ADAM rule scores and guilt display

## Main Components
- **Session State**: Manages singleton instances of ARC, ADAM, FUEL, and context loop
- **Metrics**: Total blocks, living agents, average FUEL
- **Event Log**: Recent system events and feedback
- **Plots**:
  - FUEL agent histories (alive/dead color-coded)
  - ARC block bar plot (valid/invalid, strict rule borders)
- **Crisis/Era**: Current era and crisis status prominently shown

## Usage
Run with:

    streamlit run visualization/dashboard.py

Use the UI to step or run continuously. Inspect metrics, plots, and event logs for system feedback and analysis.
