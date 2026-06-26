def dedupe_jobs(jobs):
    seen = set()
    out = []

    for j in jobs:
        key = (j["title"], j["company"], j["url"])

        if key not in seen:
            seen.add(key)
            out.append(j)

    return out
