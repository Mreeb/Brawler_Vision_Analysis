import os
import cv2
import json
from ultralytics import YOLO
from firstpick import first_team
from skimage.metrics import structural_similarity as ssim

def load_images_from_folder(folder_path): 
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            images[filename] = img
    return images

def find_most_similar_image(input_image_path, folder_path):
    input_image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    images = load_images_from_folder(folder_path)

    max_similarity = 0
    most_similar_image = None

    for filename, image in images.items():
        resized_image = cv2.resize(image, (input_image.shape[1], input_image.shape[0]))
        similarity, _ = ssim(input_image, resized_image, full=True)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_image = filename
    return most_similar_image, max_similarity

import re

def Compare_Picked_Brawlers(boxes_folder_path, picked_brawlers_folder_path):
    blue_picked = {}
    red_picked = {}
    picked_count = 0

    # Regular expression to remove patterns like (1), (2), etc., trailing spaces, and "Picked" or "picked" at the end
    pattern = re.compile(r'\s*(\(\d+\)|Picked|picked)?\s*$', re.IGNORECASE)

    for input_image_filename in os.listdir(boxes_folder_path):
        if input_image_filename.startswith("Picked") and (input_image_filename.endswith(".png") or input_image_filename.endswith(".jpg")):
            input_image_path = os.path.join(boxes_folder_path, input_image_filename)
            most_similar, _ = find_most_similar_image(input_image_path, picked_brawlers_folder_path)
            
            # Clean the name by removing underscores, patterns like (1), (2), etc., "Picked", and trailing spaces
            most_similar_cleaned = os.path.splitext(most_similar.replace("_", ""))[0]
            most_similar_cleaned = pattern.sub("", most_similar_cleaned)

            if "Blue" in input_image_filename:
                position = input_image_filename.split("_")[2]
                blue_picked[position] = most_similar_cleaned
            elif "Red" in input_image_filename:
                position = input_image_filename.split("_")[2]
                red_picked[position] = most_similar_cleaned
            picked_count += 1

    # Additional cleaning check for "Picked", "picked", and trailing spaces before returning
    def clean_picked_suffix(name):
        return pattern.sub("", name)

    # Apply cleaning to final blue_picked and red_picked dictionaries
    blue_picked = {key: clean_picked_suffix(value) for key, value in blue_picked.items()}
    red_picked = {key: clean_picked_suffix(value) for key, value in red_picked.items()}

    return blue_picked, red_picked, picked_count

def Compare_Banned_Brawlers(boxes_folder_path, banned_brawlers_folder_path):
    blue_banned = []
    red_banned = []
    banned_count = 0

    # Regular expression to remove patterns like (1), (2), etc., trailing spaces, and "Banned" or "banned" at the end
    pattern = re.compile(r'\s*(\(\d+\)|Banned|banned)?\s*$', re.IGNORECASE)

    for input_image_filename in os.listdir(boxes_folder_path):
        if input_image_filename.startswith("Banned") and (input_image_filename.endswith(".png") or input_image_filename.endswith(".jpg")):
            input_image_path = os.path.join(boxes_folder_path, input_image_filename)
            most_similar, _ = find_most_similar_image(input_image_path, banned_brawlers_folder_path)
            
            # Clean the name by removing underscores, patterns like (1), (2), etc., "Banned", and trailing spaces
            most_similar_cleaned = os.path.splitext(most_similar.replace("_", ""))[0]
            most_similar_cleaned = pattern.sub("", most_similar_cleaned)

            if "Blue" in input_image_filename:
                blue_banned.append(most_similar_cleaned)
            elif "Red" in input_image_filename:
                red_banned.append(most_similar_cleaned)
            banned_count += 1

    # Additional cleaning check for "Banned", "banned", and trailing spaces before returning
    def clean_banned_suffix(name):
        return pattern.sub("", name)

    # Apply cleaning to final blue_banned and red_banned lists
    blue_banned = [clean_banned_suffix(name) for name in blue_banned]
    red_banned = [clean_banned_suffix(name) for name in red_banned]

    return blue_banned, red_banned, banned_count

def Generate_Team_Data(boxes_folder_path, picked_brawlers_folder_path, banned_brawlers_folder_path, side, game_mode):
    blue_picked, red_picked, picked_count = Compare_Picked_Brawlers(boxes_folder_path, picked_brawlers_folder_path)
    blue_banned, red_banned, banned_count = Compare_Banned_Brawlers(boxes_folder_path, banned_brawlers_folder_path)
    total_images = picked_count + banned_count

    if total_images != 12:
        print(f"Warning: Expected 12 images, but found {total_images} images in total.")
        for position in ["1st", "2nd", "3rd"]:
            if position not in blue_picked:
                blue_picked[position] = "Unidentified"
            if position not in red_picked:
                red_picked[position] = "Unidentified"

        while len(blue_banned) < 3:
            blue_banned.append("Unidentified")
        while len(red_banned) < 3:
            red_banned.append("Unidentified")

    # Create team data based on the side value
    if side == "Red":
        team_data = {
            "Game_Mode": game_mode,
            "First_Pick": side,
            "Red_Team": {
                "Banned": red_banned,
                "Picked": {
                    "1st": red_picked.get("1st", "Unidentified"),
                    "2nd": red_picked.get("2nd", "Unidentified"),
                    "3rd": red_picked.get("3rd", "Unidentified")
                }
            },
            "Blue_Team": {
                "Banned": blue_banned,
                "Picked": {
                    "1st": blue_picked.get("1st", "Unidentified"),
                    "2nd": blue_picked.get("2nd", "Unidentified"),
                    "3rd": blue_picked.get("3rd", "Unidentified")
                }
            }
        }
    else:  # side is "Blue"
        team_data = {
            "Game_Mode": game_mode,
            "First_Pick": side,
            "Blue_Team": {
                "Banned": blue_banned,
                "Picked": {
                    "1st": blue_picked.get("1st", "Unidentified"),
                    "2nd": blue_picked.get("2nd", "Unidentified"),
                    "3rd": blue_picked.get("3rd", "Unidentified")
                }
            },
            "Red_Team": {
                "Banned": red_banned,
                "Picked": {
                    "1st": red_picked.get("1st", "Unidentified"),
                    "2nd": red_picked.get("2nd", "Unidentified"),
                    "3rd": red_picked.get("3rd", "Unidentified")
                }
            }
        }

    return team_data

# Example usage
if __name__ == "__main__":
    boxes_folder_path = "boxes"  # Path to your 'boxes' folder
    picked_brawlers_folder_path = "PICKED_BRAWLERS"  # Path to 'Picked Brawlers' folder
    banned_brawlers_folder_path = "BANNED_BRAWLERS"  # Path to 'Banned Brawlers' folder

    model = YOLO("FirstPick.pt")
    
    side = first_team(image_path="Processed_Images/IMG_.png", model=model)

    team_data = Generate_Team_Data(
        boxes_folder_path,
        picked_brawlers_folder_path,
        banned_brawlers_folder_path,
        side
    )
    
    print(json.dumps(team_data, indent=4))