""" Export face vertex indices of a mesh object to a NumPy array.

Author: zhaoyafei0210@gmail.com
"""
import bpy
import numpy as np


__all__ = ['get_face_vertex_indices_as_numpy']

def get_face_vertex_indices_as_numpy(mesh_name, expected_num_edges=None):
    """
    Export face vertex indices of a mesh object to a NumPy array.

    Parameters:
        mesh_name: str, the name of the mesh object.
        expected_num_edges: int or None, the expected number of edges for each face. If None, no check is performed.

    Returns:
        face_vertex_indices_array: np.ndarray, a 2D array where each row represents the vertex indices of a face.
    """
    # Get the mesh object by name
    obj = bpy.data.objects.get(mesh_name)
    
    # Check if the mesh object exists
    assert obj is not None, f"No mesh found with the name: {mesh_name}"
    
    # Ensure the object is of type 'MESH'
    assert obj.type == 'MESH', f"Object {mesh_name} is not a mesh"

    # Access the mesh data
    mesh = obj.data

    # Ensure mesh data is updated for correct results (useful if object is in edit mode)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create an empty list to store face vertex indices
    face_vertex_indices = []

    # Loop through each face in the mesh and check for consistent edge numbers (optional)
    for face in mesh.polygons:
        if expected_num_edges and len(face.vertices) != expected_num_edges:
            raise ValueError(f"Face with index {face.index} does not have {expected_num_edges} edges. It has {len(face.vertices)} edges.")
        face_vertex_indices.append(face.vertices[:])

    # Convert to NumPy array
    face_vertex_indices_array = np.array(face_vertex_indices)

    return face_vertex_indices_array

if __name__ == "__main__":
    mesh_name = "Cube"  # Replace with the name of your mesh object
    expected_num_edges = None  # Set to 3 for triangles, 4 for quads, or None for no check
    vertex_indices_array = get_face_vertex_indices_as_numpy(mesh_name, expected_num_edges)
    print(vertex_indices_array)

