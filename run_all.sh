# Run Old-School Cat Filter on Linux
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

echo "▶ Running video_filter.py (filtering videos with cats)..."
python3 cat_video_filter.py

echo "✅ All scripts executed successfully!"

