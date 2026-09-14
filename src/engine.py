import operator
from typing import Any, Dict, List

class RuleEngine:
    def __init__(self):
        # Mapping string operators to Python's built-in operators for fast execution
        self.operators = {
            "EQUALS": operator.eq,
            "NOT_EQUALS": operator.ne,
            "GREATER_THAN": operator.gt,
            "LESS_THAN": operator.lt,
            "CONTAINS": lambda user_val, rule_val: rule_val in user_val if isinstance(user_val, (list, str)) else False,
            "NOT_CONTAINS": lambda user_val, rule_val: rule_val not in user_val if isinstance(user_val, (list, str)) else False,
        }

    def evaluate_condition(self, user_context: Dict[str, Any], condition: Dict[str, Any]) -> bool:
        """Evaluates a single condition against the user context."""
        field = condition.get("field")
        op_string = condition.get("operator")
        rule_value = condition.get("value")

        # If the user context doesn't contain the requested field, the condition fails
        if field not in user_context:
            return False

        user_value = user_context[field]
        op_func = self.operators.get(op_string)

        if not op_func:
            return False

        try:
            return op_func(user_value, rule_value)
        except Exception:
            # Safeguard against type mismatches during runtime evaluation
            return False

    def evaluate_rules(self, user_context: Dict[str, Any], rules: List[Dict[str, Any]], logical_operator: str = "AND") -> bool:
        """
        Evaluates a list of targeting rules using a specific logical connection (AND / OR).
        """
        if not rules:
            return True

        results = [self.evaluate_condition(user_context, cond) for cond in rules]

        if logical_operator == "OR":
            return any(results)
        
        # Default fallback is strict "AND" matching
        return all(results)
