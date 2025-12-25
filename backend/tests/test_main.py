from fastapi.testclient import TestClient

# Assuming the FastAPI app instance is in backend/src/main.py
# This will fail until the app is created.
from src.main import app

client = TestClient(app)

def test_health_check():
    """Tests if the /health endpoint returns a 200 OK status code
    and the expected JSON response.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
