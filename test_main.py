from fastapi.testclient import TestClient
import pytest
from src.candidate_tracker_app.main import app
from src.candidate_tracker_app.database import candidates

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_candidates():
    candidates.clear()
    yield


def test_create_candidate():
    response = client.post(
        "/candidates",
        json={
            "name": "Michael Faniyi",
            "email": "mfaniyi@yahoo.com",
            "phone": "08026554422",
            "position": "AI Engineer",
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Michael Faniyi"


def test_invalid_email():
    response = client.post(
        "/candidates",
        json={
            "name": "Michael Famiyi",
            "email": "michael-faniyi",
            "phone": "08026554422",
            "position": "AI Engineer",
        },
    )
    assert response.status_code == 422


def test_invalid_phone():
    response = client.post(
        "/candidates",
        json={
            "name": "Michael Faniyi",
            "email": "mfaniyi@yahoo.com",
            "phone": "my-phone-number",
            "position": "AI Engineer",
        },
    )
    assert response.status_code == 422


def test_get_candidates():
    response = client.get("/candidates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_candidate():
    client.post(
        "/candidates",
        json={
            "name": "Michael",
            "email": "michael@example.com",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    response = client.get("/candidates/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_candidate_not_found():
    response = client.get("/candidates/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate not found"


def test_update_candidate():
    client.post(
        "/candidates",
        json={
            "name": "Michael",
            "email": "michael@example.com",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    response = client.put(
        "/candidates/1",
        json={
            "name": "Michael Olawole",
            "email": "olawole@yahoo.com",
            "phone": "08034870324",
            "position": "ML Engineer",
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Michael Olawole"


def test_delete_candidate():
    client.post(
        "/candidates",
        json={
            "name": "Michael",
            "email": "michael@example.com",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    response = client.delete("/candidates/1")
    assert response.status_code == 204


def test_update_candidate_not_found():
    response = client.put(
        "/candidates/999",
        json={
            "name": "Michael",
            "email": "michael@example.com",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate not found"


def test_delete_candidate_not_found():
    response = client.delete("/candidates/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate not found"