# from ultralytics import YOLO

# model = YOLO('FirstPick.pt')

def first_team(image_path, model, conf_threshold=0.80):
    results = model(image_path, conf=conf_threshold, save=True)
    mid_x = 240
    left_count = 0
    right_count = 0
    
    for result in results:
        if result.boxes is not None:  # Check if there are any detected boxes
            for box in result.boxes.xyxy:  # Extract bounding box coordinates
                x_center = (box[0] + box[2]) / 2  # Calculate center x-coordinate of bounding box
                
                if x_center > mid_x:
                    right_count += 1
                else:
                    left_count += 1

    if right_count > left_count:
        return "Blue"  # More objects on the right
    else:
        return "Red"   # More objects on the left

# side = first_team('Processed_Images/IMG_.png', model)

# print(f"{side} side had to Pick First.")
