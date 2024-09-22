"""Adds a new UV map to a mesh object in Blender.

Author: zhaoyafei0210@gmail.com
"""

import bpy
import numpy as np

__all__ = ['add_uv_map_from_numpy']

def is_valid_object(bpy_obj_name:str, type:str='MESH') -> bool:
    """Check if bpy_obj_name is a valid object name.

    Parameters:
        bpy_obj_name: object name
        type: object type, default is 'MESH'

    Returns: 
        True if bpy_obj_name is a valid object name, otherwise False
    
    """
    return (bpy_obj_name and bpy_obj_name in bpy.data.objects.keys() and bpy.data.objects[bpy_obj_name].type==type)



def add_uv_map(
    mesh_name: str, 
    uv_coords: list[list] | np.ndarray, 
    uv_polygons: list[list] | np.ndarray, 
    uv_name: str = "UVMap"
) -> None:
    """
    Adds a new UV map to a mesh object in Blender.

    Parameters:
        mesh_name (str): The name of the mesh object.
        uv_coords (list or np.ndarray): A list or numpy array of UV coordinates.
        uv_polygons (list or np.ndarray): A list or numpy array of polygon vertex indices.
        uv_name (str, optional): The name of the UV map. Defaults to "UVMap".

    Returns:
        None
    """
    
    if not is_valid_object(mesh_name):
        raise ValueError(f"Object '{mesh_name}' not found.")
    # Get the mesh object by name
    mesh = bpy.data.objects.get(mesh_name)
    
    if mesh is None or not mesh.type == 'MESH':
        print(f"Object '{mesh_name}' is not a valid mesh")
        return

    # Get the mesh data (this contains the UV layers, vertices, etc.)
    mesh_data = mesh.data

    # Create a new UV layer (UV map) if it doesn't exist
    if uv_name not in mesh_data.uv_layers:
        uv_layer = mesh_data.uv_layers.new(name=uv_name)
    else:
        uv_layer = mesh_data.uv_layers[uv_name]
    
    # Ensure active UV layer is the one we're working with
    mesh_data.uv_layers.active = uv_layer

    # Assign UV coordinates to the UV map
    for polygon in mesh_data.polygons:
        for ii, loop_idx in enumerate(polygon.loop_indices):
            # vert_idx = mesh_data.loops[loop_idx].vertex_index
            # Get UV coordinates for this vertex
            # uv_coord = uv_coords[uv_polygons[polygon.index][polygon.vertices.index(vert_idx)]]
            print(f'polygon.index: {polygon.index}')
            print(f'loop_idx: {loop_idx}')
            # print(f'vert_idx: {vert_idx}')
            uv_coord = uv_coords[uv_polygons[polygon.index][ii]]
            # Assign the UV coordinate to the corresponding loop index
            uv_layer.data[loop_idx].uv = uv_coord
    
    print(f"UV map '{uv_name}' added to mesh '{mesh_name}'.")


if __name__=="__main__":
    mesh_name = "Cube"
    uv_name = "MyUVMap"
    uv_coords = [
        [0.625, 0.5],
        [0.875, 0.5],
        [0.875, 0.75],
        [0.625, 0.75],
        [0.375, 0.75],
        [0.625, 0.75],
        [0.625, 1.0],
        [0.375, 1.0],
        [0.375, 0.0],
        [0.625, 0.0],
        [0.625, 0.25],
        [0.375, 0.25],
        [0.125, 0.5],
        [0.375, 0.5],
        [0.375, 0.75],
        [0.125, 0.75],
        [0.375, 0.5],
        [0.625, 0.5],
        [0.625, 0.75],
        [0.375, 0.75],
        [0.375, 0.25],
        [0.625, 0.25],
        [0.625, 0.5],
        [0.375, 0.5]
    ]

    uv_coords = np.array(uv_coords) + np.array([0.25, 0.]) # move a little bit to the right

    # List of polygon vertex indices (for each polygon)
    uv_polygons = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15],
        [16, 17, 18, 19],
        [20, 21, 22, 23]
    ]

    add_uv_map(mesh_name, uv_coords, uv_polygons, uv_name=uv_name)
