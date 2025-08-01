# Shared Context Module

## Overview
Provides the `LiveContextLoop` class to coordinate ARC, ADAM, and FUEL simulations, manage crisis mode, and aggregate events and logs.

## Main Class
- **LiveContextLoop**: Orchestrates simulation steps, crisis detection, and event aggregation.

## Key Methods
- `LiveContextLoop.step()`: Executes a simulation step, detects crisis, updates all subsystems, aggregates events, and logs state.

## Fields
- `arc`, `adam`, `fuel`: References to ARC, ADAM, and FUEL simulation objects.
- `step_num`: Current step number.
- `logs`: List of dicts with step state, scores, guilt, fuel stats, events, era, and crisis mode.
- `crisis_mode`: Boolean, true if system is in crisis.
- `era`: Integer, increments on new crisis.

## Crisis Detection
Crisis mode is triggered if more than 1 FUEL agent dies in a step or more than 2 invalid ARC blocks in the last 7 blocks. Era increments on new crisis.

## Usage
Instantiate with ARC, ADAM, and FUEL objects. Call `step()` to advance simulation and access `logs` for state and events.
