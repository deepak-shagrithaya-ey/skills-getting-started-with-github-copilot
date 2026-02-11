import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json().get("message", "")


def test_signup_duplicate():
    client.post("/activities/Chess Club/signup?email=dupeuser@mergington.edu")
    response = client.post("/activities/Chess Club/signup?email=dupeuser@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
