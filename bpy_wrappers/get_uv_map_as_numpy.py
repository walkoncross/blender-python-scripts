"""Retrieve UV coordinates and polygon indices from a specified mesh.

Author: zhaoyafei0210@gmail.com
"""
import bpy
import numpy as np

def get_uv_map_as_numpy(
        mesh_name: str, 
        uv_name: str='UVMap'
) -> tuple[np.ndarray, np.ndarray]:
    """
    Retrieve UV coordinates and polygon indices from a specified mesh.

    Args:
        mesh_name (str): The name of the mesh object.
        uv_name (str): The name of the UV map.

    Returns:
        tuple: A tuple containing:
            - numpy.ndarray: UV coordinates.
            - numpy.ndarray: Polygon indices.
    """
    # Get the object by name
    obj = bpy.data.objects.get(mesh_name)
    if obj is None or obj.type != 'MESH':
        raise ValueError(f"Object '{mesh_name}' is not a valid mesh.")
    
    # Make sure the mesh is up-to-date
    mesh = obj.data

    # Find the UV map
    uv_layer = mesh.uv_layers.get(uv_name)
    if uv_layer is None:
        raise ValueError(f"UV map '{uv_name}' not found on mesh '{mesh_name}'.")

    # Ensure we're in object mode to access evaluated data
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Store UV coordinates and triangle indices
    uv_coords = []
    uv_polygons = []

    # Access UV coordinates for each loop in the mesh
    for loop in mesh.loops:
        uv_coords.append(uv_layer.data[loop.index].uv)

    # Access face vertex indices
    for poly in mesh.polygons:
        uv_polygons.append([loop_index for loop_index in poly.loop_indices])

    # Convert to numpy arrays
    uv_coords = np.array(uv_coords)
    uv_polygons = np.array(uv_polygons)

    return uv_coords, uv_polygons


if __name__ == "__main__":
    uv_coords, uv_polygons = get_uv_map_as_numpy('Cube', 'UVMap')
    print(f'---> uv_coords.shape: {uv_coords.shape}')
    print(f'---> uv_coords: {uv_coords}')
    print(f'---> uv_polygons.shape: {uv_polygons.shape}')
    print(f'---> uv_polygons: {uv_polygons}')