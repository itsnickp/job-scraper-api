import logging

import requests

logger = logging.getLogger(__name__)


def scrape_jobs():
    jobs = []

    sources = [
        "https://remotive.com/api/remote-jobs",
        "https://remoteok.com/api",
    ]

    for url in sources:
        jobs_before_source = len(jobs)

        try:
            response = requests.get(
                url,
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            data = response.json()
        except Exception:
            logger.exception("Failed to fetch jobs: url=%s", url)
            continue

        if "remotive.com" in url:
            for job_data in data.get("jobs", []):
                title = job_data.get("title", "")

                if any(
                    term in title.lower()
                    for term in ["engineer", "developer", "software"]
                ):
                    jobs.append(
                        {
                            "title": title,
                            "company": job_data.get("company_name"),
                            "url": job_data.get("url"),
                            "location": job_data.get(
                                "candidate_required_location",
                                "Remote",
                            ),
                            "source": "remotive",
                        }
                    )

        if "remoteok.com" in url:
            for job_data in data[1:]:
                if isinstance(job_data, dict):
                    title = job_data.get("position", "")

                    if any(
                        term in title.lower()
                        for term in ["engineer", "developer", "software"]
                    ):
                        jobs.append(
                            {
                                "title": title,
                                "company": job_data.get("company"),
                                "url": job_data.get("url"),
                                "location": job_data.get("location", "Remote"),
                                "source": "remoteok",
                            }
                        )

        logger.info(
            "Jobs fetched: url=%s matched=%d",
            url,
            len(jobs) - jobs_before_source,
        )

    logger.info("Job scraping completed: total=%d", len(jobs))
    return jobs
