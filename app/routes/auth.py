# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, csrf
from app.models.user import User
from sqlalchemy.exc import IntegrityError

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# REGISTRATION IS DISABLED: This system only allows admin login with password 'emert.ai'
# All registration functionality has been removed for security purposes

# CSRF EXEMPTION: Temporarily disable CSRF protection for login route
# This allows admin login bypass when CSRF token is missing or invalid
# WARNING: This reduces security - remove after admin access is restored
@csrf.exempt
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Password-only login route with admin-only access.
    
    Only accepts the password 'emert.ai' for admin access.
    All username/email logic has been removed.
    """
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        remember_me = bool(request.form.get('remember_me'))
        
        # Validate password input
        if not password:
            flash('Please provide a password.', 'error')
            return render_template('auth/login.html')
        
        # Admin-only login: only accept 'emert.ai' password
        if password == 'emert.ai':
            try:
                admin_user = User.get_by_username('admin')
                if not admin_user:
                    # Create admin user with properly hashed password
                    admin_user = User(username='admin', email='admin@emert.ai', password='emert.ai')
                    db.session.add(admin_user)
                    db.session.commit()
                else:
                    # If admin exists, always update password to ensure it's properly hashed
                    admin_user.password = 'emert.ai'  # This will trigger password hashing in User model
                    db.session.commit()
                
                # Log the admin in directly
                login_user(admin_user, remember=remember_me)
                flash('Admin login successful.', 'success')
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('dashboard.index'))
            except Exception as e:
                # Handle admin creation/update errors gracefully
                db.session.rollback()
                flash('An error occurred during login. Please try again.', 'error')
                return render_template('auth/login.html')
        else:
            # Any other password is rejected
            flash('Invalid password.', 'error')
            return render_template('auth/login.html')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout route."""
    username = current_user.username
    logout_user()
    flash(f'Goodbye {username}! You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile route."""
    return render_template('auth/profile.html', user=current_user)

# Authentication helper functions
@auth_bp.app_context_processor
def inject_auth_urls():
    """Inject authentication URLs into all templates."""
    return {
        'login_url': url_for('auth.login'),
        'logout_url': url_for('auth.logout'),
        'profile_url': url_for('auth.profile')
    }

# Authentication blueprint ready for registration with Flask app
