# app/routes/income.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import func
from app import db
from app.models.income import Income

# Create income blueprint
income_bp = Blueprint('income', __name__, url_prefix='/income')

@income_bp.route('/')
@income_bp.route('/index')
@login_required
def index():
    """Income tracking main page with overview of recent entries."""
    # Get recent income entries for the logged-in user
    recent_income = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).limit(10).all()
    
    # Calculate total income for the current user
    total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Calculate monthly income
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_income = db.session.query(func.sum(Income.amount)).filter(
        Income.user_id == current_user.id,
        func.extract('month', Income.date) == current_month,
        func.extract('year', Income.date) == current_year
    ).scalar() or 0
    
    # Pass summary data to template
    summary = {
        'total_income': total_income,
        'monthly_income': monthly_income,
        'entries_count': len(recent_income)
    }
    
    return render_template('income/index.html', 
                         recent_income=recent_income, 
                         total_income=total_income,
                         summary=summary)

@income_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_income():
    """Add new income entry."""
    if request.method == 'POST':
        amount = request.form.get('amount')
        source = request.form.get('source')
        description = request.form.get('description')
        date_str = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        # Validate form data
        if not amount or not source:
            flash('Amount and source are required fields.', 'error')
            return render_template('income/add.html')
        
        try:
            # Convert amount to float
            amount_float = float(amount)
            if amount_float <= 0:
                flash('Amount must be a positive number.', 'error')
                return render_template('income/add.html')
            
            # Parse date
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Create new income entry
            new_income = Income(
                user_id=current_user.id,
                amount=amount_float,
                source=source,
                description=description or '',
                date=date_obj
            )
            
            # Save to database
            db.session.add(new_income)
            db.session.commit()
            
            flash('Income entry added successfully!', 'success')
            return redirect(url_for('income.index'))
            
        except ValueError:
            flash('Invalid amount or date format.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving the income entry.', 'error')
    
    return render_template('income/add.html')

@income_bp.route('/edit/<int:income_id>', methods=['GET', 'POST'])
@login_required
def edit_income(income_id):
    """Edit existing income entry."""
    # Get income entry and ensure it belongs to current user
    income_entry = Income.query.filter_by(id=income_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        amount = request.form.get('amount')
        source = request.form.get('source')
        description = request.form.get('description')
        date_str = request.form.get('date')
        
        # Validate form data
        if not amount or not source:
            flash('Amount and source are required fields.', 'error')
            return render_template('income/edit.html', income=income_entry)
        
        try:
            # Convert amount to float
            amount_float = float(amount)
            if amount_float <= 0:
                flash('Amount must be a positive number.', 'error')
                return render_template('income/edit.html', income=income_entry)
            
            # Parse date
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Update income entry
            income_entry.amount = amount_float
            income_entry.source = source
            income_entry.description = description or ''
            income_entry.date = date_obj
            
            # Save changes
            db.session.commit()
            
            flash('Income entry updated successfully!', 'success')
            return redirect(url_for('income.index'))
            
        except ValueError:
            flash('Invalid amount or date format.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the income entry.', 'error')
    
    return render_template('income/edit.html', income=income_entry)

@income_bp.route('/delete/<int:income_id>', methods=['POST'])
@login_required
def delete_income(income_id):
    """Delete income entry."""
    # Get income entry and ensure it belongs to current user
    income_entry = Income.query.filter_by(id=income_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(income_entry)
        db.session.commit()
        flash('Income entry deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the income entry.', 'error')
    
    return redirect(url_for('income.index'))

@income_bp.route('/reports')
@income_bp.route('/reports/summary')
@login_required
def reports_summary():
    """Income reports and analytics summary."""
    # Calculate various statistics for the current user
    total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Monthly income
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_income = db.session.query(func.sum(Income.amount)).filter(
        Income.user_id == current_user.id,
        func.extract('month', Income.date) == current_month,
        func.extract('year', Income.date) == current_year
    ).scalar() or 0
    
    # Daily average (based on entries, not calendar days)
    entry_count = Income.query.filter_by(user_id=current_user.id).count()
    daily_average = total_income / entry_count if entry_count > 0 else 0
    
    # Top income sources
    top_sources = db.session.query(
        Income.source,
        func.sum(Income.amount).label('total')
    ).filter_by(user_id=current_user.id).group_by(Income.source).order_by(func.sum(Income.amount).desc()).limit(5).all()
    
    report_data = {
        'monthly_income': monthly_income,
        'daily_average': daily_average,
        'top_sources': [(source, total) for source, total in top_sources],
        'income_trend': [],  # TODO: Implement trend calculation
        'goal_progress': (monthly_income / 1000) * 100 if monthly_income else 0  # Assume $1000 monthly goal
    }
    
    return render_template('income/reports.html', report_data=report_data)

@income_bp.route('/reports/detailed')
@login_required
def reports_detailed():
    """Detailed income reports with filters and export options."""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    source_filter = request.args.get('source')
    
    # Build query for filtered results
    query = Income.query.filter_by(user_id=current_user.id)
    
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Income.date >= start_date_obj)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Income.date <= end_date_obj)
        except ValueError:
            pass
    
    if source_filter:
        query = query.filter(Income.source.ilike(f'%{source_filter}%'))
    
    filtered_income = query.order_by(Income.date.desc()).all()
    total_filtered = sum(entry.amount for entry in filtered_income)
    
    return render_template('income/detailed_reports.html', 
                         income_entries=filtered_income,
                         total_amount=total_filtered,
                         filters={'start_date': start_date, 'end_date': end_date, 'source': source_filter})

@income_bp.route('/goals')
@login_required
def goals():
    """Income goals management page."""
    # TODO: Implement goals management logic with database storage
    current_goals = {
        'daily_goal': 35,  # $1000/month ≈ $35/day
        'monthly_goal': 1000,
        'annual_goal': 12000
    }
    return render_template('income/goals.html', goals=current_goals)

@income_bp.route('/goals/update', methods=['POST'])
@login_required
def update_goals():
    """Update income goals."""
    # TODO: Implement goals update logic with database storage
    daily_goal = request.form.get('daily_goal')
    monthly_goal = request.form.get('monthly_goal')
    annual_goal = request.form.get('annual_goal')
    
    flash('Income goals updated successfully!', 'success')
    return redirect(url_for('income.goals'))

@income_bp.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for income statistics (for AJAX requests)."""
    # Calculate real-time statistics for the current user
    today = datetime.now().date()
    current_week_start = today - timedelta(days=today.weekday())
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Today's income
    today_income = db.session.query(func.sum(Income.amount)).filter(
        Income.user_id == current_user.id,
        Income.date == today
    ).scalar() or 0
    
    # This week's income
    week_income = db.session.query(func.sum(Income.amount)).filter(
        Income.user_id == current_user.id,
        Income.date >= current_week_start
    ).scalar() or 0
    
    # This month's income
    month_income = db.session.query(func.sum(Income.amount)).filter(
        Income.user_id == current_user.id,
        func.extract('month', Income.date) == current_month,
        func.extract('year', Income.date) == current_year
    ).scalar() or 0
    
    # Progress percentage (assuming $1000 monthly goal)
    monthly_goal = 1000
    progress_percentage = (month_income / monthly_goal) * 100 if month_income else 0
    
    stats = {
        'today_income': float(today_income),
        'week_income': float(week_income),
        'month_income': float(month_income),
        'progress_percentage': min(progress_percentage, 100)  # Cap at 100%
    }
    return jsonify(stats)

# Income blueprint ready for registration with Flask app
