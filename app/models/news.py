"""News model."""
from datetime import datetime, date
from app import db


class News(db.Model):
    """News model - equivalent to Laravel's News."""
    
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, comment='標題')
    content = db.Column(db.Text, nullable=False, comment='內容')
    image = db.Column(db.String(255), nullable=True, comment='圖片')
    published_at = db.Column(db.Date, default=date.today, nullable=False, comment='發布日期')
    is_active = db.Column(db.Boolean, default=True, nullable=False, comment='是否啟用')
    views = db.Column(db.Integer, default=0, nullable=False, comment='閱讀次數')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<News {self.title}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'image': self.image,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'is_active': self.is_active,
            'views': self.views,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def increment_views(self):
        """Increment view count."""
        self.views = (self.views or 0) + 1
        db.session.commit()

