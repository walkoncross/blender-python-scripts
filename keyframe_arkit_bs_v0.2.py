
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


def insert_bs_keyframe_at(bpy_obj_name, data_dict, frame_id=1):
    bpy_obj = bpy.data.objects[bpy_obj_name]

    # bpy.context.scene.frame_set(frame_id)
    input_data_keys = data_dict.keys()

    # shape keys
    # print('-'*20 + ' shape keys fcurves ' + '-'*20)
    # print('At frame #{}'.format(frame_id))
    print('-'*10 + ' Keyframe shape keys fcurves at frame #{}'.format(frame_id) + '-'*10)

    if bpy_obj.data.shape_keys:
        print(bpy_obj.data.shape_keys.name)
        key_blocks = bpy_obj.data.shape_keys.key_blocks
        for key in key_blocks:
            # this can be used to insert or delete a keyframe but not modify
            if key.name not in input_data_keys:
                continue

            key.value = data_dict[key.name]
            print('key name : %s \t value : %s' % (key.name, key.value))
            key.keyframe_insert(data_path="value", frame=frame_id)

        # fcurves = bpy_obj.data.shape_keys.animation_data.action.fcurves

        # for fc in fcurves:
        #     # this can be used to modify an existing keyframe but not directly reference the key name
        #     print('group : %s \t index : %s' % (fc.data_path, fc.array_index))

        #     for key in fc.keyframe_points:
        #         print('frame # : %s \t value : %s' % (key.co[0], key.co[1]))


def insert_pose_keyframe_at(bpy_obj_name, pose_data_list, frame_id=1):
    """

    """
    bone_name_list = ['Head', 'LeftEye', 'RightEye']

    print('-'*10 + ' Keyframe pose bones fcurves at frame #{}'.format(frame_id) + '-'*10)

    # Get a bone.
    bpy_obj = bpy.data.objects[bpy_obj_name]
    # print(bpy_obj.name)

    pose_bones = bpy_obj.pose.bones

    # Set the keyframe at frame 1.
    for i, bone_name in enumerate(bone_name_list):
        offset = i*3

        # Intrisic Rotation Order in UE4's object local space: -Z/Y/X = [yaw, pitch, roll]
        # Corres. intrinsic order in Blender's world space: Z/-X/-Y = [yaw, pitch, roll], extrinsic order in Blender: Y/-X/Z
        r1, r2, r3 = pose_data_list[offset:offset+3]

        if bone_name == 'Head':
            # depends on "Head" bone's local axes: Y/-X/Z
            xyz_angles = [-r2, r1, r3]
            rot_order = 'YXZ'  # depends on each bone's local axes
        else:
            # depends on "LeftEye/RightEye" bones' local axes: Z/X/Y
            xyz_angles = [r2, r3, r1]
            rot_order = 'ZXY'  # depends on "LeftEye/RightEye" bones' local axes

        # create a new euler with default axis rotation order
        # mathutils.Euler() uses extrinsic rotation order, but the input angles are always in 'xyz' order
        # eul = mathutils.Euler([-r1, r2, r3], 'YXZ')
        eul = mathutils.Euler(xyz_angles, rot_order[::-1])

        # components of an existing euler can use slice notation to get a tuple
        print("Values: %f, %f, %f" % eul[:])

        # the order can be set at any time too
        # eul.order = 'ZYX'
        quat = eul.to_quaternion()

        pose_bones[bone_name].rotation_quaternion = quat
        pose_bones[bone_name].keyframe_insert(
            data_path='rotation_quaternion',
            frame=frame_id
        )



def keyframe_arkit_bs_from_csv_file(
        head_mesh_name, 
        csv_path, 
        start_frame=1, 
        time_downsample_rate=2,
        teeth_mesh_name=None,
        armature_name=None,
    ):
    """Read arkit bs list from a .csv file and keyframe them on to a rigged character.

    csv_path:      input .csv file with LiveLinkeFace-captured ARKit BS.
    """
    dataframe = pandas.read_csv(csv_path)
    # df_dict_list = dataframe.to_dict('index')

    # time_downsample_rate = 2  # 60fps->30fps
    # time_downsample_rate = 1
    frame_num = dataframe.shape[0] // time_downsample_rate

    # livelikeface_data_keys = dataframe.keys().to_list()
    # pose_keys = livelikeface_data_keys[-9:]

    for ii in range(frame_num):
        frame_data = dataframe.iloc[ii*time_downsample_rate]
        arkit_bs = frame_data[2:-9].to_dict()

        cur_key_frame_id = ii+start_frame

        # print('arkit_bs: ')
        # print(arkit_bs)
        if head_mesh_name and head_mesh_name in bpy.data.objects.keys():
            insert_bs_keyframe_at(head_mesh_name, arkit_bs, cur_key_frame_id)
        
        if teeth_mesh_name and teeth_mesh_name in bpy.data.objects.keys():
            insert_bs_keyframe_at(teeth_mesh_name, arkit_bs, cur_key_frame_id)

        if armature_name and armature_name in bpy.data.armatures.keys():
            pose_data = frame_data[-9:]

            # print('Pose Data: ')
            # print(pose_data.to_dict())

            pose_data_list = pose_data.to_list()
            insert_pose_keyframe_at(armature_name, pose_data_list, cur_key_frame_id)

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    return cur_key_frame_id


def clear_animation_data(bpy_obj_name):
    if bpy_obj_name and bpy_obj_name in bpy.data.objects.keys():
        bpy_obj = bpy.data.objects[bpy_obj_name]
        bpy_obj.animation_data_clear()


if __name__ == "__main__":
    head_mesh_name = 'Wolf3D_Head'
    teeth_mesh_name = 'Wolf3D_Teeth'
    armature_name = 'AvatarRoot'
    time_downsample_rate = 2 # 60fps -> 30 fps
    
    start_frame = 1

    clear_animation_data(head_mesh_name)
    clear_animation_data(teeth_mesh_name)
    clear_animation_data(armature_name)

    # csv_path = r'/Users/zhaoyafei/Downloads/LiveLinkFace_bs_conversion/20210112_MySlate_2/MySlate_2_JAMESs_iPhone12Pro.csv'
    csv_path = r'/Users/zhaoyafei/Downloads/LiveLinkFace_bs_conversion/20210129_MySlate_3/MySlate_3_JAMESs_iPhone12Pro.csv'
    # csv_path = r'/Users/zhaoyafei/Downloads/LiveLinkFace/20210812_MySlate_8/MySlate_8_JZs_iPhone12Pro.csv'
    # csv_path = r'/Users/zhaoyafei/Downloads/LiveLinkFace/20210812_MySlate_9/MySlate_9_JZs_iPhone12Pro.csv'
    # csv_path = r'/Users/zhaoyafei/Downloads/LiveLinkFace/20210812_MySlate_11/MySlate_11_JZs_iPhone12Pro.csv'

    end_frame = keyframe_arkit_bs_from_csv_file(
                    head_mesh_name, 
                    csv_path, 
                    start_frame, 
                    time_downsample_rate, 
                    teeth_mesh_name, 
                    armature_name)

    print('===> end_frame: ', end_frame)

    # bpy_obj_name = 'Wolf3D_Head'

    # for i in range(30):
    #     print_bs_keyframe_at(bpy_obj_name)

    csv_path_list = [
        r'/Users/zhaoyafei/Downloads/LiveLinkFace/20210812_MySlate_8/MySlate_8_JZs_iPhone12Pro.csv',
        r'/Users/zhaoyafei/Downloads/LiveLinkFace/20210812_MySlate_9/MySlate_9_JZs_iPhone12Pro.csv',
        r'/Users/zhaoyafei/Downloads/LiveLinkFace/20210812_MySlate_11/MySlate_11_JZs_iPhone12Pro.csv'
    ]

    start_frame =  end_frame + 15

    for csv_path in csv_path_list:
        # clear_all_animation_data()
        end_frame = keyframe_arkit_bs_from_csv_file(
                        head_mesh_name, 
                        csv_path, 
                        start_frame, 
                        time_downsample_rate, 
                        teeth_mesh_name, 
                        armature_name)
        start_frame =  end_frame + 15

        print('===> end_frame: ', end_frame)