"""Rename a shape key

Author: zhaoyafei0210@gmail.com
"""
import bpy


def rename_shape_key(bpy_obj, key_name, new_key_name):
    """ rename a shape key, shape_keys[key_name].name = new_key_name
    """
    print('===> delete_shape_key_by_name(): ')
    print('---> Try to delete shape_key: {} from {}'.format(key_name, bpy_obj.name))
    # setting the active shapekey
    index = bpy_obj.data.shape_keys.key_blocks.keys().index(key_name)
    bpy_obj.active_shape_key_index = index

    # rename
    bpy_obj.data.shape_keys.key_blocks[index].name = new_key_name
    # renaming might fail if new_key_name already in shape_keys.key_blocks.keys()
    new_key_name = bpy_obj.data.shape_keys.key_blocks[index].name

    return new_key_name


if __name__ == '__main__':
    bpy_obj = bpy.context.active_object
    key_name = 'Key 1'
    new_key_name = 'Key_1'

    new_shape_key = rename_shape_key(bpy_obj, key_name, new_key_name)
