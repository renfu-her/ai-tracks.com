"""ProjectCase model."""
from datetime import datetime
from app import db
from app.models.case_photo import CasePhoto


class ProjectCase(db.Model):
    """Project case model - equivalent to Laravel's ProjectCase."""
    
    __tablename__ = 'project_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, comment='名稱')
    sub_name = db.Column(db.String(255), nullable=True, comment='副標題')
    url = db.Column(db.String(255), nullable=True, comment='網址')
    content = db.Column(db.Text, nullable=False, comment='內容')
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=True, comment='類別ID')
    status = db.Column(db.Boolean, default=True, nullable=False, comment='狀態')
    views = db.Column(db.Integer, default=0, nullable=False, comment='閱讀次數')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    case_photos = db.relationship('CasePhoto', backref='project_case', lazy='dynamic', 
                                   cascade='all, delete-orphan', order_by='CasePhoto.sort_order')
    
    def get_first_image(self, default_image=None):
        """
        Get the first image ordered by sort_order.
        
        Args:
            default_image: Default image path if no photos exist
            
        Returns:
            CasePhoto object or None
        """
        first_photo = self.case_photos.order_by(CasePhoto.sort_order).first()
        return first_photo if first_photo else None
    
    def get_first_image_url(self, default_image='images/default-case.jpg'):
        """
        Get the URL of the first image, or default image if none exists.
        
        Args:
            default_image: Default image path relative to static folder
            
        Returns:
            Image URL string
        """
        first_photo = self.get_first_image()
        if first_photo:
            from app.utils.helpers import storage_url
            return storage_url(first_photo.image)
        else:
            from flask import url_for
            return url_for('static', filename=default_image)
    
    def __repr__(self):
        return f'<ProjectCase {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'sub_name': self.sub_name,
            'url': self.url,
            'content': self.content,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'status': self.status,
            'views': self.views or 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'case_photos': [photo.to_dict() for photo in self.case_photos.all()]
        )
    
    def increment_views(self):
        """Increment view count."""
        self.views = (self.views or 0) + 1
        db.session.commit()

