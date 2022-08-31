"""Delete a shape key by name from an object.

Author: zhaoyafei0210@gmail.com
"""
import bpy


def delete_shape_key_by_name(bpy_obj, key_name):
    """ Delete shape_key by name
    """
    print('===> delete_shape_key_by_name(): ')
    print('---> Try to delete shape_key: {} from {}'.format(key_name, bpy_obj.name))

    # setting the active shapekey
    index = bpy_obj.data.shape_keys.key_blocks.keys().index(key_name)
    bpy_obj.active_shape_key_index = index

    # delete it
    state = bpy.ops.object.shape_key_remove()
    if 'FINISHED' in state:
        print('---> Finised to delete shape_key: ', key_name)
    else:
        print('---> Failed to delete shape_key: ', key_name)


if __name__ == '__main__':
    bpy_obj = bpy.context.active_object
    key_name = 'Key 1'
    delete_shape_key_by_name(bpy_obj, key_name)
