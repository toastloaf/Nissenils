#!/bin/bash
# Setup script for Real-time Object Roleplay AI

echo "🎭 Setting up Real-time Object Roleplay AI"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"
echo ""

# Create virtual environment (optional)
read -p "Create virtual environment? (recommended) [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
echo "This may take several minutes..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ All dependencies installed successfully"
echo ""

# Check for GPU
echo "Checking for CUDA GPU..."
python3 -c "import torch; print('✓ CUDA available:', torch.cuda.is_available())"
echo ""

# Download models (they will be cached)
echo "Note: Models will be downloaded on first run (~500MB-1GB)"
echo ""

echo "=========================================="
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  python3 object_roleplay.py"
echo ""
echo "Or if using virtual environment:"
echo "  source venv/bin/activate"
echo "  python3 object_roleplay.py"
echo "=========================================="
