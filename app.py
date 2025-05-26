from flask import Flask, request, jsonify, Response
from PIL import Image
import pytesseract
import numpy as np
import cv2
import subprocess
import os
import json

# Path to Tesseract binary
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

app = Flask(__name__)

def preprocess_dual(image: Image.Image):
    """Convert image to grayscale and produce both normal and inverted versions."""
    img = np.array(image)
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img
    inverted = cv2.bitwise_not(gray)
    return gray, inverted

def contains_croatian_chars(text):
    cro_chars = set("čćđžšČĆĐŽŠ")
    return any(c in text for c in cro_chars)

def run_ocr(image_np, lang='Latin', config='--oem 3 --psm 6'):
    """Run Tesseract OCR on a grayscale image with specified language and config."""
    return pytesseract.image_to_string(image_np, config=config, lang=lang)

@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files.get('image')
    if not file:
        return Response(json.dumps({'error': 'No image uploaded'}, ensure_ascii=False),
                        mimetype='application/json'), 400

    try:
        image = Image.open(file.stream).convert('RGB')
    except Exception as e:
        return Response(json.dumps({'error': f'Invalid image file: {str(e)}'}, ensure_ascii=False),
                        mimetype='application/json'), 400

    gray, inverted = preprocess_dual(image)

    try:
        # Step 1: Try Croatian OCR
        text_hrv_normal = run_ocr(gray, lang='Latin')
        text_hrv_inverted = run_ocr(inverted, lang='Latin+hrv')
        text_hrv = text_hrv_inverted if len(text_hrv_inverted.strip()) > len(text_hrv_normal.strip()) else text_hrv_normal

        if contains_croatian_chars(text_hrv):
            final_text = text_hrv
        else:
            # Step 2: Fallback to English OCR
            text_eng_normal = run_ocr(gray, lang='eng')
            text_eng_inverted = run_ocr(inverted, lang='eng')
            text_eng = text_eng_inverted if len(text_eng_inverted.strip()) > len(text_eng_normal.strip()) else text_eng_normal
            final_text = text_eng if len(text_eng.strip()) > len(text_hrv.strip()) else text_hrv

        final_text = final_text.replace('£', 'E')

    except Exception as e:
        return Response(json.dumps({'error': f'OCR failed: {str(e)}'}, ensure_ascii=False),
                        mimetype='application/json'), 500

    return Response(json.dumps({'text': final_text}, ensure_ascii=False), mimetype='application/json')

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
    return "Hello from Flask OCR!"

if __name__ == '__main__':
    app.run(debug=True)
