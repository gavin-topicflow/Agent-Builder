#!/usr/bin/env python3
"""
Script to create 3 test pull requests in a GitHub repository.

Requirements:
- Python 3.6+
- requests library: pip install requests

Usage:
1. Set environment variables:
   export GITHUB_TOKEN="your_github_personal_access_token"
   export GITHUB_REPO="owner/repo-name"

2. Run the script:
   python create_test_prs.py
"""

import os
import sys
import requests
from datetime import datetime

# Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = "gavin-topicflow/Agent-Builder"  # Format: "owner/repo"
BASE_BRANCH = os.environ.get("BASE_BRANCH", "main")  # Default to 'main'

# GitHub API base URL
API_BASE = "https://api.github.com"


def check_config():
    """Check if required configuration is present."""
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Create a token at: https://github.com/settings/tokens")
        print("Required scopes: repo")
        sys.exit(1)

    if not GITHUB_REPO:
        print("Error: GITHUB_REPO environment variable not set")
        print("Format: owner/repo-name")
        sys.exit(1)


def get_headers():
    """Get headers for GitHub API requests."""
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_base_sha():
    """Get the SHA of the base branch."""
    url = f"{API_BASE}/repos/{GITHUB_REPO}/git/refs/heads/{BASE_BRANCH}"
    response = requests.get(url, headers=get_headers())

    if response.status_code != 200:
        print(f"Error getting base branch: {response.json()}")
        sys.exit(1)

    return response.json()["object"]["sha"]


def create_branch(branch_name, base_sha):
    """Create a new branch from base SHA."""
    url = f"{API_BASE}/repos/{GITHUB_REPO}/git/refs"
    data = {"ref": f"refs/heads/{branch_name}", "sha": base_sha}

    response = requests.post(url, headers=get_headers(), json=data)

    if response.status_code == 201:
        print(f"✓ Created branch: {branch_name}")
        return True
    elif response.status_code == 422:
        print(f"! Branch {branch_name} already exists, deleting and recreating...")
        delete_branch(branch_name)
        response = requests.post(url, headers=get_headers(), json=data)
        if response.status_code == 201:
            print(f"✓ Created branch: {branch_name}")
            return True

    print(f"Error creating branch: {response.json()}")
    return False


def delete_branch(branch_name):
    """Delete a branch."""
    url = f"{API_BASE}/repos/{GITHUB_REPO}/git/refs/heads/{branch_name}"
    requests.delete(url, headers=get_headers())


def create_file_commit(branch_name, file_path, content, commit_message):
    """Create a commit that adds or updates a file."""
    # Get current file SHA if it exists
    url = f"{API_BASE}/repos/{GITHUB_REPO}/contents/{file_path}"
    params = {"ref": branch_name}
    response = requests.get(url, headers=get_headers(), params=params)

    sha = None
    if response.status_code == 200:
        sha = response.json()["sha"]

    # Create or update file
    import base64

    data = {
        "message": commit_message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch_name,
    }

    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=get_headers(), json=data)

    if response.status_code in [200, 201]:
        print(f"  ✓ Committed: {commit_message}")
        return True

    print(f"  Error creating commit: {response.json()}")
    return False


def create_pull_request(branch_name, title, body):
    """Create a pull request."""
    url = f"{API_BASE}/repos/{GITHUB_REPO}/pulls"
    data = {"title": title, "head": branch_name, "base": BASE_BRANCH, "body": body}

    # Assign the PR to gavin-topicflow
    assignees = ["gavin-topicflow"]

    response = requests.post(url, headers=get_headers(), json=data)

    if response.status_code == 201:
        pr_url = response.json()["html_url"]
        pr_number = response.json()["number"]
        print(f"✓ Created PR #{pr_number}: {pr_url}")

        # Assign the PR
        assign_url = f"{API_BASE}/repos/{GITHUB_REPO}/issues/{pr_number}/assignees"
        assign_data = {"assignees": assignees}
        assign_response = requests.post(
            assign_url, headers=get_headers(), json=assign_data
        )

        if assign_response.status_code == 201:
            print(f"  ✓ Assigned to: {', '.join(assignees)}")
        else:
            print(
                f"  ! Warning: Could not assign PR: {assign_response.json().get('message', 'Unknown error')}"
            )

        return pr_number

    print(f"Error creating PR: {response.json()}")
    return None


def main():
    """Main function to create 3 test pull requests."""
    print("=" * 60)
    print("GitHub Test PR Generator")
    print("=" * 60)
    print()

    check_config()

    print(f"Repository: {GITHUB_REPO}")
    print(f"Base branch: {BASE_BRANCH}")
    print()

    # Get base branch SHA
    print("Getting base branch SHA...")
    base_sha = get_base_sha()
    print(f"Base SHA: {base_sha[:7]}")
    print()

    # Timestamp for unique branch names
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # PR configurations
    prs = [
        {
            "branch": f"test/feature-a-{timestamp}",
            "title": "Add feature A - Test PR 1",
            "body": "This is a test pull request to add Feature A.\n\n- Adds new functionality\n- Updates documentation",
            "files": [
                (
                    "feature-a.txt",
                    "Feature A implementation\n\nThis is a test feature.",
                    "Add feature A implementation",
                )
            ],
        },
        {
            "branch": f"test/bugfix-b-{timestamp}",
            "title": "Fix bug B - Test PR 2",
            "body": "This is a test pull request to fix Bug B.\n\n- Fixes critical issue\n- Adds test coverage",
            "files": [
                ("bugfix-b.txt", "Bug B fix\n\nThis fixes the issue.", "Fix bug B"),
                ("test-b.txt", "Test for bug B fix", "Add test for bug B"),
            ],
        },
        {
            "branch": f"test/refactor-c-{timestamp}",
            "title": "Refactor component C - Test PR 3",
            "body": "This is a test pull request to refactor Component C.\n\n- Improves code quality\n- Better performance",
            "files": [
                (
                    "component-c.txt",
                    "Refactored Component C\n\nMuch cleaner now.",
                    "Refactor component C",
                )
            ],
        },
    ]

    created_prs = []

    for i, pr_config in enumerate(prs, 1):
        print(f"Creating PR {i}/3...")
        print("-" * 60)

        # Create branch
        if not create_branch(pr_config["branch"], base_sha):
            continue

        # Create commits
        for file_path, content, commit_msg in pr_config["files"]:
            create_file_commit(pr_config["branch"], file_path, content, commit_msg)

        # Create PR
        pr_number = create_pull_request(
            pr_config["branch"], pr_config["title"], pr_config["body"]
        )

        if pr_number:
            created_prs.append(pr_number)

        print()

    print("=" * 60)
    print(f"Summary: Created {len(created_prs)} pull request(s)")
    print("=" * 60)


if __name__ == "__main__":
    main()
