#!/bin/bash
# SmartView MCP Server Installation Script

set -e

echo "🚀 Installing Equinix SmartView MCP Server v2.0"
echo ""

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

echo "✅ Python detected"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Add your OAuth credentials to .env"
echo "3. Configure Claude Desktop (see README.md)"
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
