"""Get vertices of a mesh object as a NumPy array.

Author: zhaoyafei0210@gmail.com
"""
import bpy
import numpy as np


__all__ = ['get_vertices_as_numpy']

def get_vertices_as_numpy(mesh_obj_name):
    """Get vertices of a mesh object as a NumPy array.

    Parameters:
        mesh_obj_name: Name of the mesh object.
    
    Returns: 
        NumPy array of vertices.
    """

    # Get Mesh object
    obj = bpy.data.objects.get(mesh_obj_name)
    if obj is None:
        print(f"Object '{mesh_obj_name}' not found.")
        return None
    
    if obj.type != 'MESH':
        print(f"Object '{mesh_obj_name}' is not a mesh.")
        return None

    # Update object to ensure it is up to date (especially if there are modifiers)
    obj.update_from_editmode()

    # Get all vertex coordinates
    vertices = np.array([vert.co for vert in obj.data.vertices])

    return vertices


if __name__ == "__main__":
    mesh_obj_name = "Cube"
    vertices_array = get_vertices_as_numpy(mesh_obj_name)

    # Print NumPy array
    if vertices_array is not None:
        print(vertices_array)

