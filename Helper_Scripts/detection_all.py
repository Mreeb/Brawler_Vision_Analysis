from ultralytics import YOLO
from PIL import Image, ImageDraw
import os

model = YOLO('StableDetection1.pt')

# Define the output folder for cropped images 
output_folder = 'allboxesv5'
os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

# Define the path for the images to be processed
processed_images_folder = 'ProcessedScreenshotsv5'

# Get a list of all images in the folder (only files with common image extensions)
image_files = [f for f in os.listdir(processed_images_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Loop through each image file in the folder
for image_file in image_files:
    image_path = os.path.join(processed_images_folder, image_file)
    
    # Open the image
    image = Image.open(image_path)
    image_width, image_height = image.size

    # Define line positions for invisible lines
    num_sections = 9
    line_interval = image_width // num_sections
    line_adjustments = [-50, -55, -30, -20, 70, 65, 60, 60, 10]
    line_positions = [(line_interval * i) + line_adjustments[i - 1] for i in range(1, num_sections)]

    line_labels = [
        "Blue_Banned", "Blue_3rd", "Blue_2nd", "Blue_1st",
        "Red_1st", "Red_2nd", "Red_3rd", "Red_Banned"
    ]

    # Draw lines for debugging
    draw = ImageDraw.Draw(image)
    for j, line_x in enumerate(line_positions):
        draw.line([(line_x, 0), (line_x, image_height)], fill='white', width=1)
    
    # Save the image with lines for debugging
    image_with_lines_path = os.path.join('image_with_lines', f'{image_file}_with_lines.png')
    os.makedirs('image_with_lines', exist_ok=True)
    image.save(image_with_lines_path)

    # Run the model on the current image
    predictions = model(image_path, save=True, conf=0.7)
    original_image = Image.open(image_path)

    # Iterate through detected objects and crop them
    for i, result in enumerate(predictions[0].boxes.xyxy):  # xyxy format
        x_min, y_min, x_max, y_max = map(int, result[:4])  # Bounding box coordinates
        object_center_x = (x_min + x_max) // 2  # Center x-coordinate of the detected object

        closest_line = None
        min_distance = float('inf')

        # Determine the closest line to the object
        for j, line_x in enumerate(line_positions):
            distance = abs(object_center_x - line_x)  # Calculate the distance from the line

            if distance < min_distance:
                min_distance = distance
                closest_line = line_labels[j]

        # Crop and save the image with the closest line name
        cropped_image = original_image.crop((x_min, y_min, x_max, y_max))
        cropped_image.save(os.path.join(output_folder, f'{closest_line}_crop_{i}_{image_file}.png'))

    print(f"Processed {image_file} and saved cropped images in {output_folder}")

print(f"Debug images with lines saved in 'image_with_lines' folder")
