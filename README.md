# AI Tracks - Flask Application

A professional AI technology portfolio website built with Flask, converted from Laravel.

## Features

- **Case Studies Management**: Showcase your projects with image galleries
- **News/Blog System**: Share updates and articles with Markdown support
- **Contact Form**: Receive inquiries from potential clients
- **Responsive Design**: Bootstrap 5 responsive layout
- **Image Processing**: Automatic WebP conversion and optimization
- **SEO Optimized**: Meta tags, Open Graph, and Twitter Cards
- **uWSGI Ready**: Production-ready with uWSGI configuration

## Requirements

- Python 3.8+
- pip
- Virtual environment (recommended)
- uWSGI (for production)
- SQLite/PostgreSQL/MySQL

## Installation

### 1. Clone the Repository

```bash
cd /path/to/ai-tracks.com
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and set your configuration:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///ai_tracks.db
```

### 5. Initialize Database

```bash
# Initialize migration repository (first time only)
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### 6. Run Development Server

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Production Deployment with uWSGI

### 1. Update Configuration

Edit `uwsgi.ini` and update the following:

```ini
# Update the application directory
chdir = /path/to/your/ai-tracks.com

# Update virtual environment path (if using)
home = /path/to/your/venv

# Update socket path (if using Nginx)
socket = /tmp/ai-tracks.sock

# Update log paths
logto = /var/log/uwsgi/ai-tracks.log
```

### 2. Create Log Directory

```bash
sudo mkdir -p /var/log/uwsgi
sudo chown $USER:$USER /var/log/uwsgi
```

### 3. Run with uWSGI

```bash
uwsgi --ini uwsgi.ini
```

### 4. Nginx Configuration (Optional)

If using Nginx as reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/ai-tracks.sock;
    }

    location /static {
        alias /path/to/ai-tracks.com/static;
        expires 30d;
    }

    location /uploads {
        alias /path/to/ai-tracks.com/uploads;
        expires 30d;
    }
}
```

### 5. Systemd Service (Optional)

Create `/etc/systemd/system/ai-tracks.service`:

```ini
[Unit]
Description=AI Tracks uWSGI Service
After=network.target

[Service]
User=your-user
Group=www-data
WorkingDirectory=/path/to/ai-tracks.com
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uwsgi --ini uwsgi.ini

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable ai-tracks
sudo systemctl start ai-tracks
sudo systemctl status ai-tracks
```

## Project Structure

```
ai-tracks.com/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration
│   ├── models/                  # Database models
│   │   ├── project_case.py
│   │   ├── case_photo.py
│   │   ├── news.py
│   │   ├── slider.py
│   │   └── contact.py
│   ├── controllers/             # Business logic
│   │   └── frontend_controller.py
│   ├── routes/                  # URL routes
│   │   └── frontend.py
│   ├── services/                # Services (image processing, etc.)
│   │   └── image_service.py
│   ├── forms/                   # WTForms
│   │   └── contact_form.py
│   ├── utils/                   # Helper functions
│   │   └── helpers.py
│   └── templates/               # Jinja2 templates
│       ├── base.html
│       ├── home.html
│       ├── cases.html
│       ├── case_detail.html
│       ├── news.html
│       ├── news_detail.html
│       └── contact.html
├── static/                      # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── uploads/                     # User uploads
├── migrations/                  # Database migrations
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore
├── run.py                       # Development server
├── wsgi.py                      # WSGI entry point
├── uwsgi.ini                    # uWSGI configuration
└── README.md
```

## Database Models

- **ProjectCase**: Portfolio case studies
- **CasePhoto**: Case study images
- **News**: News/blog articles
- **Slider**: Homepage slider images
- **Contact**: Contact form submissions

## Key Features Implemented

### From Laravel to Flask

- ✅ Eloquent ORM → SQLAlchemy ORM
- ✅ Blade Templates → Jinja2 Templates
- ✅ Laravel Routes → Flask Blueprints
- ✅ Laravel Validation → Flask-WTF
- ✅ Storage::url() → Custom helper functions
- ✅ Intervention/Image → Pillow (WebP conversion)
- ✅ Laravel Pagination → Flask-SQLAlchemy pagination

### Template Syntax Conversion

| Laravel Blade | Flask Jinja2 |
|--------------|--------------|
| `@extends('layout')` | `{% extends "layout.html" %}` |
| `@section('content')` | `{% block content %}` |
| `{{ $var }}` | `{{ var }}` |
| `@if/@endif` | `{% if %}/{% endif %}` |
| `@foreach/@endforeach` | `{% for %}/{% endfor %}` |
| `route('home')` | `url_for('frontend.home')` |
| `asset('css/app.css')` | `url_for('static', filename='css/app.css')` |
| `Storage::url($path)` | `{{ path\|storage_url }}` |

## Common Commands

```bash
# Run development server
python run.py

# Create database migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade

# Run with uWSGI (development)
uwsgi --ini uwsgi.ini

# Install new package
pip install package-name
pip freeze > requirements.txt
```

## Troubleshooting

### Database Errors

```bash
# Reset database
rm ai_tracks.db
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### uWSGI Issues

Check logs:
```bash
tail -f /var/log/uwsgi/ai-tracks.log
```

Test configuration:
```bash
uwsgi --ini uwsgi.ini --check-static
```

### Permission Issues

```bash
# Fix upload directory permissions
chmod 755 uploads/
chown -R $USER:www-data uploads/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Contact

- Phone: 0922-013-171
- Email: renfu.her@gmail.com

## Acknowledgments

- Converted from Laravel application
- Built with Flask, SQLAlchemy, and Bootstrap 5
- Image processing with Pillow
- Markdown rendering with marked.js

