FROM python:3.14-slim

RUN apt-get update && apt-get install -y \
    espeak \
    espeak-ng \
    espeak-ng-data \
    ffmpeg \
    hunspell \
    hunspell-en-us \
    libsndfile1 \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m wn download omw-pt
RUN python -m wn download oewn
RUN python -m wn download odenet

EXPOSE 5000
CMD ["python", "run.py"]
