import mathutils
from math import radians, degrees

vec = mathutils.Vector((1.0, 2.0, 3.0))

mat_rot = mathutils.Matrix.Rotation(radians(90.0), 4, 'X')
mat_trans = mathutils.Matrix.Translation(vec)

print("--> mat_rot:")
print(mat_rot)

quat = mat_rot.to_quaternion()

print("--> quat:")
print(quat)
print("--> quat.axis:")
print(quat.axis)
print("--> degrees(quat.angle):")
print(degrees(quat.angle))

print("--> mat_trans:")
print(mat_trans)

mat = mat_trans * mat_rot

print("--> mat=mat_trans * mat_rot:")
print(mat)

mat3 = mat.to_3x3()

print("--> mat3:")
print(mat3)

quat1 = mat.to_quaternion()
quat2 = mat3.to_quaternion()

print("--> quat1:")
print(quat1)
print("--> quat1.axis:")
print(quat1.axis)
print("--> degrees(quat1.angle):")
print(degrees(quat1.angle))

print("--> quat2:")
print(quat2)
print("--> quat2.axis:")
print(quat2.axis)
print("--> degrees(quat2.angle):")
print(degrees(quat2.angle))

quat_diff = quat1.rotation_difference(quat2)

print("--> quat_diff:")
print(quat_diff)

print("--> quat_diff.angle:")
print(quat_diff.angle)

mat.invert()

print("--> mat.invert:")
print(mat)