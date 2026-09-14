import unittest
from src.client import FeatureFlagClient

class TestFeatureFlagEngine(unittest.TestCase):
    def setUp(self):
        # Setting up a complex configuration simulating real-world production flags
        self.mock_flags_config = {
            "premium-dashboard-feature": {
                "is_active": True,
                "rollout_percentage": 50.0,  # Only 50% of targeted users get the feature
                "logical_operator": "AND",
                "rules": [
                    {"field": "country", "operator": "EQUALS", "value": "Brazil"},
                    {"field": "tags", "operator": "CONTAINS", "value": "beta-tester"}
                ]
            }
        }
        self.client = FeatureFlagClient(self.mock_flags_config)

    def test_user_matches_all_rules_and_passes_rollout(self):
        """Should return True if user is from Brazil, is a beta-tester, and falls within the 50% threshold."""
        user_context = {
            "id": "user_26",  # This specific ID combined with the key hashes below 50.0%
            "country": "Brazil",
            "tags": ["beta-tester", "developer"]
        }
        result = self.client.is_enabled("premium-dashboard-feature", user_context)
        self.assertTrue(result)

    def test_user_fails_country_rule(self):
        """Should return False if user matches tags but is from USA."""
        user_context = {
            "id": "user_26",
            "country": "USA",
            "tags": ["beta-tester"]
        }
        result = self.client.is_enabled("premium-dashboard-feature", user_context)
        self.assertFalse(result)

    def test_user_missing_required_tag(self):
        """Should return False if user is from Brazil but does not have the beta-tester tag."""
        user_context = {
            "id": "user_26",
            "country": "Brazil",
            "tags": ["regular-user"]
        }
        result = self.client.is_enabled("premium-dashboard-feature", user_context)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
