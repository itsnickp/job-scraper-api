import hashlib
import logging

from app.models.job import Job

logger = logging.getLogger(__name__)


def make_hash(job):
    key = f"{job['title']}-{job['company']}-{job['location']}"
    return hashlib.md5(key.encode()).hexdigest()


def create_jobs(db, jobs):
    inserted = 0

    for job_data in jobs:
        make_hash(job_data)
        exists = db.query(Job).filter(Job.url == job_data["url"]).first()

        if not exists:
            db.add(Job(**job_data))
            inserted += 1

    db.commit()
    logger.info(
        "Jobs stored: received=%d inserted=%d",
        len(jobs),
        inserted,
    )


def fetch_jobs(db, limit=50):
    jobs = db.query(Job).limit(limit).all()
    logger.info("Jobs fetched from database: count=%d limit=%d", len(jobs), limit)
    return jobs
