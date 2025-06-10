# Project Setup Instructions

This project fetches recent 1000 commits from the Node.js GitHub repository and displays them grouped by author using Flask.

## Prerequisites

- Python3
- pip

## Setup (Local)

1. **Clone the repo and navigate to the base directory**
```bash
git clone https://github.com/codezilla322/backendcodechallenge
cd source
```


2. **Install dependencies**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Create a `.env` file** (you can copy from `.env.example`):
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=

GITHUB_API_URL=https://api.github.com
GITHUB_TOKEN=
GITHUB_API_VERSION=2022-11-28

PAGE_SIZE=100
```

4. **Set Flask environment variables**
```bash
export FLASK_APP=src/app.py
export FLASK_ENV=development
export FLASK_RUN_PORT=5000
```

5. **Run database migration**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```


6. **Run the Flask app**
```bash
flask run
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/github/fetch_commits` | Fetches 1000 recent commits from the `nodejs/node` repository |
| `GET`  | `/api/github/commits?author=<author_name_or_email>` | Displays commits filtered by the author's name or email |


## Run Tests

```bash
cd src
python -m pytest
```

## Notes

- The app connects to a MySQL database using environment variables.
- Make sure your database is up and running before starting the app.