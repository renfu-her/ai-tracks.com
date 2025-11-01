"""WSGI entry point for uWSGI and production servers."""
import os
from app import create_app

# Create the application instance
# Note: Using 'application' for uWSGI compatibility
application = create_app(os.getenv('FLASK_ENV', 'production'))

# For backward compatibility and development
app = application

if __name__ == '__main__':
    application.run()

