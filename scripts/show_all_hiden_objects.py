"""Show all hidden objects in the current scene.

Author: zhaoyafei0210@gmail.com
"""
import bpy


def show_all_hidden_objects() -> None:
    """
    Show all hidden objects in the current scene
    """
    # Ensure execution in the 3D view context
    # Ensure execution in the 3D view context
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(area=area):
                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.object.hide_view_clear(select=True)
                bpy.ops.object.select_all(action='DESELECT')
            break

if __name__=='__main__':
    show_all_hidden_objects()