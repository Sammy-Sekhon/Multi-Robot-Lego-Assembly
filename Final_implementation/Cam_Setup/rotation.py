import numpy as np
import math
import shared

'''
    CHECK AND RETURN THE ROTATION MATRIX 
    of the lego piece
'''

def rotation_matrix_to_euler_angles(R):
    """Converts a rotation matrix to ZYX Euler angles (yaw, pitch, roll)."""
    pitch = math.asin(-R[2, 0])
    yaw = math.atan2(R[1, 0], R[0, 0])
    roll = math.atan2(R[2, 1], R[2, 2])
    return yaw, pitch, roll

def pitchBool(share):
    out = rotation_matrix_to_euler_angles(share.getRotation())
    if math.fabs(out[1]) != 0.0:
        return True
    else:
        return False

# # rotation matrix 
# R = np.array([[1.0, 0.0, 0.0],
#               [0.0, 1.0, 0.0],
#               [0.0, 0.0, 1.0]])

# out = rotation_matrix_to_euler_angles(R)

# print(out[1])
# print(math.fabs(out(1)) != 0.0)

# print("Yaw (radians):", yaw)
# print("Pitch (radians):", pitch)
# print("Roll (radians):", roll)

# # Convert to degrees if needed
# yaw_deg = math.degrees(yaw)
# pitch_deg = math.degrees(pitch)
# roll_deg = math.degrees(roll)


# print("Yaw (degrees):", yaw_deg)
# print("Pitch (degrees):", pitch_deg)
# print("Roll (degrees):", roll_deg)




# rotation matrix 
# R = np.array([[0.0, 0.0, 1.0],
#               [0.0, 1.0, 0.0],
#               [-1.0, 0.0, 0.0]])

# out = rotation_matrix_to_euler_angles(R)

# print(out)
# print(math.fabs(out(1)) != 0.0)

# print(math.fabs(pitch) != 0.0)

# print("Yaw (radians):", yaw)
# print("Pitch (radians):", pitch)
# print("Roll (radians):", roll)

# # Convert to degrees if needed
# yaw_deg = math.degrees(yaw)
# pitch_deg = math.degrees(pitch)
# roll_deg = math.degrees(roll)
