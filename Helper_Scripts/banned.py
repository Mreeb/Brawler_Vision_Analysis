import os
import shutil

# Define input and output folder paths
input_folder = "Brawlericons"
output_folder = "BannedIcons"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each image in the input folder
for filename in os.listdir(input_folder):
    # Check if "banned" is in the filename (case-insensitive) and it's an image file
    if "banned" in filename.lower() and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Define full paths for input and output
        source_path = os.path.join(input_folder, filename)
        destination_path = os.path.join(output_folder, filename)
        
        # Copy the file to the output folder
        shutil.copy2(source_path, destination_path)

print("Files with 'banned' in the name have been copied to 'BannedIcons' folder.")
