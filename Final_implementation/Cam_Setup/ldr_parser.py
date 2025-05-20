import re
import numpy as np
import os
import time
import requests
import json


LDU_TO_MM = 0.4  # LDraw units to mm conversion (1 LDU = 0.4 mm)

API_KEY = '1c0cf802b9af9ebe51692db94489a636'
BASE_URL = "https://rebrickable.com/api/v3/lego/parts/"
CACHE_FILE = "part_cache.json"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        part_cache = json.load(f)
else:
    part_cache = {}

def fetch_part(part_num):
    if part_num in part_cache:
        return part_cache[part_num]

    response = requests.get(f"{BASE_URL}{part_num}/", headers={"Authorization": f"key {API_KEY}"})

    # handle limits
    if response.status_code == 429:
        print("Rate limited. Sleeping for 60s...")
        time.sleep(60)
        return fetch_part(part_num)
    
    
    if response.status_code == 200:
        data = response.json()
        part_cache[part_num] = data

        with open(CACHE_FILE, "w") as f:
            json.dump(part_cache, f, indent=4)
        return data
    else:
        return {"name": "Unknown", "part_num": part_num}

# def clean_part_number(part_num):
#     match = re.match(r'(\d+)', part_num)
#     return match.group(1) if match else part_num

def parse_ldr(file_path):
    parsed_bricks = []
    step_ctr = 0
    with open("MinecraftSwamp.ldr", "r") as file:
        for line in file:
            line=line.strip()
            if line.startswith("0"):  # skip the meta commands
                if "STEP" in line:
                    step_ctr += 1
                continue
                
            if line.startswith("1"):    # parse the brick lines
                parts = re.split(r'\s+', line)

                x,z,y = [float(coord) * LDU_TO_MM for coord in parts[2:5]]

                color_code = int(parts[1])

                # 3x3 Rotation Matrix for part
                # rot_mtx = np.array([float(num) for num in parts[5:14]]).reshape((3,3))
                rot_mtx = []
                for num in parts[5:14]:
                    rot_mtx.append(num)

                part_file = parts[14].replace('.dat', '')
                # part_file = clean_part_number(part_file)

                part_info = fetch_part(part_file)
                part_name = part_info.get('name', 'Unknown Part')

                parsed_bricks.append({
                    "step": step_ctr,
                    "position_mm": {"x": x, "y": y, "z": z},
                    "color_code": color_code,
                    "part_num": part_file,
                    "part_name": part_name,
                    "rotation_matrix": rot_mtx,
                    "part": part_file
                })
    return parsed_bricks

def output_json(in_file):
    with open("pieces.json", 'w') as out_file:
        json.dump(in_file, out_file, indent=4)

    return out_file
# parsed_data = parse_ldr("MinecraftSwamp.ldr")
# output = output_json(parsed_data)

# for brick in parsed_data:
#     print(f"Step {brick['step']}:")
#     print(f"Part Number: {brick['part_num']}")
#     print(f"Part Name: {brick['part_name']}")
#     print(f"Color Code: {brick['color_code']}")
#     print(f"  Position (mm): {brick['position_mm']}")
#     print(f"  Rotation Matrix:\n{brick['rotation_matrix']}")
#     print(f"  Part: {brick['part']}\n")


