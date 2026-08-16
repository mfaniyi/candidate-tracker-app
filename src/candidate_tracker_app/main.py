from fastapi import FastAPI, status, HTTPException
from .models import Candidate
from .database import candidates

app = FastAPI(
    title="Candidate Tracker API",
    description="An API for managing job candidates.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Candidate Tracker API is running"}


@app.post("/candidates", status_code=status.HTTP_201_CREATED)
def create_candidate(candidate: Candidate):
    new_candidate = {
        "id": len(candidates) + 1,
        "name": candidate.name,
        "email": candidate.email,
        "phone": candidate.phone,
        "position": candidate.position,
    }
    candidates.append(new_candidate)
    return new_candidate


@app.get("/candidates")
def get_candidates():
    return candidates


@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: int):
    for candidate in candidates:
        if candidate["id"] == candidate_id:
            return candidate

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Candidate not found",
    )