"""
Module calling API requests
"""

import math

import requests


def get_workflows(owner: str, repo: str, bearer_token: str) -> list[dict]:
    """

    :param owner: owner of the repository:
    :param repo: name of the repository:
    :param bearer_token: bearer token:
    :return workflows: list of all workflows:
    """
    repo_data = requests.get(f"https://api.github.com/repos/{owner}/{repo}/actions/runs",
                             headers={"Authorization": f"Bearer {bearer_token}",
                                      "Accept": "application/vnd.github.v3+json"},
                             timeout=20).json()
    return repo_data["workflow_runs"]


def get_minutes_from_workflow(owner: str, repo: str, workflow: dict, bearer_token: str) -> int:
    """

    :param owner: owner of the repository:
    :param repo: name of the repository:
    :param workflow: workflow run:
    :param bearer_token: bearer token:
    :return minutes: the duration of the workflow run in minutes:
    """
    workflow_run = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{workflow["id"]}/timing",
        headers={"Authorization": f"Bearer {bearer_token}",
                 "Accept": "application/vnd.github.v3+json"},
        timeout=20).json()
    try:
        return math.ceil(workflow_run["run_duration_ms"] / 1000 / 60)
    except KeyError:
        return 0
