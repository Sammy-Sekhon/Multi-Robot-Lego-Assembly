from pyniryo import *
from shared import SharedData
import threading as th
import niryo_vision


# ned2_102 = NiryoRobot("192.168.0.102")
# ned2_102.calibrate_auto()
# ned2_102.grasp_with_tool()
# ned2_102.release_with_tool()
# observation_pose = PoseObject(
#     x=0.150744, y=-0.012502, z=0.179668,
#     roll=0.355, pitch=1.553, yaw=1.873,
# )
# ned2_102.move_pose(observation_pose)
# ned2_102.grasp_with_tool()

piece_offset_x = -0.0078
piece_offset_y = -0.0078
piece_offset_z = 0.003
starting = [0.165476, -0.230722, 0.095170, 0.892, 1.533, -0.664,]

observation_pose = PoseObject(
    x=0.007052, y=0.178, z=0.351,
    roll=-2.812, pitch=1.489, yaw=-1.298,
)
# observation_pose = PoseObject(
#     x=0.150744, y=-0.012502, z=0.179668,
#     roll=0.355, pitch=1.553, yaw=1.873,
# )


# ned2_102.move_pose(*starting)

classObjs = {
    'black_hole_2x2':0,
    'blue_plate_2x4': 1,
    'blue_plate_6x10':2, 
    'brown_brick_2x2':3,
    'brown_brick_2x4':4,
    'brown_corner_brick_2x2':5,
    'brown_plate_2x2':6,
    'brown_plate_2x4':7,
    'brown_plate_2x6':8,
    'brown_plate_4x6':9,
    'craft_brick_1x2':10,
    'craft_tile_2x2':11,
    'dark_green_brick_2x2':12,
    'dark_green_brick_2x4':13,
    'dark_green_plate_1stud_2x2':14,
    'dark_green_plate_2studs_2x4':15,
    'green_corner_2x2':16,
    'green_hole_2x2':17,
    'green_plate_4x4':18,
    'red_groove_2x2':19,
    'red_plate_2x2':20,
    'tnt_1x2':21
    }

inst_len = 3


def test(share):
    ind,lego_pieces = get_piece(share)
    print(classObjs[lego_pieces[ind].info()[0]])
    share.setObjIndex(classObjs[lego_pieces[ind].info()[0]])

    print(share.getObjIndex())



def ass_xyz(share):
    ind,lego_pieces = get_piece(share)
    return lego_pieces[ind].info()[2],lego_pieces[ind].info()[3],lego_pieces[ind].info()[4]

def set_pick_obj(share):
    ind,lego_pieces = get_piece(share)
    print(ind)
    print(lego_pieces)
    share.setObjIndex(classObjs[lego_pieces[ind].info()[0]])
    share.setRotation(lego_pieces[ind].info()[6])

def get_piece(share):
    ind = share.getIndex()
    lego_pieces = share.get_LegoList()
    return ind,lego_pieces



# def assemble_pos(x,y,z):
#     # ass_pos = [0.165476, -0.230722, 0.095170, 0.355, 1.553, 1.873,]
#     ass_pos = [0.165476, -0.230722, 0.095170, 0.966, 1.516, -0.613,]
#     ass_pos[0] = ass_pos[0] + piece_offset_x * x
#     ass_pos[1] = ass_pos[1] + piece_offset_y * y
#     ass_pos[2] = ass_pos[2] + piece_offset_z * z
#     return ass_pos

def assembly(ned2,share):
    ind,lego_pieces = get_piece(share)

    ned2.move_pose(observation_pose)

    x,y,z = ass_xyz(share)

    ass_pos = [-0.00718, -0.207, 0.318,0.436,1.497, -1.181]

    ned2.move_pose(*ass_pos)

    

    ass_pos = [(x/1000), (y/1000), 0.170, 0.892, 1.533, -0.664,]

    ned2.move_pose(*ass_pos)

    

    if rotation.pitchBool(share):
        ass_pos[3] = -1.057
        ass_pos[4] = 1.547
        ass_pos[5] = -1.057
        # ass_pos[1] = ass_pos[1] 

    ned2.move_pose(*ass_pos)

    # ass_pos = [(x/1000), (y/1000), (z/1000) - 0.003, 0.892, 1.533, -0.664,]
    ass_pos[0] = (x/1000)
    ass_pos[1] = (y/1000)
    ass_pos[2] = (z/1000)
    ned2.move_pose(*ass_pos)

    ass_pos[2] = ass_pos[2] + 0.006
    ned2.release_with_tool()


    ass_pos[2] = ass_pos[2] + 10*piece_offset_z
    ned2.move_pose(*ass_pos)

    ned2.grasp_with_tool()

    ass_pos[2] = ass_pos[2] - 13*piece_offset_z
    ned2.move_pose(*ass_pos)


    ass_pos[2] = ass_pos[2] + 4*piece_offset_z
    ned2.move_pose(*ass_pos)

    ned2.release_with_tool()


    # ass compl

    share.setIndex(ind + 1)
    set_pick_obj(share)
    share.setGrab(2)


    pass