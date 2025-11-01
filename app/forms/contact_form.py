"""Contact form with validation."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError


class ContactForm(FlaskForm):
    """Contact form - equivalent to Laravel validation rules."""
    
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='請輸入姓名'),
            Length(max=255, message='姓名長度不能超過255個字元')
        ]
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='請輸入電子郵件'),
            Email(message='請輸入有效的電子郵件格式'),
            Length(max=255, message='電子郵件長度不能超過255個字元')
        ]
    )
    
    phone = StringField(
        'Phone',
        validators=[
            Length(max=20, message='電話號碼長度不能超過20個字元')
        ]
    )
    
    subject = StringField(
        'Subject',
        validators=[
            DataRequired(message='請輸入主旨'),
            Length(max=255, message='主旨長度不能超過255個字元')
        ]
    )
    
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message='請輸入訊息內容'),
            Length(max=1000, message='訊息內容長度不能超過1000個字元')
        ]
    )
    
    privacy = BooleanField(
        'Privacy Policy',
        validators=[
            DataRequired(message='請同意隱私政策')
        ]
    )
    
    def validate_privacy(self, field):
        """Custom validator to ensure privacy checkbox is checked."""
        if not field.data:
            raise ValidationError('請同意隱私政策')

