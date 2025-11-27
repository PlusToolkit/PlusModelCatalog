# PlusModelCatalog

This repository contains 3D printable models for the Plus Toolkit

## Documentation

View the documentation at: [Read the Docs](https://plusmodelcatalog.readthedocs.io/)

## Building Documentation Locally

### Prerequisites

```bash
pip install -r docs/requirements.txt
```

This installs:
- Sphinx and extensions
- VTK for STL rendering
- Supporting packages

### Generate and Build

```bash
# Generate catalog pages from STL files
cd docs
python generate_catalog.py --repo-root .. --docs-dir .

# Build HTML documentation
sphinx-build -b html . _build/html

# View documentation
start _build/html/index.html  # Windows
# or
open _build/html/index.html   # macOS
# or
xdg-open _build/html/index.html  # Linux
```

### Quick Build Script

On Windows:
```batch
cd docs
python generate_catalog.py --repo-root .. --docs-dir .
sphinx-build -b html . _build/html
start _build\html\index.html
```

## Adding New Models

1. Add STL file to appropriate directory (Tools, TrackingFixtures, etc.)
2. Commit to repository
3. Documentation automatically regenerates on next build

To add descriptions, edit the model info dictionaries in `generate_catalog.py`.

## Contributing

Contributions of new models are welcome! Please ensure:
- STL files are clean and printable
- Include source CAD files when possible
- Add appropriate descriptions in `generate_catalog.py`

## Migration from CMake

This repository previously used CMake + VTK + custom C++ tools. The new system:
- Uses Python + VTK instead of C++ + VTK
- Generates markdown instead of HTML directly
- Uses Sphinx for documentation generation
- Integrates with ReadTheDocs for hosting
- Maintains the same table format and download links

## Support

For questions about the Plus Toolkit, visit:
- Website: https://plustoolkit.github.io/
- GitHub: https://github.com/PlusToolkit/
