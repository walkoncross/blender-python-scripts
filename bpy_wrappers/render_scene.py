import bpy
import os.path as osp

def render_scene(
    output_path: str = '', 
    resolution_x: int = 1920, 
    resolution_y: int = 1080, 
    fps: int = 30, 
    frame_start: int = 1, 
    frame_end: int = 250, 
    output_format: str = 'FFMPEG', 
    camera_name: str = None,
    render_engine: str = 'workbench'
) -> None:
    """
    Renders a Blender scene to a video file.

    Parameters:
        output_path (str): The path to the output video file. If empty, the output file will be named after the input file with a "_render.mp4" suffix, and saved in the working directory..
        resolution_x (int, optional): The horizontal resolution of the output video. Defaults to 1920.
        resolution_y (int, optional): The vertical resolution of the output video. Defaults to 1080.
        fps (int, optional): The frame rate of the output video. Defaults to 30.
        frame_start (int, optional): The starting frame of the animation. Defaults to 1.
        frame_end (int, optional): The ending frame of the animation. Defaults to 250.
        output_format (str, optional): The format of the output images (PNG, BMP, JPEG, WEBP, etc.) or video (FFMPEG). Defaults to 'FFMPEG'.
        camera_name (str, optional): The name of the camera to use for rendering. Defaults to None.
        render_engine (str, optional): The render engine to use 'eevee', 'workbench', 'cycles'. Defaults to 'cycles'.
    
    Returns:
        None
    """
    assert frame_end >= frame_start, 'frame_end must be >= frame_start'

    # Load the input Blender file
    # if input_file is None or input_file=='':
    #     input_file = './cube.blend'
    # else:
    #     bpy.ops.wm.open_mainfile(filepath=input_file)
    input_file = bpy.context.blend_data.filepath
    if input_file == '':
        input_file = 'cube.blend'

    output_format = output_format.upper()
    # Set up the rendering engine (Cycles or Eevee)
    render_engine = render_engine.lower()

    if render_engine == 'ev':
        render_engine = 'eevee'
    elif render_engine == 'cy':
        render_engine = 'cycles'
    elif render_engine == 'wb':
        render_engine = 'workbench'

    if 'cycles' not in render_engine and 'eevee' not in render_engine:
        render_engine = 'workbench'

    if 'cycles' in render_engine:
        render_engine = 'CYCLES'
    elif 'eevee' in render_engine:
        render_engine = 'BLENDER_EEVEE_NEXT'
    else:
        render_engine = 'BLENDER_WORKBENCH'

    print(f'--> render_engine: {render_engine}')

    if output_path is None or output_path=='':
        output_path = osp.join('./', osp.splitext(osp.basename(input_file))[0] + f'_render-by-{render_engine}')
    else:
        output_path = osp.splitext(output_path)[0] # let blender to decide the `file extension`

    if not output_path.endswith('_'):
        output_path += '_'
    
    bpy.context.scene.render.engine = render_engine
    
    # Set output resolution
    bpy.context.scene.render.resolution_x = resolution_x
    bpy.context.scene.render.resolution_y = resolution_y
    bpy.context.scene.render.resolution_percentage = 100
    
    # Set frame rate
    bpy.context.scene.render.fps = fps
    
    # Set start and end frames for the animation
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end

    # if frame_end - frame_start > 1 and output_format!='FFMPEG':
    #     output_path += '_' # saving multiple images

    # Set output format to FFMPEG (for video rendering)

    bpy.context.scene.render.image_settings.file_format = output_format
    if output_format == 'FFMPEG':
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
        bpy.context.scene.render.ffmpeg.audio_codec = 'AAC'
    
        # Set up the video output properties
        bpy.context.scene.render.ffmpeg.video_bitrate = 6000
        bpy.context.scene.render.ffmpeg.audio_bitrate = 192
    
    # Set the active camera if a camera name is provided
    if camera_name:
        camera = bpy.data.objects.get(camera_name)
        if camera and camera.type == 'CAMERA':
            bpy.context.scene.camera = camera
            print(f"Using camera: {camera_name}")
        else:
            print(f"Camera '{camera_name}' not found or not a valid camera object, using default camera.")

        output_path += f'from-{camera_name}_'

    print(f'--> output_path: {output_path}')

    # Set output path for the video
    bpy.context.scene.render.filepath = output_path
    # let blender to decide the `file extension`
    bpy.context.scene.render.use_file_extension = True

    # Render the animation in off-screen mode
    bpy.ops.render.render(animation=True, write_still=False)
    
    print(f"Video rendered to: {output_path}-*")


if __name__=='__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Render a scene to a video.')
    # input is passed by blend's commandline option: -b input_file
    # parser.add_argument('--input_file', type=str, default='', help='Path to the input Blender file. If not specified, the default scene will be used.')
    parser.add_argument('--output_file', type=str, default='', help='Path to the output video file. If not specified, the output file will be named after the input file with a "_render.mp4" suffix, and saved in the working directory.')
    parser.add_argument('--resolution_x', type=int, default=1280, help='Output video resolution in the x direction.')
    parser.add_argument('--resolution_y', type=int, default=720, help='Output video resolution in the y direction.')
    parser.add_argument('--fps', type=int, default=24, help='Frames per second for the video.')
    parser.add_argument('--frame_start', type=int, default=1, help='Start frame for the animation.')
    parser.add_argument('--frame_end', type=int, default=12, help='End frame for the animation.')
    parser.add_argument('--output_format', type=str, default='FFMPEG', help='The format of the output images (PNG, BMP, JPEG, WEBP, etc.) or video (FFMPEG). Defaults to FFMPEG.')
    parser.add_argument('--camera_name', type=str, default="", help='Name of the camera to use for rendering. If empty, the first camera will be used.')
    parser.add_argument('--render_engine', type=str, default="workbench", help='Render engine to use, maybe "cycles", "eevee", or "workbench" ')

    argv = sys.argv

    # skip blender command line args
    try:
        index = argv.index("--") + 1
    except ValueError:
        index = len(argv)

    argv = argv[index:]

    args = parser.parse_args(argv)

    print(f'==> args: {args}')

    render_scene(
        # args.input_file,
        args.output_file,
        resolution_x=args.resolution_x,
        resolution_y=args.resolution_y,
        fps=args.fps,
        frame_start=args.frame_start,
        frame_end=args.frame_end,
        output_format=args.output_format,
        camera_name=args.camera_name,
        render_engine=args.render_engine
    )
