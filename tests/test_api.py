"""Tests for API endpoints"""

import pytest
from fastapi.testclient import TestClient
from src.api.app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_api_info(client):
    """Test API info endpoint"""
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "models" in data
    assert "thresholds" in data
    assert "anonymization" in data


def test_anonymize_no_file(client):
    """Test anonymize endpoint without file"""
    response = client.post("/api/v1/anonymize")
    assert response.status_code == 422  # Unprocessable Entity


def test_anonymize_invalid_format(client):
    """Test anonymize endpoint with invalid file format"""
    files = {"file": ("test.txt", b"not an image", "text/plain")}
    response = client.post("/api/v1/anonymize", files=files)
    assert response.status_code in [400, 500]


def test_anonymize_oversized_file(client):
    """Test anonymize endpoint with oversized file"""
    # Create a file larger than 10MB
    large_data = b"x" * (11 * 1024 * 1024)  # 11MB
    files = {"file": ("large.jpg", large_data, "image/jpeg")}
    response = client.post("/api/v1/anonymize", files=files)
    assert response.status_code in [400, 413]

