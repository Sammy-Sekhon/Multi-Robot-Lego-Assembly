import numpy as np

# Define Robot and LDR coordinate matrices
B = np.array([[-24, 24, 3.2],
              [-40, -16, 3.2],
              [-56, 0, 6.4],
              [-56, 40, 12.8],
              [-16, 40, 6.4],
              [-56, 8, 16],
              [-8, 40, 9.6],
              [-4, 60, 9.6],
              [-56, -20, 16],
              [-56, 40, 60.8]])

A = np.array([[48.648, -284.069, 99.463],
              [72.444, -313.502, 102.366],
              [80.432, -301.771, 100.214],
              [26.871, -315.310, 105.636],
              [25.873, -275.396, 101.482],
              [58.123, -315.671, 102.385],
              [24.76, -266.611, 101.343],
              [15.142, -266.644, 96.025],
              [92.028, -312.196, 103.574],
              [32.076, -310.31, 145.937]])

# Step 1: Compute centroids
C_A = np.mean(A, axis=0)
C_B = np.mean(B, axis=0)

# Step 2: Center the points
A_prime = A - C_A
B_prime = B - C_B

# Step 3: Compute cross-covariance matrix
H = A_prime.T @ B_prime

# Step 4: SVD
U, S, Vt = np.linalg.svd(H)

# Step 5: Compute rotation matrix
R = Vt.T @ U.T

# Ensure proper rotation matrix (det(R) = 1)
if np.linalg.det(R) < 0:
    Vt[2, :] *= -1
    R = Vt.T @ U.T

# Step 6: Compute translation vector
T = C_B - R @ C_A

print("Rotation Matrix (R):\n", R)
print("Translation Vector (T):\n", T)

# Function to apply inverse transformation (LDR to Robot)
def inverse_transform(point):
    print(np.linalg.inv(R) @ (point - T))
    return np.linalg.inv(R) @ (point - T)

# Example usage
new_ldr_point = np.array([-56, 8, 25.6])  # Example point in LDR coordinates
transformed_point = inverse_transform(new_ldr_point)
print("Actual Robot Point:", A[0])
print("Transformed Robot Point (after inverse transform):", transformed_point)