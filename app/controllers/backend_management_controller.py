"""Backend management controller for cases, news, and contacts."""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from datetime import datetime
from sqlalchemy import desc, asc
from app import db
from app.models import ProjectCase, CasePhoto, News, Slider, Contact
from app.utils.auth import admin_required


class BackendManagementController:
    """Backend management controller for content management."""
    
    # ========== Project Cases Management ==========
    
    @staticmethod
    @login_required
    @admin_required
    def cases():
        """Cases management page."""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        sort = request.args.get('sort', 'latest')
        query = ProjectCase.query
        
        if sort == 'oldest':
            query = query.order_by(asc(ProjectCase.created_at))
        elif sort == 'name':
            query = query.order_by(asc(ProjectCase.name))
        else:
            query = query.order_by(desc(ProjectCase.created_at))
        
        cases_pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return render_template(
            'backend/cases.html',
            cases=cases_pagination,
            current_sort=sort
        )
    
    @staticmethod
    @login_required
    @admin_required
    def create_case():
        """Create new case."""
        if request.method == 'POST':
            name = request.form.get('name')
            sub_name = request.form.get('sub_name', '')
            url = request.form.get('url', '')
            content = request.form.get('content', '')
            status = request.form.get('status') == 'on'
            
            if not name or not content:
                flash('名稱和內容為必填項目', 'danger')
                return redirect(url_for('backend.cases'))
            
            case = ProjectCase(
                name=name,
                sub_name=sub_name,
                url=url,
                content=content,
                status=status
            )
            
            try:
                db.session.add(case)
                db.session.commit()
                flash('案例創建成功', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'創建案例失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.cases'))
    
    @staticmethod
    @login_required
    @admin_required
    def delete_case(case_id):
        """Delete case."""
        case = ProjectCase.query.get_or_404(case_id)
        
        try:
            db.session.delete(case)
            db.session.commit()
            flash('案例刪除成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'刪除案例失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.cases'))
    
    @staticmethod
    @login_required
    @admin_required
    def toggle_case_status(case_id):
        """Toggle case status."""
        case = ProjectCase.query.get_or_404(case_id)
        case.status = not case.status
        
        try:
            db.session.commit()
            status = '啟用' if case.status else '停用'
            flash(f'案例已{status}', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'操作失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.cases'))
    
    # ========== News Management ==========
    
    @staticmethod
    @login_required
    @admin_required
    def news():
        """News management page."""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        news_pagination = News.query.order_by(desc(News.created_at)).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return render_template('backend/news.html', news=news_pagination)
    
    @staticmethod
    @login_required
    @admin_required
    def create_news():
        """Create new news."""
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content', '')
            published_at = request.form.get('published_at')
            is_active = request.form.get('is_active') == 'on'
            
            if not title or not content:
                flash('標題和內容為必填項目', 'danger')
                return redirect(url_for('backend.news'))
            
            try:
                published_date = datetime.strptime(published_at, '%Y-%m-%d').date() if published_at else datetime.utcnow().date()
            except:
                published_date = datetime.utcnow().date()
            
            news = News(
                title=title,
                content=content,
                published_at=published_date,
                is_active=is_active
            )
            
            try:
                db.session.add(news)
                db.session.commit()
                flash('消息創建成功', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'創建消息失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.news'))
    
    @staticmethod
    @login_required
    @admin_required
    def delete_news(news_id):
        """Delete news."""
        news = News.query.get_or_404(news_id)
        
        try:
            db.session.delete(news)
            db.session.commit()
            flash('消息刪除成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'刪除消息失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.news'))
    
    @staticmethod
    @login_required
    @admin_required
    def toggle_news_status(news_id):
        """Toggle news status."""
        news = News.query.get_or_404(news_id)
        news.is_active = not news.is_active
        
        try:
            db.session.commit()
            status = '啟用' if news.is_active else '停用'
            flash(f'消息已{status}', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'操作失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.news'))
    
    # ========== Contacts Management ==========
    
    @staticmethod
    @login_required
    @admin_required
    def contacts():
        """Contacts management page."""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        status_filter = request.args.get('status', 'all')
        query = Contact.query
        
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        
        contacts_pagination = query.order_by(desc(Contact.created_at)).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return render_template(
            'backend/contacts.html',
            contacts=contacts_pagination,
            current_status=status_filter
        )
    
    @staticmethod
    @login_required
    @admin_required
    def update_contact_status(contact_id):
        """Update contact status."""
        contact = Contact.query.get_or_404(contact_id)
        new_status = request.form.get('status')
        
        if new_status in ['pending', 'processing', 'completed']:
            contact.status = new_status
            if new_status == 'completed' and not contact.replied_at:
                contact.replied_at = datetime.utcnow()
            
            try:
                db.session.commit()
                flash('聯絡訊息狀態已更新', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'更新失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.contacts'))
    
    @staticmethod
    @login_required
    @admin_required
    def delete_contact(contact_id):
        """Delete contact."""
        contact = Contact.query.get_or_404(contact_id)
        
        try:
            db.session.delete(contact)
            db.session.commit()
            flash('聯絡訊息刪除成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'刪除失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.contacts'))

