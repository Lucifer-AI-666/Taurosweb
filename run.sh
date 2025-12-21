#!/bin/bash
# TauroBot 3.0 Ultimate - Run Script
# This script helps you easily start the Telegram bot

set -e

echo "🐂 TauroBot 3.0 Ultimate - Launcher"
echo "===================================="
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  File .env non trovato!"
    echo "Copiando .env.example in .env..."
    cp .env.example .env
    echo "✅ File .env creato."
    echo ""
    echo "⚠️  IMPORTANTE: Modifica il file .env con il tuo TELEGRAM_BOT_TOKEN!"
    echo "   Ottieni il token da @BotFather su Telegram"
    echo ""
    read -p "Premi INVIO quando hai configurato il file .env..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment non trovato. Creazione in corso..."
    python3 -m venv venv
    echo "✅ Virtual environment creato."
fi

# Activate virtual environment
echo "🔄 Attivazione virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installazione/aggiornamento dipendenze..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo ""
echo "✅ Dipendenze installate!"
echo ""

# Check if Ollama is running
echo "🔍 Verifica connessione Ollama..."
OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
if curl -s "${OLLAMA_HOST}/api/tags" > /dev/null 2>&1; then
    echo "✅ Ollama è raggiungibile su ${OLLAMA_HOST}"
else
    echo "⚠️  Ollama non sembra essere in esecuzione su ${OLLAMA_HOST}"
    echo "   Avvia Ollama con: ollama serve"
    echo "   Oppure scarica da: https://ollama.ai"
    echo ""
    read -p "Vuoi continuare comunque? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🚀 Avvio TauroBot 3.0 Ultimate..."
echo "   Premi Ctrl+C per fermare il bot"
echo ""
echo "===================================="
echo ""

# Run the bot
python bot.py
