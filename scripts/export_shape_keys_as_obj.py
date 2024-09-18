"""
Export all Shape Keys as OBJs in Blender

Author: zhaoyafei0210@gmail.com
"""

import bpy
import os
import os.path as osp



def export_shape_keys_as_obj(obj_name, export_path):
    """
    Exports all shape keys of a specified Blender object as OBJ files.

    Parameters:
    obj_name (str): The name of the object whose shape keys are to be exported.
    export_path (str): The directory path where the OBJ files will be saved.

    The function creates the export directory if it does not exist,
    resets all shape keys to zero, and exports each shape key as a separate OBJ file.
    """
    # Reference the active object
    print('=' * 16)
    print(f'Export Shape Keys as OBJs for: {obj_name}, to: {export_path}')

    obj = bpy.data.objects[obj_name]

    # CHANGE THIS to the folder you want to save your OBJ files in
    # NOTE: no spaces, no trailing slash

    if not osp.exists(export_path):
        print('Export path does not exist, creating...')
        os.makedirs(export_path)

    # only select the obj_name object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    key_blocks = obj.data.shape_keys.key_blocks

    # Reset all shape keys to 0 (skipping the Basis shape on index 0
    for key_block in key_blocks[1:]:
        key_block.value = 0

    # Export basis
    key_block = key_blocks[0]
    # Set OBJ file path and Export OBJ
    obj_file_path = osp.join(export_path, '00_' + key_block.name + ".obj")
    bpy.ops.wm.obj_export(
        filepath=obj_file_path, 
        export_selected_objects=True, 
        global_scale=1
    )

    # key_block.value = 0  # Reset shape key value to 0

    # Iterate over shape key blocks and save each as an OBJ file
    for key_block in obj.data.shape_keys.key_blocks[1:]:
        key_block.value = 1.0  # Set shape key value to max

        # Set OBJ file path and Export OBJ
        obj_file_path = osp.join(export_path, key_block.name + ".obj")
        bpy.ops.wm.obj_export(
            filepath=obj_file_path, 
            export_selected_objects=True, 
            global_scale=1
        )

        key_block.value = 0  # Reset shape key value to 0

    print('Export complete.')


if __name__ == "__main__":
    obj_name = 'Cube'
    export_path = "/Users/zhaoyafei/downloads/exported_blendshape_objs"

    export_shape_keys_as_obj(
        obj_name, 
        export_path
    )
