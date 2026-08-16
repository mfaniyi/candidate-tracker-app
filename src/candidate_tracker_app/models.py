from pydantic import BaseModel, EmailStr, Field


class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(
        min_length=10,
        max_length=15,
        pattern=r"^\+?[0-9]+$",
    )
    position: str


class Candidate(CandidateCreate):
    id: int