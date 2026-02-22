#!/bin/bash

# 🌿 Plant Health Guardian - Quick Start Script

echo "🌿 Plant Health Guardian"
echo "========================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # macOS/Linux
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

# Check if model files exist
if [ ! -f "models/best_model.pth" ]; then
    echo "⚠️  WARNING: models/best_model.pth not found!"
    echo "   Please download it from Colab and place in models/ folder"
    echo ""
fi

if [ ! -f "data/label_mapping.json" ]; then
    echo "⚠️  WARNING: data/label_mapping.json not found!"
    echo "   Please download it from Colab and place in data/ folder"
    echo ""
fi

# Run the app
echo ""
echo "🚀 Starting Streamlit app..."
echo "🌐 Open browser at: http://localhost:8501"
echo ""
streamlit run app.py
