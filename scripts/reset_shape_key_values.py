
"""Reset shape key values

Author: zhaoyafei0210@gmail.com

"""

import bpy


def reset_shape_key_values(bpy_obj_name):
    """Reset shape key values
    """
    if bpy_obj_name and bpy_obj_name in bpy.data.objects.keys():
        bpy_obj = bpy.data.objects[bpy_obj_name]
        # bpy_obj.data.shape_keys.animation_data_clear()

        key_blocks = bpy_obj.data.shape_keys.key_blocks
        for key in key_blocks:
            key.value = 0.0
            

if __name__ == "__main__":
    mesh_obj_name = 'DuXiong.001'

    reset_shape_key_values(mesh_obj_name)
