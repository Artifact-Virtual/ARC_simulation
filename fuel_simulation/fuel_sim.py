import numpy as np
import random


class FuelAgent:
    def __init__(self, agent_id, fuel=10):
        self.agent_id = agent_id
        self.fuel = fuel
        self.alive = True
        self.history = []

    def act(self, context, crisis_mode=False):
        if not self.alive:
            self.history.append(self.fuel)
            return
        # Random economic event
        if crisis_mode and random.random() < 0.2:
            self.fuel -= random.randint(1, 3)
        elif self.fuel <= 0:
            self.alive = False
        elif self.fuel < 3 and random.random() < 0.6:
            self.fuel += 2  # get help
        elif random.random() < 0.5:
            self.fuel -= 1
        else:
            self.fuel += 1
        self.history.append(self.fuel)


class FuelSimulator:
    def __init__(self, n_agents=10):
        self.agents = [FuelAgent(i) for i in range(n_agents)]
        self.events = []
        self.dead_last_step = 0

    def step(self, crisis_mode=False):
        prev_alive = sum([a.alive for a in self.agents])
        for agent in self.agents:
            agent.act(None, crisis_mode=crisis_mode)
        after_alive = sum([a.alive for a in self.agents])
        died_now = prev_alive - after_alive
        if died_now > 0:
            self.events.append(f"{died_now} FUEL agents died this step.")
        self.dead_last_step = died_now

    def get_stats(self):
        return [(a.agent_id, a.fuel, a.alive) for a in self.agents]
