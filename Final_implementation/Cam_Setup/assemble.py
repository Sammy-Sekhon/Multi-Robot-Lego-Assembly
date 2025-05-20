from pyniryo import *
from shared import SharedData
import threading as th
import niryo_vision
import coord
import rotation


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

# Define offsets for placing pieces in the assembly
piece_offset_x = -0.0078
piece_offset_y = -0.0078
piece_offset_z = 0.003
# Define a starting pose, likely for initialization or a home position
starting = [0.165476, -0.230722, 0.095170, 0.892, 1.533, -0.664,]

# Define a pose for observing the workspace or picking area
observation_pose = PoseObject(
    x=0.007052, y=0.178, z=0.351,
    roll=-2.812, pitch=1.489, yaw=-1.298,
)
# Another potential observation pose, commented out
# observation_pose = PoseObject(
#     x=0.150744, y=-0.012502, z=0.179668,
#     roll=0.355, pitch=1.553, yaw=1.873,
# )


# Move the robot to the starting pose, commented out
# ned2_102.move_pose(*starting)

# Dictionary mapping object names to numerical indices
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


# Function to test retrieving a piece's class index from shared data
def test(share):
    ind,lego_pieces = get_piece(share)
    print(classObjs[lego_pieces[ind].info()[0]])
    share.setObjIndex(classObjs[lego_pieces[ind].info()[0]])

    print(share.getObjIndex())


# Function to retrieve the x, y, and z coordinates of a piece from shared data
def ass_xyz(share):
    ind,lego_pieces = get_piece(share)
    return lego_pieces[ind].info()[2],lego_pieces[ind].info()[3],lego_pieces[ind].info()[4]

# Function to set the object index and rotation in shared data based on the current piece
def set_pick_obj(share):
    ind,lego_pieces = get_piece(share)
    print(ind)
    print(lego_pieces)
    share.setObjIndex(classObjs[lego_pieces[ind].info()[0]])
    share.setRotation(lego_pieces[ind].info()[6])

# Function to get the current piece index and the list of Lego pieces from shared data
def get_piece(share):
    ind = share.getIndex()
    lego_pieces = share.get_LegoList()
    return ind,lego_pieces



# Function to calculate the assembly position based on piece coordinates and offsets, commented out
# def assemble_pos(x,y,z):
#     # ass_pos = [0.165476, -0.230722, 0.095170, 0.355, 1.553, 1.873,]
#     ass_pos = [0.165476, -0.230722, 0.095170, 0.966, 1.516, -0.613,]
#     ass_pos[0] = ass_pos[0] + piece_offset_x * x
#     ass_pos[1] = ass_pos[1] + piece_offset_y * y
#     ass_pos[2] = ass_pos[2] + piece_offset_z * z
#     return ass_pos

# Main assembly function that controls the robot's movement for placing a piece
def assembly(ned2,share):
    ind,lego_pieces = get_piece(share)

    # Move the robot to the observation pose
    ned2.move_pose(observation_pose)

    # Get the x, y, and z coordinates of the piece to be assembled
    x,y,z = ass_xyz(share)

    ass_pos = [-0.00718, -0.207, 0.318,0.436,1.497, -1.181]

    # Move the robot to the observation pose
    ned2.move_pose(*ass_pos)


 
    ass_pos = [(x/1000), (y/1000), 0.170, 0.892, 1.533, -0.664,]

    # Move the robot to the pick position
    ned2.move_pose(*ass_pos)


    # Adjust the robot's orientation if a specific pitch rotation is required
    if rotation.pitchBool(share):
        ass_pos[3] = -1.057
        ass_pos[4] = 1.547
        ass_pos[5] = -1.057
        # ass_pos[1] = ass_pos[1]

    ned2.move_pose(*ass_pos)

    # Define the final placement position, slightly above the target
    # ass_pos = [(x/1000), (y/1000), (z/1000) - 0.003, 0.892, 1.533, -0.664,]
    ass_pos[0] = (x/1000)
    ass_pos[1] = (y/1000)
    ass_pos[2] = (z/1000)
    # Move the robot to the final placement position
    ned2.move_pose(*ass_pos)

    # Move slightly down to place the piece
    ass_pos[2] = ass_pos[2] + 0.006
    ned2.release_with_tool()


    # Move up after releasing the piece
    ass_pos[2] = ass_pos[2] + 10*piece_offset_z
    ned2.move_pose(*ass_pos)

    ned2.grasp_with_tool()

    # Move down slightly
    ass_pos[2] = ass_pos[2] - 13*piece_offset_z
    ned2.move_pose(*ass_pos)


    # Move up again
    ass_pos[2] = ass_pos[2] + 4*piece_offset_z
    ned2.move_pose(*ass_pos)

    ned2.release_with_tool()


    # Assembly complete for the current piece

    # Increment the index to process the next piece
    share.setIndex(ind + 1)
    # Update shared data with the next piece's information
    set_pick_obj(share)

    share.setGrab(2)


    pass