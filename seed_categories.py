"""Seed product categories."""
from app import create_app, db
from app.models.product_category import ProductCategory


def seed_categories():
    """Seed product categories."""
    app = create_app()
    
    with app.app_context():
        # Check if categories already exist
        if ProductCategory.query.count() > 0:
            print("Categories already exist. Skipping seed.")
            return
        
        categories = [
            {
                'name': 'Python',
                'slug': 'python',
                'description': 'Python 相關專案',
                'status': True,
                'sort_order': 1
            },
            {
                'name': 'Laravel',
                'slug': 'laravel',
                'description': 'Laravel 相關專案',
                'status': True,
                'sort_order': 2
            },
            {
                'name': 'Web',
                'slug': 'web',
                'description': 'Web 開發相關專案',
                'status': True,
                'sort_order': 3
            },
            {
                'name': 'AI Tools',
                'slug': 'ai-tools',
                'description': 'AI 工具相關專案',
                'status': True,
                'sort_order': 4
            }
        ]
        
        for cat_data in categories:
            category = ProductCategory(**cat_data)
            db.session.add(category)
        
        db.session.commit()
        print("Successfully seeded product categories:")
        for cat in ProductCategory.query.all():
            print(f"  - {cat.name} (slug: {cat.slug})")


if __name__ == '__main__':
    seed_categories()

