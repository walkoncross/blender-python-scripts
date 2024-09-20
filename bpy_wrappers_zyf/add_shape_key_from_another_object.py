"""Delete a shape key by name from an object.

Author: zhaoyafei0210@gmail.com
"""
import bpy


__all__ = ['add_shape_key_from_target_object']


def add_shape_key_from_target_object(
        basis_obj_name, 
        target_obj_name, 
        shape_key_name=''
    ):
    """Add a shape key to the basis object from the target object. 
    Both objects must have the same topology (vertex order).
    
    Args:
        basis_obj_name: The name of the object to which the shape key will be added.
        target_obj_name: The name of the object from which the shape key will be taken.
        shape_key_name: The name of the new shape key (default is '', means the same name as the target object).
    """
    print('===> add_shape_key_from_target_object()')

    basis_obj = bpy.data.objects[basis_obj_name]
    target_obj = bpy.data.objects[target_obj_name]

    if basis_obj.type != 'MESH':
        print(f"Object '{basis_obj_name}' is not a mesh.")
        return
    
    if target_obj.type != 'MESH':
        print(f"Object '{target_obj_name}' is not a mesh.")
        return

    # Ensure the object has a basis shape key
    if basis_obj.data.shape_keys is None:
        basis_obj.shape_key_add(name="Basis")  # Add basis shape
        print('---> Add basis shape key')

    # deselect all
    bpy.ops.object.select_all(action='DESELECT')

    print('---> basis object name: ', basis_obj_name)
    print('---> another object name: ', target_obj_name)

    # select
    target_obj.select_set(True)
    basis_obj.select_set(True)

    bpy.context.view_layer.objects.active = basis_obj

    state = bpy.ops.object.join_shapes()

    if shape_key_name is None or shape_key_name is '':
        shape_key_name = target_obj_name

    if 'FINISHED' in state:
        # new_shape_key = basis_obj.data.shape_keys.key_blocks[-1].name
        basis_obj.data.shape_keys.key_blocks[-1].name = shape_key_name
        print('---> Added shape key name: ', shape_key_name)
    else:
        shape_key_name = None
        print('---> Failed to add shape key')

    return shape_key_name


if __name__ == '__main__':
    basis_obj_name = 'Cube'

    create_new_cubes = False
    # basis_obj_name = 'POLYWINK_Bella'
    # target_obj_name = 'jawOpen'
    # target_obj_name = 'cheekPuff'
    # target_obj_name = 'mouthRight'

    target_obj_name = 'cube-bigger'

    if create_new_cubes:
        # create a bigger cube with size 4
        bpy.ops.mesh.primitive_cube_add(
            size=4, 
            enter_editmode=False, 
            align='WORLD', 
            location=(0, 0, 0), 
            scale=(1, 1, 1)
        )

        # rename it
        bpy.context.object.name = target_obj_name

    # add shape key
    add_shape_key_from_target_object(basis_obj_name, target_obj_name, 'ScaleUp')

    target_obj_name = 'cube-smaller'

    if create_new_cubes:
        # create a smaller cube with size 1
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            enter_editmode=False, 
            align='WORLD', 
            location=(0, 0, 0), 
            scale=(1, 1, 1)
        )

        # rename it
        bpy.context.object.name = target_obj_name

    # add shape key
    add_shape_key_from_target_object(basis_obj_name, target_obj_name, 'ScaleDown')
