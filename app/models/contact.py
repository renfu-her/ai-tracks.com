"""Contact model."""
from datetime import datetime
from app import db


class Contact(db.Model):
    """Contact model - equivalent to Laravel's Contact."""
    
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, comment='姓名')
    email = db.Column(db.String(255), nullable=False, comment='信箱')
    phone = db.Column(db.String(20), nullable=True, comment='電話')
    subject = db.Column(db.String(255), nullable=False, comment='主旨')
    message = db.Column(db.Text, nullable=False, comment='訊息')
    status = db.Column(db.Enum('pending', 'processing', 'completed', name='contact_status'), 
                       default='pending', nullable=False, comment='處理狀態')
    reply = db.Column(db.Text, nullable=True, comment='回覆內容')
    replied_at = db.Column(db.DateTime, nullable=True, comment='回覆時間')
    image = db.Column(db.String(255), nullable=True, comment='圖片')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Contact {self.name} - {self.subject}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'reply': self.reply,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None,
            'image': self.image,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

