import bpy

__all__ = []

if __name__ == "__main__":
    # create a new default project
    # bpy.ops.preferences.addon_disable(module='ComfyUI Node Editor')
    bpy.ops.wm.read_factory_settings(use_empty=False)

    # save project
    file_path = "./default_blender_project.blend"
    bpy.ops.wm.save_as_mainfile(filepath=file_path)

    print(f"Blender project saved at: {file_path}")

    # create a new empty project
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # save project
    file_path = "./empty_blender_project.blend"
    bpy.ops.wm.save_as_mainfile(filepath=file_path)

    print(f"Blender project saved at: {file_path}")
