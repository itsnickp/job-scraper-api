import logging

from fastapi import APIRouter, Query

from app.core.database import SessionLocal
from app.models.job import Job

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/sync")
def sync_jobs():
    from app.scraper.jobs import scrape_jobs

    db = SessionLocal()

    try:
        jobs = scrape_jobs()
        inserted = 0

        for job_data in jobs:
            if not job_data.get("title"):
                continue

            exists = db.query(Job).filter(Job.url == job_data["url"]).first()

            if not exists:
                db.add(Job(**job_data))
                inserted += 1

        db.commit()
        logger.info(
            "Job sync completed: scraped=%d inserted=%d",
            len(jobs),
            inserted,
        )

        return {
            "scraped": len(jobs),
            "inserted": inserted,
        }
    except Exception:
        db.rollback()
        logger.exception("Job sync failed")
        raise
    finally:
        db.close()


@router.get("/")
def get_jobs(
    source: str | None = None,
    keyword: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    db = SessionLocal()

    try:
        query = db.query(Job)

        if source:
            query = query.filter(Job.source == source)

        if keyword:
            query = query.filter(Job.title.contains(keyword))

        return (
            query.order_by(Job.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    finally:
        db.close()
