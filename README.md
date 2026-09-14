<img width="1425" height="723" alt="image" src="https://github.com/user-attachments/assets/bc48fc6a-6fe5-4b0f-ab5e-031f166687b8" />


# 🚀 The "Don't Break Prod on a Friday" Feature Flag SDK

A lightweight, blazing-fast, and completely stateless **Feature Flag & A/B Testing SDK** written in pure, organic Python. 

Are you tired of deploying code at 4:59 PM on a Friday and praying to the server gods? Do you want to hide your half-baked features from your boss while testing them live? Or maybe you just don't want to pay thousands of dollars to expensive SaaS tools just to see if a blue button converts better than a red one? 

**This SDK is your shield. Welcome to stress-free production.**

---

## ⚡ Why Use This? (Besides being free)

- **Microsecond In-Memory Speed**: We don't do slow database queries here. Your server checks rules faster than your project manager changes requirements.
- **Pure Math Wizardry**: Uses cryptographic MD5 hashing to distribute users into A/B test percentages deterministically. No state saved. If `user_42` is in the 20% test group today, they stay there tomorrow. No tracking, no database storage, just pure math.
- **The Ultimate Kill-Switch**: Did your new feature start spitting out 500 internal server errors? Flip `is_active` to `False` in your config. Boom. Instantly rolled back without a single code redeploy. Go back to drinking your coffee.
- **Overkill Rule Customization**: Chain together complex logical rules (`AND` / `OR`). Target only developers from Brazil who are beta testers and have an even user ID. Because why not.

---

## 📂 Inside the Machine

```text
├── src/
│   ├── client.py        # The brain you actually talk to
│   ├── engine.py        # The cold, logical rule evaluator (No if/else spaghetti here)
│   └── evaluation.py    # The cryptographic MD5 lottery machine
└── tests/
    └── test_engine.py   # Proof to your team that your code actually works
```

---

## 🛠️ Quick Start (Before everything catches fire)

Here is how you inject this safety net into your Python project:

```python
from src.client import FeatureFlagClient

# 1. Define your chaotic rules (Usually loaded from a JSON file so you can change it on the fly)
chaos_control_config = {
    "shaky-new-payment-gateway": {
        "is_active": True,
        "rollout_percentage": 25.0,  # Only sacrifice 25% of your traffic to test it
        "logical_operator": "AND",
        "rules": [
            {"field": "country", "operator": "EQUALS", "value": "Brazil"},
            {"field": "tags", "operator": "CONTAINS", "value": "brave-beta-tester"}
        ]
    }
}

# 2. Boot up the SDK
guard_dog = FeatureFlagClient(chaos_control_config)

# 3. Define the brave user currently visiting your app
unsuspecting_user = {
    "id": "user_26",
    "country": "Brazil",
    "tags": ["brave-beta-tester", "coffee-drinker"]
}

# 4. Cross your fingers and check the flag
if guard_dog.is_enabled("shaky-new-payment-gateway", unsuspecting_user):
    print("🚀 Living dangerously! Serving the new feature.")
else:
    print("🔒 Safe and sound. Serving the old, boring, functional UI.")
```

---

## 🧪 Testing the Matrix

To run the automated tests and prove to your Tech Lead that you write clean code:

```bash
python -m unittest discover -s tests
```

## 📄 License
This codebase is completely free and open-source under the **MIT License**. Use it to save your production environment, build your startup, or just flex on your coworkers.
