import bpy
import math


def print_armature_object_info(armature_obj_name):
    # Set mode
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    arm_obj = bpy.data.objects[armature_obj_name]

    print('='*64)
    print('armature object name: ', armature_obj_name)
    print('[Object] ' + arm_obj.name + ':: arm_obj.name: \n', arm_obj.name)
    print('[Object] ' + arm_obj.name + ':: arm_obj.location: \n', arm_obj.location)
    print('[Object] ' + arm_obj.name + ':: arm_obj.rotation_mode: \n', arm_obj.rotation_mode)
    if arm_obj.rotation_mode == "QUATERNION":
        print('[Object] ' + arm_obj.name + ':: arm_obj.rotation_quaternion: \n', arm_obj.rotation_quaternion)
        print('[Object] ' + arm_obj.name + ':: arm_obj.rotation_quaternion.to_matrix(): \n', arm_obj.rotation_quaternion.to_matrix())
        euler = arm_obj.rotation_quaternion.to_euler('XYZ')
        print('[Object] ' + arm_obj.name + ':: arm_obj.rotation_quaternion.to_euler("XYZ"): \n', [math.degrees(eu) for eu in euler])
    elif arm_obj.rotation_mode == "AXIS_ANGLE":
        print('[Object] ' + arm_obj.name + ':: arm_obj.rotation_axis_angle: \n', arm_obj.rotation_axis_angle[0:4])
        print('[Object] ' + arm_obj.name + ':: arm_obj.rotation_axis_angle.to_matrix(): \n', arm_obj.rotation_axis_angle.to_matrix())
        euler = arm_obj.rotation_axis_angle.to_euler('XYZ')
        print('[Object] ' + arm_obj.name + ':: arm_obj.rotation_quaternion.to_euler("XYZ"): \n', [math.degrees(eu) for eu in euler])
    else:
        print('[Object] ' + arm_obj.name + ':: arm_obj.rotation_euler: \n', [math.degrees(eu) for eu in arm_obj.rotation_euler])
        print('[Object] ' + arm_obj.name + ':: arm_obj.rotation_euler.to_matrix(): \n', arm_obj.rotation_euler.to_matrix())

    print('-'*16)
    print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_basis: \n', arm_obj.matrix_basis)
    # print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_basis X arm_obj.location: \n', arm_obj.matrix_basis @ arm_obj.location)
    
    print('-'*16)
    print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_local: \n', arm_obj.matrix_local)
    # print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_local X arm_obj.location: \n', arm_obj.matrix_local @ arm_obj.location)
    
    print('-'*16)
    print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_parent_inverse: \n', arm_obj.matrix_parent_inverse)
    # print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_parent_inverse X arm_obj.location: \n', arm_obj.matrix_parent_inverse @ arm_obj.location)
    
    print('-'*16)
    print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_world: \n', arm_obj.matrix_world)
    # print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_world X arm_obj.location: \n', arm_obj.matrix_world @ arm_obj.location)

    print('-'*16)
    print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_basis.inverted(): \n', arm_obj.matrix_basis.inverted())
    # print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_basis X arm_obj.location: \n', arm_obj.matrix_basis @ arm_obj.location)
    
    print('-'*16)
    print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_local.inverted(): \n', arm_obj.matrix_local.inverted())
    # print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_local X arm_obj.location: \n', arm_obj.matrix_local @ arm_obj.location)
    
    print('-'*16)
    print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_parent_inverse.inverted(): \n', arm_obj.matrix_parent_inverse.inverted())
    # print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_parent_inverse X arm_obj.location: \n', arm_obj.matrix_parent_inverse @ arm_obj.location)
    
    print('-'*16)
    print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_world.inverted(): \n', arm_obj.matrix_world.inverted())
    # print('[Object] ' + arm_obj.name + ':: arm_obj.matrix_world X arm_obj.location: \n', arm_obj.matrix_world @ arm_obj.location)

    print('='*64)


def print_armature_restbones_info(armature_obj_name):
    """    
    refer to: 
    https://docs.blender.org/api/current/bpy.types.Armature.html?highlight=armature#bpy.types.Armature.bones
    https://docs.blender.org/api/current/bpy.types.ArmatureBones.html#bpy.types.ArmatureBones
    https://docs.blender.org/api/current/bpy.types.Bone.html#bpy.types.Bone

    """
    # Set mode
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    arm_obj = bpy.data.objects[armature_obj_name]
    arm_data = arm_obj.data

    print('='*64)
    print('armature object name: ', armature_obj_name)
    print('[Object] ' + arm_obj.name + ':: arm_obj.name: \n', arm_obj.name)

    print('='*64)
    print('armature.bones info')

    for Bone in arm_data.bones:
        print('='*32)

        print('-'*16)
        print('[Bone] ' + Bone.name + ':: Bone.name: \n', Bone.name)

        print('-'*16)
        # head: Location of head end of the bone relative to its parent
        print('[Bone] ' + Bone.name + ':: Bone.head: \n', Bone.head)

        print('-'*16)
        # tail: Location of tail end of the bone relative to its parent
        print('[Bone] ' + Bone.name + ':: Bone.tail: \n', Bone.tail)

        print('-'*16)
        # head_local: Location of head end of the bone relative to armature
        print('[Bone] ' + Bone.name + ':: Bone.head_local: \n', Bone.head_local)

        print('-'*16)
        # tail_local: Location of tail end of the bone relative to armature
        print('[Bone] ' + Bone.name + ':: Bone.tail_local: \n', Bone.tail_local)

        print('-'*16)
        # head: Location of head end of the bone relative to its parent
        print('[Bone] ' + Bone.name + ':: Bone.matrix.inverted() @ Bone.head: \n', Bone.matrix.inverted() @ Bone.head)

        print('-'*16)
        # head_local: Location of head end of the bone relative to armature
        print('[Bone] ' + Bone.name + ':: Bone.matrix_local.inverted() @ Bone.head_local: \n', Bone.matrix_local.inverted() @ Bone.head_local)

        print('-'*16)
        # tail: Location of tail end of the bone relative to its parent
        print('[Bone] ' + Bone.name + ':: Bone.matrix.inverted() @ Bone.tail: \n', Bone.matrix.inverted() @ Bone.tail)

        print('-'*16)
        # tail: Location of tail end of the bone relative to its parent
        print('[Bone] ' + Bone.name + ':: Bone.matrix_local.inverted() @ Bone.tail_local: \n', Bone.matrix_local.inverted() @ Bone.tail_local)

        print('-'*16)
        # vector: The direction this bone is pointing. Utility function for (tail - head)
        print('[Bone] ' + Bone.name + ':: Bone.vector: \n', Bone.vector)

        print('-'*16)
        # length: Length of the bone
        print('[Bone] ' + Bone.name + ':: Bone.length: \n', Bone.length)
        print('-'*16)

        print('-'*16)
        # matrix: 3x3 bone matrix (relative to its parent)
        print('[Bone] ' + Bone.name + ':: Bone.matrix: \n', Bone.matrix)

        print('-'*16)
        # matrix_local: 4x4 bone matrix relative to armature
        print('[Bone] ' + Bone.name + ':: Bone.matrix_local: \n', Bone.matrix_local)

        print('-'*16)
        # matrix: 3x3 bone matrix (relative to its parent)
        print('[Bone] ' + Bone.name + ':: Bone.matrix.inverted(): \n', Bone.matrix.inverted())

        print('-'*16)
        # matrix_local: 4x4 bone matrix relative to armature
        print('[Bone] ' + Bone.name + ':: Bone.matrix_local.inverted(): \n', Bone.matrix_local.inverted())

        if Bone.parent:
            matrix_calc = Bone.parent.matrix_local.inverted() @ Bone.matrix_local
            print('-'*16)
            # matrix: 3x3 bone matrix (relative to its parent)
            print('[Bone] ' + Bone.name + ':: matrix_calc = Bone.parent.matrix_local.inverted() @ Bone.matrix_local.inverted(): \n', matrix_calc)

        print('-'*16)
        # x_axis: Vector pointing down the x-axis of the bone.  (relative to its parent)
        print('[Bone] ' + Bone.name + ':: Bone.x_axis: \n', Bone.x_axis)
        # y_axis: Vector pointing down the y-axis of the bone. (relative to its parent)
        print('[Bone] ' + Bone.name + ':: Bone.y_axis: \n', Bone.y_axis)
        # z_axis: Vector pointing down the z-axis of the bone. (relative to its parent)
        print('[Bone] ' + Bone.name + ':: Bone.z_axis: \n', Bone.z_axis)

        print('='*32)

    print('='*64)

    # Set mode
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def print_armature_editbones_info(armature_obj_name):
    """ 
    refer to: 
        https://docs.blender.org/api/current/bpy.types.Armature.html?highlight=armature#bpy.types.Armature.edit_bones
        https://docs.blender.org/api/current/bpy.types.ArmatureEditBones.html#bpy.types.ArmatureEditBones
        https://docs.blender.org/api/current/bpy.types.EditBone.html?highlight=edit_bones

    """
    
    arm_obj = bpy.data.objects[armature_obj_name]
    arm_data = arm_obj.data

    # Set mode
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

    print('='*64)
    print('armature object name: ', armature_obj_name)
    print('[Object] ' + arm_obj.name + ':: arm_obj.name: \n', arm_obj.name)

    print('='*32)
    print('armature.edit_bones info')
    print('='*32)

    for EditBone in arm_data.edit_bones:
        print('='*32)

        print('-'*16)
        print('[EditBone] ' + EditBone.name + ':: EditBone.name: \n', EditBone.name)
        
        print('-'*16)
        # head: Location of head end of the bone (relative to armature)
        print('[EditBone] ' + EditBone.name + ':: EditBone.head: \n', EditBone.head)

        print('-'*16)
        # tail: Location of tail end of the bone (relative to armature)
        print('[EditBone] ' + EditBone.name + ':: EditBone.tail: \n', EditBone.tail)

        print('-'*16)
        # vector: The direction this bone is pointing. Utility function for (tail - head)
        print('[EditBone] ' + EditBone.name + ':: EditBone.vector: \n', EditBone.vector)

        print('-'*16)
        # length: Length of the bone
        print('[EditBone] ' + EditBone.name + ':: Bone.length: \n', EditBone.length)

        print('-'*16)
        # roll: Bone rotation around head-tail axis
        print('[EditBone] ' + EditBone.name + ':: EditBone.roll: \n', math.degrees(EditBone.roll))

        print('-'*16)
        # matrix: Matrix combining location and rotation of the bone (head position, direction and roll), 
        # in armature space (does not include/support bone’s length/size)
        print('[EditBone] ' + EditBone.name + ':: EditBone.matrix: \n', EditBone.matrix)

        print('-'*16)
        # matrix: Matrix combining location and rotation of the bone (head position, direction and roll), 
        # in armature space (does not include/support bone’s length/size)
        print('[EditBone] ' + EditBone.name + ':: EditBone.matrix.inverted(): \n', EditBone.matrix.inverted())

        print('-'*16)
        # x_axis: Vector pointing down the x-axis of the bone.  (relative to armature)
        print('[EditBone] ' + EditBone.name + ':: EditBone.x_axis: \n', EditBone.x_axis)
        # y_axis: Vector pointing down the y-axis of the bone. (relative to armature)
        print('[EditBone] ' + EditBone.name + ':: EditBone.y_axis: \n', EditBone.y_axis)
        # z_axis: Vector pointing down the z-axis of the bone. (relative to armature)
        print('[EditBone] ' + EditBone.name + ':: EditBone.z_axis: \n', EditBone.z_axis)

        # print('-'*16)
        # # x_axis: Vector pointing down the x-axis of the bone.  (relative to armature)
        # print('[EditBone] ' + EditBone.name + ':: EditBone.matrix @ EditBone.x_axis: \n', EditBone.matrix @ EditBone.x_axis)
        # # y_axis: Vector pointing down the y-axis of the bone. (relative to armature)
        # print('[EditBone] ' + EditBone.name + ':: EditBone.matrix @ EditBone.y_axis: \n', EditBone.matrix @ EditBone.y_axis)
        # # z_axis: Vector pointing down the z-axis of the bone. (relative to armature)
        # print('[EditBone] ' + EditBone.name + ':: EditBone.matrix @ EditBone.z_axis: \n', EditBone.matrix @ EditBone.z_axis)    
        #     
        print('='*32)
    
    print('='*64)

    # Set mode
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def print_armature_posebones_info(armature_obj_name):
    """
        refer to: 
        https://docs.blender.org/api/current/bpy.types.Object.html?highlight=types%20object#bpy.types.Object.pose
        https://docs.blender.org/api/current/bpy.types.Pose.html?highlight=pose#bpy.types.Pose
        https://docs.blender.org/api/current/bpy.types.PoseBone.html?highlight=posebone#bpy.types.PoseBone
    """
    # Set mode
    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    arm_obj = bpy.data.objects[armature_obj_name]
    pose_bones = arm_obj.pose.bones

    print('='*64)
    print('armature object name: ', armature_obj_name)
    print('[Object] ' + arm_obj.name + ':: arm_obj.name: \n', arm_obj.name)

    print('='*32)
    print('armature.edit_bones info')

    for PoseBone in pose_bones:
        print('='*32)
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.name: \n', PoseBone.name)

        print('-'*16)
        # bone: Bone associated with this PoseBone
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.bone: \n', PoseBone.bone)

        print('-'*16)
        # parent: Parent of this pose bone, type: PoseBone
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.parent: \n', PoseBone.parent)
        
        print('-'*16)
        # child: Child of this pose bone, type: PoseBone
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.child: \n', PoseBone.child)
        
        print('-'*16)
        # head: Location of head of the channel’s bone (relative to armature)
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.head: \n', PoseBone.head)
        
        print('-'*16)
        # tail: Location of tail of the channel’s bone (relative to armature)
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.tail: \n', PoseBone.tail)

        print('-'*16)
        # vector: The direction this bone is pointing. Utility function for (tail - head)
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.vector: \n', PoseBone.vector)
       
        print('-'*16)
        # length: Length of the bone
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.length: \n', PoseBone.length)

        print('-'*16)
        # matrix: Final 4x4 matrix after constraints and drivers are applied (object space)
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.matrix: \n', PoseBone.matrix)

        print('-'*16)
        # matrix_basis: Alternative access to location/scale/rotation relative to the parent and own rest bone
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.matrix_basis: \n', PoseBone.matrix_basis)

        print('-'*16)
        # matrix_channel: 4x4 matrix, before constraints
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.matrix_channel: \n', PoseBone.matrix_channel)

        print('-'*16)
        # matrix: Final 4x4 matrix after constraints and drivers are applied (object space)
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.matrix.inverted(): \n', PoseBone.matrix.inverted())

        print('-'*16)
        # matrix_basis: Alternative access to location/scale/rotation relative to the parent and own rest bone
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.matrix_basis.inverted(): \n', PoseBone.matrix_basis.inverted())

        print('-'*16)
        # matrix_channel: 4x4 matrix, before constraints
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.matrix_channel.inverted(): \n', PoseBone.matrix_channel.inverted())

        print('-'*16)
        # matrix_channel: 4x4 matrix, before constraints
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.bone.matrix_local: \n', PoseBone.bone.matrix_local)

        # print('-'*16)
        # # matrix_channel: 4x4 matrix, before constraints
        # print('[PoseBone] ' + PoseBone.name + ':: PoseBone.bone.matrix_local.inverted() @ PoseBone.matrix: \n', PoseBone.bone.matrix_local.inverted() @ PoseBone.matrix)

        print('-'*16)
        # matrix: Final 4x4 matrix after constraints and drivers are applied (object space)
        matrix_calc = PoseBone.bone.matrix_local @ PoseBone.matrix_basis
        parent = PoseBone.parent
        while parent:
            matrix_calc = parent.bone.matrix_local @ parent.matrix_basis @ parent.bone.matrix_local.inverted() @ matrix_calc
            parent = parent.parent
        print('matrix_calc (by Product of a sequence) : \n', matrix_calc)

        parent = PoseBone.parent
        if parent:
            print('-'*16)
            # matrix: Final 4x4 matrix after constraints and drivers are applied (object space)
            matrix_calc2 = parent.matrix @ parent.bone.matrix_local.inverted() @ PoseBone.bone.matrix_local @ PoseBone.matrix_basis
            print('matrix_calc2 = parent.matrix @ parent.bone.matrix_local.inverted() @ PoseBone.bone.matrix_local @ PoseBone.matrix_basis : \n', matrix_calc2)

        print('-'*16)
        # matrix_channel: 4x4 matrix, before constraints
        matrix_channel_calc = PoseBone.matrix @ PoseBone.bone.matrix_local.inverted()
        print('matrix_channel_calc = PoseBone.matrix @ PoseBone.bone.matrix_local.inverted(): \n', matrix_channel_calc)

        if PoseBone.parent:
            print('-'*16)
            # matrix_channel: 4x4 matrix, before constraints
            print('[PoseBone] ' + PoseBone.name + ':: PoseBone.parent.matrix_channel.inverted() @ PoseBone.matrix_channel: \n', PoseBone.parent.matrix_channel.inverted() @ PoseBone.matrix_channel)

        print('-'*16)
        # rotation_mode: 
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.rotation_mode: \n', PoseBone.rotation_mode)

        print('-'*16)

        if PoseBone.rotation_mode == "QUATERNION":
            print('[PoseBone] ' + PoseBone.name + ':: PoseBone.rotation_quaternion: \n', PoseBone.rotation_quaternion)
            print('[PoseBone] ' + PoseBone.name + ':: PoseBone.rotation_quaternion.to_matrix(): \n', PoseBone.rotation_quaternion.to_matrix())
            euler = PoseBone.rotation_quaternion.to_euler('XYZ')
            print('[PoseBone] ' + PoseBone.name + ':: PoseBone.rotation_quaternion.to_euler("XYZ"): \n', [math.degrees(eu) for eu in euler])
        elif PoseBone.rotation_mode == "AXIS_ANGLE":
            print('[PoseBone] ' + PoseBone.name + ':: PoseBone.rotation_axis_angle: \n', PoseBone.rotation_axis_angle[0:4])
            print('[PoseBone] ' + PoseBone.name + ':: PoseBone.rotation_axis_angle.to_matrix(): \n', PoseBone.rotation_axis_angle.to_matrix())
            euler = PoseBone.rotation_axis_angle.to_euler('XYZ')
            print('[PoseBone] ' + PoseBone.name + ':: PoseBone.rotation_quaternion.to_euler("XYZ"): \n', [math.degrees(eu) for eu in euler])
        else:
            # rotation_euler: Rotation in Eulers
            print('[PoseBone] ' + PoseBone.name + ':: PoseBone.rotation_euler: \n', [math.degrees(eu) for eu in PoseBone.rotation_euler])
            print('[PoseBone] ' + PoseBone.name + ':: PoseBone.rotation_euler.to_matrix(): \n', PoseBone.rotation_euler.to_matrix())

        print('-'*16)
        # x_axis: Vector pointing down the x-axis of the bone.  (relative to armature)
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.x_axis: \n', PoseBone.x_axis)
        # y_axis: Vector pointing down the y-axis of the bone. (relative to armature)
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.y_axis: \n', PoseBone.y_axis)
        # z_axis: Vector pointing down the z-axis of the bone. (relative to armature)
        print('[PoseBone] ' + PoseBone.name + ':: PoseBone.z_axis: \n', PoseBone.z_axis)

        # print('-'*16)
        # # x_axis: Vector pointing down the x-axis of the bone.  (relative to armature)
        # print('[PoseBone] ' + PoseBone.name + ':: PoseBone.matrix @ PoseBone.x_axis: \n', PoseBone.matrix @ PoseBone.x_axis)
        # # y_axis: Vector pointing down the y-axis of the bone. (relative to armature)
        # print('[PoseBone] ' + PoseBone.name + ':: PoseBone.matrix @ PoseBone.y_axis: \n', PoseBone.matrix @ PoseBone.y_axis)
        # # z_axis: Vector pointing down the z-axis of the bone. (relative to armature)
        # print('[PoseBone] ' + PoseBone.name + ':: PoseBone.matrix @ PoseBone.z_axis: \n', PoseBone.matrix @ PoseBone.z_axis)        

        print('='*32)
    
    print('='*64)
    # Set mode
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def add_armature_with_bones(bone_num=4):
    pass

# armature_obj_name = 'frank_smplx'
armature_obj_name = 'Armature'
print('\n'*4)
print('*'*64)
print_armature_object_info(armature_obj_name)
print_armature_restbones_info(armature_obj_name)
print_armature_editbones_info(armature_obj_name)
print_armature_posebones_info(armature_obj_name)