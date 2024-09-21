"""Clears the sequence editor in the current Blender scene.

Author: zhaoyafei0210@gmail.com
"""
import bpy

__all__ = ['clear_sequence_editor']

def clear_sequence_editor() -> None:
    '''
    Clears the sequence editor in the current Blender scene.
    
    This function removes all strips from the sequence editor, effectively clearing it.

    Returns: 
        None
    '''
    bpy.context.scene.sequence_editor_clear()

