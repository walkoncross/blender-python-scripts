import bpy
import numpy as np
import math


def print_object_matrix(obj_name='Cube'):
    """
    Refer to:
    https://docs.blender.org/api/current/bpy.types.Object.html?highlight=object#bpy.types.Object
    """
    obj = bpy.data.objects[obj_name]
    print('\n')
    print('*'*64)
    print('='*64)
    print('[Object] ' + obj_name +':: obj.name: \n', obj.name)
    print('[Object] ' + obj_name +':: obj.location: \n', obj.location)
    print('[Object] ' + obj_name +':: obj.rotation_mode: \n', obj.rotation_mode)
    if obj.rotation_mode == "QUATERNION":
        print('[Object] ' + obj_name +':: obj.rotation_quaternion: \n', obj.rotation_quaternion)
        print('[Object] ' + obj_name +':: obj.rotation_quaternion.to_matrix(): \n', obj.rotation_quaternion.to_matrix())
    elif obj.rotation_mode == "AXIS_ANGLE":
        print('[Object] ' + obj_name +':: obj.rotation_axis_angle: \n', obj.rotation_axis_angle[0:4])
        print('[Object] ' + obj_name +':: obj.rotation_axis_angle.to_matrix(): \n', obj.rotation_axis_angle.to_matrix())
    else:
        print('[Object] ' + obj_name +':: obj.rotation_euler: \n', [math.degrees(eu) for eu in obj.rotation_euler])
        print('[Object] ' + obj_name +':: obj.rotation_euler.to_matrix(): \n', obj.rotation_euler.to_matrix())

    print('-'*16)
    # matrix_basis:
    # Matrix access to location, rotation and scale (including deltas), before constraints and parenting are applied
    # Type
    # float multi-dimensional array of 4 * 4 items in [-inf, inf], default ((0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0))
    print('[Object] ' + obj_name +':: obj.matrix_basis: \n', obj.matrix_basis)
    # print('[Object] ' + obj_name +':: obj.matrix_basis @ obj.location: \n', obj.matrix_basis @ obj.location)
    
    print('-'*16)    
    # matrix_local:
    # Parent relative transformation matrix. Warning: Only takes into account object parenting, so e.g. in case of bone parenting you get a matrix relative to the Armature object, not to the actual parent bone
    # Type
    # float multi-dimensional array of 4 * 4 items in [-inf, inf], default ((0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0))    
    print('[Object] ' + obj_name +':: obj.matrix_local: \n', obj.matrix_local)
    # print('[Object] ' + obj_name +':: obj.matrix_local @ obj.location: \n', obj.matrix_local @ obj.location)
    
    print('-'*16)
    # matrix_parent_inverse
    # Inverse of object’s parent matrix at time of parenting
    # Type
    # float multi-dimensional array of 4 * 4 items in [-inf, inf], default ((1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0), (0.0, 0.0, 1.0, 0.0), (0.0, 0.0, 0.0, 1.0))    
    print('[Object] ' + obj_name +':: obj.matrix_parent_inverse: \n', obj.matrix_parent_inverse)
    # print('[Object] ' + obj_name +':: obj.matrix_parent_inverse @ obj.location: \n', obj.matrix_parent_inverse @ obj.location)
    
    print('-'*16)
    # matrix_world
    # Worldspace transformation matrix
    # Type
    # float multi-dimensional array of 4 * 4 items in [-inf, inf], default ((1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0), (0.0, 0.0, 1.0, 0.0), (0.0, 0.0, 0.0, 1.0))    
    print('[Object] ' + obj_name +':: obj.matrix_world: \n', obj.matrix_world)
    # print('[Object] ' + obj_name +':: obj.matrix_world @ obj.location: \n', obj.matrix_world @ obj.location)
    
    print('='*32)

    # matrix_local = matrix_parent_inverse * matrix_basis 
    # matrix_world = parent.matrix_world * matrix_local

    # matrix_parent_inverse = parent.matrix_world.inverted (Only at the momont of parenting)

    # 如果没有父节点： matrix_parent_inverse = Identity_4x4
    # matrix_local = matrix_basis = matrix_world

    print('='*32)
    matrix_local_calc = obj.matrix_parent_inverse @ obj.matrix_basis
    print('[Object] ' + obj_name +':: matrix_local_calc = obj.matrix_parent_inverse @ obj.matrix_basis: \n', matrix_local_calc)

    print('='*64)

    if obj.parent:
        print('='*64)
        print('PARENT')

        # print('[Object] ' + obj_name +':: obj.parent.name: \n', obj.parent.name)
        # print('[Object] ' + obj_name +':: obj.parent.location: \n', obj.parent.location)
        # print('[Object] ' + obj_name +':: obj.parent.rotation_mode: \n', obj.parent.rotation_mode)
        # print('[Object] ' + obj_name +':: obj.parent.rotation_euler: \n', obj.parent.rotation_euler)
        # print('[Object] ' + obj_name +':: obj.parent.rotation_euler.to_matrix(): \n', obj.parent.rotation_euler.to_matrix())
        # print('-'*16)

        print('='*32)

        matrix_world_calc = obj.parent.matrix_world @ obj.matrix_local
        print('[Object] ' + obj_name +':: matrix_world_calc = obj.parent.matrix_world @ obj.matrix_local: \n', matrix_world_calc)

        parent = obj.parent
        matrix_world_calc2 = obj.matrix_local
        while parent:
            matrix_world_calc2 = parent.matrix_local @ matrix_world_calc2
            parent = parent.parent

        print('-'*16)
        print('[Object] ' + obj_name +':: matrix_world_calc2 (by Product of a sequence): \n', matrix_world_calc2)

        # print('-'*16)
        # matrix_parent_inverse_calc = obj.parent.matrix_world.inverted()
        # print('[Object] ' + obj_name +':: matrix_parent_inverse_calc= obj.parent.matrix_world.inverted(): \n', matrix_parent_inverse_calc)
    
        print('='*64)

        print_object_matrix(obj.parent.name)


def add_parented_cubes():
    # Set mode
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # add a cube into the scene
    bpy.ops.mesh.primitive_cube_add()
    
    # set object name and objcet data (mesh) name
    obj_name1 = 'Cube1'
    bpy.context.object.name = obj_name1
    obj1 = bpy.data.objects[obj_name1]
    obj1.data.name = obj_name1

    # set object location and rotation
    obj1.location = [1, 1, 1]
    obj1.rotation_euler = [30, 45, 60]

    obj1.show_axis = True
    obj1.show_in_front = True

    print('bpy.context.selected_objects:', bpy.context.selected_objects)

    # add a second cube into the scene
    bpy.ops.mesh.primitive_cube_add()

    # set object name and objcet data (mesh) name
    obj_name2 = 'Cube2'
    bpy.context.object.name = obj_name2
    obj2 = bpy.data.objects[obj_name2]
    obj2.data.name = obj_name2

    # set object location and rotation
    obj2.location = [3, 3, 3]
    obj2.rotation_euler = [50, 75, 30]

    obj2.show_axis = True
    obj2.show_in_front = True

    obj2.parent= obj1
    # must set matrix_parent_inverse to keep obj2's location and rotatoin
    obj2.matrix_parent_inverse = obj1.matrix_world.inverted()

    # add a second cube into the scene
    bpy.ops.mesh.primitive_cube_add()

    # set object name and objcet data (mesh) name
    obj_name3 = 'Cube3'
    bpy.context.object.name = obj_name3
    obj3 = bpy.data.objects[obj_name3]
    obj3.data.name = obj_name3

    # set object location and rotation
    obj3.location = [5, 6, 7]
    obj3.rotation_euler = [80, 20, 100]

    obj3.show_axis = True
    obj3.show_in_front = True

    obj3.parent= obj2
    # must set matrix_parent_inverse to keep obj3's location and rotatoin
    obj3.matrix_parent_inverse = obj2.matrix_world.inverted()

    # set NEW location and rotation
    obj1.location = [-1, 1, 1]
    obj1.rotation_euler = [30, 45, 10]

    # set NEW location and rotation
    obj2.location = [3, 2, 5]
    obj2.rotation_euler = [50, 75, 30]

    # set NEW location and rotation
    obj3.location = [5, 8, 6]
    obj3.rotation_euler = [40, 30, 20]


def main_test():
    # add_parented_cubes()

    # obj_name = 'Cube1'
    # print_object_matrix(obj_name)

    obj_name = 'Cube3'
    print_object_matrix(obj_name)

    # obj_name = 'Cube'
    # print_object_matrix(obj_name)

    # obj_name = 'Cube.002'
    # print_object_matrix(obj_name)

main_test()