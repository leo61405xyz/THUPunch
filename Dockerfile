FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    libnss3 \
    libsm6 \
    libgbm-dev \
    libdbus-glib-1-2 \
    fonts-liberation \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get -y install tesseract-ocr

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

WORKDIR /app

COPY . ./ 
VOLUME /app

RUN python3 -m pip install -r requirements.txt
CMD python THUPunch.py