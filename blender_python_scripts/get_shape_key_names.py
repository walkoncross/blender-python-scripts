"""Get shape-key names.

Author: zhaoyafei0210@gmail.com
"""
import bpy
import json

def get_shape_key_names(obj_name):
    """
    Get shape-key names of a mesh object

    Parameters:
        obj_name: Name of the mesh object.

    Returns:
        shape_key_names: List of shape-key names.
    """
    obj = bpy.data.objects[obj_name]
    return [sk.name for sk in obj.data.shape_keys.key_blocks]


def get_all_shape_key_names():
    """
    Get shape-key names of all shape-key data.

    Returns:
        all_shape_key_names: list of list of shape-key names.
    """
    all_shape_key_names = []
    for sk in bpy.data.shape_keys:
        # print(sk.name)

        kb_names = [kb.name for kb in sk.key_blocks]
        # all_shape_key_names[sk.name] = kb_names
        all_shape_key_names.append(
            {
                'user_name': sk.user.name,
                'shape_key': sk.name,
                'key_block_names': kb_names
            }
        )

    return all_shape_key_names


if __name__ == "__main__":
    print(get_shape_key_names('Cube'))

    all_shape_key_names = get_all_shape_key_names()
    print(json.dumps(all_shape_key_names, indent=2))

    with open('/Users/zhaoyafei/downloads/all_shape_key_names.json', 'w') as f:
        json.dump(all_shape_key_names, f, indent=2)