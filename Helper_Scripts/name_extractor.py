import os

folder_path = 'Brawlericons'

# Verify the folder exists and is a directory
if not os.path.exists(folder_path):
    print(f"The folder '{folder_path}' does not exist.")
elif not os.path.isdir(folder_path):
    print(f"The path '{folder_path}' is not a directory.")
else:
    image_files = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            name_without_extension = os.path.splitext(filename)[0]
            image_files.append(name_without_extension)

    # Print the resulting list
    print("Image files without extensions:", image_files)