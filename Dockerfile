# TauroBot 3.0 Ultimate - Dockerfile
# Bot AI avanzato per Telegram con Ollama

FROM python:3.11-slim

# Metadata
LABEL maintainer="Lucifer-AI-666"
LABEL version="3.0.0"
LABEL description="TauroBot 3.0 Ultimate - Bot AI per Telegram"

# Variabili di ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Rome

# Directory di lavoro
WORKDIR /app

# Installa dipendenze di sistema per pyttsx3 e audio
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak \
    libespeak1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e installa dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY . .

# Crea directory per memoria e logs
RUN mkdir -p /app/memory /app/logs

# Volume per persistenza dati
VOLUME ["/app/memory", "/app/logs"]

# Utente non-root per sicurezza
RUN useradd --create-home --shell /bin/bash taurobot && \
    chown -R taurobot:taurobot /app
USER taurobot

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Comando di avvio
CMD ["python", "bot.py"]
