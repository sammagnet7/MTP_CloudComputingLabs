import sys
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

def run(results):
    """
    Test 2: Logic & Communication Check
    Verifies that the API handles valid and invalid products correctly.
    """
    test_id = 2
    score = 0
    max_marks = 1
    status = "Fail"
    message = ""

    try:
        # Import student app
        from main import app

        # Use TestClient (FastAPI's built-in tester)
        client = TestClient(app)

        # MOCK the requests.get call so we don't need real network
        with patch("requests.get") as mock_get:
            
            # --- Subtest A: Invalid Product (404) ---
            # Configure mock to return 404
            mock_response_404 = MagicMock()
            mock_response_404.status_code = 404
            mock_get.return_value = mock_response_404

            payload = {"userName": "LogicBot", "rating": 1, "comment": "Fail me"}
            response = client.post("/api/v2/reviews/products/999", json=payload)

            if response.status_code != 404:
                message = f"Logic Error: Expected 404 for non-existent product, got {response.status_code}. Did you implement verify_product_exists?"
                results.append({"testid": test_id, "status": status, "score": score, "maximum marks": max_marks, "message": message})
                return

            # --- Subtest B: Valid Product (200) ---
            # Configure mock to return 200
            mock_response_200 = MagicMock()
            mock_response_200.status_code = 200
            mock_get.return_value = mock_response_200

            response = client.post("/api/v2/reviews/products/1", json=payload)

            if response.status_code == 200:
                score = 1
                status = "Pass"
                message = "API logic handles valid and invalid products correctly."
            else:
                message = f"Logic Error: Valid product request failed with {response.status_code}."

    except ImportError:
        message = "Could not import 'main.py'. Check your syntax."
    except Exception as e:
        message = f"Logic Check Crashed: {str(e)}"

    results.append({
        "testid": test_id,
        "status": status,
        "score": score,
        "maximum marks": max_marks,
        "message": message
    })
