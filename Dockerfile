FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      tesseract-ocr \
      tesseract-ocr-eng \
      tesseract-ocr-hrv \
      tesseract-ocr-srp-latn \
      tesseract-ocr-script-latn \
      fonts-dejavu-core \
      fonts-liberation \
      fonts-freefont-ttf \
      fonts-noto-core \
      libjpeg-dev \
      zlib1g-dev \
      libpng-dev \
 && which tesseract && tesseract --version \
 && rm -rf /var/lib/apt/lists/*
 
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "1", "--timeout", "10", "app:app"]
