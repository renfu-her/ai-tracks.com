"""Image processing service for WebP conversion and resizing."""
import os
import uuid
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename


class ImageService:
    """Service for handling image uploads, conversion, and processing."""
    
    @staticmethod
    def process_and_save(file, subfolder='', max_width=1920, max_height=1080, quality=80):
        """
        Process uploaded image: resize and convert to WebP format.
        
        Args:
            file: FileStorage object from request.files
            subfolder: Subfolder within uploads directory (e.g., 'cases', 'news')
            max_width: Maximum width for resizing
            max_height: Maximum height for resizing
            quality: WebP quality (0-100)
            
        Returns:
            Relative path to saved file (e.g., 'cases/uuid.webp')
        """
        # Generate unique filename
        filename = f"{uuid.uuid4().hex}.webp"
        
        # Get upload folder path
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        
        # Create subfolder if specified
        if subfolder:
            folder_path = os.path.join(upload_folder, subfolder)
            relative_path = os.path.join(subfolder, filename)
        else:
            folder_path = upload_folder
            relative_path = filename
        
        # Ensure directory exists
        os.makedirs(folder_path, exist_ok=True)
        
        # Full path for saving
        filepath = os.path.join(folder_path, filename)
        
        # Open and process image
        image = Image.open(file.stream)
        
        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image while maintaining aspect ratio
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save as WebP
        image.save(filepath, 'WEBP', quality=quality, method=6)
        
        return relative_path
    
    @staticmethod
    def delete_image(relative_path):
        """
        Delete image file from uploads directory.
        
        Args:
            relative_path: Relative path to the file (e.g., 'cases/uuid.webp')
            
        Returns:
            Boolean indicating success
        """
        if not relative_path:
            return False
        
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        filepath = os.path.join(upload_folder, relative_path)
        
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception as e:
            current_app.logger.error(f"Error deleting file {filepath}: {e}")
        
        return False
    
    @staticmethod
    def process_slider_image(file, quality=85):
        """
        Process slider image with specific dimensions.
        
        Args:
            file: FileStorage object from request.files
            quality: WebP quality (0-100)
            
        Returns:
            Relative path to saved file
        """
        return ImageService.process_and_save(
            file, 
            subfolder='sliders', 
            max_width=1920, 
            max_height=1080, 
            quality=quality
        )
    
    @staticmethod
    def process_case_image(file, quality=80):
        """
        Process case photo with specific dimensions.
        
        Args:
            file: FileStorage object from request.files
            quality: WebP quality (0-100)
            
        Returns:
            Relative path to saved file
        """
        return ImageService.process_and_save(
            file, 
            subfolder='cases', 
            max_width=1920, 
            max_height=1080, 
            quality=quality
        )
    
    @staticmethod
    def process_news_image(file, quality=80):
        """
        Process news image with specific dimensions.
        
        Args:
            file: FileStorage object from request.files
            quality: WebP quality (0-100)
            
        Returns:
            Relative path to saved file
        """
        return ImageService.process_and_save(
            file, 
            subfolder='news', 
            max_width=1920, 
            max_height=1080, 
            quality=quality
        )

