"""Login form."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Login form."""
    
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='請輸入用戶名'),
            Length(min=3, max=80, message='用戶名長度應在3-80個字元之間')
        ]
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='請輸入密碼'),
            Length(min=6, message='密碼長度至少6個字元')
        ]
    )
    
    remember_me = BooleanField('Remember Me')

