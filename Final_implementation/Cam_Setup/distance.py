import math
from shared import SharedData




HEIGHT = 480
WIDTH = 640

MID_X = 640//2
MID_Y = 480//2

def dist_from_center(xm,ym):
  """Calculates the Euclidean distance between two points.

  Args:
    x1: x-coordinate of the first point.
    y1: y-coordinate of the first point.
    x2: x-coordinate of the second point.
    y2: y-coordinate of the second point.

  Returns:
    The Euclidean distance between the two points.   

  """
  
    
  distance = math.sqrt((MID_X - xm)**2 + (MID_Y - ym)**2)
  return distance
    

def find_shortest(lst_objs,share):
    distances = []
    objects = []



    for result in lst_objs:  
      x1, y1, x2, y2, score, classid = result

      if classid == share.getObjIndex(): 
        xm = int((x1+x2)/2)
        ym = int((y1+y2))/2

        objects.append((xm,ym))
        distances.append(dist_from_center(xm,ym)) 

    try:
       ret = objects[distances.index(min(distances))]
    except Exception as e:
        ret = (0,0)

    return ret

def get_angle(xm, ym):

    delta_x = xm
    delta_y = ym

    # Change in y / Change in x = Tan
    # arctan = angle in rad
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)

    # Make the angle positive
    angle_degrees = (angle_degrees + 360) % 360

    return angle_degrees

def get_x_component(distance, angle):

    angle_radians = math.radians(angle)
    x_component = distance * math.cos(angle_radians)

    return x_component

def get_y_component(distance, angle):

    angle_radians = math.radians(angle)
    y_component = distance * math.sin(angle_radians)

    return y_component

   