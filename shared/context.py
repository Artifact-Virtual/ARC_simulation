import numpy as np
import random


class MessageBus:
    def __init__(self):
        self.events = []

    def post_event(self, event):
        self.events.append(event)

    def get_events_for_arc(self, arc_id):
        return [e for e in self.events if e.get("target_arc") == arc_id]

    def resolve_cross_arc_events(self, network):
        # Clear after handling; you can expand for actual dispute resolution
        self.events = []

    def get_state(self):
        return {"events": self.events}


class AgentRegistry:
    def __init__(self):
        self.arcs = {}
        
    def register_arc(self, arc_id, arc):
        self.arcs[arc_id] = arc
        
    def arc_counts(self):
        return list(range(len(self.arcs)))


class LiveContextLoop:
    """
    Advanced Multi-ARC Constitutional Intelligence Network.
    Manages a sophisticated network of interconnected ARC blockchains with circular validation,
    ADAM governance protocols, and a unified FUEL economic substrate.
    
    Features:
    - Dynamic ARC addition/removal with circular validation
    - Cross-ARC validation network ensuring system integrity
    - Economic stress propagation across constitutional layers
    - Constitutional era tracking with network-wide consensus
    - Multi-layer event correlation and crisis detection
    - Real-time network topology management
    """
    
    def __init__(self, arc_sim_class, adam_class, fuel_sim, initial_arc_count=3):
        print("🔄 Initializing Advanced Multi-ARC Constitutional Intelligence Network...")
        
        self.arc_sim_class = arc_sim_class
        self.adam_class = adam_class
        self.fuel_sim = fuel_sim
        self.message_bus = MessageBus()
        self.agent_registry = AgentRegistry()
        self.step_count = 0
        self.logs = []
        self.event_log = []
        
        # Multi-ARC network state
        self.arcs = {}  # {arc_id: arc_instance}
        self.adams = {}  # {arc_id: adam_instance}
        self.arc_relationships = {}  # {arc_id: [validator_arc_ids]}
        self.validation_history = {}  # Track cross-ARC validations
        
        # System-wide state tracking
        self.crisis_mode = False
        self.constitutional_era = 1
        self.total_violations = 0
        self.governance_events = []
        self.crisis_indicators = []
        
        # Initialize network with circular validation
        print(f"📜 Creating {initial_arc_count} interconnected constitutional ARCs...")
        for i in range(initial_arc_count):
            self.add_arc(i)
        
        self._setup_circular_validation()
        
        print("✅ Advanced Multi-ARC Constitutional Intelligence Network initialized!")
        
    def add_arc(self, arc_id):
        """Dynamically add a new ARC to the network with automatic validator assignment"""
        if arc_id in self.arcs:
            return False
        
        print(f"🆕 Adding ARC-{arc_id} to network...")
        
        # Create new ARC and ADAM
        self.arcs[arc_id] = self.arc_sim_class(arc_id)
        self.adams[arc_id] = self.adam_class(arc_id)
        self.agent_registry.register_arc(arc_id, self.arcs[arc_id])
        
        # Setup validation relationships
        self._setup_circular_validation()
        
        self.governance_events.append({
            "step": self.step_count,
            "event": "arc_added",
            "arc_id": arc_id,
            "total_arcs": len(self.arcs)
        })
        
        return True
    
    def remove_arc(self, arc_id):
        """Dynamically remove an ARC from the network (minimum 1 ARC required)"""
        if arc_id not in self.arcs or len(self.arcs) <= 1:
            return False  # Can't remove if only one left
        
        print(f"🗑️ Removing ARC-{arc_id} from network...")
        
        # Remove ARC and ADAM
        del self.arcs[arc_id]
        del self.adams[arc_id]
        
        # Rebuild validation relationships
        self._setup_circular_validation()
        
        self.governance_events.append({
            "step": self.step_count,
            "event": "arc_removed",
            "arc_id": arc_id,
            "total_arcs": len(self.arcs)
        })
        
        return True
    
    def _setup_circular_validation(self):
        """Setup circular validation network where each ARC validates others in sequence"""
        arc_ids = sorted(self.arcs.keys())
        n_arcs = len(arc_ids)
        
        if n_arcs == 0:
            return
        
        self.arc_relationships = {}
        for i, arc_id in enumerate(arc_ids):
            validators = []
            
            if n_arcs == 1:
                # Single ARC validates itself
                validators = [arc_id]
            elif n_arcs == 2:
                # Two ARCs validate each other
                other_idx = 1 - i
                validators = [arc_ids[other_idx]]
            else:
                # Multiple ARCs: each validates next two in circular pattern
                next_idx = (i + 1) % n_arcs
                secondary_idx = (i + 2) % n_arcs
                validators = [arc_ids[next_idx], arc_ids[secondary_idx]]
            
            self.arc_relationships[arc_id] = validators
            
        print(f"🔄 Circular validation network: {self.arc_relationships}")
        
    def step(self):
        """Execute comprehensive simulation step with cross-ARC validation"""
        self.step_count += 1
        step_events = []
        self.crisis_indicators = []
        
        # === FUEL Economic Foundation Layer ===
        fuel_stats = self.fuel_sim.get_stats()
        alive_count = len([s for s in fuel_stats if s[2]])
        deaths_this_step = getattr(self.fuel_sim, 'dead_last_step', 0)
        
        # Multi-factor crisis detection
        previous_crisis = self.crisis_mode
        mass_death_crisis = deaths_this_step >= 2
        scheduled_crisis = self.step_count % 50 == 0
        resource_crisis = alive_count <= 3
        
        self.crisis_mode = mass_death_crisis or scheduled_crisis or resource_crisis
        
        if mass_death_crisis:
            self.crisis_indicators.append(f"Mass casualties: {deaths_this_step} agents died")
        if resource_crisis:
            self.crisis_indicators.append(f"Resource shortage: Only {alive_count} agents surviving")
        if scheduled_crisis:
            self.crisis_indicators.append("Scheduled economic stress test")
            
        if self.crisis_mode and not previous_crisis:
            step_events.append(f"🚨 Economic crisis triggered: {'; '.join(self.crisis_indicators)}")
            
        # Step FUEL simulation
        try:
            self.fuel_sim.step(crisis_mode=self.crisis_mode)
        except Exception as e:
            step_events.append(f"FUEL error: {str(e)}")
        
        economic_stress = max(0, (8 - alive_count) / 8.0)
        
        # === ARC Constitutional Layer with Circular Validation ===
        validation_results = {}
        arc_violations = {}
        
        for arc_id in self.arcs:
            try:
                adam = self.adams[arc_id]
                arc = self.arcs[arc_id]
                
                # ARC processes its constitutional block
                violation = arc.step(adam, economic_stress, self.agent_registry, self.message_bus)
                arc_violations[arc_id] = violation
                
                if violation:
                    self.total_violations += 1
                    step_events.append(f"📜 Constitutional violation in ARC-{arc_id}")
                
                # Cross-validation: this ARC validates its assigned targets
                validators = self.arc_relationships.get(arc_id, [])
                for target_id in validators:
                    if target_id in self.arcs and target_id != arc_id:
                        validation_result = self._cross_validate_arc(arc_id, target_id)
                        validation_results[f"{arc_id}→{target_id}"] = validation_result
                        
                        if not validation_result.get("valid", True):
                            step_events.append(f"❌ ARC-{arc_id} rejected ARC-{target_id}'s block")
                        
            except Exception as e:
                step_events.append(f"ARC-{arc_id} error: {str(e)}")
        
        # === ADAM Governance Layer - Network Consensus ===
        governance_actions = []
        network_stress = self._calculate_network_stress(validation_results)
        
        for arc_id, adam in self.adams.items():
            try:
                arc_blocks = self.arcs[arc_id].blocks
                
                # Enhanced governance with network awareness
                action = self._adam_network_governance(
                    adam, arc_blocks, economic_stress, alive_count, 
                    network_stress, arc_violations.get(arc_id, False)
                )
                
                if action:
                    governance_actions.append(f"🧠 ARC-{arc_id}: {action}")
                    
            except Exception as e:
                step_events.append(f"ADAM-{arc_id} error: {str(e)}")
        
        # Network-wide governance consensus
        if governance_actions:
            step_events.extend(governance_actions)
            
            # Constitutional era advancement requires network majority
            if len(governance_actions) >= len(self.arcs) // 2 + 1:
                self.constitutional_era += 1
                step_events.append(f"🏛️ Constitutional era advanced to {self.constitutional_era}")
        
        # === Cross-System Event Resolution ===
        self.message_bus.resolve_cross_arc_events(self.agent_registry)
        
        # === Dynamic Network Management ===
        self._manage_network_dynamics(economic_stress, network_stress, validation_results)
        
        # === State Collection and Logging ===
        if step_events:
            self.event_log.extend(step_events)
            
        state = self.get_current_state()
        state["events"] = step_events
        state["validation_results"] = validation_results
        self.logs.append(state)
        
        # Maintain performance
        if len(self.logs) > 500:
            self.logs = self.logs[-500:]
        if len(self.event_log) > 200:
            self.event_log = self.event_log[-200:]
    
    def _cross_validate_arc(self, validator_id, target_id):
        """Perform sophisticated cross-validation between ARCs"""
        validator_arc = self.arcs[validator_id]
        target_arc = self.arcs[target_id]
        
        if not target_arc.blocks:
            return {"valid": True, "reason": "no_blocks", "validator": validator_id, "target": target_id}
        
        latest_block = target_arc.blocks[-1]
        
        try:
            # Multi-criteria validation
            validator_rule_idx = getattr(validator_arc, 'current_rule_index', 0)
            
            # Primary validation using validator's current rule
            primary_valid = validator_arc._validate_block_with_rule(latest_block, validator_rule_idx)
            
            # Secondary validation: check block structure
            structure_valid = self._validate_block_structure(latest_block)
            
            # Consensus validation: does block align with network standards
            consensus_valid = self._validate_network_consensus(latest_block, validator_id)
            
            overall_valid = primary_valid and structure_valid and consensus_valid
            
            result = {
                "valid": overall_valid,
                "validator": validator_id,
                "target": target_id,
                "block_step": latest_block.get("step", 0),
                "rule_used": validator_rule_idx,
                "primary_valid": primary_valid,
                "structure_valid": structure_valid,
                "consensus_valid": consensus_valid,
                "timestamp": self.step_count
            }
            
            # Track validation history for network analysis
            key = f"{validator_id}→{target_id}"
            if key not in self.validation_history:
                self.validation_history[key] = []
            self.validation_history[key].append(result)
            
            # Keep recent history only
            if len(self.validation_history[key]) > 50:
                self.validation_history[key] = self.validation_history[key][-50:]
            
            return result
            
        except Exception as e:
            return {
                "valid": False, 
                "error": str(e),
                "validator": validator_id,
                "target": target_id
            }
    
    def _validate_block_structure(self, block):
        """Validate basic block structure requirements"""
        required_fields = ["step", "data", "valid"]
        return all(field in block for field in required_fields)
    
    def _validate_network_consensus(self, block, validator_id):
        """Check if block aligns with current network consensus rules"""
        # Simplified consensus: block should have reasonable step progression
        if "step" in block:
            return abs(block["step"] - self.step_count) <= 5
        return True
    
    def _adam_network_governance(self, adam, arc_blocks, economic_stress, alive_count, network_stress, has_violation):
        """Enhanced ADAM governance with network awareness"""
        try:
            # Standard ADAM governance
            base_action = adam.observe_and_govern(
                arc_blocks, economic_stress, alive_count, self.crisis_mode
            )
            
            # Network-specific enhancements
            if network_stress > 0.5:
                return f"{base_action}; network_stress_response" if base_action else "network_stabilization"
            elif has_violation and economic_stress > 0.3:
                return f"{base_action}; violation_economic_response" if base_action else "crisis_management"
            
            return base_action
            
        except Exception:
            # Fallback governance action
            if network_stress > 0.7:
                return "emergency_governance"
            return None
    
    def _calculate_network_stress(self, validation_results):
        """Calculate comprehensive network validation stress"""
        if not validation_results:
            return 0.0
        
        total_validations = len(validation_results)
        failed_validations = sum(1 for r in validation_results.values() if not r.get("valid", True))
        
        return failed_validations / total_validations if total_validations > 0 else 0.0
    
    def _manage_network_dynamics(self, economic_stress, network_stress, validation_results):
        """Intelligent dynamic ARC network management"""
        current_arc_count = len(self.arcs)
        
        # Network expansion conditions
        expansion_conditions = (
            economic_stress < 0.2 and           # Economy is stable
            network_stress < 0.1 and           # Network is healthy
            current_arc_count < 6 and          # Not too many ARCs
            self.step_count % 100 == 0         # Periodic expansion check
        )
        
        if expansion_conditions:
            new_id = max(self.arcs.keys()) + 1 if self.arcs else 0
            if self.add_arc(new_id):
                self.event_log.append(f"🆕 Network expanded: Added ARC-{new_id}")
        
        # Network contraction conditions
        contraction_conditions = (
            (network_stress > 0.6 or economic_stress > 0.8) and  # High stress
            current_arc_count > 2 and                            # Keep minimum viable network
            self.step_count % 150 == 0                           # Periodic contraction check
        )
        
        if contraction_conditions:
            problematic_arc = self._find_most_problematic_arc(validation_results)
            if problematic_arc is not None and self.remove_arc(problematic_arc):
                self.event_log.append(f"🗑️ Network contracted: Removed ARC-{problematic_arc}")
    
    def _find_most_problematic_arc(self, validation_results):
        """Identify ARC causing most validation failures"""
        arc_failure_counts = {}
        
        for key, result in validation_results.items():
            if not result.get("valid", True):
                target_id = result.get("target")
                if target_id is not None:
                    arc_failure_counts[target_id] = arc_failure_counts.get(target_id, 0) + 1
        
        if arc_failure_counts:
            return max(arc_failure_counts.keys(), key=lambda k: arc_failure_counts[k])
        return None
        
    def get_current_state(self):
        """Generate comprehensive multi-ARC network state for dashboard"""
        
        # === Economic Layer Metrics ===
        fuel_stats = self.fuel_sim.get_stats()
        alive_agents = [stat for stat in fuel_stats if stat[2]]
        dead_agents = [stat for stat in fuel_stats if not stat[2]]
        
        fuel_levels = [stat[1] for stat in alive_agents] if alive_agents else [0]
        avg_fuel = np.mean(fuel_levels)
        
        # === Multi-ARC Network Architecture ===
        network_arcs = []
        for arc_id, arc in self.arcs.items():
            adam = self.adams[arc_id]
            
            # Collect validation metrics for this ARC
            validator_count = len(self.arc_relationships.get(arc_id, []))
            recent_failures = sum(1 for key, history in self.validation_history.items()
                                if key.startswith(f"{arc_id}→") 
                                for result in history[-10:] 
                                if not result.get("valid", True))
            
            arc_data = {
                "arc_id": arc_id,
                "total_blocks": len(arc.blocks),
                "disputed_blocks": len(getattr(arc, 'disputed_blocks', [])),
                "last_block_valid": arc.blocks[-1]["valid"] if arc.blocks else True,
                "current_rule": getattr(arc, 'current_rule_index', 0),
                "rule_strictness": getattr(arc, 'rule_strictness', 1.0),
                "validators": self.arc_relationships.get(arc_id, []),
                "validator_count": validator_count,
                "recent_validation_failures": recent_failures,
                "adam_guilt": getattr(adam, 'guilt', 0),
                "adam_policy": getattr(adam, 'policy', 'moderate'),
                "council_events": len(getattr(adam, 'council_log', []))
            }
            network_arcs.append(arc_data)
        
        # === Validation Network Metrics ===
        total_validation_pairs = len(self.validation_history)
        recent_network_failures = sum(
            1 for history in self.validation_history.values()
            for result in history[-5:] 
            if not result.get("valid", True)
        )
        
        validation_metrics = {
            "total_validation_pairs": total_validation_pairs,
            "recent_failures": recent_network_failures,
            "network_stress": self._calculate_network_stress(getattr(self, '_last_validation_results', {})),
            "circular_validation_active": len(self.arc_relationships) > 0,
            "average_validators_per_arc": np.mean([len(validators) for validators in self.arc_relationships.values()]) if self.arc_relationships else 0
        }
        
        # === Comprehensive State Structure ===
        return {
            # Core simulation metrics
            "step": self.step_count,
            "era": self.constitutional_era,
            "crisis_mode": self.crisis_mode,
            "crisis_indicators": self.crisis_indicators,
            
            # Advanced network state for sophisticated dashboard
            "network_state": {
                "arcs": network_arcs,
                "validation_relationships": self.arc_relationships,
                "validation_metrics": validation_metrics,
                "total_arc_count": len(self.arcs),
                "active_validators": len([arc for arc in network_arcs if arc["validators"]]),
                "network_topology": "circular",
                "dynamic_management_active": True
            },
            
            # Economic substrate metrics
            "fuel_alive": len(alive_agents),
            "fuel_dead": len(dead_agents),
            "fuel_avg": float(avg_fuel),
            "fuel_deaths_this_step": getattr(self.fuel_sim, 'dead_last_step', 0),
            "economic_stress": max(0, (8 - len(alive_agents)) / 8.0),
            "economic_health": 1.0 - max(0, (8 - len(alive_agents)) / 8.0),
            
            # Governance and constitutional metrics
            "total_violations": self.total_violations,
            "governance_events": self.governance_events[-20:],
            "system_events": self.event_log[-10:],
            "constitutional_stability": 1.0 - min(1.0, self.total_violations / max(1, self.step_count)),
            
            # Cross-system integration metrics
            "total_disputes": len(self.message_bus.events),
            "system_complexity": len(self.arcs) * len(self.validation_history),
            "integration_health": 1.0 - validation_metrics["network_stress"],
            
            # Legacy compatibility for existing dashboard components
            "adam_scores": np.array([arc["council_events"] for arc in network_arcs]),
            "adam_guilt": np.array([arc["adam_guilt"] for arc in network_arcs]),
            "adam_policies": [arc["adam_policy"] for arc in network_arcs],
            "arc_data": network_arcs
        }
