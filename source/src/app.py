import os
from flask import Flask
from flask_migrate import Migrate
from models import db

# Initialize the Flask application
app = Flask(__name__)

# Retrieve MySQL connection details from environment variables
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_host = os.getenv('MYSQL_HOST')
mysql_db = os.getenv('MYSQL_DB')

# Ensure all required environment variables are set
if not all([mysql_user, mysql_password, mysql_host, mysql_db]):
    raise ValueError("Environment variables for MySQL connection are not set properly.")

# Configure the SQLAlchemy database URI for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
)
# Disable SQLALCHEMY_TRACK_MODIFICATIONS to avoid overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# Set up Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Import and register the API blueprint
from api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# Run the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run()