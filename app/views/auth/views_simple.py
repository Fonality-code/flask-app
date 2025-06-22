"""
Authentication views
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.views.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm
from datetime import datetime

try:
    from app.utils.upload_service import upload_service
except ImportError:
    upload_service = None


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user and user.check_password(form.password.data):
            if user.account_status != 'active':
                flash('Your account is not active. Please contact support.', 'error')
                return render_template('auth/login.html', form=form)

            # Update last login
            user.last_login = datetime.now()
            db.session.commit()

            login_user(user, remember=form.remember_me.data)

            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data.lower()).first()
        if existing_user:
            flash('Email address already registered.', 'error')
            return render_template('auth/register.html', form=form)

        # Create new user
        user = User(
            email=form.email.data.lower(),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            date_of_birth=form.date_of_birth.data,
            country=form.country.data,
            city=form.city.data,
            address=form.address.data,
            preferred_language=form.preferred_language.data,
            account_type=form.account_type.data,
            business_name=form.business_name.data,
            business_type=form.business_type.data,
            business_description=form.business_description.data,
            website_url=form.website_url.data
        )
        user.set_password(form.password.data)

        try:
            db.session.add(user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {e}")
            flash('An error occurred during registration. Please try again.', 'error')

    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html', user=current_user)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password page"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html', form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password changed successfully.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/change_password.html', form=form)


@auth.route('/admin')
@login_required
def admin():
    """Admin dashboard - requires admin role"""
    if not current_user.has_role('admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))

    users = User.query.all()
    return render_template('auth/admin.html', users=users)


@auth.route('/admin/users/<int:user_id>')
@login_required
def admin_user_detail(user_id):
    """Admin user detail page"""
    if not current_user.has_role('admin') and not current_user.can_access_user(user_id, 'read'):
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)
    return render_template('auth/user_detail.html', user=user)
