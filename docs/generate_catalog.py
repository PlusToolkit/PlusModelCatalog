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
    
    def find_stl_files(self, directory: Path, recursive: bool = True) -> List[Path]:
        """Find all STL files in directory"""
        if recursive:
            return sorted(directory.glob('**/*.stl'))
        return sorted(directory.glob('*.stl'))
    
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
    
    def generate_tools_page(self):
        """Generate tools catalog page"""
        tools_dir = self.repo_root / 'Tools'
        models = []
        
        # Define tools with descriptions
        tool_info = {
            'Scalpel': "Generic scalpel (100mm long handle, 20mm long blade).",
            'Cautery': "Generic cautery (95mm long handle, 20mm long blade).",
            'Needle_BardDuaLok57': "Bard DuaLok57 double-hook needle (without hooks).",
            'Stylus_100mm': "Pointer tool with built-in sensor holder. 100mm long, sharp tip.",
            'Stylus_Candycane_100mm_WithHolder': "Pointer tool with built-in sensor holder. 100mm long, curved tip for ultrasound calibration.",
            'Stylus_Candycane_70mm_1.0': "Pointer tool with built-in sensor holder. 70mm long, curved tip for ultrasound calibration.",
            'UsProbe_SPL40': "Mock linear ultrasound probe (width: 40mm)",
            'UsProbe_Ultrasonix_L14-5_38': "Ultrasonix L14-5/38 linear ultrasound probe.",
            'UsProbe_Ultrasonix_C5-2_60': "Ultrasonix C5-2/60 curvilinear ultrasound probe.",
            'UsProbe_Ultrasonix_EC9-5_10': "Ultrasonix EC9-5/10 endocavity curvilinear ultrasound probe.",
            'UsProbe_Telemed_L12': "Telemed L12 linear ultrasound probe.",
        }
        
        for stl_file in self.find_stl_files(tools_dir, recursive=True):
            model_id = stl_file.stem
            description = tool_info.get(model_id, "")
            models.append(self.generate_model_entry(stl_file, description))
        
        markdown = self.generate_table_markdown(
            models,
            "Tools",
            "Tracking tools, ultrasound probes, and surgical instruments for image-guided interventions."
        )
        
        output_file = self.docs_dir / 'catalog' / 'tools.md'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(markdown)
        print(f"Generated {output_file}")
    
    def generate_tracking_fixtures_page(self):
        """Generate tracking fixtures catalog page"""
        fixtures_dir = self.repo_root / 'TrackingFixtures'
        models = []
        
        fixture_info = {
            'Block4x4-ThreeHoles': "Block of solid material 40x40x14 mm size, with an extruded interface with three M4 holes 7 mm apart.",
            'CauteryGrabber': "Fixture for attaching tracker to cautery. Use hex-head cap screw M6 thread, 30mm long with wing nut.",
            'SensorHolder_Wing_1.0': "Clip to mount MarkerHolder or 8mm Ascension EM sensor. With wing for easy attachment.",
            'Stylus_Polaris': "Optical marker with slots for NDI Polaris pegs and reflective spheres.",
            'Ultrasound_Polaris': "Optical marker with slots for NDI Polaris pegs and reflective spheres.",
            'ArmL-30': "Connector between ultrasound clip and Polaris markers.",
            'NeedleClip-Assembly_16-20G': "Clamps to needle size 16-20 G through sterile bag.",
        }
        
        for stl_file in self.find_stl_files(fixtures_dir, recursive=True):
            model_id = stl_file.stem
            description = fixture_info.get(model_id, "")
            models.append(self.generate_model_entry(stl_file, description))
        
        markdown = self.generate_table_markdown(
            models,
            "Tracking Fixtures",
            "Fixtures for mounting tracker markers (optical and electromagnetic) on tools and objects."
        )
        
        output_file = self.docs_dir / 'catalog' / 'tracking-fixtures.md'
        output_file.write_text(markdown)
        print(f"Generated {output_file}")
    
    def generate_fcal_phantoms_page(self):
        """Generate fCal phantoms catalog page"""
        fcal_dir = self.repo_root / 'fCalPhantom'
        models = []
        
        for stl_file in self.find_stl_files(fcal_dir, recursive=True):
            models.append(self.generate_model_entry(
                stl_file,
                f"fCal phantom component: {stl_file.stem}"
            ))
        
        markdown = self.generate_table_markdown(
            models,
            "fCal Calibration Phantoms",
            "Calibration phantoms for ultrasound probe calibration and validation."
        )
        
        output_file = self.docs_dir / 'catalog' / 'fcal-phantoms.md'
        output_file.write_text(markdown)
        print(f"Generated {output_file}")
    
    def generate_anatomy_page(self):
        """Generate anatomy models catalog page"""
        anatomy_dir = self.repo_root / 'Anatomy'
        models = []
        
        for stl_file in self.find_stl_files(anatomy_dir, recursive=True):
            models.append(self.generate_model_entry(
                stl_file,
                f"Anatomical model: {stl_file.stem}"
            ))
        
        markdown = self.generate_table_markdown(
            models,
            "Anatomy Models",
            "Anatomical models for simulation and training."
        )
        
        output_file = self.docs_dir / 'catalog' / 'anatomy.md'
        output_file.write_text(markdown)
        print(f"Generated {output_file}")
    
    def generate_needletutor_page(self):
        """Generate needle tutor catalog page"""
        needletutor_dir = self.repo_root / 'UsNeedleTutor'
        models = []
        
        for stl_file in self.find_stl_files(needletutor_dir, recursive=True):
            models.append(self.generate_model_entry(
                stl_file,
                f"Needle tutor component: {stl_file.stem}"
            ))
        
        markdown = self.generate_table_markdown(
            models,
            "Needle Tutor Components",
            "Components for ultrasound-guided needle insertion training system."
        )
        
        output_file = self.docs_dir / 'catalog' / 'needletutor.md'
        output_file.write_text(markdown)
        print(f"Generated {output_file}")
    
    def generate_index_page(self):
        """Generate catalog index page"""
        markdown = """# Model Catalog

Browse the 3D printable models organized by category:

```{toctree}
:maxdepth: 1

tools
tracking-fixtures
fcal-phantoms
anatomy
needletutor
```

## About the Catalog

This catalog contains 3D printable models (STL files) for:

- **Tools**: Tracking styluses, ultrasound probe models, surgical instruments
- **Tracking Fixtures**: Mounts and clips for attaching tracking markers
- **fCal Phantoms**: Calibration phantoms for ultrasound systems
- **Anatomy Models**: Anatomical models for training and simulation
- **Needle Tutor**: Components for needle insertion training

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
        self.generate_index_page()
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
