from fastapi import FastAPI

app = FastAPI(
    title="Candidate Tracker API",
    description="An API for managing job candidates.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Candidate Tracker API is running"}