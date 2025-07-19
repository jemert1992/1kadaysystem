# app/routes/income.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

# Create income blueprint
income_bp = Blueprint('income', __name__, url_prefix='/income')

@income_bp.route('/')
@income_bp.route('/index')
@login_required
def index():
    """Income tracking main page."""
    return render_template('income/index.html')

@income_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_income():
    """Add new income entry."""
    if request.method == 'POST':
        # TODO: Implement income entry logic
        flash('Income entry functionality to be implemented')
        return redirect(url_for('income.index'))
    return render_template('income/add.html')

@income_bp.route('/goals')
@login_required
def goals():
    """Income goals management page."""
    return render_template('income/goals.html')

@income_bp.route('/history')
@login_required
def history():
    """Income history and reports page."""
    return render_template('income/history.html')

@income_bp.route('/example')
def example():
    """Example route for testing income blueprint."""
    return 'Income route example successful!'
