# from PIL import Image
# import os

# # Define input and output folder paths
# input_folder = "Draft screenshots"
# output_folder = "Collars"

# # Create the output folder if it doesn't exist
# os.makedirs(output_folder, exist_ok=True)

# # Process each image in the input folder
# for filename in os.listdir(input_folder):
#     # Only process image files
#     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#         image_path = os.path.join(input_folder, filename)
        
#         # Open the image
#         with Image.open(image_path) as img:
#             # Resize the image to 1200x800
#             img_resized = img.resize((1200, 800))
            
#             # Crop the lower half of the resized image for Brawler Detection
#             lower_half = img_resized.crop((0, 500, 1200, 800))
            
#             # Save the lower half to the output folder with the same filename
#             lower_half.save(os.path.join(output_folder, filename))

# print("Processing complete!'.")



# from PIL import Image
# import os

# # Define input and output folder paths
# input_folder = "Draft Screenshots"
# output_folder = "Boundary"

# # Create the output folder if it doesn't exist
# os.makedirs(output_folder, exist_ok=True)

# # Process each image in the input folder
# for filename in os.listdir(input_folder):
#     # Only process image files
#     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#         image_path = os.path.join(input_folder, filename)
        
#         # Open the image
#         with Image.open(image_path) as img:
#             # Resize the image to 1200x800
#             img_resized = img.resize((1200, 800))
            
#             # Define the crop box for the lower half, excluding left and right sides
#             # For example, removing 100 pixels from both left and right sides
#             crop_box = (380, 500, 860, 800)  # (left, upper, right, lower)
            
#             # Crop the specified region from the resized image
#             cropped_image = img_resized.crop(crop_box)
            
#             # Save the cropped image to the output folder with the same filename
#             cropped_image.save(os.path.join(output_folder, filename))

# print("Processing complete!")




from PIL import Image
import os

# Define input and output folder paths
input_folder = "Draft screenshots"
output_folder = "Collars"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each image in the input folder
for filename in os.listdir(input_folder):
    # Only process image files
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(input_folder, filename)
        
        # Open the image
        with Image.open(image_path) as img:
            # Resize the image to 1200x800
            img_resized = img.resize((1200, 800))
            
            # Crop the lower half of the resized image for Brawler Detection
            lower_half = img_resized.crop((0, 0, 600, 200))
            
            # Save the lower half to the output folder with the same filename
            lower_half.save(os.path.join(output_folder, filename))

print("Processing complete!'.")