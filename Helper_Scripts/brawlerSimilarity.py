import cv2
import os
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
        # Resize images to be the same size for SSIM comparison
        resized_image = cv2.resize(image, (input_image.shape[1], input_image.shape[0]))

        # Calculate SSIM similarity
        similarity, _ = ssim(input_image, resized_image, full=True)

        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_image = filename

    return most_similar_image, max_similarity

# Example usage
folder_path = "PICKED_BRAWLERS"
input_image_path = "Blue_3rd_crop_9_IMG_202.png"
most_similar, similarity_score = find_most_similar_image(input_image_path, folder_path)
print(f"Most similar image: {most_similar} with similarity score: {similarity_score:.2f}")
