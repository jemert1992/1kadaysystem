# app/routes/__init__.py
from flask import Blueprint

# Import all blueprint modules
from .dashboard import dashboard_bp
from .income import income_bp
from .api import api_bp

# List of all blueprints to register
blueprints = [
    dashboard_bp,
    income_bp,
    api_bp
]

def register_blueprints(app):
    """Register all blueprints with the Flask app."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

# Create a routes blueprint for package-level routes
routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/routes-test')
def example():
    """Example route for testing routes package."""
    return 'Routes package initialized successfully!'
