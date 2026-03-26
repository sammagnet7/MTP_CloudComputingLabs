import os
import sqlalchemy
from sqlalchemy import create_engine, text

def run(results):
    """
    Test 3: Database Integration Check
    Verifies that data is ACTUALLY written to the SQLite file.
    """
    test_id = 3
    score = 0
    max_marks = 1
    status = "Fail"
    message = ""

    # Path to the DB file (We check both default and /data locations)
    # Since we are running in the grader (same container/fs), we need to find where they wrote it.
    
    # We inspect their config to find the path
    try:
        import database
        db_url = database.DATABASE_URL
        # Convert 'sqlite:///./reviews.db' -> './reviews.db'
        db_path = db_url.replace("sqlite:///", "")
        
        # Handle absolute paths if they used /data
        if db_path.startswith("/"):
            # Ensure we can access it (we are root in grader usually)
            pass
    except:
        db_path = "reviews.db" # Fallback

    try:
        # Create a direct connection to their DB
        engine = create_engine(f"sqlite:///{db_path}")
        
        # Verify the LogicBot data we inserted in Test 2 exists
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM reviews WHERE user_name='LogicBot'"))
            row = result.fetchone()
            
            if row:
                score = 1
                status = "Pass"
                message = "Data verification successful. Row found in SQLite database."
            else:
                message = "Integration Fail: API returned 200, but data was NOT found in the database file."

    except Exception as e:
        message = f"Database Inspection Failed: {str(e)}. (Path checked: {db_path})"

    results.append({
        "testid": test_id,
        "status": status,
        "score": score,
        "maximum marks": max_marks,
        "message": message
    })
