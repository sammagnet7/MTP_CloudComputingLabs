#!/usr/bin/python3
import json
import os
import sys

# Import our helper modules
import conftest
from checks import check_config, check_logic, check_db

# Results container
overall = {"data": []}
RESULTS_FILE = '/home/.evaluationScripts/evaluate.json'

def main():
    print("--- 🤖 Starting White Box Autograder ---")
    
    # 1. Setup Environment
    if not conftest.setup_paths():
        print("❌ Critical: Could not find student code.")
        return

    # 2. Run Checks
    print("\nRunning Static Analysis...")
    check_config.run(overall["data"])

    print("\nRunning Logic Verification...")
    check_logic.run(overall["data"])

    print("\nRunning Database Inspection...")
    check_db.run(overall["data"])

    # 3. Write Results
    try:
        with open(RESULTS_FILE, 'w', encoding='utf-8') as file:
            json.dump(overall, file, indent=4)
        print(f"\n✅ Results saved to {RESULTS_FILE}")
    except Exception as e:
        print(f"\n❌ Failed to write results: {e}")

if __name__ == "__main__":
    main()
