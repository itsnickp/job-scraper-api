import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

import pytest
from fastapi.testclient import TestClient
from httpx import Response

from app.core.database import Base, SessionLocal, engine
from app.main import app
from app.models.job import Job

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_jobs_returns_200():
    response: Response = client.get("/jobs/")

    assert response.status_code == 200
    assert response.json() == []


def test_sync_jobs_returns_200(monkeypatch):
    from app.scraper import jobs as jobs_scraper

    scraped_jobs = [
        {
            "title": "Backend Engineer",
            "company": "Example Company",
            "location": "Remote",
            "url": "https://example.com/jobs/backend-engineer",
            "source": "test",
        }
    ]
    monkeypatch.setattr(jobs_scraper, "scrape_jobs", lambda: scraped_jobs)

    response: Response = client.post("/jobs/sync")

    assert response.status_code == 200
    assert response.json() == {"scraped": 1, "inserted": 1}


def test_get_jobs_filters_by_keyword():
    db = SessionLocal()

    try:
        db.add_all(
            [
                Job(
                    title="Backend Engineer",
                    company="Example Company",
                    location="Remote",
                    url="https://example.com/jobs/backend-engineer",
                    source="test",
                ),
                Job(
                    title="Product Designer",
                    company="Example Company",
                    location="Remote",
                    url="https://example.com/jobs/product-designer",
                    source="test",
                ),
            ]
        )
        db.commit()
    finally:
        db.close()

    response: Response = client.get("/jobs/?keyword=Engineer")

    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) == 1
    assert jobs[0]["title"] == "Backend Engineer"
