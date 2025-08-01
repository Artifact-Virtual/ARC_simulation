class FuelMainnet:
    def __init__(self):
        self.liquidity = 1_000_000
        self.price = 1.0
        self.bridges = []

    def step(self, subnets, agent_registry, message_bus):
        # Handle bridge requests
        for subnet in subnets:
            while subnet.bridge_requests:
                req = subnet.bridge_requests.pop(0)
                amt = req["amount"]
                if self.liquidity >= amt:
                    self.liquidity -= amt
                    subnet.liquidity += amt
                    self.bridges.append(req)
                    message_bus.post_event({"type": "fuel_bridge_complete", "arc": subnet.arc_id, "amount": amt})

    def get_state(self):
        return {"liquidity": self.liquidity, "price": self.price, "bridges": self.bridges}
