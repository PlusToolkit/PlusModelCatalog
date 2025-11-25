#!/usr/bin/env python3
"""
STL Model Renderer using VTK
Renders STL files to PNG images for documentation
"""

import vtk
import sys
import os
import argparse
from pathlib import Path


def render_stl_to_image(stl_file, output_image, width=400, height=300,
                        camera_position=None, camera_focal_point=None,
                        camera_view_up=None):
    """
    Render an STL file to a PNG image using VTK.

    Parameters:
    -----------
    stl_file : str
        Path to input STL file
    output_image : str
        Path to output PNG file
    width : int
        Image width in pixels
    height : int
        Image height in pixels
    camera_position : tuple
        Camera position (x, y, z). If None, automatically computed.
    camera_focal_point : tuple
        Camera focal point (x, y, z). If None, uses model center.
    camera_view_up : tuple
        Camera up vector (x, y, z)
    """

    # Read STL file
    reader = vtk.vtkSTLReader()
    reader.SetFileName(stl_file)
    reader.Update()

    # Create mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Set actor properties for better visualization
    actor.GetProperty().SetColor(0.8, 0.8, 0.9)  # Light blue-gray
    actor.GetProperty().SetSpecular(0.3)
    actor.GetProperty().SetSpecularPower(20)
    actor.GetProperty().SetAmbient(0.2)
    actor.GetProperty().SetDiffuse(0.8)

    # Create renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1.0, 1.0, 1.0)  # White background (will be made transparent)

    # Create render window
    render_window = vtk.vtkRenderWindow()
    render_window.SetOffScreenRendering(1)
    render_window.AddRenderer(renderer)
    render_window.SetSize(width, height)
    render_window.SetAlphaBitPlanes(1)  # Enable alpha channel

    # Setup camera
    camera = renderer.GetActiveCamera()
    camera.ParallelProjectionOn()
    camera.Roll(0)
    camera.Pitch(-20)
    camera.Yaw(-20)
    renderer.ResetCamera()
    camera.Zoom(1.0)


    renderer.ResetCameraClippingRange()

    # Render
    render_window.Render()

    # Save to image
    window_to_image = vtk.vtkWindowToImageFilter()
    window_to_image.SetInput(render_window)
    window_to_image.SetScale(1)
    window_to_image.SetInputBufferTypeToRGBA()  # Include alpha channel
    window_to_image.ReadFrontBufferOff()
    window_to_image.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetFileName(output_image)
    writer.SetInputConnection(window_to_image.GetOutputPort())
    writer.Write()

    print(f"Rendered {stl_file} -> {output_image}")


def batch_render_stls(input_dir, output_dir, file_pattern="*.stl", **render_kwargs):
    """
    Batch render all STL files in a directory.

    Parameters:
    -----------
    input_dir : str
        Directory containing STL files
    output_dir : str
        Directory for output PNG files
    file_pattern : str
        Glob pattern for STL files
    **render_kwargs : dict
        Additional arguments passed to render_stl_to_image
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    stl_files = list(input_path.glob(file_pattern))

    if not stl_files:
        print(f"No STL files found matching {file_pattern} in {input_dir}")
        return

    print(f"Found {len(stl_files)} STL files to render")

    for stl_file in stl_files:
        output_file = output_path / f"{stl_file.stem}.png"
        try:
            render_stl_to_image(str(stl_file), str(output_file), **render_kwargs)
        except Exception as e:
            print(f"Error rendering {stl_file}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Render STL files to PNG images using VTK')
    parser.add_argument('input', help='Input STL file or directory')
    parser.add_argument('output', help='Output PNG file or directory')
    parser.add_argument('--width', type=int, default=400, help='Image width (default: 400)')
    parser.add_argument('--height', type=int, default=300, help='Image height (default: 300)')
    parser.add_argument('--batch', action='store_true', help='Batch process directory')
    parser.add_argument('--pattern', default='*.stl', help='File pattern for batch mode (default: *.stl)')
    parser.add_argument('--camera-pos', nargs=3, type=float, metavar=('X', 'Y', 'Z'),
                       help='Camera position')
    parser.add_argument('--camera-focal', nargs=3, type=float, metavar=('X', 'Y', 'Z'),
                       help='Camera focal point')

    args = parser.parse_args()

    render_kwargs = {
        'width': args.width,
        'height': args.height,
    }

    if args.camera_pos:
        render_kwargs['camera_position'] = tuple(args.camera_pos)
    if args.camera_focal:
        render_kwargs['camera_focal_point'] = tuple(args.camera_focal)

    if args.batch:
        batch_render_stls(args.input, args.output, args.pattern, **render_kwargs)
    else:
        render_stl_to_image(args.input, args.output, **render_kwargs)


if __name__ == '__main__':
    main()
