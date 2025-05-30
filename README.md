# 🐱 PurgeAllButCats

**Delete everything – except your cat photos.**
*Other pets are welcome too!*

![IMG_0047](https://github.com/user-attachments/assets/782f1b24-9669-4d39-b392-6f1afcca2c7b)

---

## 🐾 Two Purr-fect Modes

### 1. **Old-School Cat Filter**

Basic cat media detection. Keeps anything that looks feline enough.

```bash
cat_photo_filter.py
cat_video_filter.py
```

> 💬 *"If it meows (or looks like it does), it stays."*

---

### 2. **👑 Exclusive Pet Mode**

Keeps only the selected pet's photos/videos.
Just provide a reference image filename – your majestic companion deserves the spotlight.

```bash
my_pet_photo_filter.py
my_pet_video_filter.py
```

> 💬 *"Meee! I am the only one!"*

> ⚠️ Note: Accuracy depends on how visible your pet's face is in the reference photo.

---

## 🚀 How It Works

1. **Place the script(s)** inside your target folder (where your photos/videos are).
2. Run the script of your choice depending on the mode you want to use.

---

## 🧪 Example Commands

### 🐾 Old-School Cat Filter

```bash
python3 cat_photo_filter.py      # for images
python3 cat_video_filter.py      # for videos
```

### 👑 Exclusive Pet Filter

```bash
python3 my_pet_photo_filter.py my_pet.jpg      # for images
python3 my_pet_video_filter.py my_pet.jpg      # for videos
```

---

## 🤖 Automation Scripts

You can use **run\_all.sh** (Linux/macOS) or **run\_all.bat** (Windows) to automate the entire process.

---

### 🐧 `run_all.sh` – Linux/macOS

```bash
#!/bin/bash
set -e

echo "🐍 Creating virtual environment..."
python3 -m venv venv

echo "🔄 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing required libraries..."
pip install --upgrade pip
pip install torch torchvision opencv-python pandas requests seaborn "numpy>=2.0.0"

echo "▶ Running thumbnail.py (thumbnails deletion)..."
python3 thumbnail.py

echo "▶ Running cat_photo_filter.py (filtering images with cats)..."
python3 cat_photo_filter.py

echo "▶ Running cat_video_filter.py (filtering videos with cats)..."
python3 cat_video_filter.py

echo "✅ All scripts executed successfully!"
```

> 📁 This will:
>
> * Set up a virtual environment
> * Install required libraries
> * Delete thumbnails
> * Filter your media for cat content

---

### 🪠 `run_all.bat` – Windows

```bat
@echo off
REM Stop on error
setlocal enabledelayedexpansion

echo 🐍 Creating virtual environment...
python -m venv venv

echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📦 Installing required libraries...
python -m pip install --upgrade pip
python -m pip install torch torchvision opencv-python pandas requests seaborn "numpy>=2.0.0"

echo ▶ Running thumbnail.py (thumbnails deletion)...
python thumbnail.py

echo ▶ Running cat_photo_filter.py (filtering images with cats)...
python cat_photo_filter.py

echo ▶ Running cat_video_filter.py (filtering videos with cats)...
python cat_video_filter.py

echo ✅ All scripts executed successfully!

pause
```

> 📁 Same steps as above, adapted for Windows systems.

---

## 💌 Personal Note

> *This script was created to help filter through a massive export of photos – to keep only the most precious ones.*
> *It is dedicated to my beloved girl, who recently made her way to the clouds.*
> *You were the best. There will always be a place in my heart for you and the memories we shared.*
> *I miss you deeply, Selina. This is for you.*


---

## 📦 Requirements

* Python 3.8+
* Packages: `torch`, `torchvision`, `opencv-python`, `pandas`, `requests`, `seaborn`, `numpy>=2.0.0`

---

## 🐾 License

MIT – Free for everyone who loves their pets 💖

---
