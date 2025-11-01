"""Backend controller for admin panel."""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import desc, asc
from app import db
from app.models import ProjectCase, CasePhoto, News, Slider, Contact, User
from app.forms.auth_form import LoginForm
from app.utils.auth import admin_required


class BackendController:
    """Backend controller for admin panel."""
    
    @staticmethod
    def login():
        """Admin login page."""
        if current_user.is_authenticated:
            return redirect(url_for('backend.dashboard'))
        
        form = LoginForm()
        
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            
            if user and user.check_password(form.password.data) and user.is_active:
                login_user(user, remember=form.remember_me.data)
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('backend.dashboard'))
            else:
                flash('用戶名或密碼錯誤，或帳號已被停用', 'danger')
        
        return render_template('backend/login.html', form=form)
    
    @staticmethod
    def logout():
        """Admin logout."""
        logout_user()
        flash('已成功登出', 'success')
        return redirect(url_for('backend.login'))
    
    @staticmethod
    @login_required
    @admin_required
    def dashboard():
        """Admin dashboard."""
        # Get statistics
        stats = {
            'total_cases': ProjectCase.query.count(),
            'active_cases': ProjectCase.query.filter_by(status=True).count(),
            'total_news': News.query.count(),
            'active_news': News.query.filter_by(is_active=True).count(),
            'total_contacts': Contact.query.count(),
            'pending_contacts': Contact.query.filter_by(status='pending').count(),
            'total_sliders': Slider.query.count(),
            'active_sliders': Slider.query.filter_by(is_active=True).count(),
            'total_users': User.query.count(),
            'admin_users': User.query.filter_by(role='admin').count()
        }
        
        # Get recent activities
        recent_contacts = Contact.query.order_by(desc(Contact.created_at)).limit(5).all()
        recent_cases = ProjectCase.query.order_by(desc(ProjectCase.created_at)).limit(5).all()
        
        return render_template(
            'backend/dashboard.html',
            stats=stats,
            recent_contacts=recent_contacts,
            recent_cases=recent_cases
        )
    
    @staticmethod
    @login_required
    @admin_required
    def users():
        """User management page."""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        users_pagination = User.query.order_by(desc(User.created_at)).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return render_template('backend/users.html', users=users_pagination)
    
    @staticmethod
    @login_required
    @admin_required
    def create_user():
        """Create new user."""
        from flask import request
        
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role', 'user')
            
            # Validate
            if User.query.filter_by(username=username).first():
                flash('用戶名已存在', 'danger')
                return redirect(url_for('backend.users'))
            
            if User.query.filter_by(email=email).first():
                flash('電子郵件已存在', 'danger')
                return redirect(url_for('backend.users'))
            
            # Create user
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            
            try:
                db.session.add(user)
                db.session.commit()
                flash('用戶創建成功', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'創建用戶失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.users'))
    
    @staticmethod
    @login_required
    @admin_required
    def delete_user(user_id):
        """Delete user."""
        if user_id == current_user.id:
            flash('無法刪除自己的帳號', 'danger')
            return redirect(url_for('backend.users'))
        
        user = User.query.get_or_404(user_id)
        
        try:
            db.session.delete(user)
            db.session.commit()
            flash('用戶刪除成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'刪除用戶失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.users'))
    
    @staticmethod
    @login_required
    @admin_required
    def toggle_user_status(user_id):
        """Toggle user active status."""
        if user_id == current_user.id:
            flash('無法停用自己的帳號', 'danger')
            return redirect(url_for('backend.users'))
        
        user = User.query.get_or_404(user_id)
        user.is_active = not user.is_active
        
        try:
            db.session.commit()
            status = '啟用' if user.is_active else '停用'
            flash(f'用戶已{status}', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'操作失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.users'))

