from ultralytics import YOLO
from pyniryo import *
import numpy as np
import time
import cv2
import os
import json
import distance
from sklearn.linear_model import LinearRegression


# Corresponding 2D (camera) and 3D (robot arm) points
image_points = np.array([
      [86, 37],
      [109, 204],
      [103, 355],
      [345, 352],
      [343, 210],
      [338, 58],
      [555, 39],
      [562, 215],
      [555, 341],
      [219, 112],
      [213, 216],
      [214, 352],
      [492, 49],
      [505, 216],
      [505, 342],
      [412, 94],
      [416, 216],
      [414, 345],
], dtype=np.float32)

world_points = np.array([
      [175.41, 149.175, 89.475],
      [166.996, 272.638, 90.173],
      [174.141, 386.237, 90.071],
      [-1.670, 399.472, 89.645],
      [-5.017, 292.231, 88.663],
      [-9.315, 176.046, 87.786],
      [-174.368, 178.659, 88.533],
      [-176.548, 310.819, 89.343],
      [-164.216, 402.701, 90.240],
      [79.509, 212.622, 88.205],
      [90.335, 291.832, 89.044],
      [90.192, 394.955, 89.636],
      [-131.451, 175.517, 87.832],
      [-136.776, 303.073, 89.371],
      [-132.156, 400.605, 89.008],
      [-63.871, 206.561, 88.593],
      [-68.418, 300.354, 88.821],
      [-60.175, 399.301, 89.719],
], dtype=np.float32)

world_points_2d = world_points[:, :2]
H, status = cv2.findHomography(image_points, world_points_2d)


# fit Z using Linear Regression
X_train = world_points_2d
y_train = world_points[:, 2]

z_model = LinearRegression().fit(X_train, y_train)

# map 2D image point to 3D world coordinates
def map_2d_to_3d(img_point, H):
    img_point_h = np.array([img_point[0], img_point[1], 1.0])
    world_point_h = np.dot(H, img_point_h)
    world_point_h /= world_point_h[2]  # Normalize by scale factor
    return world_point_h[:2]

# get 3D coordinates (z included)
def get_full_3d(img_point, H, z_model):
    xy = map_2d_to_3d(img_point, H)
    z = z_model.predict([xy])[0]
    return np.array([xy[0], xy[1], z])

'''
    Return the next position for the PICKING up of the pieces
'''
def next_pos(share,xm,ym):

    # observation_pose = {
    #     "x":0.150744, "y":-0.012502, "z":0.179668,
    #     "roll":-1.811, "pitch":1.543, "yaw":-0.274,
    # }    

    observation_pose = {
        "x":0.007052, "y":0.178, "z":0.351,
        "roll":-2.812, "pitch":1.489, "yaw":-1.298,
    }

    if share.getGrab() == 2:
        share.setPos(observation_pose)
        share.setGrab(0)
        share.setUpdate(0)
        return 0

    if xm == 0 or ym == 0:
        share.setPos(observation_pose)
        return 0
    

    if share.getGrab() == 0: 
        mapped_3d = get_full_3d([xm, ym], H, z_model)
                        
        curr_pos = {"x": mapped_3d[0] / 1000, 
                    "y": mapped_3d[1] / 1000, 
                    "z": mapped_3d[2] / 1000,
                    "roll":0.355, 
                    "pitch":1.553, 
                    "yaw":1.873
                }
        
        share.setGrab(3)
    



    print(curr_pos)
    share.setPos(curr_pos)