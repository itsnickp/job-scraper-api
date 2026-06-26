# Job Scraper API

[![CI](https://github.com/itsnickp/job-scraper-api/actions/workflows/ci.yml/badge.svg)](https://github.com/itsnickp/job-scraper-api/actions/workflows/ci.yml)

A FastAPI backend that collects and serves remote software engineering jobs from multiple sources.

## What This Project Does

- Fetches jobs from Remotive and RemoteOK
- Filters software and IT roles
- Stores jobs in PostgreSQL through SQLAlchemy
- Exposes REST endpoints to synchronize, filter, and paginate jobs
- Runs automated tests with GitHub Actions

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Psycopg2
- Pydantic Settings
- Requests
- Beautiful Soup
- Pytest
- Docker and Docker Compose

## API Endpoints

### Synchronize jobs

```http
POST /jobs/sync
```

Fetches jobs from the configured sources and inserts jobs whose URLs are not already stored.

### List jobs

```http
GET /jobs/
```

Supported query parameters:

| Parameter | Default | Description |
| --- | ---: | --- |
| `source` | — | Filter by source name, such as `remotive` |
| `keyword` | — | Filter by text contained in the job title |
| `skip` | `0` | Number of matching records to skip |
| `limit` | `20` | Number of records to return; maximum `100` |

Examples:

```http
GET /jobs/?keyword=engineer
GET /jobs/?source=remotive&skip=0&limit=20
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Run Locally

### 1. Start PostgreSQL

Run PostgreSQL 15 in Docker:

```bash
docker run --name job-scraper-db \
  -e POSTGRES_DB=jobscraper \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -d postgres:15-alpine
```

### 2. Create the environment file

Linux or macOS:

```bash
cp .env.example .env
```

Windows Command Prompt:

```bat
copy .env.example .env
```

The application loads `.env` automatically through Pydantic Settings. The default template contains:

```dotenv
DATABASE_URL=postgresql://user:password@localhost:5432/jobscraper
```

An exported environment variable overrides the value in `.env`.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the API

```bash
uvicorn app.main:app --reload
```

## Run with Docker Compose

The Compose configuration starts the API and PostgreSQL. The API connects to the database using the `db` service hostname.

```bash
docker compose up --build
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

Stop the services:

```bash
docker compose down
```

Stop the services and remove the PostgreSQL data volume:

```bash
docker compose down -v
```

## Running Tests

The test suite uses a test-only project-level SQLite database so CI does not require a PostgreSQL service. Production and Docker environments continue to use PostgreSQL.

Run all tests:

```bash
python -m pytest -q
```

The tests cover:

- Listing jobs
- Synchronizing scraped jobs
- Filtering jobs by title keyword

## Continuous Integration

The GitHub Actions workflow runs on every push and pull request to `main`. It uses Python 3.11, installs the pinned dependencies, sets a test-only SQLite `DATABASE_URL`, and runs `pytest`.

## Project Structure

```text
job-scraper-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── deps.py
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── scraper/
│   ├── services/
│   ├── sources/
│   ├── utils/
│   └── main.py
├── tests/
│   └── test_jobs.py
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Notes

- SQLAlchemy creates missing tables at application startup.
- Alembic is intentionally not included for this project scope.
- Existing SQLite data is not automatically transferred to PostgreSQL.
