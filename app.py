from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image uploaded'}), 400

    image = Image.open(file.stream)
    text = pytesseract.image_to_string(image, lang='hrv+eng')
    return jsonify({'text': text})
