from sqlalchemy import Index
from models import db

class GitCommit(db.Model):
    """
    Represents a Git commit in the database.
    Attributes:
        id (int): The primary key for the Git commit.
        sha (str): The unique SHA-1 hash of the commit. Must be 40 characters long.
        author_id (int): The foreign key referencing the ID of the commit's author in the 'git_authors' table.
        committed_at (datetime): The timestamp when the commit was made.
    Methods:
        __repr__():
            Returns a string representation of the GitCommit instance, showing the commit's SHA.
        to_dict():
            Converts the GitCommit instance into a dictionary where keys are column names and values are their corresponding values.
    """
    __tablename__ ='git_commits'
    id = db.Column(db.Integer, primary_key=True)
    sha = db.Column(db.String(40), nullable=False, unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('git_authors.id'), nullable=False)
    committed_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f'<GitCommit: {self.sha}>'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class GitAuthor(db.Model):
    """
    Represents a Git author in the database.
    Attributes:
        id (int): The primary key for the Git author.
        name (str): The name of the Git author.
        email (str): The unique email address of the Git author.
    Methods:
        __repr__():
            Returns a string representation of the GitAuthor instance, showing the author's name.
        to_dict():
            Converts the GitAuthor instance into a dictionary where keys are column names and values are their corresponding values.
    """
    __tablename__ ='git_authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

    email_index = Index('email_index', email)

    def __repr__(self):
        return f'<GitAuthor: {self.name}>'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}