"""Export UV map of a mesh object to numpy array.

Author: zhaoyafei0210@gmail.com
"""
import bpy
import numpy as np

def get_uv_coords_as_numpy(obj_name):
    # Ensure the object exists
    obj = bpy.data.objects.get(obj_name)
    assert obj is not None, f"Object '{obj_name}' not found"
    
    # Ensure the object is a mesh and has UVs
    assert obj.type == 'MESH', f"Object '{obj_name}' is not a mesh"
    
    # Switch to object mode to avoid issues with accessing data
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Get the active UV map
    uv_layer = obj.data.uv_layers.active
    assert uv_layer is not None, f"Object '{obj_name}' has no active UV map"
    
    # Prepare an empty list to store the UV coordinates
    uv_coords = []

    print(f'length of obj.data.loops: {len(obj.data.loops)}')

    # Iterate through each loop (vertex per face corner) to get UVs
    for loop in obj.data.loops:
        # print(f'loop index: {loop.index}')
        uv = uv_layer.data[loop.index].uv[:]
        # print(f'len(uv): {len(uv)}')
        uv_coords.append(uv)

    # Convert the list of UVs to a NumPy array
    uv_array = np.array(uv_coords)
    
    return uv_array

if __name__ == "__main__":
    obj_name = "Cube"
    uv_array = get_uv_coords_as_numpy(obj_name)

    if uv_array is not None:
        print("UV coordinates exported to NumPy array:")
        print(uv_array)
