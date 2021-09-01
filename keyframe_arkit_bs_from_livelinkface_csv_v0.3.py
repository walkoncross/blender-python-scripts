
"""Read arkit bs list from a .csv file and keyframe them on to a rigged character.

Author: zhaoyafei0210@gmail.com

"""

import pandas

import bpy
import mathutils
import math


def print_bs_keyframe_at(bpy_obj_name, frame_id=0):
    bpy_obj = bpy.data.objects[bpy_obj_name]

    bpy.context.scene.frame_set(frame_id)
    # shape keys
    print('-'*10 + ' Print shape keys fcurves at frame #{}'.format(frame_id) + '-'*10)
    if bpy_obj.data.shape_keys:
        print(bpy_obj.data.shape_keys.name)
        for key in bpy_obj.data.shape_keys.key_blocks:
            # this can be used to insert or delete a keyframe but not modify
            print('key name : %s \t value : %s' % (key.name, key.value))


def is_valid_object(bpy_obj_name, type='MESH'):
    return (bpy_obj_name and bpy_obj_name in bpy.data.objects.keys() and bpy.data.objects[bpy_obj_name].type==type)


def insert_bs_keyframe_at(bpy_obj_name, data_dict, frame_id=1):
    """
    Keyframe blendshape data from .csv file exported from LiveLinkFace
    """
    bpy_obj = bpy.data.objects[bpy_obj_name]
    # print('='*32)
    # print(data_dict.keys())

    # bpy.context.scene.frame_set(frame_id)
    input_data_keys = data_dict.keys()

    # shape keys
    # print('-'*20 + ' shape keys fcurves ' + '-'*20)
    # print('At frame #{}'.format(frame_id))
    print('-'*10 + ' Keyframe shape keys fcurves at frame #{}'.format(frame_id) + '-'*10)

    if bpy_obj.data and bpy_obj.data.shape_keys:
        print('--> keyframe for shape_key: ', bpy_obj.data.shape_keys.name)
        key_blocks = bpy_obj.data.shape_keys.key_blocks
        for key in key_blocks:
            # this can be used to insert or delete a keyframe but not modify
            if key.name not in input_data_keys:
                continue

            key.value = data_dict[key.name]
            # print('key name : %s \t value : %s' % (key.name, key.value))
            key.keyframe_insert(data_path="value", frame=frame_id)

        # fcurves = bpy_obj.data.shape_keys.animation_data.action.fcurves

        # for fc in fcurves:
        #     # this can be used to modify an existing keyframe but not directly reference the key name
        #     print('group : %s \t index : %s' % (fc.data_path, fc.array_index))

        #     for key in fc.keyframe_points:
        #         print('frame # : %s \t value : %s' % (key.co[0], key.co[1]))


def insert_pose_keyframe_at(bpy_obj_name, pose_data_list, frame_id=1, bone_name_list=[]):
    """
    Keyframe pose data from .csv file exported from LiveLinkFace
    """
    if not bone_name_list:
        bone_name_list = ['Head', 'LeftEye', 'RightEye']

    print('-'*10 + ' Keyframe pose bones fcurves at frame #{}'.format(frame_id) + '-'*10)
    
    # Get a bone.
    bpy_obj = bpy.data.objects[bpy_obj_name]
    # print(bpy_obj.name)

    arm_matrix_world = bpy_obj.matrix_world.to_3x3()

    bones = bpy_obj.data.bones
    pose_bones = bpy_obj.pose.bones

    # Set the keyframe at frame 1.
    for i, bone_name in enumerate(bone_name_list):
        offset = i*3

        # LiveLinkFace's [yaw, pitch, roll] corresponds to Intrisic Rotation Order in UE4's object local space: Z/Y/-X
        # Corres. intrinsic order in Blender's world space: -Z/-X/Y = [yaw, pitch, roll], extrinsic order in Blender: Y/-X/-Z
        r1, r2, r3 = pose_data_list[offset:offset+3]
        xyz_angles = [-r2, r3, -r1]
        rot_order = 'ZXY'
        # create a new euler with default axis rotation order
        # mathutils.Euler() uses extrinsic rotation order, but the input angles are always in 'xyz' order
        eul = mathutils.Euler(xyz_angles, rot_order[::-1])

        # eul = mathutils.Euler(xyz_angles, rot_order[::-1])
        rot_mat = eul.to_matrix().to_3x3()
        matrix_world = arm_matrix_world @ bones[bone_name].matrix_local.to_3x3()
        rot_mat = (matrix_world.inverted() @ rot_mat @
                   matrix_world)  # to bone's local space

        quat = rot_mat.to_quaternion()

        pose_bones[bone_name].rotation_quaternion = quat
        pose_bones[bone_name].keyframe_insert(
            data_path='rotation_quaternion',
            frame=frame_id
        )


def keyframe_arkit_bs_from_csv_file(
    arkit_rigged_mesh_obj_names,
    csv_path,
    start_frame=1,
    time_downsample_rate=2,
    armature_obj_name=None,
    bone_name_list=[]
):
    """Read arkit bs list from a .csv file and keyframe them on to a rigged character.

    arkit_rigged_mesh_obj_names: list of str, arkit 51-bs rigged mesh objects
    csv_path:      input .csv file with LiveLinkeFace-captured ARKit BS.
    """
    dataframe = pandas.read_csv(csv_path)
    # df_dict_list = dataframe.to_dict('index')

    # time_downsample_rate = 2  # 60fps->30fps
    # time_downsample_rate = 1
    frame_num = dataframe.shape[0] // time_downsample_rate

    # livelikeface_data_keys = dataframe.keys().to_list()
    # pose_keys = livelikeface_data_keys[-9:]

    if arkit_rigged_mesh_obj_names:
        first_keyframed_obj_name = arkit_rigged_mesh_obj_names[0]
        if not is_valid_object(first_keyframed_obj_name, 'MESH'):  
            raise Exception('Error: Invalid "MESH" object: ', first_keyframed_obj_name)
    else:
        first_keyframed_obj_name = ""

    if armature_obj_name and not is_valid_object(armature_obj_name, "ARMATURE"):
        raise Exception('Error: Invalid "ARMATURE" object: ', armature_obj_name)

    if not first_keyframed_obj_name and not armature_obj_name:
        raise Exception('Error: Must have at least one valid "MESH" object or one "ARMATURE" object')

    for ii in range(frame_num):
        frame_data = dataframe.iloc[ii*time_downsample_rate]
        arkit_bs = frame_data[2:-9].to_dict()

        cur_key_frame_id = ii+start_frame

        # print('arkit_bs: ')
        # print(arkit_bs)
        insert_bs_keyframe_at(first_keyframed_obj_name, arkit_bs, cur_key_frame_id)
 
        pose_data = frame_data[-9:]

        # print('Pose Data: ')
        # print(pose_data.to_dict())

        pose_data_list = pose_data.to_list()
        insert_pose_keyframe_at(
            armature_obj_name, pose_data_list, cur_key_frame_id, bone_name_list)

    if len(arkit_rigged_mesh_obj_names)>1:
        print('---> Get animation_data.action of MESH object: ', first_keyframed_obj_name)
        action = bpy.data.objects[first_keyframed_obj_name].data.shape_keys.animation_data.action

        for mesh_obj_name in arkit_rigged_mesh_obj_names[1:]:
            if not is_valid_object(mesh_obj_name, 'MESH'):
                print('==> Skip invalid MESH object: ', mesh_obj_name)
                continue

            # set to the first mesh's animation_data.action
            print('---> Set MESH object "{}" animation data to the animation data of "{}" : '.format(mesh_obj_name, first_keyframed_obj_name))

            anim_data = bpy.data.objects[mesh_obj_name].data.shape_keys.animation_data

            if not anim_data:
                anim_data = bpy.data.objects[mesh_obj_name].data.shape_keys.animation_data_create()
            
            anim_data.action = action

    # bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    return cur_key_frame_id


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
    arkit_rigged_mesh_obj_names = ['Wolf3D_Head', 'Wolf3D_Teeth']
    armature_obj_name = 'AvatarRoot'
    bone_name_list = ['Head', 'LeftEye', 'RightEye']

    # time_downsample_rate = 4  # 100 fps -> 25 fps
    time_downsample_rate = 2  # 60 fps -> 30 fps
    # time_downsample_rate = 1  # 25 fps -> 25 fps

    start_frame = 1
    # time_downsample_rate = 4  # 100 fps -> 25 fps
    time_downsample_rate = 2  # 60 fps -> 30 fps
    # time_downsample_rate = 1  # 25 fps -> 25 fps

    start_frame = 1

    clear_keyframed_shape_key_data(arkit_rigged_mesh_obj_names[0])
    clear_keyframed_animation_data(armature_obj_name)

    # csv_path = r'/Users/zhaoyafei/Downloads/LiveLinkFace_data/20210112_MySlate_2/MySlate_2_JAMESs_iPhone12Pro.csv'
    csv_path = r'/Users/zhaoyafei/Downloads/LiveLinkFace_data/20210129_MySlate_3/MySlate_3_JAMESs_iPhone12Pro.csv'
    # csv_path = r'/Users/zhaoyafei/Downloads/LiveLinkFace_data/20210812_MySlate_8/MySlate_8_JZs_iPhone12Pro.csv'
    # csv_path = r'/Users/zhaoyafei/Downloads/LiveLinkFace_data/20210812_MySlate_9/MySlate_9_JZs_iPhone12Pro.csv'
    # csv_path = r'/Users/zhaoyafei/Downloads/LiveLinkFace_data/20210812_MySlate_11/MySlate_11_JZs_iPhone12Pro.csv'

    end_frame = keyframe_arkit_bs_from_csv_file(
        arkit_rigged_mesh_obj_names,
        csv_path,
        start_frame,
        time_downsample_rate,
        armature_obj_name,
        bone_name_list)

    print('===> end_frame: ', end_frame)

    # bpy_obj_name = 'Wolf3D_Head'

    # for i in range(30):
    #     print_bs_keyframe_at(bpy_obj_name)

    csv_path_list = [
        r'/Users/zhaoyafei/Downloads/LiveLinkFace_data/20210812_MySlate_8/MySlate_8_JZs_iPhone12Pro.csv',
        r'/Users/zhaoyafei/Downloads/LiveLinkFace_data/20210812_MySlate_9/MySlate_9_JZs_iPhone12Pro.csv',
        r'/Users/zhaoyafei/Downloads/LiveLinkFace_data/20210812_MySlate_11/MySlate_11_JZs_iPhone12Pro.csv'
    ]

    start_frame = end_frame + 15

    for csv_path in csv_path_list:
        # clear_all_animation_data()
        end_frame = keyframe_arkit_bs_from_csv_file(
            arkit_rigged_mesh_obj_names,
            csv_path,
            start_frame,
            time_downsample_rate,
            armature_obj_name,
            bone_name_list)
            
        start_frame = end_frame + 15

        print('===> end_frame: ', end_frame)
