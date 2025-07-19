# app/routes/api.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health')
def health_check():
    """API health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@api_bp.route('/user/profile')
@login_required
def user_profile():
    """Get current user profile data."""
    # TODO: Implement user profile API
    return jsonify({
        'message': 'User profile API to be implemented',
        'user_id': current_user.id if current_user.is_authenticated else None
    })

@api_bp.route('/income/summary')
@login_required
def income_summary():
    """Get income summary data."""
    # TODO: Implement income summary API
    return jsonify({
        'message': 'Income summary API to be implemented',
        'total_income': 0,
        'monthly_goal': 0,
        'progress': 0
    })

@api_bp.route('/dashboard/stats')
@login_required
def dashboard_stats():
    """Get dashboard statistics data."""
    # TODO: Implement dashboard stats API
    return jsonify({
        'message': 'Dashboard stats API to be implemented',
        'stats': {}
    })

@api_bp.route('/example')
def example():
    """Example route for testing API blueprint."""
    return jsonify({
        'message': 'API route example successful!',
        'endpoint': '/api/example'
    })
