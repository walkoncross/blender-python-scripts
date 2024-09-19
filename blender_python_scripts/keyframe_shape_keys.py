"""Read arkit bs list from a .csv file and keyframe them on to a rigged character.

Author: zhaoyafei0210@gmail.com

"""
import bpy
# import mathutils


def __is_valid_object(bpy_obj_name:str, type:str='MESH') -> bool:
    """Check if bpy_obj_name is a valid object name.

    Parameters:
        bpy_obj_name: object name
        type: object type, default is 'MESH'

    Returns: 
        True if bpy_obj_name is a valid object name, otherwise False
    
    """
    return (bpy_obj_name and bpy_obj_name in bpy.data.objects.keys() and bpy.data.objects[bpy_obj_name].type==type)


# def insert_bs_keyframe_at(bpy_obj_name, data_dict, frame_id=1):
#     """
#     Keyframe blendshape data from .csv file exported from LiveLinkFace
#     """
#     bpy_obj = bpy.data.objects[bpy_obj_name]
#     # print('='*32)
#     # print(data_dict.keys())

#     # bpy.context.scene.frame_set(frame_id)
#     input_data_keys = data_dict.keys()

#     # shape keys
#     # print('-'*20 + ' shape keys fcurves ' + '-'*20)
#     # print('At frame #{}'.format(frame_id))
#     print('-'*10 + ' Keyframe shape keys fcurves at frame #{}'.format(frame_id) + '-'*10)

#     if bpy_obj.data and bpy_obj.data.shape_keys:
#         print('--> keyframe for shape_key: ', bpy_obj.data.shape_keys.name)
#         key_blocks = bpy_obj.data.shape_keys.key_blocks
#         for key in key_blocks:
#             # this can be used to insert or delete a keyframe but not modify
#             if key.name not in input_data_keys:
#                 continue

#             key.value = data_dict[key.name]
#             # print('key name : %s \t value : %s' % (key.name, key.value))
#             key.keyframe_insert(data_path="value", frame=frame_id)

#         # fcurves = bpy_obj.data.shape_keys.animation_data.action.fcurves

#         # for fc in fcurves:
#         #     # this can be used to modify an existing keyframe but not directly reference the key name
#         #     print('group : %s \t index : %s' % (fc.data_path, fc.array_index))

#         #     for key in fc.keyframe_points:
#         #         print('frame # : %s \t value : %s' % (key.co[0], key.co[1]))


# def insert_pose_keyframe_at(bpy_obj_name, pose_data_list, frame_id=1, bone_name_list=[]):
#     """
#     Keyframe pose data from .csv file exported from LiveLinkFace
#     """
#     if not bone_name_list:
#         bone_name_list = ['Head', 'LeftEye', 'RightEye']

#     print('-'*10 + ' Keyframe pose bones fcurves at frame #{}'.format(frame_id) + '-'*10)
    
#     # Get a bone.
#     bpy_obj = bpy.data.objects[bpy_obj_name]
#     # print(bpy_obj.name)

#     arm_matrix_world = bpy_obj.matrix_world.to_3x3()

#     bones = bpy_obj.data.bones
#     pose_bones = bpy_obj.pose.bones

#     # Set the keyframe at frame 1.
#     for i, bone_name in enumerate(bone_name_list):
#         offset = i*3

#         # LiveLinkFace's [yaw, pitch, roll] corresponds to Intrisic Rotation Order in UE4's object local space: Z/Y/-X
#         # Corres. intrinsic order in Blender's world space: -Z/-X/Y = [yaw, pitch, roll], extrinsic order in Blender: Y/-X/-Z
#         r1, r2, r3 = pose_data_list[offset:offset+3]
#         xyz_angles = [-r2, r3, -r1]
#         rot_order = 'ZXY'
#         # create a new euler with default axis rotation order
#         # mathutils.Euler() uses extrinsic rotation order, but the input angles are always in 'xyz' order
#         eul = mathutils.Euler(xyz_angles, rot_order[::-1])

#         # eul = mathutils.Euler(xyz_angles, rot_order[::-1])
#         rot_mat = eul.to_matrix().to_3x3()
#         matrix_world = arm_matrix_world @ bones[bone_name].matrix_local.to_3x3()
#         rot_mat = (matrix_world.inverted() @ rot_mat @
#                    matrix_world)  # to bone's local space

#         quat = rot_mat.to_quaternion()

#         pose_bones[bone_name].rotation_quaternion = quat
#         pose_bones[bone_name].keyframe_insert(
#             data_path='rotation_quaternion',
#             frame=frame_id
#         )


def keyframe_shape_key(
        mesh_name: str, 
        shape_key_name: str, 
        shape_key_values: list[float], 
        start_frame: int = 1
    ) -> None:
    """
    Keyframe a single shape key with a list of values.

    Parameters:
        mesh_name: str, name of the mesh object
        shape_key_name: str, name of the shape key to keyframe
        shape_key_values: list[float], list of values to keyframe for the shape key
        start_frame: int, the frame to start keyframing from (default is 1)

    Returns:
        None
    """
    assert __is_valid_object(mesh_name), f"Mesh object '{mesh_name}' not found."
    assert len(shape_key_values)>0, "Shape key values cannot be empty."

    # Get the mesh object
    mesh_obj = bpy.data.objects.get(mesh_name)

    # Get the shape key block of the mesh
    assert mesh_obj.data.shape_keys is not None, f"Mesh object '{mesh_name}' has no shape keys."
    
    shape_keys = mesh_obj.data.shape_keys.key_blocks
    shape_key = shape_keys.get(shape_key_name)
    
    assert shape_key, f"Shape key '{shape_key_name}' not found in mesh '{mesh_name}'."

    
    # Loop through the list of values and keyframe each value
    for i, value in enumerate(shape_key_values):
        current_frame = start_frame + i
        shape_key.value = value
        shape_key.keyframe_insert(data_path="value", frame=current_frame)
        # print(f"Keyframe added for shape key '{shape_key_name}' at frame {current_frame} with value {value}.")


def keyframe_shape_keys(
        mesh_name: str, 
        shape_key_names: list[str], 
        shape_key_values: list[list[float]], 
        start_frame=1
    ) -> None:
    """Keyframe shape keys from a .csv file.

    Parameters:
        mesh_name: str, name of the mesh object
        shape_key_names: list of str, shape key names
        shape_key_values: list of list of float, shape key values for each shape key
        start_frame: int, the frame to start keyframing from (default is 1)

    Returns:
        None
    """
    # Get the mesh object
    mesh_obj = bpy.data.objects.get(mesh_name)
    
    assert mesh_obj, f"Mesh object '{mesh_name}' not found."
    assert __is_valid_object(mesh_name, type='MESH'), f"Object '{mesh_name}' is not a mesh object."

    # Get the shape key block of the mesh
    assert mesh_obj.data.shape_keys is not None, f"Mesh object '{mesh_name}' has no shape keys."
    
    # shape_key_values = np.array(shape_key_values)

    # Ensure shape_key_names and shape_key_values have the same length
    assert len(shape_key_names) == len(shape_key_values), "Shape key names and values lists must have the same length."

    shape_keys = mesh_obj.data.shape_keys.key_blocks

    # Loop through the shape keys and their corresponding values
    for key_name, key_values in zip(shape_key_names, shape_key_values):
        shape_key = shape_keys.get(key_name)
        
        if not shape_key:
            print(f"Shape key '{key_name}' not found in mesh '{mesh_name}'.")
            continue
        
        # Loop through the values for this shape key and keyframe them
        for i, value in enumerate(key_values):
            current_frame = start_frame + i
            shape_key.value = value
            shape_key.keyframe_insert(data_path="value", frame=current_frame)
            print(f"Keyframe added for shape key '{key_name}' at frame {current_frame} with value {value}.")



if __name__ == "__main__":
    import numpy as np
    
    num_frames = 180
    
    mesh_name = "Cube"
    shape_keys = ['Stretch', 'Squash', 'ScaleUp', 'ScaleDown']

    increment_values = np.linspace(0, 1, num_frames//2)
    decrement_values = np.linspace(1, 0, num_frames//2)

    inc_dec_values = np.concatenate([increment_values, decrement_values])
    dec_inc_values = np.concatenate([decrement_values, increment_values])

    shape_key_values = [
        inc_dec_values,
        dec_inc_values,
        dec_inc_values,
        inc_dec_values,
    ]

    keyframe_shape_key(mesh_name, shape_keys[0], shape_key_values[0])
    keyframe_shape_keys(mesh_name, shape_keys[:2], shape_key_values[:2], num_frames+1)
    keyframe_shape_keys(mesh_name, shape_keys, shape_key_values, num_frames*2+1)
    
    
