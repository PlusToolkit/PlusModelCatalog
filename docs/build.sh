#!/bin/bash
# Build PlusModelCatalog documentation

set -e

cd "$(dirname "$0")"

echo "Building PlusModelCatalog Documentation..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Generate catalog pages
echo ""
echo "Generating catalog pages from STL files..."
python generate_catalog.py --repo-root .. --docs-dir .

# Build documentation
echo ""
echo "Building Sphinx documentation..."
sphinx-build -b html . _build/html

echo ""
echo "========================================"
echo "Build completed successfully!"
echo "Documentation is in: _build/html"
echo "========================================"
echo ""

# Open in browser (platform-specific)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open _build/html/index.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open _build/html/index.html
fi

deactivate
