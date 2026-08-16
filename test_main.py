from fastapi.testclient import TestClient
from src.candidate_tracker_app.main import app


client = TestClient(app)


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
    response = client.get("/candidates/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_candidate_not_found():
    response = client.get("/candidates/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate not found"


def test_update_candidate():
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
    response = client.delete("/candidates/1")
    assert response.status_code == 204