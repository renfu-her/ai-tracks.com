"""ProductCategory model."""
from datetime import datetime
from app import db


class ProductCategory(db.Model):
    """Product category model."""
    
    __tablename__ = 'product_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, comment='類別名稱')
    slug = db.Column(db.String(100), nullable=False, unique=True, comment='URL 友好名稱')
    description = db.Column(db.Text, nullable=True, comment='描述')
    status = db.Column(db.Boolean, default=True, nullable=False, comment='狀態')
    sort_order = db.Column(db.Integer, default=0, nullable=False, comment='排序')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    project_cases = db.relationship('ProjectCase', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<ProductCategory {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'status': self.status,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

