#!/bin/bash

# Setup script for AI Tracks Flask Application

echo "======================================"
echo "AI Tracks - Flask Setup Script"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3.12 --version 2>/dev/null || python3 --version 2>/dev/null || python --version 2>/dev/null)
echo "Found: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment with Python 3.12..."
    # Try python3.12 first, fallback to python3 or python
    if command -v python3.12 &> /dev/null; then
        python3.12 -m venv venv
    elif command -v python3 &> /dev/null; then
        python3 -m venv venv
    else
        python -m venv venv
    fi
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    
    # Generate a random secret key
    SECRET_KEY=$(python3.12 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || python -c "import secrets; print(secrets.token_hex(32))")
    
    # Update secret key in .env
    sed -i "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
    
    echo "✓ .env file created with random SECRET_KEY"
    echo "  Please review and update .env file with your configuration"
else
    echo "✓ .env file already exists"
fi

# Create upload directories
echo ""
echo "Creating upload directories..."
mkdir -p uploads/cases uploads/news uploads/sliders
echo "✓ Upload directories created"

# Initialize database
echo ""
echo "Initializing database..."

if [ ! -d "migrations" ]; then
    echo "  Initializing Flask-Migrate..."
    flask db init
fi

echo "  Creating migration..."
flask db migrate -m "Initial migration"

echo "  Applying migration..."
flask db upgrade

echo "✓ Database initialized"

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To run the development server:"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "To run with uWSGI (production):"
echo "  1. Update uwsgi.ini with your paths"
echo "  2. uwsgi --ini uwsgi.ini"
echo ""
echo "The application will be available at:"
echo "  http://localhost:5000"
echo ""

