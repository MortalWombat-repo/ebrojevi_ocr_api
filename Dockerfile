FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      tesseract-ocr \
      tesseract-ocr-eng \
      tesseract-ocr-hrv \
      tesseract-ocr-srp \
      fonts-dejavu-core \
 && which tesseract && tesseract --version \
 && rm -rf /var/lib/apt/lists/*
 
# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

EXPOSE 9696

# Exec form invoking a shell to expand $PORT
ENTRYPOINT [ "sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app" ]
