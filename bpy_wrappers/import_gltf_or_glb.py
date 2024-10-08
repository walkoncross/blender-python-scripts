"""    Import a .gltf/.glb file from the specified path and perform basic operations on the imported objects.

Author: zhaoyafei0210@gmail.com
"""
import bpy


__all__ = ['import_gltf_or_glb']

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
    scale: tuple | None = None,
    hide_all: bool = True,
    delete_all: bool = False
) -> list[bpy.types.Object]:
    """
    Import a .gltf/.glb file from the specified path and perform basic operations on the imported objects.

    Parameters:
    - file_path (str): Path to the .gltf/.glb file.
    - scale (tuple or None): Scale of the imported object, default is None for (1, 1, 1).
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

    # Import the .glb file
    # bpy.ops.import_scene.gltf(filepath=file_path)
    # fix issue: bones turned into icosphere (https://www.reddit.com/r/blenderhelp/comments/1bo83cx/hello_please_i_am_trying_to_export_a_file_as_gltf/)
    bpy.ops.import_scene.gltf(filepath=file_path, bone_heuristic='TEMPERANCE') 

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
    # Example call
    file_path = "/Users/zhaoyafei/Downloads/nv-audio2face/mark_mid_v5.glb"
    imported_objects = import_gltf_or_glb(file_path, hide_all=True, delete_all=False)

    print(f'imported_objects: {imported_objects}')

    # file_path = "/Users/zhaoyafei/Downloads/nv-audio2face/claire_mid_v5.glb"
    # imported_objects = import_gltf_or_glb(file_path, hide_all=False, delete_all=False)
    # print(f'imported_objects: {imported_objects}')
