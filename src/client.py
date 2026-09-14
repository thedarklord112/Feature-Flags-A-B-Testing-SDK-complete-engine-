from typing import Dict, Any, Optional
from src.engine import RuleEngine
from src.evaluation import EvaluationEngine

class FeatureFlagClient:
    def __init__(self, flags_config: Dict[str, Any]):
        """
        Initializes the SDK Client with a configuration dictionary 
        containing all available flags and their custom targeting rules.
        """
        self.flags = flags_config
        self.rule_engine = RuleEngine()
        self.eval_engine = EvaluationEngine()

    def is_enabled(self, flag_key: str, user_context: Dict[str, Any], fallback: bool = False) -> bool:
        """
        Determines whether a specific feature flag is active for a given user context.
        Evaluates targeting conditions first, then applies percentage rollouts.
        """
        # If the flag doesn't exist in our configuration, return the user-defined fallback
        if flag_key not in self.flags:
            return fallback

        flag_data = self.flags[flag_key]
        
        # 1. Global Kill-Switch Check
        if not flag_data.get("is_active", True):
            return False

        # 2. Targeted Strategy & Rules Evaluation
        rules = flag_data.get("rules", [])
        logical_operator = flag_data.get("logical_operator", "AND")
        
        # If the user context fails the specific targeting conditions, the flag is denied
        if not self.rule_engine.evaluate_rules(user_context, rules, logical_operator):
            return False

        # 3. Deterministic Percentage Rollout Check
        user_id = user_context.get("id")
        if not user_id:
            # If no user ID is provided, we cannot evaluate percentage distributions safely
            return False

        rollout_percentage = flag_data.get("rollout_percentage", 100.0)
        return self.eval_engine.determine_variant(user_id, flag_key, rollout_percentage)
