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


def import_gltf_or_glb(
    file_path: str,
    scale: list | None = None,
    hide_all: bool = True,
    delete_all: bool = False
) -> None:
    """
    Import a .gltf/.glb file from the specified path and perform basic operations on the imported objects.

    Parameters:
    - file_path (str): Path to the .gltf/.glb file.
    - scale (tuple): Scale of the imported object, default is (1, 1, 1).
    - hide_all (bool): Whether to hide all objects in the current scene before importing, default is True.
    - delete_all (bool): Whether to delete all objects in the current scene before importing, default is True.
    """
    if delete_all:
        # Delete all objects in the current scene (optional)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        bpy.ops.object.select_all(action='DESELECT')
    elif hide_all:
        # Hide all objects in the current scene (optional)
        hide_all_objects()

    # Import the .glb file
    bpy.ops.import_scene.gltf(filepath=file_path)

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


# Example call
file_path = "/Users/zhaoyafei/Downloads/nv-audio2face/mark_mid_v5.glb"
import_gltf_or_glb(file_path, hide_all=True, delete_all=False)

# file_path = "/Users/zhaoyafei/Downloads/nv-audio2face/claire_mid_v5.glb"
# import_gltf_or_glb(file_path, hide_all=False, delete_all=False)
