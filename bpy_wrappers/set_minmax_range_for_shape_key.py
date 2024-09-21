"""Delete a shape key by name from an object.

Author: zhaoyafei0210@gmail.com
"""
import bpy


def set_minmax_range_for_shape_key(bpy_obj, key_name, min=0, max=1.0):
    """ Delete shape_key by name
    """
    print('===> set_minmax_range_for_all_shape_key(): ')
    print('---> mesh: {}'.format(bpy_obj.name))
    print('---> min: {}'.format(min))
    print('---> max: {}'.format(max))

    # bpy_obj = bpy.data.objects[mesh_obj_name]

    # setting the active shapekey
    index = bpy_obj.data.shape_keys.key_blocks.keys().index(key_name)
    bpy_obj.active_shape_key_index = index

    bpy_obj.data.shape_keys.key_blocks[key_name].slider_min = min
    bpy_obj.data.shape_keys.key_blocks[key_name].slider_max = max


def set_minmax_range_for_all_shape_key(bpy_obj, min=0, max=1.0):
    """ Delete shape_key by name
    """
    print('===> set_minmax_range_for_all_shape_key(): ')
    print('---> mesh: {}'.format(bpy_obj.name))
    print('---> min: {}'.format(min))
    print('---> max: {}'.format(max))

    # bpy_obj = bpy.data.objects[mesh_obj_name]

    # setting the active shapekey
    for ind, kb in enumerate(bpy_obj.data.shape_keys.key_blocks):
        bpy_obj.active_shape_key_index = ind
        key_name = kb.name

        bpy_obj.data.shape_keys.key_blocks[key_name].slider_min = min
        bpy_obj.data.shape_keys.key_blocks[key_name].slider_max = max


if __name__ == '__main__':
    bpy_obj = bpy.context.active_object
    min_val = -1.0
    max_val = 1.0

    key_name = 'jawOpen'
    set_minmax_range_for_shape_key(bpy_obj, key_name, min_val, max_val)
    # set_minmax_range_for_all_shape_key(bpy_obj, min_val, max_val)
