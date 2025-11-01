"""Backend routes for admin panel."""
from flask import Blueprint, request
from flask_login import login_required
from app.controllers.backend_controller import BackendController
from app.controllers.backend_management_controller import BackendManagementController
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


@backend_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Edit user."""
    if request.method == 'POST':
        return BackendController.update_user(user_id)
    return BackendController.edit_user(user_id)


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


# Cases management (requires admin)
@backend_bp.route('/cases')
@login_required
@admin_required
def cases():
    """Cases management."""
    return BackendManagementController.cases()


@backend_bp.route('/cases/create', methods=['POST'])
@login_required
@admin_required
def create_case():
    """Create case."""
    return BackendManagementController.create_case()


@backend_bp.route('/cases/<int:case_id>/photos/upload', methods=['POST'])
@login_required
@admin_required
def upload_case_photo(case_id):
    """Upload case photo."""
    return BackendManagementController.upload_case_photo(case_id)


@backend_bp.route('/cases/<int:case_id>/photos/<int:photo_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_case_photo(case_id, photo_id):
    """Delete case photo."""
    return BackendManagementController.delete_case_photo(case_id, photo_id)


@backend_bp.route('/cases/<int:case_id>/photos/order', methods=['POST'])
@login_required
@admin_required
def update_case_photo_order(case_id):
    """Update case photo order."""
    return BackendManagementController.update_case_photo_order(case_id)


@backend_bp.route('/cases/<int:case_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_case(case_id):
    """Edit case."""
    if request.method == 'POST':
        return BackendManagementController.update_case(case_id)
    return BackendManagementController.edit_case(case_id)


@backend_bp.route('/cases/<int:case_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_case(case_id):
    """Delete case."""
    return BackendManagementController.delete_case(case_id)


@backend_bp.route('/cases/<int:case_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_case_status(case_id):
    """Toggle case status."""
    return BackendManagementController.toggle_case_status(case_id)


# News management (requires admin)
@backend_bp.route('/news')
@login_required
@admin_required
def news():
    """News management."""
    return BackendManagementController.news()


@backend_bp.route('/news/create', methods=['POST'])
@login_required
@admin_required
def create_news():
    """Create news."""
    return BackendManagementController.create_news()


@backend_bp.route('/news/<int:news_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_news(news_id):
    """Edit news."""
    if request.method == 'POST':
        return BackendManagementController.update_news(news_id)
    return BackendManagementController.edit_news(news_id)


@backend_bp.route('/news/<int:news_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_news(news_id):
    """Delete news."""
    return BackendManagementController.delete_news(news_id)


@backend_bp.route('/news/<int:news_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_news_status(news_id):
    """Toggle news status."""
    return BackendManagementController.toggle_news_status(news_id)


# Contacts management (requires admin)
@backend_bp.route('/contacts')
@login_required
@admin_required
def contacts():
    """Contacts management."""
    return BackendManagementController.contacts()


@backend_bp.route('/contacts/<int:contact_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_contact_status(contact_id):
    """Update contact status."""
    return BackendManagementController.update_contact_status(contact_id)


@backend_bp.route('/contacts/<int:contact_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_contact(contact_id):
    """Delete contact."""
    return BackendManagementController.delete_contact(contact_id)


# Categories management (requires admin)
@backend_bp.route('/categories')
@login_required
@admin_required
def categories():
    """Categories management."""
    return BackendManagementController.categories()


@backend_bp.route('/categories/create', methods=['POST'])
@login_required
@admin_required
def create_category():
    """Create category."""
    return BackendManagementController.create_category()


@backend_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    """Edit category."""
    if request.method == 'POST':
        return BackendManagementController.update_category(category_id)
    return BackendManagementController.edit_category(category_id)


@backend_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    """Delete category."""
    return BackendManagementController.delete_category(category_id)


# Media management (requires admin)
@backend_bp.route('/media')
@login_required
@admin_required
def media():
    """Media management."""
    return BackendManagementController.media()


@backend_bp.route('/media/update-image', methods=['POST'])
@login_required
@admin_required
def update_media_image():
    """Update media image."""
    return BackendManagementController.update_media_image()


@backend_bp.route('/media/delete-image', methods=['POST'])
@login_required
@admin_required
def delete_media_image():
    """Delete media image."""
    return BackendManagementController.delete_media_image()


@backend_bp.route('/media/add-image', methods=['POST'])
@login_required
@admin_required
def add_media_image():
    """Add media image."""
    return BackendManagementController.add_media_image()

