FROM python:3.11-slim

# Install Tesseract and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-hrv \
    tesseract-ocr-srp \
    locales \
    fonts-dejavu-core \
    && locale-gen en_US.UTF-8 \
    && update-locale LANG=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

RUN tesseract --version

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Expose the application port
EXPOSE 10000

# Set the entry point to start Flask with Gunicorn
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:$PORT", "app:app"]
