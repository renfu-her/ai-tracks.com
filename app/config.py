"""Application configuration."""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_database_uri():
    """
    Get database URI from environment variables.
    
    Supports two formats:
    1. DATABASE_URL (full connection string)
       Example: mysql+pymysql://user:password@host:port/database
    
    2. Individual database settings (DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
       Will construct MySQL connection string automatically
    """
    # First, try to get DATABASE_URL directly
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return database_url
    
    # If DATABASE_URL not set, try to construct from individual settings
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'ai-tracks')
    db_driver = os.getenv('DB_DRIVER', 'pymysql')  # pymysql or mysqlclient
    
    # Construct MySQL connection string
    if db_password:
        database_uri = f'mysql+{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    else:
        database_uri = f'mysql+{db_driver}://{db_user}@{db_host}:{db_port}/{db_name}'
    
    return database_uri


class Config:
    """Base configuration."""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    # Support for MySQL, PostgreSQL, and SQLite
    # Can use DATABASE_URL (full connection string) or individual DB_* variables
    # MySQL format: mysql+pymysql://username:password@host:port/database
    # SQLite format: sqlite:///database.db
    # PostgreSQL format: postgresql://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # MySQL specific settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'connect_args': {
            'charset': 'utf8mb4'
        }
    }
    
    # File Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Pagination
    ITEMS_PER_PAGE = 9
    
    # WTForms
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Flask-Caching Configuration
    # Use simple cache for development, Redis/Memcached for production
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')  # Options: simple, redis, memcached, filesystem
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes default cache timeout
    
    # Redis cache configuration (if CACHE_TYPE=redis)
    CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST', 'localhost')
    CACHE_REDIS_PORT = int(os.getenv('CACHE_REDIS_PORT', 6379))
    CACHE_REDIS_DB = int(os.getenv('CACHE_REDIS_DB', 0))
    CACHE_REDIS_PASSWORD = os.getenv('CACHE_REDIS_PASSWORD', None)
    
    # Memcached configuration (if CACHE_TYPE=memcached)
    CACHE_MEMCACHED_SERVERS = os.getenv('CACHE_MEMCACHED_SERVERS', '127.0.0.1:11211').split(',')
    
    # Filesystem cache configuration (if CACHE_TYPE=filesystem)
    CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
    
    # Flask-Compress Configuration
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript', 'text/javascript', 'application/xml']
    COMPRESS_LEVEL = 6  # Compression level (1-9, 6 is a good balance)
    COMPRESS_MIN_SIZE = 500  # Only compress responses larger than 500 bytes


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = False
    # Enable template auto-reload for development
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False
    # Disable caching in development for easier debugging
    CACHE_TYPE = 'null'  # Disable caching in development


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # Override with environment variables
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")
    
    # Production caching - use Redis if available, otherwise simple cache
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes for production


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

