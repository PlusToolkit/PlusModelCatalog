# Quick Start Guide

## For Users: Browsing the Catalog

Visit the documentation at: **[ReadTheDocs URL]** (after setup)

Browse models by category, view rendered previews, and download STL files directly.

## For Contributors: Adding Models

### 1. Add Your STL File

Place your STL file in the appropriate directory:
- `Tools/` - Tracking tools, probes, instruments
- `TrackingFixtures/` - Tracker mounts and fixtures
- `fCalPhantom/` - Calibration phantoms
- `Anatomy/` - Anatomical models
- `UsNeedleTutor/` - Needle insertion trainer components

### 2. Add Description (Optional)

Edit `docs/generate_catalog.py` and add an entry to the appropriate `*_info` dictionary:

```python
tool_info = {
    'YourModelName': "Description of your model here.",
    # ... existing entries ...
}
```

### 3. Commit and Push

```bash
git add .
git commit -m "Add new model: YourModelName"
git push
```

The documentation will automatically rebuild on ReadTheDocs.

## For Developers: Local Development

### First Time Setup

```bash
# Navigate to docs directory
cd docs

# Install Python dependencies
pip install -r requirements.txt
```

### Building Locally

#### Windows
```batch
cd docs
build.bat
```

#### Linux/Mac
```bash
cd docs
chmod +x build.sh
./build.sh
```

Or manually:
```bash
cd docs
python generate_catalog.py --repo-root .. --docs-dir .
sphinx-build -b html . _build/html
```

### Rendering Individual STL Files

```bash
# Single file
python render_stl.py path/to/model.stl output.png

# Batch process directory
python render_stl.py --batch path/to/stls/ output_dir/

# Custom image size
python render_stl.py model.stl output.png --width 800 --height 600
```

## Repository Structure

```
PlusModelCatalog/
├── .github/workflows/      # GitHub Actions
│   └── docs.yml           # Documentation build workflow
├── docs/                  # Documentation source
│   ├── conf.py           # Sphinx configuration
│   ├── index.md          # Documentation home
│   ├── requirements.txt  # Python dependencies
│   ├── render_stl.py     # STL renderer
│   ├── generate_catalog.py # Catalog generator
│   ├── build.bat / build.sh # Build scripts
│   ├── _static/
│   │   └── css/custom.css
│   └── catalog/          # Auto-generated pages
│       ├── index.md
│       ├── tools.md
│       ├── tracking-fixtures.md
│       ├── fcal-phantoms.md
│       ├── anatomy.md
│       └── needletutor.md
├── Tools/                # STL files for tools
├── TrackingFixtures/     # STL files for fixtures
├── fCalPhantom/         # STL files for phantoms
├── Anatomy/             # STL files for anatomy
├── UsNeedleTutor/       # STL files for needle tutor
├── .readthedocs.yaml    # ReadTheDocs configuration
└── README.md            # Main readme
```

## ReadTheDocs Setup

1. Import project at readthedocs.org
2. Connect to GitHub repository
3. Build will run automatically using `.readthedocs.yaml`
4. Documentation will be available at `[project-name].readthedocs.io`

## Troubleshooting

### VTK rendering fails
- Ensure VTK is installed: `pip install vtk`
- Check that STL files are valid
- Try rendering manually: `python render_stl.py model.stl test.png`

### Missing images in documentation
- Run `python generate_catalog.py` to regenerate
- Check `_static/rendered/` directory for PNG files
- Ensure STL files exist in expected locations

### Build fails on ReadTheDocs
- Check `.readthedocs.yaml` configuration
- Verify `requirements.txt` includes all dependencies
- Check build logs on ReadTheDocs dashboard

## Dependencies

- **Python 3.11+**
- **Sphinx 7.0+** - Documentation generator
- **VTK 9.0+** - 3D rendering
- **Pillow** - Image processing
- **NumPy** - Numerical computations

All installed via `pip install -r docs/requirements.txt`

## Support

- Plus Toolkit: https://plustoolkit.github.io/
- GitHub Issues: https://github.com/PlusToolkit/PlusModelCatalog/issues
