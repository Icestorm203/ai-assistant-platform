from collections import Counter

import requests

from app.tasks.celery_app import celery_app


@celery_app.task
def generate_github_report(username: str):

    response = requests.get(
        f"https://api.github.com/users/{username}/repos",
        timeout=30
    )

    response.raise_for_status()

    repos = response.json()

    languages = Counter()

    for repo in repos:

        language = repo.get("language")

        if language:
            languages[language] += 1

    return {
        "username": username,
        "total_repositories": len(repos),
        "languages": dict(languages)
    }