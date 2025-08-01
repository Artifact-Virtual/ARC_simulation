# Arc Simulation Module

## Overview
This module implements the ARC (Abstract Rule Chain) simulation, modeling a blockchain-like chain of constitutional blocks with evolving rules.

## Main Classes
- **ArcBlock**: Represents a block in the chain. Fields: `index`, `data_hash`, `rule_name`, `constitutional_data`, `status`.
- **ArcSimulator**: Manages the chain, rules, and block addition.

## Key Methods
- `ArcSimulator.add_block(data)`: Adds a block using the current rule. Returns `True` if valid, else `False` and logs an event.
- `ArcSimulator.run_cycle(crisis_mode=False)`: Adds 7 blocks, optionally with crisis content, then evolves a rule.
- `ArcSimulator.evolve_rules(mutate_rule=None, force_idx=None, new_rule=None, note=None)`: Evolves a rule, either randomly or as specified.
- `ArcSimulator.get_chain_state(last_n=None)`: Returns the chain as a list of dicts. Optionally only the last `n` blocks.
- `ArcSimulator.reset()`: Resets the chain and rules to genesis state.

## Events
- `ArcSimulator.events`: List of string events, e.g., block rejections or rule evolutions.

## Genesis Block
- Created at initialization with a default constitution: `{"law": "Do no harm", "creator": "Genesis"}`.

## Rule System
- 7 rules, each can be evolved. Default rule accepts any data with a `type` field. Evolved rules can be stricter.

## Usage
Import and instantiate `ArcSimulator`. Use `add_block`, `run_cycle`, and `evolve_rules` to interact. Inspect `blocks` and `events` for state and logs.
