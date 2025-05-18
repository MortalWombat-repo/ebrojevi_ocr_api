from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io

# Explicitly set the Tesseract binary path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image uploaded'}), 400

    try:
        image = Image.open(file.stream)
    except Exception as e:
        return jsonify({'error': f'Invalid image file: {str(e)}'}), 400

    try:
        text = pytesseract.image_to_string(image, lang='hrv+eng')
    except Exception as e:
        return jsonify({'error': f'OCR processing failed: {str(e)}'}), 500

    return jsonify({'text': text})

import subprocess

@app.route('/debug', methods=['GET'])
def debug_tesseract():
    try:
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
        return jsonify({'tesseract_version': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
