class AdamAgent:
    def __init__(self, arc_id):
        self.arc_id = arc_id
        self.policy = "default"
        self.guilt = 0
        self.history = []
        self.council_log = []

    def trigger_council(self, reason):
        # Called by ARC when in crisis/dispute mode
        self.council_log.append({"event": "council", "arc_id": self.arc_id, "reason": reason})
        self.evolve_policy(force=True)

    def evolve_policy(self, force=False):
        # Make rules stricter or more lenient
        if force or self.guilt > 2:
            self.policy = "emergency_policy"
            self.guilt = 0
        else:
            self.policy = "default"
        self.history.append(self.policy)

    def observe_and_govern(self, arc_blocks, economic_stress, alive_count, crisis_mode):
        """Enhanced governance method for network-aware ADAM"""
        # Observe economic stress and adjust guilt
        if economic_stress > 0.5:
            self.guilt += economic_stress * 0.2
        
        # Crisis response
        if crisis_mode:
            self.guilt += 0.3
            if self.guilt > 0.8:
                self.evolve_policy(force=True)
                return "emergency_governance_activated"
        
        # Normal governance based on ARC performance
        if arc_blocks:
            recent_violations = sum(1 for block in arc_blocks[-5:] if not block.get("valid", True))
            if recent_violations > 2:
                self.guilt += 0.1
                return "rule_enforcement_increased"
        
        # Gradual guilt decay in stable periods
        if not crisis_mode and economic_stress < 0.3:
            self.guilt = max(0, self.guilt - 0.05)
        
        # Policy evolution based on accumulated guilt
        if self.guilt > 1.0:
            self.evolve_policy(force=True)
            return "policy_evolution_triggered"
        
        return None

    def get_state(self):
        return {
            "arc_id": self.arc_id,
            "policy": self.policy,
            "council_log": self.council_log,
            "guilt": self.guilt
        }
