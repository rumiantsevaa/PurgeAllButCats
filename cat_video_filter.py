import os
import cv2
import torch

# Load YOLOv5s model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()
cat_class_id = 15  # "Cat" class in COCO dataset

# Folder with videos — current script directory
folder = os.path.dirname(os.path.abspath(__file__))

# Process video files
for filename in os.listdir(folder):
    if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        path = os.path.join(folder, filename)
        cap = cv2.VideoCapture(path)
        found_cat = False
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            # Skip frames for performance (e.g., 1 of every 15)
            if frame_count % 15 != 0:
                continue

            results = model(frame)
            labels = results.pred[0][:, -1].cpu().numpy()

            if cat_class_id in labels:
                print(f'✓ Cat detected in {filename}')
                found_cat = True
                break  # No need to check further

        cap.release()

        if not found_cat:
            os.remove(path)
            print(f'✗ No cat — deleted video: {filename}')

print('\n🎉 Done: all videos without cats have been deleted.')
