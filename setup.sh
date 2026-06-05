#!/bin/bash
# BOKHARY - Setup Script
# هذا السكريبت يقوم بإعداد المشروع بشكل سريع

echo "🛡️ BOKHARY - Security Setup Script"
echo "===================================="
echo ""

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed! Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found: $(python --version)"
echo ""

# Go to backend directory
cd backend || exit

# Create virtual environment (optional but recommended)
echo "📦 Creating virtual environment..."
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
echo "✅ Virtual environment created"
echo ""

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env file
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp env.example .env
    
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your settings:"
    echo ""
    echo "   nano .env  (or use your favorite editor)"
    echo ""
    echo "   Required fields:"
    echo "   - ADMIN_API_KEY (generate with: python -c \"import secrets; print(secrets.token_urlsafe(32))\")"
    echo "   - OWNER_EMAIL (your actual email)"
    echo "   - GMAIL_USER (your gmail)"
    echo "   - GMAIL_APP_PASSWORD (from myaccount.google.com/apppasswords)"
    echo ""
else
    echo "✅ .env file already exists (skipped)"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your actual values"
echo "2. Run: python -m uvicorn main:app --reload"
echo "3. Open: http://localhost:8000"
echo ""
