import bpy

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        if obj.data and obj.data.shape_keys and obj.data.shape_keys.animation_data:
            print('=' * 32)
            print('mesh shape_keys.animation_data: ')
            print('-' * 8 + ' obj:')
            print(obj)
            print('-' * 8 + ' obj.type:')
            print(obj.type)
            print('-' * 8 + ' obj.name:')
            print(obj.name)            
            print('-' * 8 + ' obj.data.shape_keys.animation_data:')
            print(obj.data.shape_keys.animation_data)