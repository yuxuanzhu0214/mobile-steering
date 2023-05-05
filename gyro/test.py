import numpy as np
import math

def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

def quaternion_conjugate(q):
    w, x, y, z = q
    return np.array([w, -x, -y, -z])

def apply_quaternion_rotation(q, v):
    q_v = np.concatenate(([0], v))
    q_inv = quaternion_conjugate(q)
    return quaternion_multiply(quaternion_multiply(q, q_v), q_inv)[1:]

# Example quaternion (q0, q1, q2, q3)
# q = [0.18123917028394296, -0.6789676783610179, 0.11814477670254474, 0.7015675780947571]

# Reference vector (x-axis)
# ref_vector = np.array([1, 0, 0])

def quaternion_rotation(q, ref_vector):
    # Apply the quaternion rotation to the reference vector
    rotated_vector = apply_quaternion_rotation(q, ref_vector)

    # Calculate the projection of the rotated reference vector onto the plane perpendicular to the roll axis (z-axis)
    rotated_vector_proj = rotated_vector - np.dot(rotated_vector, np.array([0, 0, 1])) * np.array([0, 0, 1])

    # Check if the magnitude of rotated_vector_proj is above a small threshold
    threshold = 1e-8
    if np.linalg.norm(rotated_vector_proj) > threshold:
        # Calculate the angle between the original reference vector and the projected rotated vector
        dot_product = np.dot(ref_vector, rotated_vector_proj) / (np.linalg.norm(ref_vector) * np.linalg.norm(rotated_vector_proj))
        angle_rad = math.acos(np.clip(dot_product, -1, 1))
        # print("Rotation angle along the roll axis (in radians):", angle_rad)
        # print("Rotation angle along the roll axis (in degrees):", math.degrees(angle_rad))
    else:
        print("The magnitude of the rotated_vector_proj is too small.")