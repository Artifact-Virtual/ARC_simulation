class FuelSubnet:
    def __init__(self, arc_id):
        self.arc_id = arc_id
        self.liquidity = 100_000
        self.bridge_requests = []

    def request_fuel(self, amt):
        self.bridge_requests.append({"arc": self.arc_id, "amount": amt})

    def get_state(self):
        return {"arc_id": self.arc_id, "liquidity": self.liquidity}
