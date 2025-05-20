from pyniryo import *
from shared import SharedData
import threading as th
import niryo_vision
import coord
import assemble
import lego_piece
# import pick

# Code to only test the Vision side of things with both the arms

def call_movement_when_ready(ned2):
    while share.getUpdate() != 100:
        print(".")
        if share.getUpdate() == 1:
            # move_the_arm(ned2)
            share.setUpdate(0)
        elif share.getUpdate() == 100:
            return 0



ned2_101 = NiryoRobot("192.168.0.101")
ned2_101.calibrate_auto()
ned2_101.release_with_tool()
ned2_101.grasp_with_tool()
observation_pose = PoseObject(
    x=0.304626, y=-0.024660, z=0.375304,
    roll=3.127, pitch=1.329, yaw=3.124,
)
ned2_101.move_pose(observation_pose)


ned2_102 = NiryoRobot("192.168.0.102")
ned2_102.calibrate_auto()
ned2_102.grasp_with_tool()
ned2_102.release_with_tool()

observation_pose = PoseObject(
    x=0.150744, y=-0.012502, z=0.179668,
    roll=0.355, pitch=1.553, yaw=1.873,
)
ned2_102.move_pose(observation_pose)
ned2_102.grasp_with_tool()


parsed_ldr = lego_piece.parse_ldr("MinecraftSwamp.ldr")    # Parse the LDR file first
output_ldr = lego_piece.output_json(parsed_ldr)            # Then convert to JSON structure

parser = lego_piece.LegoParser("pieces.json")              # Create the Lego Parser object 
parser.parse()                                  # Iteratively create all Lego objects for the set
lego_pieces = parser.get_lego_pieces()   


coords = {"xm":0,"ym":0,"update":0}

share = SharedData()
share.dump(coords)
share.setIndex(3)
share.set_LegoList(lego_pieces)
assemble.set_pick_obj(share)

t1 = th.Thread(target= niryo_vision.vision, args = (ned2_101,share,))
t2 = th.Thread(target = call_movement_when_ready, args = (ned2_101,))

t1.start()
t2.start()
t1.join()

share.setUpdate(100)

t2.join()
print("Complete")