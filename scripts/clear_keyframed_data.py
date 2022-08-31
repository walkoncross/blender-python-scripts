
"""Clear keyframed (pose) animation data and shape_key (blendshapes) data

Author: zhaoyafei0210@gmail.com

"""

import pandas

import bpy


def clear_keyframed_animation_data(bpy_obj_name):
    """Clear keyframed (pose) animation data
    """
    if bpy_obj_name and bpy_obj_name in bpy.data.objects.keys():
        bpy_obj = bpy.data.objects[bpy_obj_name]
        bpy_obj.animation_data_clear()


def clear_keyframed_shape_key_data(bpy_obj_name):
    """Clear keyframed shape_key (blendshapes) data
    """
    if bpy_obj_name and bpy_obj_name in bpy.data.objects.keys():
        bpy_obj = bpy.data.objects[bpy_obj_name]
        bpy_obj.data.shape_keys.animation_data_clear()


if __name__ == "__main__":
    head_mesh_obj_name = 'Wolf3D_Head'
    teeth_mesh_obj_name = 'Wolf3D_Teeth'
    armature_obj_name = 'AvatarRoot'

    clear_keyframed_shape_key_data(head_mesh_obj_name)
    clear_keyframed_shape_key_data(teeth_mesh_obj_name)
    clear_keyframed_animation_data(armature_obj_name)