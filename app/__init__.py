"""Flask application factory."""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


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
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
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
    
    # Register template filters and context processors
    from app.utils.helpers import storage_url, format_date
    app.jinja_env.filters['storage_url'] = storage_url
    app.jinja_env.filters['format_date'] = format_date
    
    # Create upload directories if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'cases'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'news'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'sliders'), exist_ok=True)
    
    return app

