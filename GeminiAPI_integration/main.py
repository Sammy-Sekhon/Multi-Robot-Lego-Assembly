from pyniryo import *
from shared import SharedData
import threading as th
import niryo_vision
import lego_piece



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
    x=0.007052, y=0.178, z=0.351,
    roll=0.355, pitch=1.553, yaw=1.873,
)

ned2_102.move_pose(observation_pose)


file_path = "response.json"
lego_data = lego_piece.read_lego_data(file_path)
lego_pieces = lego_piece.get_all_placements_data(lego_data)





coords = {"xm":0,"ym":0,"update":0}

share = SharedData()
share.dump(coords)
share.set_LegoList(lego_pieces)


t1 = th.Thread(target= niryo_vision.vision, args = (ned2_101,share,))

t1.start()
t1.join()
print("Complete")