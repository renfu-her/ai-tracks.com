"""Helper functions for templates and application."""
from flask import url_for, current_app
from datetime import datetime
import os


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
    
    # Remove leading slashes if present
    path = path.lstrip('/')
    
    # Return URL for the upload file
    return url_for('static', filename=f'../uploads/{path}')


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

