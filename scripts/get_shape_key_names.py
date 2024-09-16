"""Get shape-key names.

Author: zhaoyafei0210@gmail.com
"""
import bpy
import json

def get_shape_key_names(obj):
    return [sk.name for sk in obj.data.shape_keys.key_blocks]


def get_all_shape_key_names():
    all_shape_key_names = {}
    for sk in bpy.data.shape_keys:
        print(sk.name)
        kb_names = [kb.name for kb in sk.key_blocks]
        all_shape_key_names[sk.name] = kb_names

    return all_shape_key_names

all_shape_key_names = get_all_shape_key_names()
print(json.dumps(all_shape_key_names, indent=2))

if __name__ == "__main__":
    all_shape_key_names = get_all_shape_key_names()
    print(json.dumps(all_shape_key_names, indent=2))

    with open('/Users/zhaoyafei/downloads/all_shape_key_names.json', 'w') as f:
        json.dump(all_shape_key_names, f, indent=2)