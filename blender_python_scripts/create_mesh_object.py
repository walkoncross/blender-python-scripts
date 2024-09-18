"""Create a mesh object from input vertices and triangles.

Author: zhaoyafei0210@gmail.com
"""
import bpy


def create_mesh_object(vertices, triangles, mesh_name="NewMesh"):
    """Create a mesh object from input vertices and triangles.
    
    Parameters:
        vertices: list of vertices or numpy.ndarray, each vertex is a tuple of (x, y, z)
        triangles: list of triangles or numpy.ndarray, each triangle is a tuple of (v1, v2, v3)
        mesh_name: name of the mesh object
    """
    # Create a new Mesh object
    mesh = bpy.data.meshes.new(mesh_name)
    
    # Create the basic structure of the Mesh (vertices and polygons)
    mesh.from_pydata(vertices, [], triangles)
    
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

if __name__ == "__main__":
    import numpy as np

    vertices = [(1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)]
    triangles = [(0, 1, 2), (2, 3, 0)]

    # Call the function to create the Mesh object
    create_mesh_object(vertices, triangles, 'MySquare')

    vertices2 = np.array(vertices) + np.array([0, 0, 1])
    triangles2 = np.array(triangles)

    # Call the function to create the Mesh object
    create_mesh_object(vertices2, triangles2, 'MySquare2')
