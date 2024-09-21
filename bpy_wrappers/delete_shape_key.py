"""Delete a shape key by name from an object.

Author: zhaoyafei0210@gmail.com
"""
import bpy


__all__ = ['delete_shape_key_by_name']


def delete_shape_key_by_name(obj_name, key_name):
    """Delete a shape key by its name from the specified object.

    Args:
        obj_name (str): The name of the object containing the shape key.
        key_name (str): The name of the shape key to delete.
    """
    print('===> delete_shape_key_by_name(): ')
    print('---> Try to delete shape_key: {} from {}'.format(key_name, obj_name))

    obj = bpy.data.objects[obj_name]
    if obj is None:
        print(f"Object '{obj_name}' not found.")
        return
    
    # Check if the object has shape keys
    if not obj.data.shape_keys:
        print(f"Object '{obj_name}' has no shape keys.")
        return
    
    # select
    obj.select_set(True)

    bpy.context.view_layer.objects.active = obj
    
    # setting the active shapekey
    key_blocks = obj.data.shape_keys.key_blocks
    shape_key = key_blocks.get(key_name)
    
    if shape_key is None:
        print(f"Shape key '{key_name}' not found.")
        return

    index = key_blocks.keys().index(key_name)
    obj.active_shape_key_index = index

    # delete it
    state = bpy.ops.object.shape_key_remove(all=False)
    if 'FINISHED' in state:
        print('---> Finised to delete shape_key: ', key_name)
    else:
        print('---> Failed to delete shape_key: ', key_name)


if __name__ == '__main__':
    obj_name = 'Cube'
    key_name = 'ScaleDown'
    delete_shape_key_by_name(obj_name, key_name)
