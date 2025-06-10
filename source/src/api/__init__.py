from flask import Blueprint
from api.github import github_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(github_bp, url_prefix='/github')