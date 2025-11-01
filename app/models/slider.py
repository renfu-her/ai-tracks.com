"""Slider model."""
from datetime import datetime
from app import db


class Slider(db.Model):
    """Slider model - equivalent to Laravel's Slider."""
    
    __tablename__ = 'sliders'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, comment='標題')
    description = db.Column(db.Text, nullable=True, comment='描述')
    image = db.Column(db.String(255), nullable=False, comment='圖片')
    link = db.Column(db.String(255), nullable=True, comment='連結')
    sort = db.Column(db.Integer, default=0, nullable=False, comment='排序')
    is_active = db.Column(db.Boolean, default=True, nullable=False, comment='是否啟用')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Slider {self.title}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'link': self.link,
            'sort': self.sort,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

