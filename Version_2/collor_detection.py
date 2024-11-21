from ultralytics import YOLO
def Game_Mode_Detection(model, image_path):
    predictions = model(image_path, save=True, conf=0.70)
    max_confidence = 0
    best_class = None
    for result in predictions:
        for box in result.boxes:
            if box.conf > max_confidence:
                max_confidence = box.conf
                best_class = box.cls

    game_mode = model.names[int(best_class)] if best_class is not None else "No detection"
    return game_mode


# model = YOLO('Mode_Detection.pt')
# game_mode=Game_Mode_Detection(
#     model=model,
#     image_path="IMG_203.png"
#     )
# print(game_mode)