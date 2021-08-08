# author: zhaoyafei0210@gmail.com
# date: Aug 04, 2021
import numpy as np
from scipy.spatial.transform import Rotation as R

import mathutils
import math

xyz_deg = np.array([45, 30, 60])
xyz_rad = np.deg2rad(xyz_deg)

# XYZ: intrinsic xyz
# xyz: extrinsic xyz
# See:  https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_euler.html
#       https://en.wikipedia.org/wiki/Euler_angles#Definition_by_intrinsic_rotations

rotmat_scipy_intrinsic_XYZ = R.from_euler('XYZ', xyz_rad).as_matrix()
rotmat_scipy_extrinsic_xyz = R.from_euler('xyz', xyz_rad).as_matrix()

print('rotmat_scipy_intrinsic_XYZ: \n', rotmat_scipy_intrinsic_XYZ)
print('rotmat_scipy_extrinsic_xyz: \n', rotmat_scipy_extrinsic_xyz)

# Print results:
# rotmat_scipy_intrinsic_XYZ:
#  [[ 0.4330127  -0.75        0.5       ]
#  [ 0.78914913  0.04736717 -0.61237244]
#  [ 0.43559574  0.65973961  0.61237244]]
# rotmat_scipy_extrinsic_xyz:
#  [[ 0.4330127  -0.43559574  0.78914913]
#  [ 0.75        0.65973961 -0.04736717]
#  [-0.5         0.61237244  0.61237244]]


euler1 = mathutils.Euler(xyz_rad.tolist(), 'XYZ')
rotmat_blender_euler_XYZ = euler1.to_matrix()

euler2 = mathutils.Euler(xyz_rad.tolist(), 'ZYX')
rotmat_blender_euler_ZYX = euler2.to_matrix()

print('rotmat_blender_euler_XYZ: \n', rotmat_blender_euler_XYZ)
print('rotmat_blender_euler_ZYX: \n', rotmat_blender_euler_ZYX)

# Print results:
# rotmat_blender_euler_XYZ:
#  <Matrix 3x3 ( 0.4330, -0.4356,  0.7891)
#             ( 0.7500,  0.6597, -0.0474)
#             (-0.5000,  0.6124,  0.6124)>
# rotmat_blender_euler_ZYX:
#  <Matrix 3x3 (0.4330, -0.7500,  0.5000)
#             (0.7891,  0.0474, -0.6124)
#             (0.4356,  0.6597,  0.6124)>

if np.allclose(rotmat_scipy_intrinsic_XYZ, np.array(rotmat_blender_euler_XYZ)):
    print("rotmat_scipy_intrinsic_XYZ = rotmat_blender_euler_XYZ")
else:
    print("rotmat_scipy_intrinsic_XYZ != rotmat_blender_euler_XYZ")

if np.allclose(rotmat_scipy_extrinsic_xyz, np.array(rotmat_blender_euler_XYZ)):
    print("rotmat_scipy_extrinsic_xyz = rotmat_blender_euler_XYZ")
else:
    print("rotmat_scipy_intrinsic_XYZ != rotmat_blender_euler_XYZ")

if np.allclose(rotmat_scipy_intrinsic_XYZ, np.array(rotmat_blender_euler_ZYX)):
    print("rotmat_scipy_intrinsic_XYZ = rotmat_blender_euler_ZYX")
else:
    print("rotmat_scipy_intrinsic_XYZ != rotmat_blender_euler_ZYX")

if np.allclose(rotmat_scipy_extrinsic_xyz, np.array(rotmat_blender_euler_ZYX)):
    print("rotmat_scipy_extrinsic_xyz = rotmat_blender_euler_ZYX")
else:
    print("rotmat_scipy_intrinsic_XYZ != rotmat_blender_euler_ZYX")

# results:
# rotmat_scipy_intrinsic_XYZ != rotmat_blender_euler_XYZ
# rotmat_scipy_extrinsic_xyz = rotmat_blender_euler_XYZ
# rotmat_scipy_intrinsic_XYZ = rotmat_blender_euler_ZYX
# rotmat_scipy_intrinsic_XYZ != rotmat_blender_euler_ZYX
