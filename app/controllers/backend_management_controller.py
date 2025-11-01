"""Backend management controller for cases, news, and contacts."""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from datetime import datetime
from sqlalchemy import desc, asc
from app import db
from app.models import ProjectCase, CasePhoto, News, Slider, Contact, ProductCategory
from app.utils.auth import admin_required
from app.services.image_service import ImageService
from werkzeug.utils import secure_filename
import os


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
        
        # Get all categories for dropdown
        categories = ProductCategory.query.order_by(asc(ProductCategory.sort_order)).all()
        
        return render_template(
            'backend/cases.html',
            cases=cases_pagination,
            current_sort=sort,
            categories=categories
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
            category_id = request.form.get('category_id')
            status = request.form.get('status') == 'on'
            
            if not name or not content:
                flash('名稱和內容為必填項目', 'danger')
                return redirect(url_for('backend.cases'))
            
            # Validate category_id if provided
            category_id = int(category_id) if category_id and category_id != '' else None
            if category_id:
                category = ProductCategory.query.get(category_id)
                if not category:
                    flash('選擇的類別不存在', 'danger')
                    return redirect(url_for('backend.cases'))
            
            case = ProjectCase(
                name=name,
                sub_name=sub_name,
                url=url,
                content=content,
                category_id=category_id,
                status=status
            )
            
            try:
                db.session.add(case)
                db.session.flush()  # Get case.id
                
                # Handle photo uploads
                if 'photos[]' in request.files:
                    files = request.files.getlist('photos[]')
                    for index, file in enumerate(files):
                        if file and file.filename:
                            image_path = ImageService.process_and_save(file, subfolder='cases', max_width=1920, max_height=1080)
                            photo = CasePhoto(
                                project_case_id=case.id,
                                image=image_path,
                                sort_order=index
                            )
                            db.session.add(photo)
                
                db.session.commit()
                flash('案例創建成功', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'創建案例失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.cases'))
    
    @staticmethod
    @login_required
    @admin_required
    def upload_case_photo(case_id):
        """Upload photo for case."""
        case = ProjectCase.query.get_or_404(case_id)
        
        if 'photo' not in request.files:
            return jsonify({'success': False, 'message': '沒有選擇檔案'}), 400
        
        file = request.files['photo']
        if file.filename == '':
            return jsonify({'success': False, 'message': '沒有選擇檔案'}), 400
        
        try:
            # Process and save image
            image_path = ImageService.process_and_save(file, subfolder='cases', max_width=1920, max_height=1080)
            
            # Get max sort_order for this case
            max_sort = db.session.query(db.func.max(CasePhoto.sort_order))\
                .filter_by(project_case_id=case_id)\
                .scalar() or -1
            
            # Create CasePhoto record
            photo = CasePhoto(
                project_case_id=case_id,
                image=image_path,
                sort_order=max_sort + 1
            )
            
            db.session.add(photo)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': '圖片上傳成功',
                'photo': {
                    'id': photo.id,
                    'image': photo.image,
                    'sort_order': photo.sort_order
                }
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'上傳失敗: {str(e)}'}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def delete_case_photo(case_id, photo_id):
        """Delete case photo."""
        photo = CasePhoto.query.filter_by(id=photo_id, project_case_id=case_id).first_or_404()
        
        try:
            # Delete image file
            ImageService.delete_image(photo.image)
            
            # Delete database record
            db.session.delete(photo)
            db.session.commit()
            
            return jsonify({'success': True, 'message': '圖片刪除成功'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'刪除失敗: {str(e)}'}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def update_case_photo_order(case_id):
        """Update photo sort order."""
        case = ProjectCase.query.get_or_404(case_id)
        
        if request.method == 'POST':
            photo_orders = request.get_json().get('orders', [])
            
            try:
                for item in photo_orders:
                    photo_id = item.get('id')
                    sort_order = item.get('sort_order')
                    
                    photo = CasePhoto.query.filter_by(id=photo_id, project_case_id=case_id).first()
                    if photo:
                        photo.sort_order = sort_order
                
                db.session.commit()
                return jsonify({'success': True, 'message': '排序更新成功'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': f'更新失敗: {str(e)}'}), 500
        
        return jsonify({'success': False, 'message': '無效的請求'}), 400
    
    @staticmethod
    @login_required
    @admin_required
    def edit_case(case_id):
        """Edit case page."""
        case = ProjectCase.query.get_or_404(case_id)
        # Load photos ordered by sort_order
        photos = case.case_photos.order_by(CasePhoto.sort_order).all()
        categories = ProductCategory.query.order_by(asc(ProductCategory.sort_order)).all()
        return render_template('backend/edit_case.html', case=case, photos=photos, categories=categories)
    
    @staticmethod
    @login_required
    @admin_required
    def update_case(case_id):
        """Update case."""
        case = ProjectCase.query.get_or_404(case_id)
        
        if request.method == 'POST':
            name = request.form.get('name')
            sub_name = request.form.get('sub_name', '')
            url = request.form.get('url', '')
            content = request.form.get('content', '')
            category_id = request.form.get('category_id')
            status = request.form.get('status') == 'on'
            
            if not name or not content:
                flash('名稱和內容為必填項目', 'danger')
                return redirect(url_for('backend.edit_case', case_id=case_id))
            
            # Validate category_id if provided
            category_id = int(category_id) if category_id and category_id != '' else None
            if category_id:
                category = ProductCategory.query.get(category_id)
                if not category:
                    flash('選擇的類別不存在', 'danger')
                    return redirect(url_for('backend.edit_case', case_id=case_id))
            
            case.name = name
            case.sub_name = sub_name
            case.url = url
            case.content = content
            case.category_id = category_id
            case.status = status
            
            try:
                db.session.commit()
                flash('案例更新成功', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'更新案例失敗: {str(e)}', 'danger')
        
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
    def edit_news(news_id):
        """Edit news page."""
        news = News.query.get_or_404(news_id)
        return render_template('backend/edit_news.html', news=news)
    
    @staticmethod
    @login_required
    @admin_required
    def update_news(news_id):
        """Update news."""
        news = News.query.get_or_404(news_id)
        
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content', '')
            published_at = request.form.get('published_at')
            is_active = request.form.get('is_active') == 'on'
            
            if not title or not content:
                flash('標題和內容為必填項目', 'danger')
                return redirect(url_for('backend.edit_news', news_id=news_id))
            
            try:
                published_date = datetime.strptime(published_at, '%Y-%m-%d').date() if published_at else news.published_at
            except:
                published_date = news.published_at
            
            news.title = title
            news.content = content
            news.published_at = published_date
            news.is_active = is_active
            
            try:
                db.session.commit()
                flash('消息更新成功', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'更新消息失敗: {str(e)}', 'danger')
        
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
    
    # ========== Product Categories Management ==========
    
    @staticmethod
    @login_required
    @admin_required
    def categories():
        """Categories management page."""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        categories_pagination = ProductCategory.query.order_by(
            asc(ProductCategory.sort_order),
            asc(ProductCategory.name)
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return render_template('backend/categories.html', categories=categories_pagination)
    
    @staticmethod
    @login_required
    @admin_required
    def create_category():
        """Create new category."""
        name = request.form.get('name')
        slug = request.form.get('slug', '')
        description = request.form.get('description', '')
        status = request.form.get('status') == 'on'
        sort_order = request.form.get('sort_order', 0, type=int)
        
        if not name:
            flash('類別名稱為必填項目', 'danger')
            return redirect(url_for('backend.categories'))
        
        # Generate slug from name if not provided
        if not slug:
            slug = name.lower().replace(' ', '-').replace('_', '-')
        
        # Check if slug already exists
        existing = ProductCategory.query.filter_by(slug=slug).first()
        if existing:
            flash('該 slug 已存在，請使用其他名稱', 'danger')
            return redirect(url_for('backend.categories'))
        
        # Handle image upload
        image_path = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                try:
                    image_path = ImageService.process_and_save(
                        image_file, 
                        subfolder='categories',
                        max_width=800,
                        max_height=400,
                        quality=90
                    )
                except Exception as e:
                    flash(f'圖片上傳失敗: {str(e)}', 'danger')
        
        category = ProductCategory(
            name=name,
            slug=slug,
            description=description,
            image=image_path,
            status=status,
            sort_order=sort_order
        )
        
        try:
            db.session.add(category)
            db.session.commit()
            flash('類別創建成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'創建類別失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.categories'))
    
    @staticmethod
    @login_required
    @admin_required
    def edit_category(category_id):
        """Edit category page."""
        category = ProductCategory.query.get_or_404(category_id)
        return render_template('backend/edit_category.html', category=category)
    
    @staticmethod
    @login_required
    @admin_required
    def update_category(category_id):
        """Update category."""
        category = ProductCategory.query.get_or_404(category_id)
        
        name = request.form.get('name')
        slug = request.form.get('slug', '')
        description = request.form.get('description', '')
        status = request.form.get('status') == 'on'
        sort_order = request.form.get('sort_order', 0, type=int)
        
        if not name:
            flash('類別名稱為必填項目', 'danger')
            return redirect(url_for('backend.edit_category', category_id=category_id))
        
        # Generate slug from name if not provided
        if not slug:
            slug = name.lower().replace(' ', '-').replace('_', '-')
        
        # Check if slug already exists (excluding current category)
        existing = ProductCategory.query.filter(
            ProductCategory.slug == slug,
            ProductCategory.id != category_id
        ).first()
        if existing:
            flash('該 slug 已存在，請使用其他名稱', 'danger')
            return redirect(url_for('backend.edit_category', category_id=category_id))
        
        # Handle image upload
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                # Delete old image if exists
                if category.image:
                    ImageService.delete_image(category.image)
                
                # Process and save new image
                try:
                    image_path = ImageService.process_and_save(
                        image_file, 
                        subfolder='categories',
                        max_width=800,
                        max_height=400,
                        quality=90
                    )
                    category.image = image_path
                except Exception as e:
                    flash(f'圖片上傳失敗: {str(e)}', 'danger')
        
        category.name = name
        category.slug = slug
        category.description = description
        category.status = status
        category.sort_order = sort_order
        
        try:
            db.session.commit()
            flash('類別更新成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'更新類別失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.categories'))
    
    @staticmethod
    @login_required
    @admin_required
    def delete_category(category_id):
        """Delete category."""
        category = ProductCategory.query.get_or_404(category_id)
        
        # Check if category has associated cases
        case_count = category.project_cases.count()
        if case_count > 0:
            flash(f'無法刪除此類別，因為有 {case_count} 個案例正在使用此類別', 'danger')
            return redirect(url_for('backend.categories'))
        
        try:
            db.session.delete(category)
            db.session.commit()
            flash('類別刪除成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'刪除類別失敗: {str(e)}', 'danger')
        
        return redirect(url_for('backend.categories'))

