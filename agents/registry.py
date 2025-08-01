from agents.validator import ValidatorAgent
from agents.forecaster import ForecasterAgent
from agents.operator import OperatorAgent


class AgentRegistry:
    def __init__(self, n_agents, n_arcs):
        self.agents = []
        for i in range(n_agents):
            arc = i % n_arcs
            if i % 3 == 0:
                self.agents.append(ValidatorAgent(i, arc))
            elif i % 3 == 1:
                self.agents.append(ForecasterAgent(i, arc))
            else:
                self.agents.append(OperatorAgent(i, arc))

    def step(self, network):
        for agent in self.agents:
            agent.step(network)

    def get_state(self):
        return [a.get_state() for a in self.agents]

    def arc_counts(self):
        from collections import Counter
        return Counter(a.arc_id for a in self.agents)
