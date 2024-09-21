"""Create shape key from input vertices.

Author: zhaoyafei0210@gmail.com
"""
import bpy


def is_valid_object(bpy_obj_name:str, type:str='MESH') -> bool:
    """Check if bpy_obj_name is a valid object name.

    Parameters:
        bpy_obj_name: object name
        type: object type, default is 'MESH'

    Returns: 
        True if bpy_obj_name is a valid object name, otherwise False
    
    """
    return (bpy_obj_name and bpy_obj_name in bpy.data.objects.keys() and bpy.data.objects[bpy_obj_name].type==type)

