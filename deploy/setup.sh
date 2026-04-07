#!/bin/bash
# TauroBot 3.0 Ultimate - Setup Script
# This script helps with initial setup and configuration
# Run from the repo root: bash deploy/setup.sh

# Resolve repo root (one level above this script's directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🐂 TauroBot 3.0 Ultimate - Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "1️⃣  Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Install dependencies
echo "2️⃣  Installing Python dependencies..."
pip3 install -r "$REPO_ROOT/backend/requirements.txt"
echo "✅ Dependencies installed"
echo ""

# Create .env file if not exists
echo "3️⃣  Setting up environment file..."
if [ ! -f "$REPO_ROOT/.env" ]; then
    cp "$REPO_ROOT/.env.example" "$REPO_ROOT/.env"
    echo "✅ .env file created from template"
    echo ""
    echo "⚠️  IMPORTANT: You need to edit .env and configure:"
    echo "   - TELEGRAM_BOT_TOKEN (from @BotFather)"
    echo "   - OLLAMA_HOST (if different from default)"
    echo "   - OLLAMA_MODEL (if you want to use a different model)"
else
    echo "ℹ️  .env file already exists"
fi
echo ""

# Create necessary directories
echo "4️⃣  Creating directories..."
mkdir -p "$REPO_ROOT/memory"
mkdir -p "$REPO_ROOT/logs"
echo "✅ Directories created"
echo ""

# Check if Ollama is installed
echo "5️⃣  Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    
    # Get Ollama host from .env or use default
    OLLAMA_HOST="http://localhost:11434"
    if [ -f "$REPO_ROOT/.env" ]; then
        CONFIGURED_HOST=$(grep "^OLLAMA_HOST=" "$REPO_ROOT/.env" | cut -d'=' -f2)
        if [ ! -z "$CONFIGURED_HOST" ]; then
            OLLAMA_HOST="$CONFIGURED_HOST"
        fi
    fi
    
    # Check if Ollama is running
    if curl -s ${OLLAMA_HOST}/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama is running at ${OLLAMA_HOST}"
    else
        echo "⚠️  Ollama is not running at ${OLLAMA_HOST}. Start it with: ollama serve"
    fi
else
    echo "⚠️  Ollama not found. Please install from: https://ollama.ai"
fi
echo ""

# Summary
echo "========================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and set your TELEGRAM_BOT_TOKEN"
echo "2. Make sure Ollama is running: ollama serve"
echo "3. Pull a model if needed: ollama pull llama2"
echo "4. Run the bot: bash deploy/run.sh or python3 deploy/run.py"
echo ""
echo "For more help, see docs/INSTALL.md"
