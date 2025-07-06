#!/bin/bash

# Setup script for D&D SRD PDF to Markdown Converter
echo "🏗️  Setting up D&D SRD PDF to Markdown Converter..."

# Check if config.py exists
if [ ! -f "config.py" ]; then
    echo "📄 Creating config.py from example..."
    cp config.example.py config.py
    echo "✅ Created config.py"
else
    echo "✅ config.py already exists"
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source .venv/bin/activate
pip install -r requirements.txt

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.py and set your OpenAI API key:"
echo "   OPENAI_API_KEY = \"sk-your-api-key-here\""
echo ""
echo "2. Make sure your PDF file is in this directory"
echo ""
echo "3. Run the converter:"
echo "   python srd_processor.py"
echo ""
echo "Or set the API key as an environment variable:"
echo "   export OPENAI_API_KEY=\"sk-your-api-key-here\""
echo "   python srd_processor.py"
