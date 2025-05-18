from flask import Flask, request, jsonify, Response
import json
import pytesseract
from PIL import Image
import io
import subprocess
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def preprocess_image(pil_image):
    # Downscale while preserving aspect ratio
    pil_image.thumbnail((1200, 1200)) 
    
    # Convert to grayscale + sharpen
    img = np.array(pil_image.convert('L'))
    img = cv2.GaussianBlur(img, (1, 1), 0)
    return Image.fromarray(img)

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

import os
@app.route('/debug', methods=['GET'])
def debug_tesseract():
    try:
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True, check=True)
        path = os.environ.get('PATH', 'PATH not set')
        return jsonify({
            'tesseract_version': result.stdout.strip(),
            'tesseract_path': pytesseract.pytesseract.tesseract_cmd,
            'current_path': path
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': str(e),
            'stderr': e.stderr,
            'path': os.environ.get('PATH', 'PATH not set')
        }), 500
    except FileNotFoundError:
        return jsonify({
            'error': 'Tesseract executable not found',
            'path': os.environ.get('PATH', 'PATH not set')
        }), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def root():
    return "Hello from Flask!"
