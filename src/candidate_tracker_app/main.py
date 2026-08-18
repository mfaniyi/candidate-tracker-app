from fastapi import FastAPI, status, HTTPException
from .models import Candidate, CandidateCreate
from .database import candidates, next_candidate_id

app = FastAPI(
    title="Candidate Tracker API",
    description="An API for managing job candidates.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Candidate Tracker API is running"}


@app.post(
    "/candidates",
    response_model=Candidate,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate(candidate: CandidateCreate):
    global next_candidate_id
    new_candidate = {
        "id": next_candidate_id,
        "name": candidate.name,
        "email": candidate.email,
        "phone": candidate.phone,
        "position": candidate.position,
    }
    candidates.append(new_candidate)
    next_candidate_id += 1
    return new_candidate


@app.get("/candidates", response_model=list[Candidate])
def get_candidates():
    return candidates


@app.get("/candidates/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id: int):
    for candidate in candidates:
        if candidate["id"] == candidate_id:
            return candidate
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Candidate not found",
    )


@app.put("/candidates/{candidate_id}", response_model=Candidate)
def update_candidate(candidate_id: int, candidate: CandidateCreate):
    for index, existing_candidate in enumerate(candidates):
        if existing_candidate["id"] == candidate_id:
            updated_candidate = {
                "id": candidate_id,
                "name": candidate.name,
                "email": candidate.email,
                "phone": candidate.phone,
                "position": candidate.position,
            }
            candidates[index] = updated_candidate
            return updated_candidate
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Candidate not found",
    )


@app.delete("/candidates/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(candidate_id: int):
    for index, candidate in enumerate(candidates):
        if candidate["id"] == candidate_id:
            candidates.pop(index)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Candidate not found",
    )