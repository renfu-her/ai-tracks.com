"""Flask application factory."""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    """Load user from session."""
    from app.models.user import User
    return User.query.get(int(user_id))


def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__,
                template_folder='templates',
                static_folder='../static')
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Enable template auto-reload in development
    if app.config.get('DEBUG'):
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.jinja_env.auto_reload = True
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'backend.login'
    login_manager.login_message = '請先登入以訪問此頁面'
    login_manager.login_message_category = 'info'
    
    # Configure database engine options for MySQL
    if 'mysql' in app.config['SQLALCHEMY_DATABASE_URI']:
        app.config.setdefault('SQLALCHEMY_ENGINE_OPTIONS', {
            'pool_size': 10,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
            'connect_args': {
                'charset': 'utf8mb4'
            }
        })
    
    # Register blueprints
    from app.routes.frontend import frontend_bp
    app.register_blueprint(frontend_bp)
    
    from app.routes.backend import backend_bp
    app.register_blueprint(backend_bp, url_prefix='/backend')
    
    # Register template filters and context processors
    from app.utils.helpers import storage_url, format_date, markdown_to_html
    from sqlalchemy import asc
    app.jinja_env.filters['storage_url'] = storage_url
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['markdown'] = markdown_to_html
    
    # Make csrf_token available in templates
    from flask_wtf.csrf import generate_csrf
    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf)
    
    # Make categories available in templates
    @app.context_processor
    def inject_categories():
        from app.models.product_category import ProductCategory
        categories = ProductCategory.query\
            .filter_by(status=True)\
            .order_by(asc(ProductCategory.sort_order))\
            .limit(4)\
            .all()
        return dict(categories=categories)
    
    # Create upload directories if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'cases'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'news'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'sliders'), exist_ok=True)
    
    return app

