from pyniryo import *
from shared import SharedData
import threading as th
import niryo_vision
import pick
import assemble
import lego_piece

# USED THIS
# to just test out various implementatoins before placing it with the rest of the code

ned2_101 = NiryoRobot("192.168.0.101")
ned2_101.calibrate_auto()
ned2_101.release_with_tool()
ned2_101.grasp_with_tool()
observation_pose = PoseObject(
    x=0.133421, y=-0.015, z=0.251,
    roll=-0.154, pitch=1.325, yaw=-0.117,
)
ned2_101.move_pose(observation_pose)

ass_pos = [0.307773, -0.029265, 0.330,-0.033, 0.124, -0.116,]
ned2_101.release_with_tool()
ned2_101.move_pose(*ass_pos)