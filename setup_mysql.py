"""MySQL database setup script."""
import sys
import pymysql
from app import create_app, db
from app.models import ProjectCase, CasePhoto, News, Slider, Contact

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_database():
    """Create database if it doesn't exist."""
    # Connect to MySQL server (without database)
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            # Create database if not exists
            cursor.execute("CREATE DATABASE IF NOT EXISTS `ai-tracks` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("[OK] Database 'ai-tracks' created or already exists")
    finally:
        connection.close()

def init_database():
    """Initialize database tables."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("[OK] Database tables created")
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"[OK] Created tables: {', '.join(tables)}")

if __name__ == '__main__':
    print("Setting up MySQL database...")
    print("=" * 50)
    
    # Check if PyMySQL is installed
    try:
        import pymysql
        print(f"[OK] PyMySQL version: {pymysql.__version__}")
    except ImportError:
        print("[ERROR] PyMySQL not installed. Please run: pip install PyMySQL")
        sys.exit(1)
    
    # Create database
    try:
        create_database()
    except Exception as e:
        print(f"[ERROR] Error creating database: {e}")
        print("\nPlease ensure:")
        print("1. MySQL is running")
        print("2. Root user has permission to create databases")
        print("3. MySQL credentials are correct")
        sys.exit(1)
    
    # Initialize tables
    try:
        init_database()
    except Exception as e:
        print(f"[ERROR] Error initializing tables: {e}")
        sys.exit(1)
    
    print("=" * 50)
    print("[OK] MySQL database setup complete!")
    print("\nYou can now run:")
    print("  flask db migrate -m 'Initial migration'")
    print("  flask db upgrade")

