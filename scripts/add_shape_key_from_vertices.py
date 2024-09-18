"""Create shape key from input vertices.

Author: zhaoyafei0210@gmail.com
"""
import bpy
import numpy as np


def create_shape_key_from_vertices(
        mesh_obj_name: str, 
        target_vertices: list | np.ndarray,
        shape_key_names: str | list[str] = 'Key'
    ) -> list[str]:
    """Create shape key from input vertices.

    Parameters:
        mesh_obj_name: Name of the mesh object, with #num_basis_vertices vertices.
        target_vertices: List of target vertices or a NumPy array of vertices, 
            must can be converted into an array with shape (#num_basis_vertices, 3) 
            or (#num_shape_key, #num_basis_vertices, 3).
        shape_key_names: Name or Prefix of the shape key or a list of shape key names 
            with length of #num_shape_key. 
    
    Returns:
        List of shape key names.
    """
    # Get the Mesh object
    obj = bpy.data.objects.get(mesh_obj_name)

    # Check if the object exists
    assert obj is not None, f"Object '{mesh_obj_name}' not found."
    
    # Check if the object is a mesh
    assert obj.type == 'MESH', f"Object '{mesh_obj_name}' is not a mesh."
    
    # Ensure the object has a basis shape key
    if obj.data.shape_keys is None:
        obj.shape_key_add(name="Basis")  # Add basis shape
    
    assert isinstance(target_vertices, list) or isinstance(target_vertices, np.ndarray), \
        "target_vertices must be a NumPy array or list of tuple of 3 floats."
    
    assert isinstance(shape_key_names, list) or isinstance(shape_key_names, str), \
        "shape_key_names must be a str or list of str."
    target_vertices = np.array(target_vertices)

    # Ensure the shape of target_vertices is valid
    assert target_vertices.ndim in {2, 3}, \
        "Invalid shape of target_vertices, must have 2 or 3 dimensions, " \
        f"but got {target_vertices.ndim}."

    # Expand target_vertices to 3D if needed
    if target_vertices.ndim == 2:
        target_vertices = np.expand_dims(target_vertices, axis=0)

    num_basis_vertices = len(obj.data.vertices)

    # Set default shape key name(s)
    if shape_key_names == '':
        print('shape_key_names is None, will use default shape key name "Key".')
        shape_key_names = 'Key'
    
    # Check the shape of target_vertices and shape_key_names, generate shape_key_names if needed
    if isinstance(shape_key_names, list):
        num_shape_key_names = len(shape_key_names)
        assert target_vertices.shape == (num_shape_key_names, num_basis_vertices, 3), \
            f"Invalid shape of target_vertices, must be " \
            f"({num_basis_vertices}, 3) or (1, {num_basis_vertices}, 3), " \
            f"but got {target_vertices.shape}."
    elif isinstance(shape_key_names, str):
        num_shape_key = target_vertices.shape[0]

        if num_shape_key == 1:
            shape_key_names = [shape_key_names]
            assert target_vertices.shape[-2:] == (num_basis_vertices, 3), \
                f"Invalid shape of target_vertices, must be " \
                f"({num_basis_vertices}, 3) or (1, {num_basis_vertices}, 3), " \
                f"but got {target_vertices.shape}."
        else:
            shape_key_names = [f"{shape_key_names}_{ii:03d}" for ii in range(num_shape_key)]
    else:
        raise TypeError(
            f"Invalid shape_key_names type, must be None, str or list[str], "
            f"but got {type(shape_key_names)}."
        )

    for ii, shape_key_name in enumerate(shape_key_names):
        shape_key = obj.shape_key_add(name=shape_key_name)
        shape_key.interpolation = 'KEY_LINEAR'

        for jj, vert in enumerate(target_vertices[ii]):
            shape_key.data[jj].co = vert

        print(f"Shape key '{shape_key_name}' created successfully for object " 
              f"'{mesh_obj_name}'.")
    
    return shape_key_names


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

    shape_key_names = create_shape_key_from_vertices(mesh_obj_name, target_vertices)
    print(f'--> Created shape_key_names: {shape_key_names}')

    # create Shape Key
    shape_key_names = create_shape_key_from_vertices(mesh_obj_name, target_vertices, "ScaleUp")
    print(f'--> Created shape_key_names: {shape_key_names}')

    target_vertices2 = vertices_array * 0.5
    shape_key_names = create_shape_key_from_vertices(mesh_obj_name, target_vertices, "ScaleDown")
    print(f'--> Created shape_key_names: {shape_key_names}')

    target_vertices3 = np.stack((target_vertices, target_vertices2), axis=0)
    shape_key_names = create_shape_key_from_vertices(mesh_obj_name, target_vertices3)
    print(f'--> Created shape_key_names: {shape_key_names}')

    shape_key_names = create_shape_key_from_vertices(mesh_obj_name, target_vertices3, ["ScaleUp2", "ScaleDown2"])
    print(f'--> Created shape_key_names: {shape_key_names}')
