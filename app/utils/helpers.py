"""Helper functions for templates and application."""
from flask import url_for, current_app
from datetime import datetime
import os
import markdown


def markdown_to_html(text):
    """
    Convert Markdown text to HTML.
    
    Args:
        text: Markdown formatted text
        
    Returns:
        HTML string
    """
    if not text:
        return ''
    
    # Configure Markdown extensions
    extensions = ['codehilite', 'fenced_code', 'tables']
    
    # Convert Markdown to HTML
    html = markdown.markdown(
        text,
        extensions=extensions,
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': False
            }
        }
    )
    
    return html


def storage_url(path):
    """
    Generate URL for uploaded files (equivalent to Laravel's Storage::url()).
    
    Args:
        path: Relative path to the file in uploads directory
        
    Returns:
        URL to the uploaded file
    """
    if not path:
        return ''
    
    # Convert backslashes to forward slashes for URL compatibility (Windows compatibility)
    path = path.replace('\\', '/')
    
    # Remove leading slashes if present
    path = path.lstrip('/')
    
    # Return URL for the upload file using uploads route
    return url_for('frontend.uploads', filename=path)


def external_url(url):
    """
    Convert relative URL to absolute URL.
    
    Args:
        url: Relative URL string
        
    Returns:
        Absolute URL string
    """
    if not url:
        return ''
    
    # If already absolute URL, return as is
    if url.startswith('http://') or url.startswith('https://'):
        return url
    
    # Get base URL from request context
    try:
        from flask import request
        base_url = request.url_root.rstrip('/')
        # Remove leading slash from url if present
        url = url.lstrip('/')
        return f"{base_url}/{url}"
    except RuntimeError:
        # If not in request context, return relative URL as is
        return url


def format_date(date_obj, format_str='%Y-%m-%d'):
    """
    Format date object to string.
    
    Args:
        date_obj: Date or datetime object
        format_str: Format string for strftime
        
    Returns:
        Formatted date string
    """
    if not date_obj:
        return ''
    
    if isinstance(date_obj, str):
        return date_obj
    
    return date_obj.strftime(format_str)


def allowed_file(filename, allowed_extensions=None):
    """
    Check if file extension is allowed.
    
    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions
        
    Returns:
        Boolean indicating if file is allowed
    """
    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_upload_path(subfolder=''):
    """
    Get the full path to the upload folder.
    
    Args:
        subfolder: Optional subfolder within uploads
        
    Returns:
        Full path to upload directory
    """
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    
    if subfolder:
        return os.path.join(upload_folder, subfolder)
    
    return upload_folder


def ensure_upload_dir(subfolder=''):
    """
    Ensure upload directory exists.
    
    Args:
        subfolder: Optional subfolder within uploads
    """
    path = get_upload_path(subfolder)
    os.makedirs(path, exist_ok=True)

