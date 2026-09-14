import hashlib
from typing import Dict, Any, List

class EvaluationEngine:
    @staticmethod
    def get_user_percentage(user_id: str, flag_key: str) -> float:
        """
        Hashes the combination of user_id and flag_key using MD5 to generate 
        a deterministic float number between 0.00 and 100.00.
        """
        # Combining user_id and flag_key ensures users are distributed 
        # randomly across different flags, preventing group clustering.
        salt_string = f"{flag_key}:{user_id}".encode("utf-8")
        hash_hex = hashlib.md5(salt_string).hexdigest()
        
        # Take the first 8 characters of the hex hash and convert to integer
        hash_int = int(hash_hex[:8], 16)
        
        # Scale to a 0.00 - 100.00 scale
        return (hash_int % 10000) / 100.0

    def determine_variant(self, user_id: str, flag_key: str, rollout_percentage: float) -> bool:
        """
        Checks if a user falls within the allowed rollout percentage threshold.
        Returns True if the user is selected, False otherwise.
        """
        if rollout_percentage >= 100.0:
            return True
        if rollout_percentage <= 0.0:
            return False

        user_score = self.get_user_percentage(user_id, flag_key)
        return user_score <= rollout_percentage
