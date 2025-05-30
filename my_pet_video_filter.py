import os
import cv2
import numpy as np
import torch

# Load YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()

# COCO animal classes
ANIMAL_CLASSES = {
    14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep',
    19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe'
}

# Folder = script directory
folder = os.path.dirname(os.path.abspath(__file__))

def get_reference_animal():
    """Select a reference animal image: load, crop, and extract features"""
    while True:
        reference_name = input("Enter the name of the reference image with an animal (or 'exit' to quit): ").strip()
        if reference_name.lower() == 'exit':
            return None, None, None

        reference_path = os.path.join(folder, reference_name)
        ref_img = cv2.imread(reference_path)
        if ref_img is None:
            print("❌ Could not load image. Please try again.")
            continue

        results = model(ref_img)
        boxes = results.pred[0]

        for *box, conf, cls in boxes:
            cls_id = int(cls)
            if cls_id in ANIMAL_CLASSES:
                x1, y1, x2, y2 = map(int, box)
                ref_crop = ref_img[y1:y2, x1:x2]
                if ref_crop.size == 0:
                    continue

                ref_hsv = cv2.cvtColor(ref_crop, cv2.COLOR_BGR2HSV)
                ref_hist = cv2.calcHist([ref_hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
                ref_hist = cv2.normalize(ref_hist, ref_hist).flatten()
                ref_mean = ref_hsv.mean(axis=(0, 1))

                print(f"✅ Reference found: {ANIMAL_CLASSES[cls_id]}")
                return ref_hist, ref_mean, reference_name

        print("❌ No animals found. Try another image.")

# Get reference
ref_hist, ref_mean_color, reference_name = get_reference_animal()
if ref_hist is None:
    exit()

# Threshold values
hist_threshold = 0.6
color_threshold = 30

# Process all video files in folder
for filename in os.listdir(folder):
    if not filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        continue

    path = os.path.join(folder, filename)
    cap = cv2.VideoCapture(path)
    found_match = False
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 15 != 0:
            continue  # Skip frames for efficiency

        results = model(frame)
        boxes = results.pred[0]

        for *box, conf, cls in boxes:
            cls_id = int(cls)
            if cls_id not in ANIMAL_CLASSES:
                continue  # Only consider animals

            x1, y1, x2, y2 = map(int, box)
            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            color_mean = hsv.mean(axis=(0, 1))

            similarity = cv2.compareHist(ref_hist, hist, cv2.HISTCMP_CORREL)
            color_diff = np.linalg.norm(ref_mean_color - color_mean)

            if similarity > hist_threshold and color_diff < color_threshold:
                print(f"✓ Match in {filename} (frame {frame_count}): {ANIMAL_CLASSES[cls_id]}, similarity: {similarity:.2f}, Δ color: {color_diff:.1f}")
                found_match = True
                break

        if found_match:
            break

    cap.release()

    if not found_match:
        os.remove(path)
        print(f"✗ Deleted: {filename} (no similar animal found)")

print("\n🎉 Done! Only videos with animals similar in color to the reference remain.")
