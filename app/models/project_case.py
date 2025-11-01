"""ProjectCase model."""
from datetime import datetime
from app import db


class ProjectCase(db.Model):
    """Project case model - equivalent to Laravel's ProjectCase."""
    
    __tablename__ = 'project_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, comment='名稱')
    sub_name = db.Column(db.String(255), nullable=True, comment='副標題')
    url = db.Column(db.String(255), nullable=True, comment='網址')
    content = db.Column(db.Text, nullable=False, comment='內容')
    status = db.Column(db.Boolean, default=True, nullable=False, comment='狀態')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    case_photos = db.relationship('CasePhoto', backref='project_case', lazy='dynamic', 
                                   cascade='all, delete-orphan', order_by='CasePhoto.sort_order')
    
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
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'case_photos': [photo.to_dict() for photo in self.case_photos.all()]
        }

