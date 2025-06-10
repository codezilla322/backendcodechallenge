from flask import Blueprint, render_template, request
from sqlalchemy import or_
from libs.github import fetch_github_commits
from models.github import GitCommit, GitAuthor
from models import db

# Define a Blueprint for GitHub-related routes
github_bp = Blueprint('github', __name__)

@github_bp.route('/fetch_commits', methods=['GET'])
def fetch_commits():
    """
    Fetches a specified number of commits from a GitHub repository.

    Query Parameters:
        owner (str): The owner of the repository (default: "nodejs").
        repo (str): The name of the repository (default: "node").
        count (int): The number of commits to fetch (default: 1000).

    Returns:
        Renders a success template if commits are fetched successfully.
    """
    # Get query parameters with default values
    owner = request.args.get("owner", "nodejs")
    repo = request.args.get("repo", "node")
    count = int(request.args.get("count", 1000))

    # Fetch commits using the helper function and render success page
    if fetch_github_commits(owner, repo, count):
        return render_template('success.html', msg=f'Fetched {count} commits from {owner}/{repo} successfully.')

@github_bp.route('/commits', methods=['GET'])
def get_commits():
    """
    Retrieves commits from the database filtered by author.

    Query Parameters:
        author (str): The name or email of the author to filter commits by.

    Returns:
        Renders a template displaying the filtered commits.
    """
    # Get the author query parameter
    author = request.args.get("author")

    # Query the database for commits and their associated authors
    commits = db.session.query(GitCommit, GitAuthor) \
                .filter(GitCommit.author_id == GitAuthor.id) \
                .filter(or_(GitAuthor.name == author, GitAuthor.email == author)) \
                .all()

    # Render the commits in a template, combining commit and author data
    return render_template('commits.html', commits=[commit[0].to_dict() | commit[1].to_dict() for commit in commits])