"""Import .obj files

Author: zhaoyafei0210@gmail.com
"""


import bpy


__all__ = ['import_obj_file']

def print_mesh_vertex(mesh_obj, first_n=8):
    print('===> print_mesh_vertex()')
    print('---> mesh object: ', mesh_obj.name)
    if isinstance(mesh_obj, str):
        mesh_obj = bpy.data.objects(mesh_obj)

    if first_n < 0:
        first_n = 8

    for ii in range(first_n):
        print('---> vertices[{}].co = {}'.format(ii,
              mesh_obj.data.vertices[ii].co))


def import_obj_file(file_path, apply_transform=False):
    """ Import .obj file as bpy object

    """
    print('===> Import .obj file: ', file_path)

    # Refer to: https://docs.blender.org/api/current/bpy.ops.import_scene.html
    # bpy.ops.import_scene.obj(filepath='', filter_glob='*.obj;*.mtl', use_edges=True, use_smooth_groups=True, use_split_objects=True, use_split_groups=False, use_groups_as_vgroups=False, use_image_search=True, split_mode='ON', global_clamp_size=0.0, axis_forward='-Z', axis_up='Y')
    # Load a Wavefront OBJ File

    # Parameters
    # filepath (string, (optional, never None)) – File Path, Filepath used for importing the file
    # filter_glob (string, (optional, never None)) – filter_glob
    # use_edges (boolean, (optional)) – Lines, Import lines and faces with 2 verts as edge
    # use_smooth_groups (boolean, (optional)) – Smooth Groups, Surround smooth groups by sharp edges
    # use_split_objects (boolean, (optional)) – Object, Import OBJ Objects into Blender Objects
    # use_split_groups (boolean, (optional)) – Group, Import OBJ Groups into Blender Objects
    # use_groups_as_vgroups (boolean, (optional)) – Poly Groups, Import OBJ groups as vertex groups
    # use_image_search (boolean, (optional)) – Image Search, Search subdirs for any associated images (Warning, may be slow)
    # split_mode (enum in ['ON', 'OFF'], (optional)) –
    # Split
    # ON Split, Split geometry, omits unused verts.
    # OFF Keep Vert Order, Keep vertex order from file.
    # global_clamp_size (float in [0, 1000], (optional)) – Clamp Size, Clamp bounds under this value (zero to disable)
    # axis_forward (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Forward
    # axis_up (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Up

    state = bpy.ops.import_scene.obj(filepath=file_path, split_mode='OFF')
    if 'FINISHED' in state:
        obj_object = bpy.context.selected_objects[0]  # <--Fix
        print('---> Imported object name: ', obj_object.name)

        if apply_transform:
            bpy.ops.object.transform_apply(
                location=True, rotation=True, scale=True)
    else:
        print('---> Error: Failed to import .obj file')

        obj_object = None

    return obj_object


if __name__ == '__main__':
    # obj_file = '/Users/zhaoyafei/work/blender-python-scripts-zyf/cube-deform1.obj'
    obj_file = '/Users/zhaoyafei/work/blender-python-scripts-zyf/blendshapes-bella/jawOpen.obj'

    imported_obj = import_obj_file(obj_file)
    print_mesh_vertex(import_obj_file, 8)
