"""Adds an sound strip to the current Blender scene.

Author: zhaoyafei0210@gmail.com
"""
import bpy

def add_sound_strip(audio_file_path: str) -> None:
    '''
    Adds an sound strip to the current Blender scene.
    '''
    # Ensure the current scene has an audio sequence
    if not bpy.context.scene.sequence_editor:
        bpy.context.scene.sequence_editor_create()

    # Add audio sequence
    seq_editor = bpy.context.scene.sequence_editor
    sound_strip = seq_editor.sequences.new_sound(
        name="Audio strip",
        filepath=audio_file_path,
        channel=1,
        frame_start=1
    )

    # Set audio to loop playback
    sound_strip.volume = 1.0  # Set volume

    # Enable audio playback
    bpy.context.scene.sync_mode = 'AUDIO_SYNC'

    print(f"Audio successfully added: {audio_file_path}")


if __name__=='__main__':
    # Call the function and pass the audio file path
    audio_path = "/Users/zhaoyafei/work/NIM-audio2face-visualization/viz-threejs/assets/out.wav"
    add_sound_strip(audio_path)

