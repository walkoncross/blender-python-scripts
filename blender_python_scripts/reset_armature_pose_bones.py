
"""Reset the rotation and location of armature pose bones

Author: zhaoyafei0210@gmail.com

"""

import bpy


def reset_armature_pose_bones(
    bpy_obj_name,
    skip_bones = []
):
    """reset the rotation and location of armature pose bones

    Args:
        bpy_obj_name (str): armature object name
        skip_bones (list of str, optional): bones we will not touch. Defaults to [].
    """
    if bpy_obj_name and bpy_obj_name in bpy.data.objects.keys():
        bpy_obj = bpy.data.objects[bpy_obj_name]
        # bpy_obj.animation_data_clear()

        pose_bones = bpy_obj.pose.bones
        for kk, pb in pose_bones.items():
            print('====' + kk)
            if kk in skip_bones:
                continue

            # pb.location = (0.0, 0.0, 0.0)
            # pb.scale = (1.0, 1.0, 1.0)
            print('---> PoseBone.location before reset: ', pb.location)
            print('---> PoseBone.scale before reset: ', pb.location)
            for ii in range(3):
                pb.location[ii] = 0.0
                pb.scale[ii] = 1.0
            print('---> PoseBone.location after reset: ', pb.location)
            print('---> PoseBone.scale after reset: ', pb.location)

            print('---> PoseBone.rotation_mode: ', pb.rotation_mode)

            if pb.rotation_mode == 'QUATERNION':
                print('---> PoseBone.rotation_quaternion before reset: ', pb.rotation_quaternion)
                # pb.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
                pb.rotation_quaternion[0] = 1.0
                pb.rotation_quaternion[1] = 0.0
                pb.rotation_quaternion[2] = 0.0
                pb.rotation_quaternion[3] = 0.0
                print('---> PoseBone.rotation_quaternion after reset: ', pb.rotation_quaternion)
            elif pb.rotation_mode == 'AXIS_ANGLE':
                print('---> PoseBone.rotation_axis_angle before reset: ', pb.rotation_quaternion)
                # pb.rotation_axis_angle =  (0.0, 0.0, 1.0, 0.0)
                pb.rotation_axis_angle[0] = 0.0
                pb.rotation_axis_angle[1] = 0.0
                pb.rotation_axis_angle[2] = 1.0
                pb.rotation_axis_angle[3] = 0.0
                print('---> PoseBone.rotation_axis_angle before reset: ', pb.rotation_quaternion)
            else:
                print('---> PoseBone.rotation_euler before reset: ', pb.rotation_euler)
                # pb.rotation_euler = (0.0, 0.0, 0.0)          
                pb.rotation_euler[0] = 0.0
                pb.rotation_euler[1] = 0.0
                pb.rotation_euler[2] = 0.0
                print('---> PoseBone.rotation_euler before reset: ', pb.rotation_euler)


if __name__ == "__main__":
    armature_obj_name = 'DeformationSystem'
    # skip_bones = ['Jaw_M']
    skip_bones = []

    reset_armature_pose_bones(
        armature_obj_name,
        skip_bones
    )