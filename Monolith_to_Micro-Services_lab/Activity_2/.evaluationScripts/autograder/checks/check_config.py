import sys
import os

def run(results):
    """
    Test 1: Configuration Check
    Verifies DATABASE_URL in database.py points to the /data volume.
    """
    test_id = 1
    score = 0
    max_marks = 1
    
    try:
        # Import the student's database module
        import database
        
        # Reload to ensure we get fresh values if run multiple times
        import importlib
        importlib.reload(database)

        db_url = getattr(database, "DATABASE_URL", "")

        # Check for /data or /app/data
        if "/data/" in db_url or "/app/data" in db_url:
            status = "Pass"
            score = 1
            message = "DATABASE_URL correctly configured for Docker Volumes."
        elif "sqlite:///./reviews.db" in db_url:
            status = "Fail"
            message = "DATABASE_URL is still pointing to local file (./reviews.db). Persistence will fail."
        else:
            status = "Fail"
            message = f"DATABASE_URL is incorrect: {db_url}"

    except ImportError:
        status = "Fail"
        message = "Could not import 'database.py'. Check your syntax."
    except Exception as e:
        status = "Fail"
        message = f"Error analyzing configuration: {str(e)}"

    results.append({
        "testid": test_id,
        "status": status,
        "score": score,
        "maximum marks": max_marks,
        "message": message
    })
