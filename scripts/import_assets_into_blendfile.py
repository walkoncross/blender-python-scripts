import sys
import argparse
import os.path as osp

import bpy

sys.path.append(osp.join(osp.dirname(osp.abspath(__file__)), "../"))

from bpy_wrappers_zyf.import_fbx import import_fbx
from bpy_wrappers_zyf.import_gltf_or_glb import import_gltf_or_glb

__all__ = []

if __name__=='__main__':
    argv = sys.argv

    print('=' * 16)
    print('Usage Help: blender --python this_script -- -h')
    print('Usage: blender --python this_script -- --other_arguments')
    print('=' * 16)

    # skip blender command line args
    try:
        index = argv.index("--") + 1
    except ValueError:
        index = len(argv)

    argv = argv[index:]

    parser = argparse.ArgumentParser()
    # parser.add_argument('--python', type=str, default=None, help='Path to the python script')
    parser.add_argument('--input', type=str, default=None, help='Path to the input file')
    parser.add_argument('--scale', type=float, default=None, help='Scale of the imported object')
    parser.add_argument('--hide_all', type=bool, default=False, help='bool, Whether to hide all objects in the current scene before importing')
    parser.add_argument('--delete_all', type=bool, default=False, help='bool, Whether to delete all objects in the current scene before importing')
    parser.add_argument('--save_project', type=bool, default=False, help='bool, Whether to save the project after importing')
    parser.add_argument('--save_path', type=str, default=None, help='Where to save the blender project, default to the same directory as the input file')

    args = parser.parse_args(argv)

    print(f'---> args: {args}')

    if args.scale is not None:
        args.scale = (args.scale, ) * 3 # for x,y,z

    if args.input is None:
        args.input = "/Users/zhaoyafei/work/3d-assets-zyf/polywink-rigging/POLYWINK_AIX_SAMPLE.fbx"
        # args.input = "/Users/zhaoyafei/Downloads/nv-audio2face/mark_mid_v5.glb"

    print(f'---> file_path: {args.input}')

    # bpy.ops.wm.read_factory_settings(use_empty=True)
    # bpy.ops.wm.read_factory_settings(use_empty=False)
    # bpy.context.view_layer.update()

    # print(f'bpy.context.screen.areas: {bpy.context.screen.areas}')

    if args.input.endswith('.fbx'):
        print('---> Import fbx...')
        imported_objects = import_fbx(
            args.input,
            scale=args.scale,
            hide_all=args.hide_all,
            delete_all=args.delete_all
        )
    elif args.input.endswith('.glb') or args.input.endswith('.gltf'):
        print('---> Import gltf or glb...')
        imported_objects = import_gltf_or_glb(
            args.input,
            scale=args.scale,
            hide_all=args.hide_all,
            delete_all=args.delete_all
        )
    else:
        raise ValueError('---> Unsupport file format')

    print(f'---> Imported_objects: {imported_objects}')
    print('---> Finished importing')

    # file_path = "/Users/zhaoyafei/Downloads/nv-audio2face/claire_mid_v5.glb"
    # imported_objects = import_fbx(file_path, hide_all=False, delete_all=False)
    # print(f'imported_objects: {imported_objects}')

    if args.save_project:
        print('---> Saving the project...')
        if args.save_path is None:
            args.save_path = osp.splitext(args.input)[0] + '.blend'
        bpy.ops.wm.save_mainfile(filepath=args.save_path)
        print(f'---> Saved into {args.save_path}')