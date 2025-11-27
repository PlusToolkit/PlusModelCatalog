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
        self.repo_root = Path(repo_root)
        self.docs_dir = Path(docs_dir)
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

    def generate_catalog_page(self,
                              directory: Path,
                              title: str,
                              description: str,
                              output_filename: str,
                              model_definitions: Dict = {},
                              exclude_files: List[str] = None) -> None:
        """
        Generate a catalog page with model definitions

        Parameters:
        -----------
        directory : Path
            Primary directory to search for models
        model_definitions : Dict
            Dictionary of model definitions with format:
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
        title : str
            Page title
        description : str
            Page description
        output_filename : str
            Output markdown filename (e.g., 'tools.md')
        exclude_files : List[str]
            List of filenames to explicitly exclude from individual entries
        """
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
                # First STL file becomes the primary (for image rendering)
                file_paths = [self.repo_root / f for f in model_info['files']]

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
                        image_file = self.repo_root / model_info['image']
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
        model_definitions = {
            'Scalpel': {
                'description': "Generic scalpel (100mm long handle, 20mm long blade)."
            },
            'Cautery': {
                'description': "Generic cautery (95mm long handle, 20mm long blade)."
            },
            'Needle_BardDuaLok57': {
                'description': "Bard DuaLok57 double-hook needle (without hooks)."
            },
            'Stylus_100mm': {
                'description': "Pointer tool with built-in sensor holder. 100mm long, sharp tip.",
                'files': ['TrackingFixtures/Stylus_100mm.stl']
            },
            'Stylus_60mm': {
                'description': "Pointer tool with built-in sensor holder. 60mm long, sharp tip.",
                'files': ['TrackingFixtures/Stylus_60mm.stl']
            },
            'Stylus_Candycane_100mm_WithHolder': {
                'description': "Pointer tool with built-in sensor holder. 100mm long, curved tip for ultrasound calibration.",
                'files': ['TrackingFixtures/Stylus_Candycane_100mm_WithHolder.stl']
            },
            'Stylus_Candycane_70mm_1.0': {
                'description': "Pointer tool with built-in sensor holder. 70mm long, curved tip for ultrasound calibration.",
                'files': ['TrackingFixtures/Stylus_Candycane_70mm_1.0.stl']
            },
            'UsProbe_SPL40': {
                'description': "Mock linear ultrasound probe (width: 40mm)"
            },
            'UsProbe_Ultrasonix_L14-5_38': {
                'description': "Ultrasonix L14-5/38 linear ultrasound probe."
            },
            'UsProbe_Ultrasonix_C5-2_60': {
                'description': "Ultrasonix C5-2/60 curvilinear ultrasound probe."
            },
            'UsProbe_Ultrasonix_EC9-5_10': {
                'description': "Ultrasonix EC9-5/10 endocavity curvilinear ultrasound probe."
            },
            'UsProbe_Telemed_L12': {
                'description': "Telemed L12 linear ultrasound probe."
            },
        }

        self.generate_catalog_page(
            directory=self.repo_root / 'Tools',
            model_definitions=model_definitions,
            title="Tools",
            description="Tracking tools, ultrasound probes, and surgical instruments for image-guided interventions.",
            output_filename='tools.md'
        )

    def generate_tracking_fixtures_page(self):
        """Generate tracking fixtures catalog page"""
        model_definitions = {
            'Block4x4-ThreeHoles': {
                'description': "Block of solid material 40x40x14 mm size, with an extruded interface with three M4 holes 7 mm apart. The block can be edited to cut out an anatomical part, so the final product will interface with an anatomy."
            },
            'CauteryGrabber': {
                'description': "New version for fixing a tracker to a cautery. For clamp tightening use hex-head cap screw, M6 thread, 30 mm long with a matching wing nut. For assembly with SensorHolder-OneHole use M4 bolt."
            },
            'SensorHolder_Wing_1.0': {
                'description': "Clip to mount a MarkerHolder or 8mm Ascension EM sensor to an object. With a wing to make it easier to fix it by glue or screws."
            },
            'Stylus_Polaris': {
                'description': "Optical marker with slots to insert NDI Polaris pegs to hold reflective spheres. To fix the NDI pegs for spheres, order this product from DigiKey: Round Standoff Threaded #4-40 Steel 0.063'' (1.60mm) 1/16''. DigiKey part number: 36-4881CT-ND",
                'files': ['TrackingFixtures/StealthStation/Stylus_Polaris.STL']
            },
            'Ultrasound_Polaris': {
                'description': "Optical marker with slots to insert NDI Polaris pegs to hold reflective spheres. To fix the NDI pegs for spheres, order this product from DigiKey: Round Standoff Threaded #4-40 Steel 0.063'' (1.60mm) 1/16''. DigiKey part number: 36-4881CT-ND",
                'files': ['TrackingFixtures/StealthStation/Ultrasound_Polaris.STL']
            },
            'ArmL-30': {
                'description': "Connector between e.g. an ultrasound clip and polaris markers.",
                'files': ['TrackingFixtures/ArmL-30.STL']
            },
            'NeedleClip-Assembly_16-20G': {
                'description': "Clamps to a needle of size 16-20 G through a sterile bag."
            },
            'SensorHolder_2.0': {
                'description': "New sensor holder design. This will replace SensorHolder-Ordered_2mm_1.0 eventually. Holds either a Model 800 Ascension EM sensor, or another PLUS fixture, e.g. for holding MicronTracker markers. This part is frequently part of an assembly, but can also be used by itself."
            },
            'SensorHolder-OneHole': {
                'description': "Holds a Model 800 sensor, and has a hole to fix to other printed components."
            },
            'OrientationLR-Plane': {
                'description': "This is the most simple reference sensor holder to be used on patients. In a certain surgical setting (e.g. when stuck on the chest) this defines the patient orientation. This allows saving virtual camera positions."
            },
            'Telemed-MicrUs-L12-SensorHolder': {
                'description': 'Parts for tracking Telemed MicrUs L12 ultrasound probe',
                'files': [
                    'TrackingFixtures/Telemed-MicrUs-L12-SensorHolder.stl',
                    'TrackingFixtures/TelemedHolder_L12_MarkedSide.stl',
                    'TrackingFixtures/TelemedHolder-L12_UnmarkedSide.stl'
                ]
            },
            'Telemed-L12-ClipOn': {
                'description': 'A plastic holder for the Telemed L12 ultrasound probe, without moving parts.',
                'files': ['TrackingFixtures/Telemed-MicruUs-L12/Telemed-L12-ClipOn.STL']
            },
            'GeMl615D_Clip_v01': {
                'description': 'Clip-on part for GE ML6-15-D ultrasound probe.',
                'files': ['TrackingFixtures/GE_ML6-15-D/GeMl615D_Clip_v01.STL'],
                'image': 'TrackingFixtures/GE_ML6-15-D/GeMl615D_Clip_v01.png'
            },
            'PolarisAscensionPlane': {
                'description': 'Part that can be tracked by both Polaris and Ascension trackers',
                'files': [
                    'TrackingFixtures/MultiModalityTracking/PolarisAscensionPlane.STL',
                    'TrackingFixtures/MultiModalityTracking/PolarisAscensionPlane.rom'
                ],
            }
        }

        # Exclude stylus files that are in Tools category
        exclude_files = [
            'Stylus_100mm.stl',
            'Stylus_60mm.stl',
            'Stylus_Candycane_100mm_WithHolder.stl',
            'Stylus_Candycane_70mm_1.0.stl',
        ]

        self.generate_catalog_page(
            directory=self.repo_root / 'TrackingFixtures',
            model_definitions=model_definitions,
            title="Tracking Fixtures",
            description="Fixtures for mounting tracker markers (optical and electromagnetic) on tools and objects.",
            output_filename='tracking-fixtures.md',
            exclude_files=exclude_files
        )

    def generate_fcal_phantoms_page(self):
        """Generate fCal phantoms catalog page"""
        model_definitions = {
            'fCal-2.0': {
                'description': 'Phantom for freehand spatial ultrasound calibration for shallow depth (up to 9 cm).',
                'files': ['fCalPhantom/fCal_2/fCal_2.0.stl'],
                'image': 'fCalPhantom/fCal_2/PhantomDefinition_fCal_2.0_Wiring_2.0.png'
            },
            'fCal-2.1': {
                'description': 'Phantom for freehand spatial ultrasound calibration for shallow depth (up to 9 cm).',
                'files': ['fCalPhantom/fCal_2/fCal_2.1.stl']
            },
            'fCal-3.1': {
                'description': 'Phantom for freehand spatial ultrasound calibration for deep structures (up to 30 cm).',
                'files': [
                    'fCalPhantom/fCal_3/fCal_3.1.stl',
                    'fCalPhantom/fCal_3/fCal_3.1_back.stl',
                    'fCalPhantom/fCal_3/fCal_3.1_front.stl',
                    'fCalPhantom/fCal_3/fCal_3.1_left.stl',
                    'fCalPhantom/fCal_3/fCal_3.1_spacer.stl'
                ],
                'image': 'fCalPhantom/fCal_3/fCal3.1.png'
            },
            'fCal_Echo1.0': {
                'description': 'Phantom for freehand spatial ultrasound calibration of tube-shaped echo probes such as intracardiac echo (ICE) catheters and transesophageal echo (TEE) probes. Developed by Robert Kreher ([Otto-von-Guericke-University Magdeburg, Germany](https://www.ovgu.de/), [Stimulate Research Campus](https://www.forschungscampus-stimulate.de/)).',
                'files': ['fCalPhantom/fCal_Echo/fCal_Echo1.0.stl'],
                'image': 'fCalPhantom/fCal_Echo/fCal_Echo1.0.png'
            }
        }

        self.generate_catalog_page(
            directory=self.repo_root / 'fCalPhantom',
            model_definitions=model_definitions,
            title="fCal Calibration Phantoms",
            description="Calibration phantoms for ultrasound probe calibration and validation.",
            output_filename='fcal-phantoms.md'
        )

    def generate_anatomy_page(self):
        """Generate anatomy models catalog page"""
        model_definitions = {
            'HumanSimple': {
                'description': 'Simple low-polygon human body model.'
            },
            'LumbarSpinePhantom': {
                'description': 'Printable 3D model of the lumbar spine with matching CT image. Note that lowest vertebra is moved in the printable model compared to CT.',
                'files': [
                    'Anatomy/LumbarSpinePhantom.stl',
                    'Anatomy/LumbarSpinePhantom_CT.mha'
                ]
            }
        }
        self.generate_catalog_page(
            directory=self.repo_root / 'Anatomy',
            model_definitions=model_definitions,
            title="Anatomy Models",
            description="Anatomical models for simulation and training.",
            output_filename='anatomy.md'
        )

    def generate_needletutor_page(self):
        """Generate needle tutor catalog page"""
        self.generate_catalog_page(
            directory=self.repo_root / 'UsNeedleTutor',
            model_definitions={},
            title="Needle Tutor Components",
            description="Components for ultrasound-guided needle insertion training system.",
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
