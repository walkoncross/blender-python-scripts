"""Get shape-key names.

Author: zhaoyafei0210@gmail.com
"""
import bpy


__all__ = ['get_shape_key_index']



def get_shape_key_index(
        mesh_obj: str | bpy.types.Object,
        shape_key_names: list[str],
        case_insensitive: bool = False
) -> list[int]:
    """Get the indices of shape keys by their names.

    Parameters:
        mesh_obj: str or bpy.types.Object, the mesh object containing the shape keys
        shape_key_names: list[str], names of the shape keys
        case_insensitive: bool, optional, default is False. If True, the comparison is case-insensitive.

    Returns:
        list[int]: A list of indices of the shape keys, or -1 if the shape key is not found.
    """
    if isinstance(mesh_obj, str):
        mesh_obj = bpy.data.objects[mesh_obj]
    obj_shape_key_names = list(mesh_obj.data.shape_keys.key_blocks.keys())

    if case_insensitive:
        shape_key_names = [name.lower() for name in shape_key_names]
        obj_shape_key_names = [name.lower() for name in obj_shape_key_names]

    shape_key_index = []
    for name in shape_key_names:
        if name in obj_shape_key_names:
            idx = obj_shape_key_names.index(name)
        else:
            idx = -1

        shape_key_index.append(idx)

    return shape_key_index


if __name__ == "__main__":
    mesh_obj = 'Cube'

    shape_key_names = ['stretch', 'squash']

    shape_key_index = get_shape_key_index(mesh_obj, shape_key_names, case_insensitive=True)
    print(f'shape_key_index: {shape_key_index}')