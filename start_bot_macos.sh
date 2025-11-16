#!/bin/bash

# 🍎 TauroBot 3.0 Ultimate - macOS Edition
# For the rich kids with their fancy MacBooks 😎

echo "🍎 TauroBot 3.0 Ultimate - macOS Startup"
echo "==========================================="
echo "💰 Welcome, MacBook owner! 💰"
echo ""

# Check Homebrew
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew not found. Installing..."
    echo "   (Even rich kids need package managers)"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
echo "✅ Homebrew found"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "📦 Installing Python 3 via Homebrew..."
    brew install python3
fi
echo "✅ Python 3 found: $(python3 --version)"

# Check .env
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "   Copy .env.example to .env and configure your token"
    echo "   (Yes, even on your expensive Mac you need to configure things)"
    exit 1
fi
echo "✅ .env file found"

# Check token
if grep -q "your_telegram_bot_token_here" .env; then
    echo "❌ Telegram token not configured in .env"
    echo "   Money can't buy a configured token, sorry! 💸"
    exit 1
fi
echo "✅ Telegram token configured"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    echo "   (Making a cozy home for your Python packages)"
    python3 -m venv venv
fi

# Activate venv (macOS style)
source venv/bin/activate

# Upgrade pip (macOS can be picky)
echo "📦 Upgrading pip..."
pip install --quiet --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
echo "   (Your Mac's SSD can handle it, don't worry)"
pip install -q -r requirements.txt

# Check Ollama (macOS has nice GUI installer)
echo ""
echo "🔍 Checking Ollama..."
if curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "✅ Ollama is running on localhost:11434"
elif [ -d "/Applications/Ollama.app" ]; then
    echo "⚠️  Ollama installed but not running"
    echo "   Opening Ollama app..."
    open -a Ollama
    echo "   Waiting for Ollama to start..."
    sleep 3
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "✅ Ollama started successfully"
    else
        echo "⚠️  Ollama started but not responding yet"
        echo "   The bot will work but AI features need Ollama ready"
    fi
else
    echo "⚠️  Ollama not detected"
    echo ""
    echo "   💡 Install Ollama for Mac:"
    echo "   1. Download from: https://ollama.com/download"
    echo "   2. Install Ollama.app"
    echo "   3. Run this script again"
    echo ""
    read -p "Continue without Ollama? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create directories
mkdir -p memory logs

# macOS notification
if command -v osascript &> /dev/null; then
    osascript -e 'display notification "TauroBot is starting..." with title "🐂 TauroBot 3.0"'
fi

echo ""
echo "🚀 Starting TauroBot..."
echo "   Your MacBook Pro's powerful M-series chip is ready!"
echo "   Press Cmd+C to stop (or just close your $3000 laptop)"
echo ""

# Start bot
python3 bot.py

# On exit, show notification
if command -v osascript &> /dev/null; then
    osascript -e 'display notification "TauroBot stopped" with title "🐂 TauroBot 3.0"'
fi
