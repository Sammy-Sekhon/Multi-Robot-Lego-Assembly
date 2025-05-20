
import json
import numpy as np
from coord_map import inverse_transform
from ldr_parser import parse_ldr, output_json

class LegoPiece:
    def __init__(self, part_name, position_mm, color_code, rotation_matrix):
        self.part_name = part_name
        self.position = self.convert_coords(position_mm)
        self.color_code = color_code
        self.part_class = self.map_part_to_class()
        self.rotation_matrix = rotation_matrix

    def map_part_to_class(self):
        part_class_mapping = {
        "Plate 6 x 10": "blue_plate_6x10",
        "Plate 4 x 6": "brown_plate_4x6",
        "Plate Special 2 x 4 with Groove and Two Center Studs (Jumper)": "dark_green_plate_2studs_2x4",
        "Brick 2 x 2 Corner": "brown_corner_brick_2x2",
        "Plate 2 x 6": "brown_plate_2x6",
        "Plate Round 2 x 2 with Axle Hole Type 1 (+ Opening)": "black_hole_2x2",
        "Brick 1 x 2 with Reddish Brown and Dark Brown Lines Print": "craft_brick_1x2",
        "Tile 2 x 2 with Dark Brown Minecraft Grid Print (Crafting Table)": "craft_tile_2x2",
        "Plate 4 x 4": "green_plate_4x4",
        "Brick 1 x 2 with Black 'TNT' Pixelated Print": "tnt_1x2"
        }
        # Handle cases with redundant names
        if self.part_name == "Plate 2 x 4":
            if self.color_code == 1:
                return "blue_plate_2x4"
            else:
                return "brown_plate_2x4"
        if self.part_name == "Brick 2 x 2":
            if self.color_code == 70:
                return "brown_brick_2x2"
            else:
                return "dark_green_brick_2x2"
        if self.part_name == "Brick 2 x 4":
            if self.color_code == 70:
                return "brown_brick_2x4"
            else:
                return "dark_green_brick_2x4"
        if self.part_name == "Plate Special 2 x 2 with Groove and Center Stud (Jumper)":
            if self.color_code == 288:
                return "dark_green_plate_1stud_2x2"
            elif self.color_code == 4:
                return "red_groove_2x2"
            else:
                return "green_hole_2x2"
        if self.part_name == "Plate 2 x 2":
            if self.color_code == 4:
                return "red_plate_2x2"
            else:
                return "brown_plate_2x2"
        return part_class_mapping.get(self.part_name, "unknown_part")

    def convert_coords(self, coords):
        try:
            temp = np.array([coords['x'], coords['y'], abs(coords['z'])])
            converted = inverse_transform(temp)
            return {"x": converted[0], "y": converted[1], "z": converted[2]}
        except Exception as e:
            print(f"Error in convert_coords: {e}")
            return {"x": 0, "y": 0, "z": 0}

    def __repr__(self):
        return (f"LegoPiece(class={self.part_class}, part_name={self.part_name}, "
                f"x={self.position['x']}, y={self.position['y']}, z={self.position['z']}, color={self.color_code})")
    
    def info(self):
        return self.part_class, self.part_name, self.position['x'], self.position['y'], self.position['z'], self.color_code, self.rotation_matrix

class LegoParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lego_pieces = []

    def load_json(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def parse(self):
        data = self.load_json()
        for part in data:
            lego_piece = LegoPiece(part["part_name"], part["position_mm"], part["color_code"], part["rotation_matrix"])
            self.lego_pieces.append(lego_piece)

    def get_lego_pieces(self):
        return self.lego_pieces

# USAGE

# parsed_ldr = parse_ldr("MinecraftSwamp.ldr")    # Parse the LDR file first
# output_ldr = output_json(parsed_ldr)            # Then convert to JSON structure

# parser = LegoParser("pieces.json")              # Create the Lego Parser object 
# parser.parse()                                  # Iteratively create all Lego objects for the set
# lego_pieces = parser.get_lego_pieces()      
# # print(lego_pieces)   
# lego_piece = np.array(lego_pieces[0].info()[6]).astype(float)[0]
# print(lego_piece)
# for piece in lego_pieces:                       # Iterate and print all Lego objects in the set
#     print(piece.info()[6])
