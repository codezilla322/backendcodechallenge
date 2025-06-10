import pytest
from libs.github import fetch_github_commits
from models.github import db, GitCommit

def test_fetch_github_commits():
    result = fetch_github_commits('nodejs', 'node', 100)
    assert result is True

    from app import app
    with app.app_context():
        commit = db.session.query(GitCommit).first()
        assert len(commit.sha) == 40        
