#!/bin/bash
apt-get update
# Install Tesseract
apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-hrv
# Run app
python app.py
