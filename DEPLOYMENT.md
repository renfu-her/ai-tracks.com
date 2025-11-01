# Deployment Guide - AI Tracks Flask Application

## Quick Start

### For Development

```bash
# On Linux/Mac
./setup.sh

# On Windows
setup.bat

# Then run
python run.py
```

### For Production with uWSGI

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and set production values

# 3. Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 4. Update uwsgi.ini paths
nano uwsgi.ini

# 5. Run uWSGI
uwsgi --ini uwsgi.ini
```

## Production Deployment

### Option 1: uWSGI + Nginx

#### Step 1: Install uWSGI and Nginx

```bash
# Install uWSGI
pip install uwsgi

# Install Nginx (Ubuntu/Debian)
sudo apt update
sudo apt install nginx
```

#### Step 2: Configure uWSGI

Edit `uwsgi.ini`:

```ini
[uwsgi]
module = wsgi:app
master = true
processes = 4
threads = 2

# Update these paths
chdir = /var/www/ai-tracks.com
home = /var/www/ai-tracks.com/venv
socket = /tmp/ai-tracks.sock
chmod-socket = 666

# Logging
logto = /var/log/uwsgi/ai-tracks.log
```

#### Step 3: Create Nginx Configuration

Create `/etc/nginx/sites-available/ai-tracks`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/ai-tracks.sock;
    }

    location /static {
        alias /var/www/ai-tracks.com/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /var/www/ai-tracks.com/uploads;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    client_max_body_size 20M;
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/ai-tracks /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Step 4: Create Systemd Service

Create `/etc/systemd/system/ai-tracks.service`:

```ini
[Unit]
Description=AI Tracks uWSGI Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai-tracks.com
Environment="PATH=/var/www/ai-tracks.com/venv/bin"
Environment="FLASK_ENV=production"
ExecStart=/var/www/ai-tracks.com/venv/bin/uwsgi --ini /var/www/ai-tracks.com/uwsgi.ini
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-tracks
sudo systemctl start ai-tracks
sudo systemctl status ai-tracks
```

### Option 2: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create upload directories
RUN mkdir -p uploads/cases uploads/news uploads/sliders

# Expose port
EXPOSE 8000

# Run with uWSGI
CMD ["uwsgi", "--ini", "uwsgi.ini", "--http", "0.0.0.0:8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
      - ./static:/app/static
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./static:/usr/share/nginx/html/static
      - ./uploads:/usr/share/nginx/html/uploads
    depends_on:
      - web
    restart: unless-stopped
```

Run with Docker:

```bash
docker-compose up -d
```

### Option 3: Platform as a Service (PaaS)

#### Heroku

1. Create `Procfile`:
```
web: uwsgi --http-socket :$PORT --master --workers 4 --threads 2 --module wsgi:app
```

2. Deploy:
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run flask db upgrade
```

#### Railway/Render

1. Connect your Git repository
2. Set environment variables
3. Deploy automatically on push

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is set up automatically
sudo certbot renew --dry-run
```

## Environment Variables

### Required Production Variables

```env
FLASK_ENV=production
SECRET_KEY=<strong-random-key>
DATABASE_URL=<database-connection-string>
```

### Optional Variables

```env
# File Upload
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Pagination
ITEMS_PER_PAGE=9

# Application
APP_NAME="AI Tracks"
APP_URL=https://yourdomain.com
```

## Database Configuration

### PostgreSQL (Recommended for Production)

```env
DATABASE_URL=postgresql://username:password@localhost/ai_tracks
```

Install PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

### MySQL

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/ai_tracks
```

Install MySQL adapter:
```bash
pip install PyMySQL
```

## Performance Optimization

### 1. Static File Serving

Let Nginx serve static files directly:

```nginx
location /static {
    alias /var/www/ai-tracks.com/static;
    expires 30d;
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
}
```

### 2. Image Optimization

Images are automatically converted to WebP format with 80% quality. Adjust in `app/services/image_service.py` if needed.

### 3. Database Connection Pooling

Update `app/config.py`:

```python
class ProductionConfig(Config):
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
```

### 4. Caching (Optional)

Install Flask-Caching:
```bash
pip install Flask-Caching
```

Configure in `app/__init__.py`:
```python
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

def create_app():
    app = Flask(__name__)
    cache.init_app(app)
    # ...
```

## Monitoring and Logging

### Application Logs

uWSGI logs to `/var/log/uwsgi/ai-tracks.log`

View logs:
```bash
tail -f /var/log/uwsgi/ai-tracks.log
```

### Nginx Logs

```bash
# Access logs
tail -f /var/log/nginx/access.log

# Error logs
tail -f /var/log/nginx/error.log
```

### System Service Status

```bash
sudo systemctl status ai-tracks
sudo journalctl -u ai-tracks -f
```

## Backup Strategy

### Database Backup

```bash
# SQLite
cp ai_tracks.db ai_tracks_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump -U username ai_tracks > backup_$(date +%Y%m%d).sql

# MySQL
mysqldump -u username -p ai_tracks > backup_$(date +%Y%m%d).sql
```

### Upload Files Backup

```bash
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/
```

### Automated Backup Script

Create `/usr/local/bin/backup-ai-tracks.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/ai-tracks"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
cp /var/www/ai-tracks.com/ai_tracks.db $BACKUP_DIR/db_$DATE.db

# Backup uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz -C /var/www/ai-tracks.com uploads/

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```

Add to crontab:
```bash
0 2 * * * /usr/local/bin/backup-ai-tracks.sh
```

## Troubleshooting

### Issue: Application won't start

Check logs:
```bash
sudo journalctl -u ai-tracks -n 50
```

Common causes:
- Wrong file permissions
- Missing environment variables
- Database connection issues

### Issue: 502 Bad Gateway

Check:
1. uWSGI is running: `sudo systemctl status ai-tracks`
2. Socket file exists: `ls -la /tmp/ai-tracks.sock`
3. Socket permissions: `chmod 666 /tmp/ai-tracks.sock`

### Issue: Static files not loading

Check Nginx configuration:
```bash
sudo nginx -t
```

Verify paths in Nginx config match your deployment.

### Issue: Image upload fails

Check:
1. Upload directory exists and is writable
2. `MAX_CONTENT_LENGTH` setting
3. Nginx `client_max_body_size` setting

## Security Checklist

- [ ] Set strong `SECRET_KEY` in production
- [ ] Use HTTPS (SSL/TLS)
- [ ] Set `FLASK_ENV=production`
- [ ] Configure firewall (UFW/iptables)
- [ ] Regular security updates
- [ ] Backup strategy in place
- [ ] File upload validation
- [ ] SQL injection protection (SQLAlchemy ORM)
- [ ] CSRF protection (Flask-WTF)
- [ ] Security headers configured

## Maintenance

### Update Application

```bash
cd /var/www/ai-tracks.com
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
sudo systemctl restart ai-tracks
```

### Monitor Disk Usage

```bash
df -h
du -sh uploads/
```

### Clean Old Uploads (if needed)

```bash
find uploads/ -type f -mtime +90 -delete
```

## Support

For issues and questions:
- Email: renfu.her@gmail.com
- Phone: 0922-013-171

