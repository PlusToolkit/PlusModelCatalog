#!/usr/bin/env python3
"""
Generate catalog markdown pages from STL model files
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional
import subprocess


class ModelCatalogGenerator:
    """Generate markdown documentation for 3D model catalog"""

    def __init__(self, repo_root: str, docs_dir: str, github_base_url: str):
        self.repo_root = Path(repo_root).resolve()
        self.docs_dir = Path(docs_dir).resolve()
        self.github_base_url = github_base_url
        self.rendered_dir = self.docs_dir / '_static' / 'rendered'
        self.rendered_dir.mkdir(parents=True, exist_ok=True)

    def get_git_last_modified(self, file_path: Path) -> str:
        """Get last git commit date for a file"""
        try:
            # Get relative path from repo root
            rel_path = file_path.relative_to(self.repo_root)
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%ad', '--date=short', '--', str(rel_path)],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception as e:
            print(f"Git error for {file_path}: {e}")
        return "Unknown"

    def render_stl(self, stl_path: Path, output_path: Path) -> bool:
        """Render STL file to PNG"""
        try:
            from render_stl import render_stl_to_image
            render_stl_to_image(str(stl_path), str(output_path), width=400, height=300)
            return True
        except Exception as e:
            print(f"Error rendering {stl_path}: {e}")
            return False

    def find_stl_files(self, directory: Path, recursive: bool = True,
                      include: List[str] = None, exclude: List[str] = None) -> List[Path]:
        """
        Find all STL files in directory with optional include/exclude filters

        Parameters:
        -----------
        directory : Path
            Directory to search
        recursive : bool
            Search subdirectories
        include : List[str]
            List of relative paths to include (if specified, only these are included)
        exclude : List[str]
            List of filenames to exclude

        Returns:
        --------
        List[Path]
            Sorted list of matching STL files
        """
        # Find both .stl and .STL files (case-insensitive)
        if recursive:
            all_files = sorted(list(directory.glob('**/*.stl')) + list(directory.glob('**/*.STL')))
        else:
            all_files = sorted(list(directory.glob('*.stl')) + list(directory.glob('*.STL')))

        # Remove duplicates (in case filesystem is case-insensitive)
        seen = set()
        unique_files = []
        for f in all_files:
            if f not in seen:
                seen.add(f)
                unique_files.append(f)
        all_files = unique_files

        # Apply include filter if specified
        if include:
            include_set = set(include)
            all_files = [f for f in all_files if f.name in include_set]

        # Apply exclude filter if specified
        if exclude:
            exclude_set = set(exclude)
            all_files = [f for f in all_files if f.name not in exclude_set]

        return all_files

    def generate_model_entry(self, stl_file: Path, description: str = "",
                            additional_files: List[Path] = None) -> Dict:
        """Generate catalog entry for a model"""
        rel_path = stl_file.relative_to(self.repo_root)
        model_id = stl_file.stem

        # Render image
        image_filename = f"{model_id}.png"
        image_path = self.rendered_dir / image_filename

        if not image_path.exists():
            print(f"Rendering {model_id}...")
            self.render_stl(stl_file, image_path)

        # Get git info
        last_modified = self.get_git_last_modified(stl_file)

        # Build download URLs
        download_files = [stl_file]
        if additional_files:
            download_files.extend(additional_files)

        downloads = []
        for f in download_files:
            rel_f = f.relative_to(self.repo_root)
            downloads.append({
                'filename': f.name,
                'url': f"{self.github_base_url}/blob/master/{rel_f}?raw=true",
                'last_modified': self.get_git_last_modified(f)
            })

        return {
            'id': model_id,
            'description': description,
            'image': f"/_static/rendered/{image_filename}",
            'downloads': downloads,
            'source_url': f"{self.github_base_url}/tree/master/{rel_path.parent}"
        }

    def generate_table_markdown(self, models: List[Dict], title: str,
                               description: str = "") -> str:
        """Generate markdown table for models"""
        md = f"# {title}\n\n"
        if description:
            md += f"{description}\n\n"

        md += "## Models\n\n"

        for model in models:
            md += f"### {model['id']}\n\n"

            # Image and description in columns
            md += "::::{grid} 1 1 2 2\n"
            md += ":gutter: 3\n\n"

            # Image column
            md += ":::{grid-item}\n"
            md += f"![{model['id']}]({model['image']})\n"
            md += ":::\n\n"

            # Info column
            md += ":::{grid-item}\n"
            if model['description']:
                md += f"{model['description']}\n\n"

            md += "**Downloads:**\n\n"
            for dl in model['downloads']:
                md += f"- [{dl['filename']}]({dl['url']}) "
                if dl['last_modified']:
                    md += f"*(Modified: {dl['last_modified']})*"
                md += "\n"

            md += f"\n[View source files on GitHub]({model['source_url']})\n"
            md += ":::\n\n"
            md += "::::\n\n"
            # Only add separator if not the last model
            if model != models[-1]:
                md += "---\n\n"

        return md

    def load_catalog_json(self, directory: Path) -> Dict:
        """
        Load catalog.json from a directory if it exists

        Returns:
        --------
        Dict with keys: 'title', 'description', 'models', 'exclude_files'
        """
        catalog_file = directory / 'catalog.json'
        if catalog_file.exists():
            try:
                with open(catalog_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        'title': data.get('title', ''),
                        'description': data.get('description', ''),
                        'models': data.get('models', {}),
                        'exclude_files': data.get('exclude_files', [])
                    }
            except Exception as e:
                print(f"Error loading {catalog_file}: {e}")
        return {'title': '', 'description': '', 'models': {}, 'exclude_files': []}

    def generate_catalog_page(self,
                              directory: Path,
                              title: str = None,
                              description: str = None,
                              output_filename: str = None,
                              model_definitions: Dict = None,
                              exclude_files: List[str] = None) -> None:
        """
        Generate a catalog page with model definitions

        Parameters:
        -----------
        directory : Path
            Primary directory to search for models
        title : str (optional)
            Page title (if None, reads from catalog.json)
        description : str (optional)
            Page description (if None, reads from catalog.json)
        output_filename : str
            Output markdown filename (e.g., 'tools.md')
        model_definitions : Dict (optional)
            Dictionary of model definitions (if None, reads from catalog.json)
            Format:
            {
                'model_id': {
                    'description': 'Model description',
                    'files': ['path/to/file.stl', 'path/to/other.stl', 'path/to/extra.rom', ...],  # Optional
                    'image': 'path/to/image.png',  # Optional: custom image
                }
            }
            If 'files' is not specified, the model_id is treated as a standalone model.
            If 'files' has multiple entries, they are grouped together.
            First .stl file in 'files' is used as primary for rendering; others are additional downloads.
        exclude_files : List[str] (optional)
            List of filenames to explicitly exclude from individual entries
            (if None, reads from catalog.json)
        """
        # Load from catalog.json if parameters not provided
        catalog_data = self.load_catalog_json(directory)

        if title is None:
            title = catalog_data['title'] or directory.name
        if description is None:
            description = catalog_data['description']
        if model_definitions is None:
            model_definitions = catalog_data['models']
        if exclude_files is None:
            exclude_files = catalog_data['exclude_files']

        # Default to empty dict/list if still None
        model_definitions = model_definitions or {}
        exclude_files = exclude_files or []
        models = []
        exclude_files = exclude_files or []

        # Track all files that are explicitly specified in model_definitions
        specified_files = set()
        for model_id, model_info in model_definitions.items():
            if 'files' in model_info:
                for f in model_info['files']:
                    filename = Path(f).name
                    specified_files.add(filename)
                    exclude_files.append(filename)

        # Add defined models (both single and grouped)
        for model_id, model_info in model_definitions.items():
            if 'files' in model_info:
                # Model with explicit file specification (single or grouped)
                # Resolve paths relative to the directory containing catalog.json
                file_paths = [(directory / f).resolve() for f in model_info['files']]

                # Find first STL file to use as primary
                primary_file = None
                additional_files = []
                for fp in file_paths:
                    if fp.suffix.lower() in ['.stl']:
                        if primary_file is None:
                            primary_file = fp
                        else:
                            additional_files.append(fp)
                    else:
                        # Non-STL files (like .rom) are always additional
                        additional_files.append(fp)

                if primary_file and primary_file.exists():
                    entry = self.generate_model_entry(
                        primary_file,
                        model_info['description'],
                        additional_files if additional_files else None
                    )

                    # Override image if custom one is specified
                    if 'image' in model_info:
                        # Resolve image path relative to the directory
                        image_file = (directory / model_info['image']).resolve()
                        if image_file.exists():
                            import shutil
                            dest_image = self.rendered_dir / f"{model_id}.png"
                            shutil.copy(image_file, dest_image)
                            entry['image'] = f"/_static/rendered/{model_id}.png"

                    entry['id'] = model_id
                    models.append(entry)

        # Add individual models from directory that weren't explicitly specified
        for stl_file in self.find_stl_files(directory, recursive=True, exclude=exclude_files):
            if stl_file.name not in specified_files:
                model_id = stl_file.stem
                # Check if this model has a description without explicit files
                if model_id in model_definitions and 'files' not in model_definitions[model_id]:
                    desc = model_definitions[model_id].get('description', "")
                else:
                    desc = ""
                models.append(self.generate_model_entry(stl_file, desc))

        # Generate and write markdown
        markdown = self.generate_table_markdown(models, title, description)
        output_file = self.docs_dir / 'catalog' / output_filename
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(markdown)
        print(f"Generated {output_file}")

    def generate_tools_page(self):
        """Generate tools catalog page"""
        self.generate_catalog_page(
            directory=self.repo_root / 'Tools',
            output_filename='tools.md'
        )

    def generate_tracking_fixtures_page(self):
        """Generate tracking fixtures catalog page"""
        self.generate_catalog_page(
            directory=self.repo_root / 'TrackingFixtures',
            output_filename='tracking-fixtures.md'
        )

    def generate_fcal_phantoms_page(self):
        """Generate fCal phantoms catalog page"""
        self.generate_catalog_page(
            directory=self.repo_root / 'fCalPhantom',
            output_filename='fcal-phantoms.md'
        )

    def generate_anatomy_page(self):
        """Generate anatomy models catalog page"""
        self.generate_catalog_page(
            directory=self.repo_root / 'Anatomy',
            output_filename='anatomy.md'
        )

    def generate_needletutor_page(self):
        """Generate needle tutor catalog page"""
        self.generate_catalog_page(
            directory=self.repo_root / 'UsNeedleTutor',
            output_filename='needletutor.md'
        )

    def generate_index_page(self):
        """Generate catalog index page"""

        # Build toctree entries
        toctree_entries = [
            "tools",
            "tracking-fixtures",
            "fcal-phantoms",
            "anatomy",
            "needletutor"
        ]

        # Build catalog descriptions
        catalog_items = [
            "- **Tools**: Tracking styluses, ultrasound probe models, surgical instruments",
            "- **Tracking Fixtures**: Mounts and clips for attaching tracking markers",
            "- **fCal Phantoms**: Calibration phantoms for ultrasound systems",
            "- **Anatomy Models**: Anatomical models for training and simulation",
            "- **Needle Tutor**: Components for needle insertion training"
        ]

        toctree = "\n".join(toctree_entries)
        catalog_list = "\n".join(catalog_items)

        markdown = f"""# Model Catalog

Browse the 3D printable models organized by category:

```{{toctree}}
:maxdepth: 1

{toctree}
```

## About the Catalog

This catalog contains 3D printable models (STL files) for:

{catalog_list}

## Using the Models

All STL files can be downloaded directly and used with 3D printers. Click on any model to see:

- Rendered preview image
- Direct download link
- Last modification date
- Link to source files on GitHub

## Repository

All models are maintained in the [PlusToolkit/PlusModelCatalog](https://github.com/PlusToolkit/PlusModelCatalog) repository.
"""
        output_file = self.docs_dir / 'catalog' / 'index.md'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(markdown)
        print(f"Generated {output_file}")

    def generate_all(self):
        """Generate all catalog pages"""
        print("Generating model catalog documentation...")

        # Generate category pages and track which ones exist
        self.generate_tools_page()
        self.generate_tracking_fixtures_page()
        self.generate_fcal_phantoms_page()
        self.generate_anatomy_page()
        self.generate_needletutor_page()
        print("Done!")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate model catalog documentation')
    parser.add_argument('--repo-root', default='..',
                       help='Root directory of PlusModelCatalog repository')
    parser.add_argument('--docs-dir', default='.',
                       help='Documentation directory')
    parser.add_argument('--github-url',
                       default='https://github.com/PlusToolkit/PlusModelCatalog',
                       help='GitHub repository base URL')

    args = parser.parse_args()

    generator = ModelCatalogGenerator(
        args.repo_root,
        args.docs_dir,
        args.github_url
    )
    generator.generate_all()


if __name__ == '__main__':
    main()
