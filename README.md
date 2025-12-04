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

1. Add STL file to the appropriate directory (Tools, TrackingFixtures, etc.)
2. Edit the corresponding `catalog.json` file in that directory to add model metadata:
   - Add a description
   - Optionally specify explicit files if not auto-discovered
   - Optionally specify a custom preview image
3. Commit to repository
4. Documentation automatically regenerates on ReadTheDocs

### Example: Adding a New Tool

```json
// Edit Tools/catalog.json
{
  "models": {
    "MyNewTool": {
      "description": "Description of my new tool with its dimensions and purpose.",
      "files": ["MyNewTool.stl"]  // Optional if file matches model ID
    }
  }
}
```

## Contributing

Contributions of new models are welcome! Please ensure:
- STL files are clean and printable
- Include source CAD files when possible
- Add appropriate descriptions in the `catalog.json` file in the model's folder

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
