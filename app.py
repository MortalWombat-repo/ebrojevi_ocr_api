from flask import Flask, request, jsonify, Response
import json
import pytesseract
from PIL import Image
import io
import subprocess
import cv2
import numpy as np
import shutil
import locale

locale.setlocale(locale.LC_ALL, 'C.UTF-8')

pytesseract.pytesseract.tesseract_cmd = shutil.which('tesseract')

def preprocess_image(pil_image):
    image = np.array(pil_image.convert("L"))  # Grayscale
    #image = cv2.GaussianBlur(image, (3, 3), 0)  # Smooth noise
    #_, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Adaptive threshold
    return Image.fromarray(image)

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files.get('image')
    if not file:
        return Response(json.dumps({'error': 'No image uploaded'}, ensure_ascii=False),
                        mimetype='application/json'), 400

    try:
        image = Image.open(file.stream)
    except Exception as e:
        return Response(json.dumps({'error': f'Invalid image file: {str(e)}'}, ensure_ascii=False),
                        mimetype='application/json'), 400

    image = preprocess_image(image)

    try:
        text = pytesseract.image_to_string(image, lang='eng+srp_latn+hrv', config='--psm 6')
    except Exception as e:
        return Response(json.dumps({'error': f'OCR processing failed: {str(e)}'}, ensure_ascii=False),
                        mimetype='application/json'), 500

    return Response(json.dumps({'text': text}, ensure_ascii=False), mimetype='application/json')

@app.route('/debug', methods=['GET'])
def debug_tesseract():
    try:
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
        return jsonify({'tesseract_version': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def root():
    return "Hello from Flask!"
