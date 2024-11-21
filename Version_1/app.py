from fastapi import FastAPI, UploadFile, File, HTTPException
from BrawlerSimilaritySearch import Generate_Team_Data
from Detection_Algorithim import Brawler_Detection
from ultralytics import YOLO
from firstpick import first_team
from io import BytesIO
from PIL import Image
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI() 

# Folder paths for Saving and Extractng Images
PROCESSED_IMAGES = "PROCESSED"
PROCESSED_DRAFTS = f"{PROCESSED_IMAGES}/DRAFTS"
PROCESSED_TURN = f"{PROCESSED_IMAGES}/TURN"
ROI_BOXES = "ROI_BOXES"

# Ensure folders exist
os.makedirs(PROCESSED_DRAFTS, exist_ok=True)
os.makedirs(PROCESSED_TURN, exist_ok=True)
os.makedirs(ROI_BOXES, exist_ok=True)

# Define image processing constants 
BRAWLER_CROP_BOX = (0, 500, 1200, 800)
TURN_CROP_BOX = (380, 500, 860, 800)
RESIZE_DIMENSIONS = (1200, 800)

# Models
BRAWLER_DETECTION_MODEL = "StableDetection1.pt"
BOUNDRY_DETECTION_MODEL = "FirstPick.pt"

model_1 = YOLO(BOUNDRY_DETECTION_MODEL)
model_2 = YOLO(BRAWLER_DETECTION_MODEL)


# DataBase
picked_brawlers_folder_path = "PICKED_BRAWLERS"  # Path to 'Picked Brawlers' folder
banned_brawlers_folder_path = "BANNED_BRAWLERS"  # Path to 'Banned Brawlers' folder


@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")

    try:
        image = Image.open(BytesIO(await file.read()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not open image: {e}")

    try:
        img_resized = image.resize(RESIZE_DIMENSIONS)
        lower_half = img_resized.crop(BRAWLER_CROP_BOX)

        draft_image_path = os.path.join(PROCESSED_DRAFTS, f"image.png")
        #Saving
        lower_half.save(draft_image_path, format="PNG")

        cropped_turn_image = img_resized.crop(TURN_CROP_BOX)

        turn_image_path = os.path.join(PROCESSED_TURN, f"image.png")
        #Saving
        cropped_turn_image.save(turn_image_path, format="PNG")

        Brawler_Detection(
            image_path=f"{PROCESSED_DRAFTS}/image.png",
            model=model_2,
            output_folder=ROI_BOXES
        )

        # Team turn Identification 
        side = first_team(
            image_path=f"{PROCESSED_TURN}/image.png",
            model = model_1,
        )


        # Brawler Classification
        team_data = Generate_Team_Data(
        ROI_BOXES,
        picked_brawlers_folder_path,
        banned_brawlers_folder_path,
        side
        )

        return team_data
    
    except Exception as e:
        return{
            "Status": f"Error: {str(e)}"
        }
    
    
# Run FastAPI app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)



# if __name__ == "__main__":
#     model_1 = YOLO(BRAWLER_DETECTION_MODEL)
#     Brawler_Detection(
#         image_path=f"{PROCESSED_DRAFTS}/image.png",
#         output_folder= CROPED_BRAWLERS,
#         model=model_1,
#     )

