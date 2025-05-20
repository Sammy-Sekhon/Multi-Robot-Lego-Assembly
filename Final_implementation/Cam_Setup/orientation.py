from pyniryo import *
from shared import SharedData
import threading as th
import niryo_vision
import coord
'''
    FUTURE IMPLEMENTATINO
    FiX FOR UPSIDE DOWN ORIENTATION OF THE PIECES
'''
ned2_101 = NiryoRobot("192.168.0.101")
ned2_101.calibrate_auto()
ned2_101.release_with_tool()
ned2_101.grasp_with_tool()
observation_pose = PoseObject(
    x=0.133421, y=-0.015, z=0.251,
    roll=-0.154, pitch=1.325, yaw=-0.117,
)
ned2_101.move_pose(observation_pose)

ned2_102 = NiryoRobot("192.168.0.102")
ned2_102.calibrate_auto()
# ned2_102.grasp_with_tool()
ned2_102.release_with_tool()
observation_pose = PoseObject(
    x=0.150744, y=-0.012502, z=0.179668,
    roll=0.355, pitch=1.553, yaw=1.873,
)
ass_pos = [0.007052, 0.178, 0.351,0.355, 1.553, 1.873,]
ned2_102.move_pose(*ass_pos)



ass_pos = [0.007052, 0.178, 0.351,0.355, 1.553, 1.873,]
ned2_102.move_pose(*ass_pos)


ass_pos = [-0.052101, 0.357, 0.101,0.121, 1.511, 1.641,]
ned2_102.move_pose(*ass_pos)

ned2_102.grasp_with_tool()

ass_pos = [-0.003601, 0.229, 0.331,0.035, 0.016, 1.610,]
ned2_102.move_pose(*ass_pos)


ass_pos = [0.267773, -0.019265, 0.333,-0.033, 0.124, -0.116,]
ned2_101.release_with_tool()
ned2_101.move_pose(*ass_pos)
ned2_101.grasp_with_tool()

ned2_102.release_with_tool()
ass_pos = [-0.003601, 0.229, 0.291,0.035, 0.016, 1.610,]
ned2_102.move_pose(*ass_pos)
ned2_102.move_pose(observation_pose)


ass_pos = [0.311896, -0.064265, 0.096,-2.502, 1.540, -2.5,]

ned2_101.move_pose(*ass_pos)
ned2_101.release_with_tool()

observation_pose = PoseObject(
    x=0.133421, y=-0.015, z=0.251,
    roll=-0.154, pitch=1.325, yaw=-0.117,
)
ned2_101.move_pose(observation_pose)