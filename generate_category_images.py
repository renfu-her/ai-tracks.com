"""Generate category images for Python, Laravel, Web, and AI Tools."""
import os
from PIL import Image, ImageDraw, ImageFont
from app import create_app, db
from app.models.product_category import ProductCategory

# Category configurations with colors and text
CATEGORIES = [
    {
        'name': 'Python',
        'slug': 'python',
        'color': (49, 140, 231),  # Python blue
        'bg_color': (240, 248, 255),  # Light blue background
    },
    {
        'name': 'Laravel',
        'slug': 'laravel',
        'color': (255, 45, 45),  # Laravel red
        'bg_color': (255, 245, 245),  # Light red background
    },
    {
        'name': 'Web',
        'slug': 'web',
        'color': (34, 197, 94),  # Green
        'bg_color': (240, 253, 244),  # Light green background
    },
    {
        'name': 'AI Tools',
        'slug': 'ai-tools',
        'color': (147, 51, 234),  # Purple
        'bg_color': (250, 245, 255),  # Light purple background
    },
]


def create_category_image(name, color, bg_color, output_path):
    """Create a category image."""
    # Image dimensions
    width, height = 800, 400
    
    # Create image with background color
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default if not available
    try:
        # Try to use a bold font
        font_large = ImageFont.truetype("arial.ttf", 80)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        try:
            font_large = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 80)
            font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 40)
        except:
            # Use default font if system fonts not available
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # Draw category name
    text = name
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 30
    
    # Draw text shadow for depth
    draw.text((x + 3, y + 3), text, fill=(200, 200, 200), font=font_large)
    # Draw main text
    draw.text((x, y), text, fill=color, font=font_large)
    
    # Draw decorative elements
    # Draw circles in corners
    circle_size = 80
    draw.ellipse([20, 20, 20 + circle_size, 20 + circle_size], 
                 fill=color, outline=None)
    draw.ellipse([width - 20 - circle_size, height - 20 - circle_size, 
                  width - 20, height - 20], 
                 fill=color, outline=None)
    
    # Draw lines
    line_width = 4
    draw.rectangle([0, height // 2 - 2, width, height // 2 + 2], fill=color)
    
    # Save image
    img.save(output_path, 'JPEG', quality=90)
    print(f"Created image: {output_path}")


def generate_and_update_categories():
    """Generate images and update categories in database."""
    app = create_app()
    app.app_context().push()
    
    # Create categories directory if it doesn't exist
    categories_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'categories')
    os.makedirs(categories_dir, exist_ok=True)
    
    # Generate images and update database
    for cat_config in CATEGORIES:
        # Generate image filename
        filename = f"{cat_config['slug']}.jpg"
        image_path = os.path.join(categories_dir, filename)
        
        # Create image
        create_category_image(
            cat_config['name'],
            cat_config['color'],
            cat_config['bg_color'],
            image_path
        )
        
        # Update or create category in database
        category = ProductCategory.query.filter_by(slug=cat_config['slug']).first()
        if category:
            # Update existing category
            category.image = f"categories/{filename}"
            print(f"Updated category: {cat_config['name']} with image: {category.image}")
        else:
            print(f"Category {cat_config['name']} not found in database. Please create it first or run seed_categories.py")
    
    # Commit changes
    try:
        db.session.commit()
        print("Successfully updated categories with images!")
    except Exception as e:
        db.session.rollback()
        print(f"Error updating categories: {e}")


if __name__ == '__main__':
    generate_and_update_categories()

