"""Create a mesh object from input vertices and faces.

Author: zhaoyafei0210@gmail.com
"""
import bpy
import numpy as np

__all__ = ['create_mesh_object']

def create_mesh_object(
        vertices: list | np.ndarray,
        edges: list | np.ndarray,
        faces: list | np.ndarray, 
        mesh_name: str = "NewMesh"
    ) -> str:
    """Create a mesh object from input vertices, edges and faces.
    
    Parameters:
        vertices: list of vertices or numpy.ndarray, each vertex is a tuple of (x, y, z)
        edges: list of edges or numpy.ndarray, each edge is a tuple of (v1, v2)
        faces: list of faces or numpy.ndarray, each triangle is a tuple of (v1, v2, v3)
        mesh_name: name of the mesh object

    Returns:
        mesh_obj_name: name of the mesh object
    """
    # Create a new Mesh object
    mesh = bpy.data.meshes.new(mesh_name)
    
    # mesh_name = mesh.name
    
    # Create the basic structure of the Mesh (vertices and polygons)
    mesh.from_pydata(vertices, edges, faces)
    
    # Update the Mesh to make its structure valid
    mesh.update()

    # Create a new object and assign the Mesh to it
    obj = bpy.data.objects.new(mesh_name, mesh)

    # Link the object to the current scene's collection
    bpy.context.collection.objects.link(obj)

    # Set as the active object
    bpy.context.view_layer.objects.active = obj

    # Select the object
    obj.select_set(True)

    print(f"Mesh object '{mesh_name}' created successfully.")

    return obj.name


if __name__ == "__main__":
    import numpy as np

    vertices = [(1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)]
    faces = [(0, 1, 2), (2, 3, 0)]

    # Call the function to create the Mesh object
    obj_name = create_mesh_object(vertices, [], faces, 'MySquare')
    print(f'Created mesh object: {obj_name}')

    vertices2 = np.array(vertices) + np.array([0, 0, 1])
    faces2 = np.array(faces)

    # Call the function to create the Mesh object
    obj_name = create_mesh_object(vertices2, [],faces2, 'MySquare2')
    print(f'Created mesh object: {obj_name}')
