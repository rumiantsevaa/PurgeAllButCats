# THIS MODE MAY BE HARSH, USE IT WITH CAUTION !!!

import os
import cv2
import numpy as np
import torch

# Load YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()

# All animal classes in COCO
ANIMAL_CLASSES = {14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep',
                  19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe'}

# Use the script's directory as the folder for photos
folder = os.path.dirname(os.path.abspath(__file__))

def get_reference_animal():
    """Get reference image with an animal"""
    while True:
        reference_name = input("Enter the name of the reference photo with an animal (or type 'exit' to quit): ").strip()
        if reference_name.lower() == 'exit':
            return None, None, None

        reference_path = os.path.join(folder, reference_name)
        ref_img = cv2.imread(reference_path)
        if ref_img is None:
            print("❌ Failed to load the photo. Please try again.")
            continue

        # Run detection on reference image
        results = model(ref_img)
        boxes = results.pred[0]

        # Search for any animal
        for *box, conf, cls in boxes:
            cls_id = int(cls)
            if cls_id in ANIMAL_CLASSES:
                # Crop the detected animal
                x1, y1, x2, y2 = map(int, box)
                ref_crop = ref_img[y1:y2, x1:x2]
                if ref_crop.size == 0:
                    continue

                # Prepare color metrics
                ref_hsv = cv2.cvtColor(ref_crop, cv2.COLOR_BGR2HSV)
                ref_hist = cv2.calcHist([ref_hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
                ref_hist = cv2.normalize(ref_hist, ref_hist).flatten()

                print(f"✅ Reference: {ANIMAL_CLASSES[cls_id]}, size: {ref_crop.shape[0]}x{ref_crop.shape[1]}")
                return ref_hist, ref_hsv.mean(axis=(0, 1)), reference_name

        print("❌ No animals found in the photo. Try another one.")

# Get the reference animal
ref_hist, ref_mean_color, reference_name = get_reference_animal()
if ref_hist is None:
    exit()

# Process other photos in the folder
for filename in os.listdir(folder):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        continue
    if filename == reference_name:
        continue

    path = os.path.join(folder, filename)
    img = cv2.imread(path)
    if img is None:
        continue

    results = model(img)
    boxes = results.pred[0]
    matched = False

    for *box, conf, cls in boxes:
        cls_id = int(cls)
        if cls_id not in ANIMAL_CLASSES:
            continue

        # Crop current animal
        x1, y1, x2, y2 = map(int, box)
        crop = img[y1:y2, x1:x2]
        if crop.size == 0:
            continue

        # Color metrics
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()

        # Compare with reference
        similarity = cv2.compareHist(ref_hist, hist, cv2.HISTCMP_CORREL)
        color_diff = np.linalg.norm(ref_mean_color - hsv.mean(axis=(0, 1)))

        if similarity > 0.6 and color_diff < 30:  # Thresholds can be adjusted
            print(f"✓ Kept: {filename} ({ANIMAL_CLASSES[cls_id]}, similarity: {similarity:.2f}, Δ color: {color_diff:.1f})")
            matched = True
            break

    if not matched:
        os.remove(path)
        print(f"✗ Deleted: {filename}")

print("\n🎉 Done! Kept only the photos with animals similar in color to the reference.")
