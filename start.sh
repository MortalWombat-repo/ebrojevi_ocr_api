#!/bin/bash
apt-get update
apt-get install -y curl tesseract-ocr tesseract-ocr-eng tesseract-ocr-hrv

python app.py
