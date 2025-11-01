"""Database models."""
from app.models.project_case import ProjectCase
from app.models.case_photo import CasePhoto
from app.models.product_category import ProductCategory
from app.models.news import News
from app.models.slider import Slider
from app.models.contact import Contact
from app.models.user import User

__all__ = [
    'ProjectCase',
    'CasePhoto',
    'ProductCategory',
    'News',
    'Slider',
    'Contact',
    'User'
]

