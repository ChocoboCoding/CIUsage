"""
Main module calling the request functions and counting the total minutes
"""
from datetime import datetime, timedelta
import os
import json

from dotenv import load_dotenv

from src.api_requests import get_workflows, get_minutes_from_workflow

load_dotenv()

REPOS = json.loads(os.getenv('REPOS', '[]'))
OWNER = os.getenv('OWNER')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')


def main():
    """
    Main function
    """
    total_minutes = 0
    for repo in REPOS:
        repo_minutes = 0
        print(f"Getting workflows for {repo}")
        workflows = get_workflows(OWNER, repo, BEARER_TOKEN)
        for workflow in workflows:
            created_at = workflow["created_at"]
            dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            if dt < datetime.now() - timedelta(days=30):
                continue

            minutes = get_minutes_from_workflow(OWNER, repo, workflow, BEARER_TOKEN)
            print(f"{workflow["name"]} took {minutes} minutes")
            repo_minutes += minutes
            total_minutes += minutes
        print(f"Repo minutes: {repo_minutes}\n")
    print(f"Total minutes: {total_minutes}")


if __name__ == "__main__":
    main()
