import math
from pyniryo import *
import json
# import pick
import numpy as np


def xpos(xm):
    return -0.768*xm + 249

def ypos(ym):
    return 0.782*ym + 127

def map(x, in_min, in_max, out_min, out_max):
      return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def next_pos(share,xm,ym):


    observation_pose = {
        "x":0.150744, "y":-0.012502, "z":0.179668,
        "roll":-1.811, "pitch":1.543, "yaw":-0.274,
    }    

    if share.getGrab() == 2:
        share.setPos(observation_pose)
        share.setGrab(0)
        share.setUpdate(0)
        return 0

    if xm == 0 or ym == 0:
        share.setPos(observation_pose)
        return 0
    
    # relative_pos = np.array(xm,ym,0.3)
    # curr_pos = pick.convert_to_arm_coordinates(relative_pos)
    

    
    if share.getGrab() == 3:
        curr_pos = share.getPos_asDict()
        curr_pos["z"] = 0.089
        

    if share.getGrab() == 0: 
        curr_pos = share.getPos_asDict()
        curr_pos["x"] = xpos(xm)/1000
        curr_pos["y"] = ypos(ym)/1000
        curr_pos["z"] = 0.100
        share.setGrab(3)

    
    

    
    

    print(curr_pos)
    share.setPos(curr_pos)
    


# xm,ym = 176,180.5
# print(xpos(xm),ypos(ym))