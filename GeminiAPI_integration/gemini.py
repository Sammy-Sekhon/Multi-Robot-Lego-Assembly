import json
import re
from google import genai
# from google.genai import types
import google.genai.types
import PIL.Image

# from parser import extract_and_standardize

image = PIL.Image.open("images/Instruction_18.jpg")

# sys_instruct = """You are an AI model specialized in interpreting LEGO instruction manuals. Given an image of a LEGO instruction page, extract the step-by-step assembly instructions in a structured format.

# Rules:
# 1. Extract steps **in exact order** as shown in the image.
# 2. Identify each LEGO piece by its official name (e.g., "Brown 2x4 LEGO Brick", towards the top of the image in a rectangular box shows a list of all the required pieces.
# 3. List the name of the LEGO pieces and assign a unique number to each (i.e 0 for the first block, 1 for the next).
# 4. Provide text-based instructions for the assembly.
# 5. **Ensure the output is a valid JSON. Do not include any extra text before or after the JSON.**"""

sys_instruct = """You are a LEGO expert. Given a LEGO instruction step image, your task is to analyze and provide structured output in JSON format. Follow these guidelines:

1. List of Pieces Used:
For each piece, specify:
quantity: (number of pieces)
description: (e.g., "8x16 blue plate") pay attention to the color
2. Placement Details (per piece):
piece: (reference to the piece description)
position:
x: (stud column number where the bottom-left corner of the piece starts, assuming bottom-left of main plate is x=1)
y: (stud row number where the bottom-left corner of the piece starts, assuming bottom-left of main plate is y=1)
z: (Piece height on top of which pieces it has been placed)
orientation: (optional, e.g., "horizontal" or "vertical", if relevant)
overlap: (optional, describe if it overlaps another piece and how)
3. Output Format:
Return only the JSON object. No explanations, no extra text.
Example format:
json
Copy
Edit
{
  "pieces": [
    { "quantity": 1, "description": "8x16 blue plate" },
    { "quantity": 1, "description": "4x8 blue plate" }
  ],
  "placements": [
    { "piece": "8x16 blue plate", "position": { "x": 1, "y": 1 }, "orientation": "horizontal" },
    { "piece": "4x8 blue plate", "position": { "x": 1, "y": 9 }, "orientation": "horizontal", "overlap": "overlaps first plate by 4 studs" }
  ]
}
⚙️ Important Notes:
Use stud coordinates for placement.
Orientation should be included if it's not obvious.
Be precise about overlap if applicable.
Return only valid JSON.
"""

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=google.genai.types.GenerateContentConfig(system_instruction=sys_instruct),
    contents=["Describe how to assemble the LEGO pieces in this image, step by step.", image]
)

# print("Response", repr(response.text))

json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
if json_match:
    clean_json_text = json_match.group(0) 
else:
    print("Error: No valid JSON found in response.")
    exit()

try:
    structured_data = json.loads(clean_json_text) 
except json.JSONDecodeError as e:
    print("Error parsing JSON:", e)
    exit()

with open("response.json", "w") as outfile:
    json.dump(structured_data, outfile, indent=4)

print("JSON output successfully saved.")

# processed_lego_data = extract_and_standardize(structured_data)
# print(json.dumps(processed_lego_data, indent=4))
