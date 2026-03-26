import sys
import os

# Define where the student code lives relative to this script
STUDENT_CODE_DIR = os.path.abspath("microservices/eCommerce-ReviewService")

def setup_paths():
    """
    Adds the student's code directory to sys.path so we can import their modules.
    """
    if STUDENT_CODE_DIR not in sys.path:
        sys.path.insert(0, STUDENT_CODE_DIR)

    # Check if the directory actually exists
    if not os.path.exists(STUDENT_CODE_DIR):
        print(f"CRITICAL ERROR: Student directory not found at {STUDENT_CODE_DIR}")
        return False
    return True
