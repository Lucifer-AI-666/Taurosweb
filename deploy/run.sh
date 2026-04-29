#!/bin/bash
# TauroBot 3.0 Ultimate - Run Script
# This script simplifies starting the bot
# Run from the repo root: bash deploy/run.sh

# Resolve repo root (one level above this script's directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🐂 Starting TauroBot 3.0 Ultimate..."
echo ""

# Check if .env file exists
if [ ! -f "$REPO_ROOT/.env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env from .env.example..."
    cp "$REPO_ROOT/.env.example" "$REPO_ROOT/.env"
    echo "✅ .env file created. Please edit it with your bot token before running again."
    echo ""
    echo "You need to:"
    echo "1. Get a bot token from @BotFather on Telegram"
    echo "2. Edit .env file and set TELEGRAM_BOT_TOKEN"
    echo "3. Make sure Ollama is running (ollama serve)"
    echo ""
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import telegram" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r "$REPO_ROOT/backend/requirements.txt"
    echo "✅ Dependencies installed!"
    echo ""
fi

# Create memory directory if it doesn't exist
mkdir -p "$REPO_ROOT/memory"

# Run the bot from the repo root so that `backend` is importable
echo "🚀 Launching bot..."
cd "$REPO_ROOT"
python3 -m backend.bot
