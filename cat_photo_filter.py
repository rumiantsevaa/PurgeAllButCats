import os
import cv2
import torch

# Load YOLOv5s model (fastest version)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()
cat_class_id = 15  # "Cat" class in COCO dataset

# Folder with images — automatically set to the script's directory
folder = os.path.dirname(os.path.abspath(__file__))

# Iterate over all files in the folder
for filename in os.listdir(folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        path = os.path.join(folder, filename)
        img = cv2.imread(path)
        if img is None:
            continue

        # Object detection
        results = model(img)
        labels = results.pred[0][:, -1].cpu().numpy()

        if cat_class_id in labels:
            print(f'✓ Cat detected: {filename}')
        else:
            os.remove(path)
            print(f'✗ No cat — deleted: {filename}')

print('\n🎉 Done: all images without cats have been deleted.')
