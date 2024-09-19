"""Rename a shape key

Author: zhaoyafei0210@gmail.com
"""
import bpy

__all__ = ['rename_shape_key']

def rename_shape_key(obj_name, key_name, new_key_name):
    """ rename a shape key, shape_keys[key_name].name = new_key_name
    """
    print('===> delete_shape_key_by_name(): ')
    print('---> Try to delete shape_key: {} from {}'.format(key_name, obj_name))

    obj = bpy.data.objects[obj_name]
    shape_keys = obj.data.shape_keys

    # setting the active shapekey
    index = shape_keys.key_blocks.keys().index(key_name)
    obj.active_shape_key_index = index

    # rename
    shape_keys.key_blocks[index].name = new_key_name
    # renaming might fail if new_key_name already in shape_keys.key_blocks.keys()
    new_key_name = shape_keys.key_blocks[index].name

    return new_key_name


if __name__ == '__main__':
    obj_name = 'Cube'
    key_name = 'ScaleUp'
    new_key_name = 'scale_up'

    new_shape_key = rename_shape_key(obj_name, key_name, new_key_name)
