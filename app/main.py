from fastapi import FastAPI

from app.core.database import Base, engine
from app.routes.jobs import router as jobs_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Scraper API")

app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
