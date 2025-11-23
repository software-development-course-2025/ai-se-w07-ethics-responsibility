"""
policy_checker.py
Minimal prototype to validate JSON policy documents against a set of required controls.
Usage:
    python src/policy_checker.py examples/sample_policies.json
"""

import json
import sys
from src.utils import load_json

REQUIRED_CONTROLS = [
    "model_card",
    "data_provenance",
    "privacy_assessment",
    "fairness_report",
    "monitoring_plan",
]

def score_policy(policy):
    results = {}
    for c in REQUIRED_CONTROLS:
        results[c] = bool(policy.get(c))
    # simple score: fraction of controls present
    score = sum(results.values()) / len(REQUIRED_CONTROLS)
    return results, score

def main(path):
    try:
        policies = load_json(path)
    except Exception as e:
        print("Error loading policies:", e)
        return 1
    if isinstance(policies, dict):
        policies = [policies]
    for i, p in enumerate(policies, start=1):
        results, score = score_policy(p)
        print(f"\nPolicy #{i} score: {score:.2f}")
        for k, v in results.items():
            print(f" - {k}: {'OK' if v else 'MISSING'}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/policy_checker.py path/to/policies.json")
    else:
        sys.exit(main(sys.argv[1]))

