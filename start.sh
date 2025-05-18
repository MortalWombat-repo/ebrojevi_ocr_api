#!/bin/bash
apt-get update
apt-get install -y curl tesseract-ocr tesseract-ocr-eng tesseract-ocr-hrv

# Install uv
curl -Ls https://astral.sh/uv/install.sh | bash
export PATH="$HOME/.cargo/bin:$PATH"

uv pip install -r requirements.txt

python app.py
