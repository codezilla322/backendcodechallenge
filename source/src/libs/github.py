import os, math
import httpx
from models import db
from models.github import GitCommit, GitAuthor

# Base URL for GitHub API
GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")
# GitHub personal access token for authentication
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# GitHub API version to use
GITHUB_API_VERSION = os.getenv("GITHUB_API_VERSION", "2022-11-28")
# Number of items per page for paginated API requests
PAGE_SIZE = os.getenv("PAGE_SIZE", 100)

def fetch_github_commits(owner, repo, commit_count):
    """
    Fetches a specified number of commits from a GitHub repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        commit_count (int): The number of commits to fetch.

    Raises:
        ValueError: If the GitHub token is not set.
    """
    if not GITHUB_TOKEN:
        raise ValueError("GitHub Token is not set")

    # Clear existing commits and authors from the database
    truncate_github_commits()

    print(f"Fetching {commit_count} commits from {owner}/{repo}...")

    # Set up headers for the GitHub API request
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION
    }

    # Loop through pages to fetch commits in batches
    for page in range(1, math.ceil(commit_count / int(PAGE_SIZE)) + 1):
        print(f"Fetching page {page}...")
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits?page={page}&per_page={PAGE_SIZE}"
        try:
            # Make the API request
            response = httpx.get(url, headers=headers)
            commits = response.json()

            # Insert each commit into the database
            for commit in commits:
                insert_github_commit(commit)

        except httpx.HTTPStatusError as e:
            # Raise an exception if the API request fails
            raise e

    print(f"Fetched {commit_count} commits from {owner}/{repo} successfully.")
    return True

def truncate_github_commits():
    """
    Deletes all existing GitHub commits and authors from the database.
    """
    from app import app
    with app.app_context():
        db.session.query(GitCommit).delete()
        db.session.query(GitAuthor).delete()
        db.session.commit()
        print("All commits and authors have been truncated.")

def insert_github_commit(commit):
    """
    Inserts a GitHub commit into the database.

    Args:
        commit (dict): The commit data from the GitHub API.

    Returns:
        int: The ID of the inserted commit.
    """
    # Extract author information from the commit
    author = commit.get("commit", {}).get("author", {})
    git_author_id = insert_github_author(author)

    # Create a new GitCommit object
    git_commit = GitCommit()
    git_commit.author_id = git_author_id
    git_commit.sha = commit.get("sha")
    git_commit.committed_at = author.get("date").replace("T", " ").replace("Z", "")

    # Save the commit to the database
    from app import app
    with app.app_context():
        db.session.add(git_commit)
        db.session.commit()
        return git_commit.id

def insert_github_author(author):
    """
    Inserts a GitHub author into the database if they do not already exist.

    Args:
        author (dict): The author data from the GitHub API.

    Returns:
        int: The ID of the inserted or existing author.
    """
    # Create a new GitAuthor object
    git_author = GitAuthor()
    git_author.name = author.get("name")
    git_author.email = author.get("email")

    # Check if the author already exists in the database
    from app import app
    with app.app_context():
        existing_author = db.session.query(GitAuthor).filter(GitAuthor.email == git_author.email).one_or_none()

        if existing_author:
            # Return the ID of the existing author
            return existing_author.id
        else:
            # Insert the new author into the database
            db.session.add(git_author)
            db.session.commit()
            return git_author.id