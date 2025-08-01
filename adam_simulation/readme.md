# ADAM Simulation Module

## Overview
Implements the ADAM agent for monitoring and evolving rules in the ARC simulation. Tracks rule performance, assigns guilt, and triggers rule evolution based on observed chain state.

## Main Class
- **AdamAgent**: Manages rule scores, guilt, voting, and rule evolution.

## Key Methods
- `AdamAgent.observe(arc_chain)`: Updates rule scores and guilt based on the last 7 blocks. Increments guilt and decrements score for invalid blocks.
- `AdamAgent.quadratic_vote()`: Returns normalized quadratic votes for each rule based on scores.
- `AdamAgent.evolve_rules(arc_sim, crisis=False)`: Evolves rules in the ARC simulator. If crisis or high guilt, applies emergency rule; otherwise, makes a rule stricter. Logs events and resets guilt as needed.

## Fields
- `rule_scores`: Numpy array of rule performance scores.
- `guilt`: Numpy array of rule guilt counters.
- `votes`: Numpy array of quadratic votes.
- `history`: List of dicts with snapshots of scores and guilt after each evolution.
- `events`: List of string events (e.g., guilt increments, rule changes).

## Usage
Instantiate `AdamAgent`. Call `observe` with the ARC chain, then use `quadratic_vote` and `evolve_rules` to update ARC rules. Inspect `history` and `events` for diagnostics.
