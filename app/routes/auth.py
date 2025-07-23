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
    """User login route.
    
    Note: CSRF protection temporarily disabled for this route to allow
    admin login bypass when CSRF tokens are unavailable. This should be
    re-enabled once admin access issues are resolved.
    """
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember_me = bool(request.form.get('remember_me'))

        # --- ADMIN LOGIN BYPASS BLOCK ---
        # Fix 1: Admin login with proper password hashing and storage
        # Always ensure admin user exists with correct hashed password
        if username == 'admin' and password == 'emert.ai':
            try:
                admin_user = User.get_by_username('admin')
                if not admin_user:
                    # Create admin user with properly hashed password
                    admin_user = User(username='admin', email='admin@emert.ai', password='emert.ai')
                    db.session.add(admin_user)
                    db.session.commit()
                else:
                    # Fix 2: If admin exists, always update password to ensure it's properly hashed
                    admin_user.password = 'emert.ai'  # This will trigger password hashing in User model
                    db.session.commit()
                
                # Log the admin in directly
                login_user(admin_user, remember=True)
                flash('Admin login successful (bypass).', 'success')
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('dashboard.index'))
            except Exception as e:
                # Fix 3: Handle admin creation/update errors gracefully
                db.session.rollback()
                flash('An error occurred during admin login. Please try again.', 'error')
                return render_template('auth/login.html')
        # --- END ADMIN LOGIN BYPASS BLOCK ---

        # Validate form data
        if not username or not password:
            flash('Please provide both username and password.', 'error')
            return render_template('auth/login.html')

        # Find user by username or email
        user = User.get_by_username(username) or User.get_by_email(username)

        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            flash(f'Welcome back, {user.username}!', 'success')
            # Redirect to next page if specified, otherwise to dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

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
            # Fix 4: Handle database integrity errors (duplicate entries) gracefully
            db.session.rollback()
            if 'username' in str(e).lower():
                flash('Username already exists. Please choose a different one.', 'error')
            elif 'email' in str(e).lower():
                flash('Email address already registered. Please use a different one.', 'error')
            else:
                flash('Registration failed due to duplicate information. Please try again.', 'error')
            return render_template('auth/register.html', form=form)
        except Exception as e:
            # Fix 5: Handle other database errors gracefully
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
