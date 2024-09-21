"""Keyframe a single shape key (i.e. blend shape) or a list of shape keys.

Author: zhaoyafei0210@gmail.com

"""
import bpy
import numpy as np

__all__ = ['keyframe_single_shape_key', 'keyframe_shape_keys']


def __is_valid_object(bpy_obj_name: str, type: str = 'MESH') -> bool:
    """Check if bpy_obj_name is a valid object name.

    Parameters:
        bpy_obj_name: object name
        type: object type, default is 'MESH'

    Returns: 
        True if bpy_obj_name is a valid object name, otherwise False
    
    """
    return (bpy_obj_name and bpy_obj_name in bpy.data.objects.keys() and
            bpy.data.objects[bpy_obj_name].type == type)


def keyframe_shape_keys(
        mesh_name: str,
        shape_key_names: list[str],
        shape_key_values: list[list[float]] | np.ndarray,
        start_frame=1
    ) -> None:
    """Keyframe shape keys from a .csv file.

    Parameters:
        mesh_name: str, name of the mesh object
        shape_key_names: list of str, shape key names
        shape_key_values: list of list of float or np.ndarray, shape key values for each shape key
        start_frame: int, the frame to start keyframing from (default is 1)

    Returns:
        end_frame (int): The last frame number after keyframing.
    """
    # Get the mesh object
    mesh_obj = bpy.data.objects.get(mesh_name)
    
    assert mesh_obj, f"Mesh object '{mesh_name}' not found."
    assert __is_valid_object(mesh_name, type='MESH'), f"Object '{mesh_name}' is not a mesh object."

    # Get the shape key block of the mesh
    assert mesh_obj.data.shape_keys is not None, f"Mesh object '{mesh_name}' has no shape keys."
    
    # Ensure shape_key_names and shape_key_values have the same length
    assert len(shape_key_names) == len(shape_key_values), "Shape key names and values lists must have the same length."

    shape_keys = mesh_obj.data.shape_keys.key_blocks

    end_frame = start_frame

    # Loop through the shape keys and their corresponding values
    for key_name, key_values in zip(shape_key_names, shape_key_values):
        shape_key = shape_keys.get(key_name)
        
        if not shape_key:
            print(f"Shape key '{key_name}' not found in mesh '{mesh_name}'.")
            continue
        
        # Loop through the values for this shape key and keyframe them
        for i, value in enumerate(key_values):
            current_frame = start_frame + i
            shape_key.value = value
            shape_key.keyframe_insert(data_path="value", frame=current_frame)
            # print(f"Keyframe added for shape key '{key_name}' at frame {current_frame} with value {value}.")

        if end_frame < current_frame:
            end_frame = current_frame

    return end_frame


def keyframe_single_shape_key(
        mesh_name: str,
        shape_key_name: str,
        shape_key_values: list[float] | tuple | np.ndarray,
        start_frame: int = 1
    ) -> None:
    """
    Keyframe a single shape key with a list of values.

    Parameters:
        mesh_name: str, name of the mesh object
        shape_key_name: str, name of the shape key to keyframe
        shape_key_values: list[float] or tuple or np.ndarray, list of values to keyframe for the shape key
        start_frame: int, the frame to start keyframing from (default is 1)

    Returns:
        end_frame (int): The last frame number after keyframing.
    """
    end_frame = keyframe_shape_keys(mesh_name, [shape_key_name], [shape_key_values], start_frame)

    return end_frame


if __name__ == "__main__":
    import numpy as np
    
    num_frames = 24 * 3
    
    mesh_name = "Cube"
    shape_keys = ['Stretch', 'Squash', 'ScaleUp', 'ScaleDown']

    increment_values = np.linspace(0, 1, num_frames // 2)
    decrement_values = np.linspace(1, 0, num_frames // 2)

    inc_dec_values = np.concatenate([increment_values, decrement_values])
    dec_inc_values = np.concatenate([decrement_values, increment_values])

    shape_key_values = [
        inc_dec_values,
        dec_inc_values,
        dec_inc_values,
        inc_dec_values,
    ]

    end_frame = keyframe_single_shape_key(mesh_name, shape_keys[0], shape_key_values[0])
    print(f'End frame: {end_frame}')

    end_frame = keyframe_shape_keys(mesh_name, shape_keys[:2], shape_key_values[:2], end_frame + 1)
    print(f'End frame: {end_frame}')

    end_frame = keyframe_shape_keys(mesh_name, shape_keys, shape_key_values, end_frame + 1)
    print(f'End frame: {end_frame}')

