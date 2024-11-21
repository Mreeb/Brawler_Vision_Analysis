from PIL import Image, ImageDraw
import os

def Brawler_Detection(image_path, model, output_folder, num_sections=9, conf_threshold=0.7):

    # Prepare the output folder
    if os.path.exists(output_folder):
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(output_folder)
    
    # Load the image
    image = Image.open(image_path)
    image_width, image_height = image.size

    # Define line intervals and adjustments
    line_interval = image_width // num_sections
    line_adjustments = [-50, -55, -30, -20, 70, 65, 60, 60, 10]
    line_positions = [(line_interval * i) + line_adjustments[i - 1] for i in range(1, num_sections)]
    line_labels = [
        "Banned_Blue", "Picked_Blue_3rd", "Picked_Blue_2nd", "Picked_Blue_1st",
        "Picked_Red_1st", "Picked_Red_2nd", "Picked_Red_3rd", "Banned_Red"
    ]

    # Draw lines on the image for debugging
    debug_image = image.copy()
    draw = ImageDraw.Draw(debug_image)
    for j, line_x in enumerate(line_positions):
        draw.line([(line_x, 0), (line_x, image_height)], fill='white', width=1)
    debug_image.save('image_with_lines.png')  # Save image with lines for debugging

    # Run YOLO model predictions
    predictions = model(image_path, save=True, conf=conf_threshold)
    original_image = Image.open(image_path)

    # Process predictions
    for i, result in enumerate(predictions[0].boxes.xyxy):  # xyxy format
        x_min, y_min, x_max, y_max = map(int, result[:4])  # Bounding box coordinates
        object_center_x = (x_min + x_max) // 2  # Center x-coordinate of the detected object

        # Find the closest line
        closest_line = None
        min_distance = float('inf')
        for j, line_x in enumerate(line_positions):
            distance = abs(object_center_x - line_x)
            if distance < min_distance:
                min_distance = distance
                closest_line = line_labels[j]

        # Crop and save the image
        cropped_image = original_image.crop((x_min, y_min, x_max, y_max))
        cropped_image.save(os.path.join(output_folder, f'{closest_line}_crop_{i}.png'))

    print(f"Cropped images saved in {output_folder}")
    print("Debug image with lines saved as image_with_lines.png")

# Example usage
# if __name__ == "__main__":
#     Brawler_Detection(
#         image_path='Processed_Images/IMG_203.png',
#         model_path='StableDetection1.pt'
#     )



# from ultralytics import YOLO
# from PIL import Image, ImageDraw
# import os

# model = YOLO('StableDetection1.pt')

# # Empty the output folder before adding new cropped images
# output_folder = 'boxes'
# if os.path.exists(output_folder):
#     for filename in os.listdir(output_folder):
#         file_path = os.path.join(output_folder, filename)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
# else:
#     os.makedirs(output_folder)  # Create the folder if it doesn't exist
# os.makedirs(output_folder, exist_ok=True)

# image_path = 'Processed_Images/IMG_203.png'
# image = Image.open(image_path)
# image_width, image_height = image.size

# num_sections = 9
# line_interval = image_width // num_sections

# # Intervals for Invisible lines for Section Location
# line_adjustments = [-50, -55, -30, -20, 70, 65, 60, 60, 10]
# line_positions = [(line_interval * i) + line_adjustments[i - 1] for i in range(1, num_sections)]

# line_labels = [
#     "Banned_Blue", "Picked_Blue_3rd", "Picked_Blue_2nd", "Picked_Blue_1st",
#     "Picked_Red_1st", "Picked_Red_2nd", "Picked_Red_3rd", "Banned_Red"
# ]

# draw = ImageDraw.Draw(image)
# for j, line_x in enumerate(line_positions):
#     draw.line([(line_x, 0), (line_x, image_height)], fill='white', width=1)
# image.save('image_with_lines.png')  # Save image with lines for debugging

# predictions = model(image_path, save=True, conf=0.7)
# original_image = Image.open(image_path)

# for i, result in enumerate(predictions[0].boxes.xyxy):  # xyxy format
#     x_min, y_min, x_max, y_max = map(int, result[:4])  # Bounding box coordinates
#     object_center_x = (x_min + x_max) // 2  # Center x-coordinate of the detected object

#     closest_line = None
#     min_distance = float('inf')
    
#     for j, line_x in enumerate(line_positions):
#         distance = abs(object_center_x - line_x)  # Calculate the distance from the line
        
#         if distance < min_distance:
#             min_distance = distance
#             closest_line = line_labels[j]

#     cropped_image = original_image.crop((x_min, y_min, x_max, y_max))
#     cropped_image.save(os.path.join(output_folder, f'{closest_line}_crop_{i}.png'))

# print(f"Cropped images saved in {output_folder}")
# print("Debug image with lines saved as image_with_lines.png")
