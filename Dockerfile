FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      tesseract-ocr \
      tesseract-ocr-eng \
      tesseract-ocr-hrv \
      tesseract-ocr-srp-latn \
      fonts-dejavu-core \
      libjpeg-dev \
      zlib1g-dev \
      libpng-dev \
 && which tesseract && tesseract --version \
 && rm -rf /var/lib/apt/lists/*
 
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 9696

ENTRYPOINT [ "sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 app:app" ]
