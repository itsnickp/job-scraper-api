import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE = "https://merojob.com"


def fetch_merojob():
    url = f"{BASE}/search-jobs/"
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []
    cards = soup.select("div.card-content, article")

    for c in cards[:15]:
        title = c.select_one("h1 a, h2 a, a")

        if not title:
            continue

        company = c.select_one("h3, .company-name")
        location = c.select_one(".location")

        jobs.append(
            {
                "title": title.text.strip(),
                "company": company.text.strip() if company else "Unknown",
                "location": location.text.strip() if location else "Nepal",
                "url": BASE + title.get("href", ""),
                "source": "merojob",
            }
        )

    return jobs
