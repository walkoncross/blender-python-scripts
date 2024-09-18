"""Save selected verts.

Author: zhaoyafei0210@gmail.com

How-to:
1. In 'Layout' window, select vertices:
    1) select mesh in 'Object Mode';
    2) change to 'Edit Mode';
    3) select the vertices, e.g. select the start vertex and then 'CTRL + select the end vertex';
2. In 'Scripting' window, run the script:
    1) copy and paste the following scripts;
    2) change save_path to where you want;
    3) run;
3. You can check the result in save_path;

"""

import os.path as osp
from datetime import datetime

import bpy
import bmesh

save_path = '/Users/zhaoyafei/blender_selected_verts.txt'
fp = open(save_path, 'a+')


# datetime object containing current date and time
now = datetime.now()
# print("now =", now)

dt_string = now.strftime("%Y/%m/%d/ %H:%M:%S")
# print("date and time =", dt_string)
fp.write('\n' + dt_string + '\n')


obj=bpy.context.object

# print('obj.name: ' + obj.name)
# print('ind\t x\t y\t z\n')
fp.write('obj.name: ' + obj.name + '\n')
fp.write('ind\t x\t y\t z\n')

if obj.mode == 'EDIT':
    bm=bmesh.from_edit_mesh(obj.data)
    for v in bm.verts:
        if v.select:
            # print(v.index)
            # print(v.co)
            write_line = '{}\t {}\t {}\t {}\n'.format(v.index, v.co.x, v.co.y, v.co.z)
            fp.write(write_line)
else:
    # print("Object is not in edit mode.")
    fp.write("Object is not in edit mode.")
    
fp.close()