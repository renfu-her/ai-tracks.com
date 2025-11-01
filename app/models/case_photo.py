"""CasePhoto model."""
from datetime import datetime
from app import db


class CasePhoto(db.Model):
    """Case photo model - equivalent to Laravel's CasePhoto."""
    
    __tablename__ = 'case_photos'
    
    id = db.Column(db.Integer, primary_key=True)
    project_case_id = db.Column(db.Integer, db.ForeignKey('project_cases.id', ondelete='CASCADE'), 
                                 nullable=False)
    image = db.Column(db.String(255), nullable=False, comment='案例照片')
    sort_order = db.Column(db.Integer, default=0, nullable=False, comment='排序')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<CasePhoto {self.id} for ProjectCase {self.project_case_id}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'project_case_id': self.project_case_id,
            'image': self.image,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

