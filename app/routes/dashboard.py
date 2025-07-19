# app/routes/dashboard.py
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

# Create dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@dashboard_bp.route('/index')
@login_required
def index():
    """Main dashboard page."""
    return render_template('dashboard/index.html')

@dashboard_bp.route('/stats')
@login_required
def stats():
    """Dashboard statistics page."""
    # TODO: Implement dashboard statistics
    return render_template('dashboard/stats.html')

@dashboard_bp.route('/settings')
@login_required
def settings():
    """Dashboard settings page."""
    return render_template('dashboard/settings.html')

@dashboard_bp.route('/example')
def example():
    """Example route for testing dashboard blueprint."""
    return 'Dashboard route example successful!'

# Create a separate blueprint for the root URL
root_bp = Blueprint('root', __name__)

@root_bp.route('/')
def homepage():
    """Friendly homepage for root URL."""
    try:
        return render_template('dashboard.html')
    except TemplateNotFound:
        return 'Welcome to the 1kadaysystem Homepage!'
