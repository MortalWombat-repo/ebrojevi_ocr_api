from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io

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
