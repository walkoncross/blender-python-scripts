"""    Import a .fbx file from the specified path and perform basic operations on the imported objects.

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


def import_fbx(
    file_path: str,
    scale: list | None = None,
    hide_all: bool = True,
    delete_all: bool = False
) -> list[bpy.types.Object]:
    """
    Import a .fbx file from the specified path and perform basic operations on the imported objects.

    Parameters:
    - file_path (str): Path to the .fbx file.
    - scale (tuple): Scale of the imported object, default is (1, 1, 1).
    - hide_all (bool): Whether to hide all objects in the current scene before importing, default is True.
    - delete_all (bool): Whether to delete all objects in the current scene before importing, default is True.

    Returns:
    - list[bpy.types.Object]: List of imported objects.
    """
    if delete_all:
        # Delete all objects in the current scene (optional)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        bpy.ops.object.select_all(action='DESELECT')
    elif hide_all:
        # Hide all objects in the current scene (optional)
        hide_all_objects()

    # Import the .fbx file
    bpy.ops.import_scene.fbx(filepath=file_path)

    # Get the imported objects
    imported_objects = bpy.context.selected_objects

    if scale is not None:
        for obj in imported_objects:
            # Print the name of the imported object
            print(f"Imported object: {obj.name}")

            # # Set position
            # obj.location = location

            # Set scale
            obj.scale = scale

    # Update the scene to apply changes
    bpy.context.view_layer.update()

    return imported_objects


if __name__=='__main__':
    file_path = "/Users/zhaoyafei/work/3d-assets-zyf/polywink-rigging/POLYWINK_AIX_SAMPLE.fbx"

    imported_objects = import_fbx(file_path, hide_all=True, delete_all=False)

    print(f'imported_objects: {imported_objects}')