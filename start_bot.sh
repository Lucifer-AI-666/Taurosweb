#!/bin/bash

# TauroBot 3.0 Starter Script
# Verifica dipendenze e avvia il bot

echo "🐂 TauroBot 3.0 Ultimate - Startup"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Check .env
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "   Copy .env.example to .env and configure your token"
    exit 1
fi
echo "✅ .env file found"

# Check token
if grep -q "your_telegram_bot_token_here" .env; then
    echo "❌ Telegram token not configured in .env"
    exit 1
fi
echo "✅ Telegram token configured"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Check Ollama
echo ""
echo "🔍 Checking Ollama..."
if curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "✅ Ollama is running on localhost:11434"
else
    echo "⚠️  Ollama not detected on localhost:11434"
    echo "   The bot will work but AI features need Ollama"
    echo "   Install: https://ollama.com"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create directories
mkdir -p memory logs

echo ""
echo "🚀 Starting TauroBot..."
echo "   Press Ctrl+C to stop"
echo ""

# Start bot
python3 bot.py
