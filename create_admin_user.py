"""Create initial admin user."""
import sys
from app import create_app, db
from app.models.user import User

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_admin_user():
    """Create default admin user."""
    app = create_app()
    
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("[INFO] Admin user already exists")
            print(f"      Username: {admin.username}")
            print(f"      Email: {admin.email}")
            print(f"      Role: {admin.role}")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@ai-tracks.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')  # Default password, should be changed
        
        try:
            db.session.add(admin)
            db.session.commit()
            print("[OK] Admin user created successfully!")
            print(f"      Username: admin")
            print(f"      Password: admin123")
            print(f"      Email: admin@ai-tracks.com")
            print("\n[WARNING] Please change the default password after first login!")
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Failed to create admin user: {e}")
            sys.exit(1)

if __name__ == '__main__':
    print("Creating admin user...")
    print("=" * 50)
    create_admin_user()
    print("=" * 50)

