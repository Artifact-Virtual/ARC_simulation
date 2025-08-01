# FUEL Simulation Module

## Overview
Implements the FUEL agent-based economic simulation. Models agents with fuel resources, survival, and crisis response.

## Main Classes
- **FuelAgent**: Individual agent with `agent_id`, `fuel`, `alive`, and `history`. Acts each step based on fuel and crisis conditions.
- **FuelSimulator**: Manages a population of agents, steps the simulation, and tracks events.

## Key Methods
- `FuelAgent.act(context, crisis_mode=False)`: Updates agent's fuel and alive status based on random events and crisis mode.
- `FuelSimulator.step(crisis_mode=False)`: Steps all agents, tracks deaths, and logs events.
- `FuelSimulator.get_stats()`: Returns a list of tuples `(agent_id, fuel, alive)` for all agents.

## Fields
- `FuelAgent.history`: List of fuel values after each step.
- `FuelSimulator.events`: List of string events (e.g., agent deaths).
- `FuelSimulator.dead_last_step`: Number of agents that died in the last step.

## Usage
Instantiate `FuelSimulator`. Call `step()` (optionally with `crisis_mode=True`) to advance the simulation. Use `get_stats()` and `events` for diagnostics and analysis.
