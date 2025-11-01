"""Frontend routes - equivalent to Laravel's web.php routes."""
from flask import Blueprint, send_from_directory, current_app
from app.controllers.frontend_controller import FrontendController
import os

# Create blueprint
frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/uploads/<path:filename>')
def uploads(filename):
    """Serve uploaded files."""
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    return send_from_directory(upload_folder, filename)


# Frontend Routes
@frontend_bp.route('/')
def home():
    """Home page."""
    return FrontendController.home()


@frontend_bp.route('/cases')
def cases():
    """Cases listing page."""
    return FrontendController.cases()


@frontend_bp.route('/cases/category/<category_slug>')
def cases_by_category(category_slug):
    """Cases listing page by category."""
    return FrontendController.cases_by_category(category_slug)


@frontend_bp.route('/cases/<int:id>')
def case_detail(id):
    """Case detail page."""
    return FrontendController.case_detail(id)


@frontend_bp.route('/news')
def news():
    """News listing page."""
    return FrontendController.news()


@frontend_bp.route('/news/<int:id>')
def news_detail(id):
    """News detail page."""
    return FrontendController.news_detail(id)


@frontend_bp.route('/contact', methods=['GET'])
def contact():
    """Contact page (GET)."""
    return FrontendController.contact()


@frontend_bp.route('/contact', methods=['POST'])
def contact_post():
    """Contact page (POST)."""
    return FrontendController.store_contact()


# API Routes for AJAX
@frontend_bp.route('/api/cases/<int:id>')
def api_get_case(id):
    """API endpoint for getting case data."""
    return FrontendController.get_case_api(id)


@frontend_bp.route('/api/news/<int:id>')
def api_get_news(id):
    """API endpoint for getting news data."""
    return FrontendController.get_news_api(id)

