"""Frontend controller - equivalent to Laravel's FrontendController."""
from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import desc, asc
from app import db
from app.models import ProjectCase, CasePhoto, News, Slider, Contact
from app.forms.contact_form import ContactForm


class FrontendController:
    """Frontend controller for handling all frontend routes."""
    
    @staticmethod
    def home():
        """Home page with featured cases, latest news, and sliders."""
        # Get featured cases (top 6, active only, with photos)
        featured_cases = ProjectCase.query\
            .filter_by(status=True)\
            .order_by(desc(ProjectCase.created_at))\
            .limit(6)\
            .all()
        
        # Get latest news (top 3, active only)
        latest_news = News.query\
            .filter_by(is_active=True)\
            .order_by(desc(News.created_at))\
            .limit(3)\
            .all()
        
        # Get active sliders, sorted by sort order
        sliders = Slider.query\
            .filter_by(is_active=True)\
            .order_by(asc(Slider.sort))\
            .all()
        
        return render_template(
            'home.html',
            featured_cases=featured_cases,
            latest_news=latest_news,
            sliders=sliders
        )
    
    @staticmethod
    def cases():
        """Cases listing page with pagination and sorting."""
        # Get sort parameter
        sort = request.args.get('sort', 'latest')
        page = request.args.get('page', 1, type=int)
        per_page = 9
        
        # Base query: active cases only
        query = ProjectCase.query.filter_by(status=True)
        
        # Apply sorting
        if sort == 'oldest':
            query = query.order_by(asc(ProjectCase.created_at))
        elif sort == 'name':
            query = query.order_by(asc(ProjectCase.name))
        else:  # latest (default)
            query = query.order_by(desc(ProjectCase.created_at))
        
        # Paginate results
        cases_pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return render_template(
            'cases.html',
            cases=cases_pagination,
            current_sort=sort
        )
    
    @staticmethod
    def case_detail(id):
        """Case detail page."""
        # Get case with photos
        case = ProjectCase.query.filter_by(id=id, status=True).first_or_404()
        
        # Get related cases (exclude current, get 3)
        related_cases = ProjectCase.query\
            .filter(ProjectCase.id != id, ProjectCase.status == True)\
            .order_by(desc(ProjectCase.created_at))\
            .limit(3)\
            .all()
        
        return render_template(
            'case_detail.html',
            case=case,
            related_cases=related_cases
        )
    
    @staticmethod
    def news():
        """News listing page with pagination."""
        page = request.args.get('page', 1, type=int)
        per_page = 9
        
        # Query active news, sorted by creation date
        news_pagination = News.query\
            .filter_by(is_active=True)\
            .order_by(desc(News.created_at))\
            .paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
        
        return render_template('news.html', news=news_pagination)
    
    @staticmethod
    def news_detail(id):
        """News detail page."""
        # Get news item
        news_item = News.query.filter_by(id=id, is_active=True).first_or_404()
        
        # Get related news (exclude current, get 3)
        related_news = News.query\
            .filter(News.id != id, News.is_active == True)\
            .order_by(desc(News.created_at))\
            .limit(3)\
            .all()
        
        return render_template(
            'news_detail.html',
            news=news_item,
            related_news=related_news
        )
    
    @staticmethod
    def contact():
        """Contact page (GET) - display form."""
        form = ContactForm()
        return render_template('contact.html', form=form)
    
    @staticmethod
    def store_contact():
        """Contact page (POST) - handle form submission."""
        form = ContactForm()
        
        if form.validate_on_submit():
            # Create new contact record
            contact = Contact(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                subject=form.subject.data,
                message=form.message.data
            )
            
            try:
                db.session.add(contact)
                db.session.commit()
                flash('訊息已成功發送，我們會盡快回覆您！', 'success')
                return redirect(url_for('frontend.contact'))
            except Exception as e:
                db.session.rollback()
                flash('發送訊息時發生錯誤，請稍後再試。', 'danger')
        else:
            # Display validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error, 'danger')
        
        return render_template('contact.html', form=form)
    
    @staticmethod
    def get_case_api(id):
        """API endpoint for getting case data (AJAX)."""
        case = ProjectCase.query.get_or_404(id)
        
        return jsonify({
            'id': case.id,
            'name': case.name,
            'sub_name': case.sub_name,
            'url': case.url,
            'content': case.content,
            'status': case.status,
            'created_at': case.created_at.isoformat() if case.created_at else None,
            'case_photos': [
                {
                    'id': photo.id,
                    'image': photo.image,
                    'sort_order': photo.sort_order
                }
                for photo in case.case_photos.order_by(CasePhoto.sort_order).all()
            ]
        })
    
    @staticmethod
    def get_news_api(id):
        """API endpoint for getting news data (AJAX)."""
        news = News.query.get_or_404(id)
        
        return jsonify({
            'id': news.id,
            'title': news.title,
            'content': news.content,
            'image': news.image,
            'published_at': news.published_at.isoformat() if news.published_at else None,
            'is_active': news.is_active
        })

