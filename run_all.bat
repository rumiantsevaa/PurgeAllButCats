# Run Old-School Cat Filter on Windows
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

echo ▶ Running video_filter.py (filtering videos with cats)...
python cat_video_filter.py

echo ✅ All scripts executed successfully!

pause
