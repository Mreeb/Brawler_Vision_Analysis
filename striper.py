import os
import re

# Define the path to your folder containing character images
characters_folder = 'PICKED_BRAWLERS'  # Replace with your folder name

# List all image files in the folder
image_files = [img for img in os.listdir(characters_folder) if os.path.isfile(os.path.join(characters_folder, img))]

# Regular expression to match image names with trailing underscores
pattern = re.compile(r'^(.*?)(_{1,})$')

# Function to rename files based on the number of underscores
def rename_image_files(image_files):
    for image in image_files:
        # Get the file name and extension
        name, ext = os.path.splitext(image)

        # Check if the name ends with one or more underscores
        match = pattern.match(name)
        if match:
            base_name = match.group(1)
            underscore_count = len(match.group(2))

            # Rename based on the count of underscores
            new_name = f"{base_name} ({underscore_count + 1}){ext}"
            
            # Define old and new file paths
            old_path = os.path.join(characters_folder, image)
            new_path = os.path.join(characters_folder, new_name)
            
            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {image} -> {new_name}")

# Run the renaming function
rename_image_files(image_files)
