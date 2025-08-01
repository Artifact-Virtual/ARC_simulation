import random


class ForecasterAgent:
    def __init__(self, agent_id, arc_id):
        self.agent_id = agent_id
        self.arc_id = arc_id
        self.score = 0

    def step(self, network):
        # Predict random shock, get fuel if right
        pred = random.choice([True, False])
        if pred and random.random() < 0.05:
            network.fuel_subnets[self.arc_id].liquidity += 20
            self.score += 1

    def get_state(self):
        return {"type": "forecaster", "arc": self.arc_id, "score": self.score}
