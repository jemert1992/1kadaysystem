# app/routes/dashboard.py
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

# Create dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@dashboard_bp.route('/home')
@login_required
def home():
    """Dashboard home page with overview."""
    # TODO: Implement dashboard home logic
    return render_template('dashboard/home.html')

@dashboard_bp.route('/analytics')
@dashboard_bp.route('/analytics/summary')
@login_required
def analytics_summary():
    """Analytics summary page with key metrics."""
    # TODO: Implement analytics summary logic
    analytics_data = {
        'total_income': 0,
        'monthly_goal': 1000,
        'daily_progress': 0,
        'completion_percentage': 0
    }
    return render_template('dashboard/analytics_summary.html', analytics=analytics_data)

@dashboard_bp.route('/quick-links')
@login_required
def quick_links():
    """Quick links page for common actions."""
    # TODO: Implement quick links logic
    links = [
        {'name': 'Add Income', 'url': '/income/add', 'icon': 'plus'},
        {'name': 'View Reports', 'url': '/reports', 'icon': 'chart'},
        {'name': 'Settings', 'url': '/settings', 'icon': 'settings'},
        {'name': 'Profile', 'url': '/auth/profile', 'icon': 'user'}
    ]
    return render_template('dashboard/quick_links.html', links=links)

# Dashboard blueprint ready for registration with Flask app
