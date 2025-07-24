# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, csrf
from app.models.user import User
from app.forms.auth import RegistrationForm
from sqlalchemy.exc import IntegrityError

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

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
            flash('Invalid password. Access denied.', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    # Create RegistrationForm instance
    form = RegistrationForm()

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validate form data
        errors = []

        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long.')

        if not email or '@' not in email:
            errors.append('Please provide a valid email address.')

        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters long.')

        if password != confirm_password:
            errors.append('Passwords do not match.')

        # Check if username or email already exists
        if User.get_by_username(username):
            errors.append('Username already exists. Please choose a different one.')

        if User.get_by_email(email):
            errors.append('Email address already registered. Please use a different one.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html', form=form)

        try:
            # Create new user
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))

        except IntegrityError as e:
            # Handle database integrity errors (duplicate entries) gracefully
            db.session.rollback()
            if 'username' in str(e).lower():
                flash('Username already exists. Please choose a different one.', 'error')
            elif 'email' in str(e).lower():
                flash('Email address already registered. Please use a different one.', 'error')
            else:
                flash('Registration failed due to duplicate information. Please try again.', 'error')
            return render_template('auth/register.html', form=form)
        except Exception as e:
            # Handle other database errors gracefully
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('auth/register.html', form=form)

    return render_template('auth/register.html', form=form)

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

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password route."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()

        if not email:
            flash('Please provide your email address.', 'error')
            return render_template('auth/forgot_password.html')

        user = User.get_by_email(email)
        if user:
            # In a production app, you would:
            # 1. Generate a secure token
            # 2. Store it in the database with expiration
            # 3. Send an email with a reset link
            # For now, we'll just show a success message
            flash('If an account with that email exists, you will receive password reset instructions.', 'info')
        else:
            # Don't reveal whether the email exists or not for security
            flash('If an account with that email exists, you will receive password reset instructions.', 'info')

        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')

# Authentication helper functions
@auth_bp.app_context_processor
def inject_auth_urls():
    """Inject authentication URLs into all templates."""
    return {
        'login_url': url_for('auth.login'),
        'register_url': url_for('auth.register'),
        'logout_url': url_for('auth.logout'),
        'profile_url': url_for('auth.profile')
    }

# Authentication blueprint ready for registration with Flask app
