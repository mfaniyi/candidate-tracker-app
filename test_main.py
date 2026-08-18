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
    create_response = client.post(
        "/candidates",
        json={
            "name": "Michael",
            "email": "michael@example.com",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    candidate_id = create_response.json()["id"]
    response = client.get(f"/candidates/{candidate_id}")
    assert response.status_code == 200
    assert response.json()["id"] == candidate_id


def test_candidate_not_found():
    response = client.get("/candidates/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate not found"


def test_update_candidate():
    create_response = client.post(
        "/candidates",
        json={
            "name": "Michael",
            "email": "michael@example.com",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    candidate_id = create_response.json()["id"]
    response = client.put(
        f"/candidates/{candidate_id}",
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
    create_response = client.post(
        "/candidates",
        json={
            "name": "Michael",
            "email": "michael@example.com",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    candidate_id = create_response.json()["id"]
    response = client.delete(f"/candidates/{candidate_id}")
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


def test_update_candidate_invalid_email():
    create_response = client.post(
        "/candidates",
        json={
            "name": "Michael",
            "email": "michael@example.com",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    candidate_id = create_response.json()["id"]
    response = client.put(
        f"/candidates/{candidate_id}",
        json={
            "name": "Michael",
            "email": "not-an-email",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    assert response.status_code == 422


def test_get_candidate_after_deletion():
    create_response = client.post(
        "/candidates",
        json={
            "name": "Michael",
            "email": "michael@example.com",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    candidate_id = create_response.json()["id"]
    delete_response = client.delete(f"/candidates/{candidate_id}")
    assert delete_response.status_code == 204
    get_response = client.get(f"/candidates/{candidate_id}")
    assert get_response.status_code == 404


def test_candidate_id_is_monotonic():
    first_response = client.post(
        "/candidates",
        json={
            "name": "First Candidate",
            "email": "first@example.com",
            "phone": "08012345678",
            "position": "AI Engineer",
        },
    )
    first_id = first_response.json()["id"]
    delete_response = client.delete(f"/candidates/{first_id}")
    assert delete_response.status_code == 204
    second_response = client.post(
        "/candidates",
        json={
            "name": "Second Candidate",
            "email": "second@example.com",
            "phone": "08087654321",
            "position": "ML Engineer",
        },
    )
    second_id = second_response.json()["id"]
    assert second_id > first_id