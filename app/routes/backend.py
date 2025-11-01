"""Backend routes for admin panel."""
from flask import Blueprint
from flask_login import login_required
from app.controllers.backend_controller import BackendController
from app.utils.auth import admin_required

# Create blueprint
backend_bp = Blueprint('backend', __name__)


# Authentication routes
@backend_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login."""
    return BackendController.login()


@backend_bp.route('/logout')
def logout():
    """Admin logout."""
    return BackendController.logout()


# Dashboard (requires admin)
@backend_bp.route('/')
@backend_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard."""
    return BackendController.dashboard()


# User management (requires admin)
@backend_bp.route('/users')
@login_required
@admin_required
def users():
    """User management."""
    return BackendController.users()


@backend_bp.route('/users/create', methods=['POST'])
@login_required
@admin_required
def create_user():
    """Create user."""
    return BackendController.create_user()


@backend_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete user."""
    return BackendController.delete_user(user_id)


@backend_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Toggle user status."""
    return BackendController.toggle_user_status(user_id)

