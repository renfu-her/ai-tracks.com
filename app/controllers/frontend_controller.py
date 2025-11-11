"""Frontend controller - equivalent to Laravel's FrontendController."""
from flask import render_template, request, redirect, url_for, flash, jsonify, Response
from sqlalchemy import desc, asc
from app import db
from app.models import ProjectCase, CasePhoto, News, Slider, Contact, ProductCategory, PageSettings
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
        
        # Get home banner image from PageSettings
        home_page_settings = PageSettings.get_or_create('home_banner')
        home_banner = home_page_settings.banner_image
        
        return render_template(
            'home.html',
            featured_cases=featured_cases,
            latest_news=latest_news,
            sliders=sliders,
            home_banner=home_banner
        )
    
    @staticmethod
    def cases():
        """Cases listing page with pagination and sorting."""
        # Get sort parameter
        sort = request.args.get('sort', 'latest')
        category_slug = request.args.get('category')
        page = request.args.get('page', 1, type=int)
        per_page = 9
        
        # Base query: active cases only
        query = ProjectCase.query.filter_by(status=True)
        
        # Filter by category if provided
        category = None
        if category_slug:
            category = ProductCategory.query.filter_by(slug=category_slug, status=True).first()
            if category:
                query = query.filter(ProjectCase.category_id == category.id)
        
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
        
        # Get page banner image for category list (when no specific category is selected)
        page_banner = None
        if not category:
            category_list_settings = PageSettings.get_or_create('category_list')
            page_banner = category_list_settings.banner_image
        
        return render_template(
            'cases.html',
            cases=cases_pagination,
            current_sort=sort,
            current_category=category_slug,
            category=category,
            page_banner=page_banner
        )
    
    @staticmethod
    def cases_by_category(category_slug):
        """Cases listing page filtered by category."""
        # Redirect to cases with category filter
        return redirect(url_for('frontend.cases', category=category_slug))
    
    @staticmethod
    def case_detail(id):
        """Case detail page."""
        # Get case with photos
        case = ProjectCase.query.filter_by(id=id, status=True).first_or_404()
        
        # Increment view count when viewing detail page
        try:
            case.views = (case.views or 0) + 1
            db.session.commit()
        except Exception:
            db.session.rollback()
        
        # Get related cases - same category only, exclude current case
        related_cases = []
        if case.category_id:
            # Only show related cases if the case has a category
            # Get cases from same category, exclude current case
            related_cases = ProjectCase.query\
                .filter(
                    ProjectCase.id != id,
                    ProjectCase.status == True,
                    ProjectCase.category_id == case.category_id
                )\
                .order_by(desc(ProjectCase.created_at))\
                .limit(5)\
                .all()
        
        # Get page banner image for category list (fallback if case has no category image)
        page_banner = None
        category_list_settings = PageSettings.get_or_create('category_list')
        page_banner = category_list_settings.banner_image
        
        return render_template(
            'case_detail.html',
            case=case,
            related_cases=related_cases,
            page_banner=page_banner
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
        
        # Get page banner image
        news_page_settings = PageSettings.get_or_create('news_list')
        
        return render_template('news.html', news=news_pagination, page_banner=news_page_settings.banner_image)
    
    @staticmethod
    def news_detail(id):
        """News detail page."""
        # Get news item
        news_item = News.query.filter_by(id=id, is_active=True).first_or_404()
        
        # Increment view count when viewing detail page
        try:
            news_item.views = (news_item.views or 0) + 1
            db.session.commit()
        except Exception:
            db.session.rollback()
        
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
        
        # Get page banner image
        contact_page_settings = PageSettings.get_or_create('contact_list')
        
        return render_template('contact.html', form=form, page_banner=contact_page_settings.banner_image)
    
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
        
        # Get page banner image
        contact_page_settings = PageSettings.get_or_create('contact_list')
        
        return render_template('contact.html', form=form, page_banner=contact_page_settings.banner_image)
    
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
    
    @staticmethod
    def sitemap():
        """Generate sitemap.xml dynamically."""
        from flask import url_for
        
        # Get base URL
        base_url = request.url_root.rstrip('/')
        
        # Get all active cases
        cases = ProjectCase.query.filter_by(status=True).order_by(desc(ProjectCase.updated_at)).all()
        
        # Get all active news
        news_items = News.query.filter_by(is_active=True).order_by(desc(News.updated_at)).all()
        
        # Get all active categories
        categories = ProductCategory.query.filter_by(status=True).order_by(asc(ProductCategory.sort_order)).all()
        
        # Start building XML
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]
        
        # Home page
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{base_url}/</loc>')
        xml_lines.append('    <changefreq>daily</changefreq>')
        xml_lines.append('    <priority>1.0</priority>')
        xml_lines.append('  </url>')
        
        # Cases listing page
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{base_url}{url_for("frontend.cases")}</loc>')
        xml_lines.append('    <changefreq>daily</changefreq>')
        xml_lines.append('    <priority>0.9</priority>')
        xml_lines.append('  </url>')
        
        # Category pages
        for category in categories:
            xml_lines.append('  <url>')
            xml_lines.append(f'    <loc>{base_url}{url_for("frontend.cases", category=category.slug)}</loc>')
            xml_lines.append('    <changefreq>weekly</changefreq>')
            xml_lines.append('    <priority>0.8</priority>')
            xml_lines.append('  </url>')
        
        # Case detail pages
        for case in cases:
            xml_lines.append('  <url>')
            xml_lines.append(f'    <loc>{base_url}{url_for("frontend.case_detail", id=case.id)}</loc>')
            if case.updated_at:
                try:
                    # Handle both datetime and date objects
                    if hasattr(case.updated_at, 'strftime'):
                        xml_lines.append(f'    <lastmod>{case.updated_at.strftime("%Y-%m-%d")}</lastmod>')
                    else:
                        xml_lines.append(f'    <lastmod>{str(case.updated_at)}</lastmod>')
                except Exception:
                    pass  # Skip lastmod if there's an error
            xml_lines.append('    <changefreq>monthly</changefreq>')
            xml_lines.append('    <priority>0.7</priority>')
            xml_lines.append('  </url>')
        
        # News listing page
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{base_url}{url_for("frontend.news")}</loc>')
        xml_lines.append('    <changefreq>daily</changefreq>')
        xml_lines.append('    <priority>0.9</priority>')
        xml_lines.append('  </url>')
        
        # News detail pages
        for news_item in news_items:
            xml_lines.append('  <url>')
            xml_lines.append(f'    <loc>{base_url}{url_for("frontend.news_detail", id=news_item.id)}</loc>')
            if news_item.updated_at:
                try:
                    if hasattr(news_item.updated_at, 'strftime'):
                        xml_lines.append(f'    <lastmod>{news_item.updated_at.strftime("%Y-%m-%d")}</lastmod>')
                    else:
                        xml_lines.append(f'    <lastmod>{str(news_item.updated_at)}</lastmod>')
                except Exception:
                    pass
            elif news_item.published_at:
                try:
                    # published_at is a Date object, not DateTime
                    if hasattr(news_item.published_at, 'strftime'):
                        xml_lines.append(f'    <lastmod>{news_item.published_at.strftime("%Y-%m-%d")}</lastmod>')
                    else:
                        xml_lines.append(f'    <lastmod>{str(news_item.published_at)}</lastmod>')
                except Exception:
                    pass
            xml_lines.append('    <changefreq>monthly</changefreq>')
            xml_lines.append('    <priority>0.7</priority>')
            xml_lines.append('  </url>')
        
        # Contact page
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{base_url}{url_for("frontend.contact")}</loc>')
        xml_lines.append('    <changefreq>monthly</changefreq>')
        xml_lines.append('    <priority>0.6</priority>')
        xml_lines.append('  </url>')
        
        # Close XML
        xml_lines.append('</urlset>')
        
        xml_content = '\n'.join(xml_lines)
        return Response(xml_content, mimetype='application/xml')

