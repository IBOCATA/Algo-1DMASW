import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_token_success():
    response = client.post("/token", data={"username": "admin", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_token_fail():
    response = client.post("/token", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
