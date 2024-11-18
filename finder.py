# import os

# banned_icons_folder = 'PickedIcons'
# banned_brawlers_folder = 'PICKED_BRAWLERS'

# banned_icons_images = {os.path.splitext(img)[0] for img in os.listdir(banned_icons_folder) if os.path.isfile(os.path.join(banned_icons_folder, img))}
# banned_brawlers_images = {os.path.splitext(img)[0] for img in os.listdir(banned_brawlers_folder) if os.path.isfile(os.path.join(banned_brawlers_folder, img))}

# common_images = banned_icons_images.intersection(banned_brawlers_images)

# images_not_in_banned_brawlers = banned_icons_images - banned_brawlers_images

# print("Images present in both BannedIcons and BANNED_BRAWLERS:")
# for img in common_images:
#     print(f"- {img}")

# print("\nImages in BannedIcons but not in BANNED_BRAWLERS:")
# for img in images_not_in_banned_brawlers:
#     print(f"- {img}")


import os

# Define the paths to your folders
banned_icons_folder = 'PickedIcons'
banned_brawlers_folder = 'PICKED_BRAWLERS'

# Get the list of image names (excluding extensions) in each folder
banned_icons_images = {os.path.splitext(img)[0] for img in os.listdir(banned_icons_folder) if os.path.isfile(os.path.join(banned_icons_folder, img))}

# Remove trailing underscores only if present in some image names from BANNED_BRAWLERS
banned_brawlers_images = {
    os.path.splitext(img)[0].rstrip('_') if os.path.splitext(img)[0].endswith('_') else os.path.splitext(img)[0]
    for img in os.listdir(banned_brawlers_folder) if os.path.isfile(os.path.join(banned_brawlers_folder, img))
}

# Find common images in both folders
common_images = banned_icons_images.intersection(banned_brawlers_images)

# Find images in BannedIcons that are not in BANNED_BRAWLERS
images_not_in_banned_brawlers = banned_icons_images - banned_brawlers_images

# Print the results
print("Images present in both BannedIcons and BANNED_BRAWLERS:")
for img in common_images:
    print(f"- {img}")

print("\nImages in BannedIcons but not in BANNED_BRAWLERS:")
for img in images_not_in_banned_brawlers:
    print(f"- {img}")
