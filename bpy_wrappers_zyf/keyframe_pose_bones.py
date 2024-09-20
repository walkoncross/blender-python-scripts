"""Keyframe one or multiple pose bones across multiple frames.

Author: zhaoyafei0210@gmail.com

"""
import bpy
import numpy as np


__all__ = ['keyframe_pose_bones', 'keyframe_single_pose_bone']


def __is_valid_object(bpy_obj_name: str, type: str = 'MESH') -> bool:
    """Check if bpy_obj_name is a valid object name.
    ...
    """
    return (bpy_obj_name and
            bpy_obj_name in bpy.data.objects.keys() and
            bpy.data.objects[bpy_obj_name].type == type)


def keyframe_pose_bones(
    armature_name: str,
    bone_names: list[str],
    rotations_per_bone: list[list] | np.ndarray,
    rotation_mode: str,
    start_frame: int = 1
) -> None:
    """
    Keyframes the rotation of the specified pose bones in a given armature object 
    across multiple frames.
    ...
    """
    assert __is_valid_object(armature_name, type='ARMATURE'), \
        f"Armature object '{armature_name}' not found."

    # Get the armature object
    armature = bpy.data.objects.get(armature_name)

    # Check if the number of rotations matches the number of bone names
    assert len(rotations_per_bone) == len(bone_names), "Number of rotations_per_bone does not match number of bone names."

    end_frame = start_frame

    # Enter pose mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    for bone_name, rotations in zip(bone_names, rotations_per_bone):
        # Get the pose bone
        pose_bone = armature.pose.bones.get(bone_name)
        
        assert pose_bone is not None, f"Pose bone '{bone_name}' not found in armature '{armature_name}'."
        
        # Set the rotation mode
        pose_bone.rotation_mode = rotation_mode
        
        for ii, rotation in enumerate(rotations):
            cur_frame = start_frame + ii
            # Set the current frame
            bpy.context.scene.frame_set(cur_frame)
            
            # Apply the rotation
            if rotation_mode == 'QUATERNION':
                pose_bone.rotation_quaternion = rotation
            elif rotation_mode == 'AXIS_ANGLE':
                pose_bone.rotation_axis_angle = rotation
            else:
                pose_bone.rotation_euler = rotation

            # Insert a keyframe for the bone's rotation
            if rotation_mode == 'QUATERNION':
                pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=cur_frame)
            elif rotation_mode == 'AXIS_ANGLE':
                pose_bone.keyframe_insert(data_path="rotation_axis_angle", frame=cur_frame)
            else:
                pose_bone.keyframe_insert(data_path="rotation_euler", frame=cur_frame)
        
        if cur_frame > end_frame:
            end_frame = cur_frame
            
    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    return end_frame


def keyframe_single_pose_bone(
    armature_name: str, 
    bone_name: str, 
    rotations: list | tuple | np.ndarray, 
    rotation_mode: str, 
    start_frame: int = 1
) -> None:
    """
    Keyframes the rotation of a single pose bone in a given armature object for a single frame.
    
    Parameters:
        armature_name (str): Name of the armature object.
        bone_name (str): Name of the pose bone to keyframe.
        rotations (list, tuple or np.ndarray): Rotation values for the bone. The format depends on the rotation mode.
        rotation_mode (str): Rotation mode ('XYZ', 'QUATERNION', etc.).
        start_frame (int, optional): The starting frame for keyframing. Defaults to 1.

    Returns:
        end_frame (int): The last frame number after keyframing.
    """
    end_frame = keyframe_pose_bones(armature_name, [bone_name], [rotations], rotation_mode, start_frame)

    return end_frame


if __name__ == "__main__":
    import math
    import mathutils

    num_frames = 24 * 3
    
    armature_name = "Armature"
    bone_names = ['Bone', 'Bone.001', 'Bone.002', 'Bone.003']

    # Convert degrees to radians
    radians_per_frame = [math.radians(90 * i / num_frames * 2) for i in range(num_frames//2)]

    # Generate Euler rotations in XYZ order
    euler_rotations = [(r, 0, 0) for r in radians_per_frame]

    euler_rotations2 = euler_rotations + euler_rotations[::-1] # rotate and reverse back
    euler_rotations3 = euler_rotations[::-1] + euler_rotations # reverse rotate and reverse back
    
    end_frame = keyframe_single_pose_bone(armature_name, bone_names[0], euler_rotations2, 'XYZ', 1)
    print(f'End frame: {end_frame}')

    quaternion_rotations = [mathutils.Euler(r).to_quaternion() for r in euler_rotations2]
    quaternion_rotations2 = [q.conjugated() for q in quaternion_rotations]

    end_frame = keyframe_single_pose_bone(armature_name, bone_names[1], quaternion_rotations2, 'QUATERNION', 1)
    print(f'End frame: {end_frame}')

    # Euler to Axis-Angle not supported
    # axis_angle_rotations = [mathutils.Euler(r).to_axis_angle() for r in euler_rotations]
    # axis_angle_rotations2 = [(-a[0], -a[1], -a[2]) for a in axis_angle_rotations]

    # Use quaternion to axis-angle
    axis_angle_rotations = [q.to_axis_angle() for q in quaternion_rotations] # list of (vector3, angle)
    axis_angle_rotations = [tuple(axis)+(angle,) for axis,angle  in axis_angle_rotations] # make list of tuples of 4 elements
    axis_angle_rotations2 = axis_angle_rotations[::-1]

    end_frame = keyframe_pose_bones(armature_name, bone_names[2:], [axis_angle_rotations, axis_angle_rotations2], 'AXIS_ANGLE', 1)
    print(f'End frame: {end_frame}')