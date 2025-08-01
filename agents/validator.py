class ValidatorAgent:
    def __init__(self, agent_id, arc_id):
        self.agent_id = agent_id
        self.arc_id = arc_id
        self.earnings = 0

    def step(self, network):
        # Validate a block, earn fuel, possibly get slashed for error
        arc = network.arcs[self.arc_id]
        if arc.blocks and arc.blocks[-1]["valid"]:
            network.fuel_subnets[self.arc_id].liquidity += 10
            self.earnings += 10

    def get_state(self):
        return {"type": "validator", "arc": self.arc_id, "earnings": self.earnings}
