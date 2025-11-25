# PlusModelCatalog with Sphinx Documentation

This repository contains 3D printable models for the Plus Toolkit, now with Sphinx-based documentation.

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

## Features

The new documentation system provides:

✅ **Automatic STL Rendering** - Uses VTK to generate preview images  
✅ **Direct Download Links** - Links to STL files on GitHub  
✅ **Organized Catalog** - Models categorized by type  
✅ **Search Functionality** - Built-in search across all models  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **Version History** - Git commit dates for each model  
✅ **Source Links** - Links to original CAD files on GitHub  

## Repository Structure

```
PlusModelCatalog/
├── Tools/                  # Tracking tools and probes
├── TrackingFixtures/       # Mounts for trackers
├── fCalPhantom/           # Calibration phantoms
├── Anatomy/               # Anatomical models
├── UsNeedleTutor/         # Needle insertion trainer
└── docs/
    ├── conf.py            # Sphinx configuration
    ├── index.md           # Documentation home
    ├── requirements.txt   # Python dependencies
    ├── render_stl.py      # STL to PNG renderer
    ├── generate_catalog.py # Catalog page generator
    └── catalog/
        ├── index.md       # Catalog index
        ├── tools.md       # Auto-generated
        ├── tracking-fixtures.md
        ├── fcal-phantoms.md
        ├── anatomy.md
        └── needletutor.md
```

## How It Works

1. **STL Rendering**: `render_stl.py` uses VTK to render STL files to PNG images
2. **Catalog Generation**: `generate_catalog.py` scans directories, renders models, and creates markdown pages
3. **Sphinx Build**: Standard Sphinx build process generates HTML documentation
4. **ReadTheDocs**: `.readthedocs.yaml` configures automated builds on ReadTheDocs

## Adding New Models

1. Add STL file to appropriate directory (Tools, TrackingFixtures, etc.)
2. Commit to repository
3. Documentation automatically regenerates on next build

To add descriptions, edit the model info dictionaries in `generate_catalog.py`.

## License

See individual model files for licensing information.

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
