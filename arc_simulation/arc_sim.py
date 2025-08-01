import random


class ArcSimulator:
    def __init__(self, arc_id):
        self.arc_id = arc_id
        self.blocks = []
        self.rules = [self.default_rule for _ in range(7)]
        self.rule_names = ["default_rule"]*7
        self.disputed_blocks = set()
        self.history = []

    def step(self, adam, subnet, agent_registry, message_bus):
        idx = len(self.blocks)
        rule_idx = (idx-1) % 7
        prev_block = self.blocks[-1] if self.blocks else None
        data = {"type": "regular", "arc": self.arc_id, "content": f"Block {idx}"}
        valid = self.rules[rule_idx](prev_block, data) if prev_block else True
        block = {
            "index": idx,
            "arc": self.arc_id,
            "rule": self.rule_names[rule_idx],
            "valid": valid,
            "disputed": False,
            "content": data["content"]
        }
        self.blocks.append(block)
        # Randomly, issue a dispute/challenge to another ARC
        if valid and random.random() < 0.1:
            arc_counts = agent_registry.arc_counts()
            available_arcs = [a for a in range(len(arc_counts)) if a != self.arc_id]
            if available_arcs:
                target_arc = random.choice(available_arcs)
                message_bus.post_event({
                    "type": "block_challenge",
                    "from_arc": self.arc_id,
                    "target_arc": target_arc,
                    "target_block": idx
                })
        # Respond to incoming disputes
        for evt in message_bus.get_events_for_arc(self.arc_id):
            if evt["type"] == "block_challenge" and evt["target_block"] < len(self.blocks):
                self.blocks[evt["target_block"]]["disputed"] = True
                self.disputed_blocks.add(evt["target_block"])
        # Allow ADAM to evolve rules if disputes mount
        if len(self.disputed_blocks) > 2:
            adam.trigger_council("dispute crisis")
            self.disputed_blocks.clear()
        self.history.append(block)

    def default_rule(self, prev_block, data):
        # Accept all, unless content contains a "bad" number
        return "4" not in data["content"]

    def get_state(self):
        return {
            "arc_id": self.arc_id,
            "blocks": self.blocks[-14:],
            "rules": self.rule_names
        }
