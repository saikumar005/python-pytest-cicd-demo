import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test GET /health returns HTTP 200 OK and status JSON."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "python-testing"}


def test_calculate_addition():
    """Test POST /calculate with valid addition request."""
    payload = {"operation": "add", "a": 10.0, "b": 5.0}
    response = client.post("/calculate", json=payload)
    
    assert response.status_code == 200
    assert response.json()["result"] == 15.0


def test_calculate_division_by_zero():
    """Test POST /calculate with zero division returns HTTP 400 Bad Request."""
    payload = {"operation": "divide", "a": 10.0, "b": 0.0}
    response = client.post("/calculate", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero"


def test_invalid_operation():
    """Test POST /calculate with unknown operation returns HTTP 400 Bad Request."""
    payload = {"operation": "power", "a": 2.0, "b": 3.0}
    response = client.post("/calculate", json=payload)
    
    assert response.status_code == 400
    assert "Unsupported operation" in response.json()["detail"]
