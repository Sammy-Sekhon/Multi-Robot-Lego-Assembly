import json
from shared import SharedData

def read_lego_data(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'")
        return None

def get_all_placements_data(lego_data):
    all_placements = []
    placements_list = lego_data.get("placements")
    if isinstance(placements_list, list):
        for placement in placements_list:
            piece = placement.get('piece')
            position = placement.get('position')
            if piece and position:
                all_placements.append((piece, position))
    return all_placements


def low_z(lego_pieces):
    min = lego_pieces[0][1]['z']
    piece = lego_pieces[0]
    for x in lego_pieces:
        if min > x[1]['z']:
            min = x[1]['z']
            piece = x
    return piece       


share = SharedData()
file_path = "response.json"
lego_data = read_lego_data(file_path)
lego_pieces = get_all_placements_data(lego_data)
share.set_LegoList(lego_pieces)
legolist = share.get_LegoList()
print(legolist)
print(low_z(lego_pieces))
share.set_PickPlaceObj(low_z(lego_pieces))
print(share.get_ass)
print(share.getObjIndex)
# legolist.remove(low_z(lego_pieces))
# print(legolist)