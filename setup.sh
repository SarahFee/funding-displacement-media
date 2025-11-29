#!/bin/bash
# Setup script for Humanitarian Funding Analysis

echo "=========================================="
echo "Humanitarian Funding Analysis - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create directory structure
echo ""
echo "Creating directory structure..."
mkdir -p data/{raw/{fts,dtm,gdelt},processed,outputs}
mkdir -p logs

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the analysis:"
echo "  python src/main.py"
echo ""
echo "To generate documentation:"
echo "  quarto render docs/"
echo ""
