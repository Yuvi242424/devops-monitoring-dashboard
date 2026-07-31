import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_health():
    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"


def test_system():
    client = app.test_client()

    response = client.get("/api/system")

    assert response.status_code == 200

    data = response.get_json()

    assert "cpu" in data
    assert "memory" in data
    assert "disk" in data
    assert "uptime" in data
    assert "processes" in data


def test_generate_load():
    client = app.test_client()

    response = client.post("/api/load")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Load Generated"


def test_generate_error():
    client = app.test_client()

    response = client.post("/api/error")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Error Generated"
