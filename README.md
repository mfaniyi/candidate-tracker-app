# Candidate Tracker API

A tested FastAPI CRUD service for managing job candidates.

The API uses an in-memory data store and Pydantic models for request validation and response formatting.

---

## Features

- Create candidates
- Retrieve all candidates
- Retrieve a candidate by ID
- Update candidates
- Delete candidates
- Email validation
- Phone number validation
- Meaningful HTTP status codes
- Pydantic request and response models
- Interactive Swagger/OpenAPI documentation
- Automated pytest test suite

---

## Technologies

- Python
- FastAPI
- Pydantic
- Uvicorn
- pytest
- HTTPX
- uv

---

## Project Structure

```text
candidate-tracker-app/
├── src/
│   └── candidate_tracker_app/
│       ├── __init__.py
│       ├── database.py
│       ├── main.py
│       └── models.py
├── test_main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## Requirements

- Python 3.14+
- uv

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/mfaniyi/candidate-tracker-app.git
cd candidate-tracker-app
```

### Install Dependencies

```bash
uv sync
```

---

## Running the API

Start the FastAPI development server:

```bash
uv run fastapi dev src/candidate_tracker_app/main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically provides interactive Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to view and test all API endpoints.

---

## API Endpoints

| Method | Endpoint | Description | Success Code |
|----------|------------|-------------|--------------|
| POST | `/candidates` | Create a candidate | 201 |
| GET | `/candidates` | Get all candidates | 200 |
| GET | `/candidates/{candidate_id}` | Get one candidate | 200 |
| PUT | `/candidates/{candidate_id}` | Update a candidate | 200 |
| DELETE | `/candidates/{candidate_id}` | Delete a candidate | 204 |

### Not Found Response

If a candidate does not exist, the API returns:

```http
404 Not Found
```

---

## Validation

Candidate data is validated using Pydantic.

### Email Validation

Emails must be valid email addresses.

#### Invalid Example

```json
{
  "email": "not-an-email"
}
```

Response:

```http
422 Unprocessable Entity
```

### Phone Number Validation

Phone numbers must contain between 10 and 15 digits and may optionally begin with `+`.

#### Valid Examples

```text
08012345678
+2348012345678
```

Malformed phone numbers are rejected with:

```http
422 Unprocessable Entity
```

---

## Running Tests

Run the complete test suite with:

```bash
uv run pytest
```

### Test Coverage

The test suite covers:

- Candidate creation
- Email validation
- Phone number validation
- Retrieving candidates
- Updating candidates
- Deleting candidates
- 404 errors for missing candidates

---

## Data Storage

This project uses an in-memory Python list for data storage.

Data is lost when the application stops or restarts.

This is intentional because the assignment focuses on building and testing a FastAPI CRUD service without an external database.

---

## License

This project was created as part of a FastAPI and REST API learning assignment.