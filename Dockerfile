FROM python:3.11-slim

# Install Tesseract and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-hrv \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Run with gunicorn
CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:$PORT", "app:app"]
