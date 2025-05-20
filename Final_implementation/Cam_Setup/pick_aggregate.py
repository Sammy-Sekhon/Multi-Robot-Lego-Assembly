from sklearn.linear_model import LinearRegression
import cv2
import numpy as np

# Corresponding 2D (camera) and 3D (robot arm) points

# image_points = np.array([[589.5,221.5],
# [568,200],
# [587.5,201],
# [608,201],
# [608.5,219.5],
# [588,221],
# [568,221.5],
# [569,243],
# [589,244.5],
# [608,244.5]], dtype=np.float32)

image_points = np.array(
[[345,265.5],
[343.5,243.5],
[343.5,222.5],
[364.5,221.5],
[385,221],
[384,241.5],
[383.5,266],
[362.5,266.5],
[362.5,244.5]
],dtype = np.float32)

# world_points = np.array([
#     [-207.338,309.991,90],
#     [-195.722,294.242,90],
#     [-213.626,296.408,90],
#     [-228.067,296.891,90],
#     [-224.102,311.202,90],
#     [-210.919,308.424,90],
#     [-196.96,312.609,90],
#     [-194.822,323.227,90],
#     [-213.19,328.623,90],
#     [-229.011,326.509,90]], dtype=np.float32)

world_points = np.array(
  [ [-19.11,334.824,90],
   [-18.692,317.947,90],
   [-15.74,302.511,90],
   [-33.675,301.046,90],
   [-56.22,299.981,90],
   [-53.863,316.251,90],
   [-55.155,338.591,90],
   [-28.153,337.166,90],
   [-32.842,320.604,90]],dtype=np.float32
)

r,p,y = 0.57,1.547,2.121

world_points_2d = world_points[:, :2]
# H, status = cv2.findHomography(image_points, world_points_2d)
H, _ = cv2.findHomography(image_points, world_points_2d, method=cv2.RANSAC, ransacReprojThreshold=4.5, confidence=0.50)


# fit Z using Linear Regression
X_train = world_points_2d
y_train = world_points[:, 2]

z_model = LinearRegression().fit(X_train, y_train)


def map_2d_to_3d(img_point, H):
    img_point_h = np.array([img_point[0], img_point[1], 1.0])
    world_point_h = np.dot(H, img_point_h)
    world_point_h /= world_point_h[2]  # Normalize by scale factor
    return world_point_h[:2]

def get_full_3d(img_point, H, z_model):
    xy = map_2d_to_3d(img_point, H)
    z = z_model.predict([xy])[0]
    return np.array([xy[0], xy[1], z])

def pos(xm,ym):
    mapped = get_full_3d([xm, ym], H, z_model)
    return mapped[0],mapped[1],mapped[2],r,p,y


print(pos(371.5,257))

