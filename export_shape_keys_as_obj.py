# Export all Shape Keys as OBJs in Blender
# Version 1.0 – August 2017
# =========================================
# Original Script by Tlousky
# https://blender.stackexchange.com/questions/86674/how-to-batch-export-shapekeys-as-obj-from-the-active-object/86678#86678
# with small tweaks by Jay Versluis
# https://www.versluis.com

import bpy
import os
import os.path as osp


# Reference the active object
obj = bpy.context.active_object

# CHANGE THIS to the folder you want to save your OBJ files in
# NOTE: no spaces, no trailing slash
exportPath = "/Users/zhaoyafei/work/blender-python-scripts-zyf/blendshapes-bella"

if not osp.exists(exportPath):
    os.makedirs(exportPath)

# Reset all shape keys to 0 (skipping the Basis shape on index 0
for skblock in obj.data.shape_keys.key_blocks[1:]:
    skblock.value = 0

# Export basis
skblock = obj.data.shape_keys.key_blocks[0]
# Set OBJ file path and Export OBJ
objFileName = skblock.name + ".obj"  # File name = shapekey name
objPath = osp.join(exportPath, objFileName)
bpy.ops.export_scene.obj(filepath=objPath, use_selection=True, global_scale=1)

skblock.value = 0  # Reset shape key value to 0

# Iterate over shape key blocks and save each as an OBJ file
for skblock in obj.data.shape_keys.key_blocks[1:]:
    skblock.value = 1.0  # Set shape key value to max

    # Set OBJ file path and Export OBJ
    objFileName = skblock.name + ".obj"  # File name = shapekey name
    objPath = osp.join(exportPath, objFileName)
    bpy.ops.export_scene.obj(
        filepath=objPath, use_selection=True, global_scale=1)

    skblock.value = 0  # Reset shape key value to 0
