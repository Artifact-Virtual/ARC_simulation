from arc_simulation.arc_sim import ArcSimulator
from adam_simulation.adam_sim import AdamAgent
from fuel_simulation.fuel_mainnet import FuelMainnet
from fuel_simulation.fuel_subnet import FuelSubnet
from agents.registry import AgentRegistry
from shared.context import MessageBus

class ArcNetwork:
    def __init__(self, n_arcs=5, n_agents=15):
        self.arcs = [ArcSimulator(arc_id=i) for i in range(n_arcs)]
        self.adams = [AdamAgent(arc_id=i) for i in range(n_arcs)]
        self.fuel_mainnet = FuelMainnet()
        self.fuel_subnets = [FuelSubnet(arc_id=i) for i in range(n_arcs)]
        self.agent_registry = AgentRegistry(n_agents, n_arcs)
        self.message_bus = MessageBus()
        self.history = []

    def step(self):
        # Each ARC processes a block and receives any disputes
        for arc, adam, subnet in zip(self.arcs, self.adams, self.fuel_subnets):
            arc.step(adam, subnet, self.agent_registry, self.message_bus)
        # Agents do work (jobs, validations, etc.)
        self.agent_registry.step(self)
        # FUEL mainnet bridges & pricing
        self.fuel_mainnet.step(self.fuel_subnets, self.agent_registry, self.message_bus)
        # Cross-ARC events: challenge, bridge, migration, etc.
        self.message_bus.resolve_cross_arc_events(self)
        # Archive state for dashboard
        self.history.append(self.get_state())

    def get_state(self):
        return {
            "arcs": [arc.get_state() for arc in self.arcs],
            "adams": [adam.get_state() for adam in self.adams],
            "fuel_mainnet": self.fuel_mainnet.get_state(),
            "fuel_subnets": [sub.get_state() for sub in self.fuel_subnets],
            "agents": self.agent_registry.get_state(),
            "messages": self.message_bus.get_state()
        }
