"""Hide all objects in the current scene.

Author: zhaoyafei0210@gmail.com
"""
import bpy


def hide_all_objects() -> None:
    """
    Hide all objects in the current scene
    """
    # Ensure execution in the 3D view context
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(area=area):
                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.object.hide_view_set(unselected=False)
                bpy.ops.object.select_all(action='DESELECT')
            break


hide_all_objects()