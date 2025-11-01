"""Page settings model for storing page-level images and settings."""
from datetime import datetime
from app import db


class PageSettings(db.Model):
    """Page settings model for storing page-level configurations."""
    
    __tablename__ = 'page_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    page_type = db.Column(db.String(50), nullable=False, unique=True, comment='頁面類型')
    banner_image = db.Column(db.String(255), nullable=True, comment='Banner 圖片')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<PageSettings {self.page_type}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'page_type': self.page_type,
            'banner_image': self.banner_image,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_or_create(page_type):
        """Get page settings or create if not exists."""
        settings = PageSettings.query.filter_by(page_type=page_type).first()
        if not settings:
            settings = PageSettings(page_type=page_type)
            db.session.add(settings)
            db.session.commit()
        return settings

