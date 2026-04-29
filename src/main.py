"""
Main module calling the request functions and counting the total minutes
"""

from api_requests import get_workflows, get_minutes_from_workflow

import os
from dotenv import load_dotenv
import json

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
            minutes = get_minutes_from_workflow(OWNER, repo, workflow, BEARER_TOKEN)
            print(f"{workflow["name"]} took {minutes} minutes")
            repo_minutes += minutes
            total_minutes += minutes
        print(f"Repo minutes: {repo_minutes}\n")
    print(f"Total minutes: {total_minutes}")


if __name__ == "__main__":
    main()
