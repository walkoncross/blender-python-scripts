"""Set (min, max) value range for a shape key by name from an object.

Author: zhaoyafei0210@gmail.com
"""
import bpy


def set_minmax_range_for_shape_key(
        bpy_obj, 
        key_name, 
        min=0, 
        max=1.0
):
    """Set the minimum and maximum value range for a specific shape key.

    Args:
        bpy_obj (str or bpy.types.Object): The Blender object containing the shape keys.
        key_name (str): The name of the shape key to modify.
        min (float, optional): The minimum value for the shape key slider. Defaults to 0.
        max (float, optional): The maximum value for the shape key slider. Defaults to 1.0.

    Raises:
        KeyError: If the specified key_name is not found in the object's shape keys.

    Note:
        This function assumes that the object has shape keys. Make sure to check
        if bpy_obj.data.shape_keys exists before calling this function.
    """
    if isinstance(bpy_obj, str):
        bpy_obj = bpy.data.objects[bpy_obj]

    print(f'===> set_minmax_range_for_shape_key(): ')
    print(f'---> mesh: {bpy_obj.name}')
    print(f'---> key: {key_name}')
    print(f'---> min: {min}')
    print(f'---> max: {max}')

    if key_name not in bpy_obj.data.shape_keys.key_blocks:
        raise KeyError(f"Shape key '{key_name}' not found in object '{bpy_obj.name}'")

    # Set the active shape key
    bpy_obj.active_shape_key_index = bpy_obj.data.shape_keys.key_blocks.find(key_name)

    # Set the min and max values
    shape_key = bpy_obj.data.shape_keys.key_blocks[key_name]
    shape_key.slider_min = min
    shape_key.slider_max = max


def set_minmax_range_for_all_shape_key(
        bpy_obj,
        min=0, 
        max=1.0
):
    """Set the minimum and maximum value range for all shape keys of a Blender object.

    This function iterates through all shape keys of the given object and sets
    their minimum and maximum slider values to the specified values.

    Args:
        bpy_obj (str or bpy.types.Object): The Blender object containing the shape keys.
        min (float, optional): The minimum value for all shape key sliders. Defaults to 0.
        max (float, optional): The maximum value for all shape key sliders. Defaults to 1.0.

    Note:
        This function assumes that the object has shape keys. Make sure to check
        if bpy_obj.data.shape_keys exists before calling this function.

    Example:
        >>> obj = bpy.context.active_object
        >>> set_minmax_range_for_all_shape_key(obj, min=-1.0, max=1.0)
    """

    if isinstance(bpy_obj, str):
        bpy_obj = bpy.data.objects[bpy_obj]

    print(f'===> set_minmax_range_for_all_shape_key(): ')
    print(f'---> mesh: {bpy_obj.name}')
    print(f'---> min: {min}')
    print(f'---> max: {max}')

    if not bpy_obj.data.shape_keys:
        print(f"Warning: Object '{bpy_obj.name}' has no shape keys.")
        return

    # Iterate through all shape keys and set their min/max values
    for shape_key in bpy_obj.data.shape_keys.key_blocks:
        shape_key.slider_min = min
        shape_key.slider_max = max

    print(f"Set min/max range for all shape keys of '{bpy_obj.name}' to [{min}, {max}]")

if __name__ == '__main__':
    bpy_obj = bpy.context.active_object
    min_val = -1.0
    max_val = 1.0

    # key_name = 'JawOpen'
    # set_minmax_range_for_shape_key(bpy_obj, key_name, min_val, max_val)
    set_minmax_range_for_all_shape_key(bpy_obj, min_val, max_val)
