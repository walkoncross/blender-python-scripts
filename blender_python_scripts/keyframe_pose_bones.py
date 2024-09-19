"""Keyframe one or multiple pose bones across multiple frames.

Author: zhaoyafei0210@gmail.com

"""
import bpy
import numpy as np


def __is_valid_object(bpy_obj_name: str, type: str = 'MESH') -> bool:
    """Check if bpy_obj_name is a valid object name.

    Parameters:
        bpy_obj_name: object name
        type: object type, default is 'MESH'

    Returns: 
        True if bpy_obj_name is a valid object name, otherwise False
    
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
    
    Parameters:
        armature_name (str): The name of the armature object.
        bone_names (list[str]): A list of names for the pose bones to be keyframed.
        rotations_per_bone (list[list] or np.ndarray): A list of lists or a numpy array containing rotation values for each bone.
        rotation_mode (str): The rotation mode to use for keyframing ('XYZ', 'QUATERNION', etc.).
        start_frame (int, optional): The starting frame for keyframing. Defaults to 1.

    Returns:
        None
    """
    assert __is_valid_object(armature_name, type='ARMATURE'), f"Armature object '{armature_name}' not found."

    # Get the armature object
    armature = bpy.data.objects.get(armature_name)

    # Check if the number of rotations matches the number of bone names
    assert len(rotations_per_bone) == len(bone_names), "Number of rotations_per_bone does not match number of bone names."

    for bone_name, rotations in zip(bone_names, rotations_per_bone):
        # Get the pose bone
        pose_bone = armature.pose.bones.get(bone_name)
        
        assert pose_bone is not None, f"Pose bone '{bone_name}' not found in armature '{armature_name}'."
        
        # Set the rotation mode
        pose_bone.rotation_mode = rotation_mode
        
        for ii, rotation in enumerate(rotations):
            frame = start_frame + ii
            # Set the current frame
            bpy.context.scene.frame_set(frame)
            
            # Enter pose mode
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='POSE')
            
            # Apply the rotation
            if rotation_mode == 'QUATERNION':
                pose_bone.rotation_quaternion = rotation
            elif rotation_mode == 'AXIS_ANGLE':
                pose_bone.rotation_axis_angle = rotation
            else:
                pose_bone.rotation_euler = rotation

            # Insert a keyframe for the bone's rotation
            if rotation_mode == 'QUATERNION':
                pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)
            elif rotation_mode == 'AXIS_ANGLE':
                pose_bone.keyframe_insert(data_path="rotation_axis_angle", frame=frame)
            else:
                pose_bone.keyframe_insert(data_path="rotation_euler", frame=frame)
            
            # Return to object mode
            bpy.ops.object.mode_set(mode='OBJECT')



def keyframe_single_pose_bone(
    armature_name: str, 
    bone_name: str, 
    rotations: list | tuple, 
    rotation_mode: str, 
    start_frame: int = 1
) -> None:
    """
    Keyframes the rotation of a single pose bone in a given armature object for a single frame.
    
    Parameters:
        armature_name (str): Name of the armature object.
        bone_name (str): Name of the pose bone to keyframe.
        rotations (list or tuple): Rotation values for the bone. The format depends on the rotation mode.
        rotation_mode (str): Rotation mode ('XYZ', 'QUATERNION', etc.).
        start_frame (int, optional): The starting frame for keyframing. Defaults to 1.

    Returns:
        None
    """
    keyframe_pose_bones(armature_name, [bone_name], [rotations], rotation_mode, start_frame)


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
    
    keyframe_single_pose_bone(armature_name, bone_names[0], euler_rotations2, 'XYZ', 1)

    quaternion_rotations = [mathutils.Euler(r).to_quaternion() for r in euler_rotations2]
    quaternion_rotations2 = [q.conjugated() for q in quaternion_rotations]

    keyframe_single_pose_bone(armature_name, bone_names[1], quaternion_rotations2, 'QUATERNION', 1)

    # Euler to Axis-Angle not supported
    # axis_angle_rotations = [mathutils.Euler(r).to_axis_angle() for r in euler_rotations]
    # axis_angle_rotations2 = [(-a[0], -a[1], -a[2]) for a in axis_angle_rotations]

    # Use quaternion to axis-angle
    axis_angle_rotations = [q.to_axis_angle() for q in quaternion_rotations] # list of (vector3, angle)
    axis_angle_rotations = [tuple(axis)+(angle,) for axis,angle  in axis_angle_rotations] # make list of tuples of 4 elements
    axis_angle_rotations2 = axis_angle_rotations[::-1]

    keyframe_pose_bones(armature_name, bone_names[2:], [axis_angle_rotations, axis_angle_rotations2], 'AXIS_ANGLE', 1)