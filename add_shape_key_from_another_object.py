"""Delete a shape key by name from an object.

Author: zhaoyafei0210@gmail.com
"""
import bpy


def add_shape_key_from_another_object(basis_obj, another_obj):
    """ Add a shape key for basis_obj from another_obj, basis_obj and another_obj must have the same topo (vertex order).
    """
    print('===> add_shape_key_from_another_object()')

    # deselect all
    bpy.ops.object.select_all(action='DESELECT')

    print('---> basis object name: ', basis_obj.name)
    print('---> another object name: ', another_obj.name)
    
    # select
    another_obj.select_set(True)
    basis_obj.select_set(True)
    
    bpy.context.view_layer.objects.active = basis_obj

    state = bpy.ops.object.join_shapes()
    if 'FINISHED' in state:
        new_shape_key = basis_obj.data.shape_keys.key_blocks[-1].name
    else:
        new_shape_key = None

    print('---> Added shape key name: ', new_shape_key)

    return new_shape_key


def add_shape_key_by_obj_names(basis_obj_name, another_obj_name):
    """ Add a shape key for basis_obj (by name) from another_obj (by name), basis_obj and another_obj must have the same topo (vertex order).
    """
    print('===> add_shape_key_by_obj_names()')
    basis_obj = bpy.data.objects[basis_obj_name]
    another_obj = bpy.data.objects[another_obj_name]

    add_shape_key_from_another_object(basis_obj, another_obj)


if __name__ == '__main__':
    # basis_obj_name = 'Cube'
    # another_obj_name = 'cube-deform1'
    basis_obj_name = 'POLYWINK_Bella'
    # another_obj_name = 'jawOpen'
    # another_obj_name = 'cheekPuff'
    another_obj_name = 'mouthRight'

    add_shape_key_by_obj_names(basis_obj_name, another_obj_name)
