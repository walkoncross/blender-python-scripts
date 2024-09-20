"""Import .obj files and add them as shape keys (blendshapes)

Author: zhaoyafei0210@gmail.com
"""

import bpy
import os.path as osp
import glob


__all = ['add_shape_key_from_another_object', 'import_multi_objs_as_shape_keys']

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


def add_shape_key_from_another_object(basis_obj, another_obj):
    """ Add a shape key for basis_obj from another_obj, basis_obj and another_obj must have the same topo (vertex order).
    """
    print('===> add_shape_key_from_another_object()')

    # deselect all
    state = bpy.ops.object.select_all(action='DESELECT')

    print('---> basis object name: ', basis_obj.name)
    print('---> another object name: ', another_obj.name)

    # select
    another_obj.select_set(True)
    basis_obj.select_set(True)

    bpy.context.view_layer.objects.active = basis_obj

    state = bpy.ops.object.join_shapes()
    if 'FINISHED' in state:
        new_shape_key = basis_obj.data.shape_keys.key_blocks[-1].name
    else:
        new_shape_key = None

    print('---> Added shape key name: ', new_shape_key)

    return new_shape_key


def delete_shape_key_by_name(bpy_obj, key_name):
    """ Delete shape_key by name
    """
    print('===> delete_shape_key_by_name(): ')
    print('---> Try to delete shape_key: {} from {}'.format(key_name, bpy_obj.name))
    # setting the active shapekey
    index = bpy_obj.data.shape_keys.key_blocks.keys().index(key_name)
    bpy_obj.active_shape_key_index = index

    # delete it
    state = bpy.ops.object.shape_key_remove()
    if 'FINISHED' in state:
        print('---> Finised to delete shape_key: ', key_name)
    else:
        print('---> Failed to delete shape_key: ', key_name)


def rename_shape_key(bpy_obj, key_name, new_key_name):
    """ rename a shape key, shape_keys[key_name].name = new_key_name
    """
    print('===> delete_shape_key_by_name(): ')
    print('---> Try to delete shape_key: {} from {}'.format(key_name, bpy_obj.name))
    # setting the active shapekey
    index = bpy_obj.data.shape_keys.key_blocks.keys().index(key_name)
    bpy_obj.active_shape_key_index = index

    # rename
    bpy_obj.data.shape_keys.key_blocks[index].name = new_key_name
    # renaming might fail if new_key_name already in shape_keys.key_blocks.keys()
    new_key_name = bpy_obj.data.shape_keys.key_blocks[index].name

    return new_key_name


def import_obj_file_as_shape_key(
    file_path,
    basis_mesh_obj_name,
    shape_key_name=None,
    apply_transform=True,
    replace=False,
):
    """Import .obj file as a bpy object and make a shape key from imported object for basis_mesh_obj_name

    """
    print('===> import_obj_file_as_shape_key(): ')

    imported_obj = import_obj_file(file_path, apply_transform)
    if import_obj_file == None:
        return None

    basis_mesh_obj = bpy.data.objects[basis_mesh_obj_name]
    shape_keys = basis_mesh_obj.data.shape_keys.key_blocks.keys()

    new_shape_key = add_shape_key_from_another_object(
        basis_mesh_obj, imported_obj)
    print('---> Temp shape_key name: ', new_shape_key)

    if new_shape_key:
        if replace and shape_key_name in shape_keys:
            delete_shape_key_by_name(basis_mesh_obj, shape_key_name)

        if shape_key_name:
            new_shape_key = rename_shape_key(
                basis_mesh_obj, new_shape_key, shape_key_name)

    print('---> Final shape_key name: ', new_shape_key)

    # delete imported object
    print('---> Try to delete imported object')
    bpy.ops.object.select_all(action='DESELECT')
    imported_obj.select_set(True)
    bpy.context.view_layer.objects.active = imported_obj
    state = bpy.ops.object.delete(use_global=True)
    if 'FINISHED' in state:
        print('---> Imported object deleted')

    basis_mesh_obj.select_set(True)

    return new_shape_key


def import_multi_objs_as_shape_keys(
    obj_folder_path,
    basis_mesh_obj_name,
    apply_transform=False,
    replace=False,
):
    obj_file_list = glob.glob(obj_folder_path + '/*.obj')

    for obj_file in obj_file_list:
        shape_key_name = osp.splitext(osp.basename(obj_file))[0]

        import_obj_file_as_shape_key(
            obj_file,
            basis_mesh_obj_name,
            shape_key_name,
            apply_transform=apply_transform,
            replace=replace)


if __name__ == '__main__':
    # obj_file = '/Users/zhaoyafei/work/blender-python-scripts-zyf/blendshapes-bella/jawOpen.obj'
    # obj_file = '/Users/zhaoyafei/work/blender-python-scripts-zyf/blendshapes-bella/mouthPucker.obj'
    # obj_file = '/Users/zhaoyafei/work/blender-python-scripts-zyf/blendshapes-bella/cheekPuff.obj'
    # shape_key_name = osp.splitext(osp.basename(obj_file))[0]
    # print('===> shape_key_name: ', shape_key_name)

    # basis_mesh_obj_name = 'POLYWINK_Bella'

    # import_obj_file_as_shape_key(
    #     obj_file,
    #     basis_mesh_obj_name,
    #     shape_key_name,
    #     apply_transform=False,
    #     replace=True,
    #     )

    obj_folder_path = '/Users/zhaoyafei/work/blender-python-scripts-zyf/blendshapes-bella'
    basis_mesh_obj_name = 'POLYWINK_Bella'
    import_multi_objs_as_shape_keys(
        obj_folder_path,
        basis_mesh_obj_name,
        apply_transform=False,
        replace=True,
    )
