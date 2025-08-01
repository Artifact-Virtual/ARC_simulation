class OperatorAgent:
    def __init__(self, agent_id, arc_id):
        self.agent_id = agent_id
        self.arc_id = arc_id
        self.jobs_done = 0

    def step(self, network):
        # Perform job, spend fuel
        subnet = network.fuel_subnets[self.arc_id]
        if subnet.liquidity > 5:
            subnet.liquidity -= 5
            self.jobs_done += 1

    def get_state(self):
        return {"type": "operator", "arc": self.arc_id, "jobs_done": self.jobs_done}
