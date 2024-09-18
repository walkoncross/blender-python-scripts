"""Create a shape key from input vertices.

Author: zhaoyafei0210@gmail.com
"""
import bpy
import numpy as np


def create_shape_key_from_vertices(mesh_obj_name, target_vertices, shape_key_name="NewShapeKey"):
    """Create a shape key from input vertices.

    Parameters:
        mesh_obj_name: Name of the mesh object.
        target_vertices: List of target vertices.
        shape_key_name: Name of the shape key.
    
    Returns:
        None
    """
    # Get the Mesh object
    obj = bpy.data.objects.get(mesh_obj_name)
    if obj is None:
        print(f"Object '{mesh_obj_name}' not found.")
        return
    
    if obj.type != 'MESH':
        print(f"Object '{mesh_obj_name}' is not a mesh.")
        return
    
    # Ensure the object has a basis shape key
    if obj.data.shape_keys is None:
        obj.shape_key_add(name="Basis")  # Add basis shape
    
    # Add a new shape key
    shape_key = obj.shape_key_add(name=shape_key_name)
    shape_key.interpolation = 'KEY_LINEAR'
    
    # Get the vertex data of the basis shape
    if len(target_vertices) != len(obj.data.vertices):
        print("The number of target vertices does not match the object's vertices.")
        return
    
    # Modify the vertex positions of the shape key
    for i, vert in enumerate(target_vertices):
        shape_key.data[i].co = vert

    print(f"Shape key '{shape_key_name}' created successfully for object '{mesh_obj_name}'.")


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

    # target_vertices = [(1.1, 1.1, 0), (1.1, -1.1, 0), (-1.1, -1.1, 0), (-1.1, 1.1, 0)]
    mesh_obj_name = "Cube"
    vertices_array = get_vertices_as_numpy(mesh_obj_name)
    # Print NumPy array
    if vertices_array is not None:
        print(vertices_array)

    target_vertices = vertices_array * 2

    # 调用函数，创建Shape Key
    create_shape_key_from_vertices(mesh_obj_name, target_vertices, "ScaleUp")

    target_vertices = vertices_array * 0.5
    create_shape_key_from_vertices(mesh_obj_name, target_vertices, "ScaleDown")
