#!/bin/bash
set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║  🔧 TauroBot 3.0 - FIX EVERYTHING                 ║"
echo "║  Risolve TUTTI i problemi trovati                 ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# 1. Fix Python dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  FIXING PYTHON DEPENDENCIES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Fix cryptography (cffi_backend error)
print_warning "Fixing cryptography cffi_backend error..."
pip3 install --ignore-installed --force-reinstall cffi cryptography 2>&1 | tail -5

# Install ALL missing dependencies
print_warning "Installing missing Python packages..."
pip3 install -r requirements.txt --upgrade

print_status "Python dependencies fixed!"
echo ""

# 2. Test Python imports
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  TESTING PYTHON IMPORTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

FAILED=0

echo -n "Testing telegram... "
if python3 -c "import telegram" 2>/dev/null; then
    print_status "OK"
else
    print_error "FAILED"
    FAILED=1
fi

echo -n "Testing ollama... "
if python3 -c "import ollama" 2>/dev/null; then
    print_status "OK"
else
    print_error "FAILED - ollama package missing"
    FAILED=1
fi

echo -n "Testing pyttsx3... "
if python3 -c "import pyttsx3" 2>/dev/null; then
    print_status "OK"
else
    print_error "FAILED"
    FAILED=1
fi

echo -n "Testing aiofiles... "
if python3 -c "import aiofiles" 2>/dev/null; then
    print_status "OK"
else
    print_error "FAILED"
    FAILED=1
fi

echo -n "Testing yaml... "
if python3 -c "import yaml" 2>/dev/null; then
    print_status "OK"
else
    print_error "FAILED"
    FAILED=1
fi

echo ""

# 3. Check .env
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  CHECKING CONFIGURATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f .env ]; then
    print_status ".env file exists"

    if grep -q "your_telegram_bot_token_here" .env; then
        print_warning ".env has placeholder token - UPDATE IT!"
    else
        print_status "Telegram token configured"
    fi
else
    print_error ".env file missing!"
    print_warning "Creating .env from .env.example..."
    cp .env.example .env
    print_warning "⚠️  EDIT .env and add your Telegram token!"
fi

echo ""

# 4. Check Ollama
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  CHECKING OLLAMA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v ollama &> /dev/null; then
    print_status "Ollama CLI installed"

    if curl -s http://localhost:11434/api/tags &>/dev/null; then
        print_status "Ollama server is running"

        if curl -s http://localhost:11434/api/tags | grep -q "llama2"; then
            print_status "llama2 model available"
        else
            print_warning "llama2 model NOT found - run: ollama pull llama2"
        fi
    else
        print_warning "Ollama server NOT running - run: ollama serve"
    fi
else
    print_error "Ollama NOT installed"
    echo ""
    echo "Install Ollama:"
    echo "  Linux:  curl -fsSL https://ollama.com/install.sh | sh"
    echo "  macOS:  brew install ollama"
    echo ""
fi

echo ""

# 5. Install Vercel CLI (optional)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  CHECKING DEPLOYMENT TOOLS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v node &> /dev/null; then
    print_status "Node.js installed: $(node -v)"

    if command -v vercel &> /dev/null; then
        print_status "Vercel CLI installed"
    else
        print_warning "Vercel CLI not installed"
        read -p "Install Vercel CLI? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            npm install -g vercel
            print_status "Vercel CLI installed!"
        fi
    fi
else
    print_error "Node.js NOT installed (needed for Vercel CLI)"
fi

echo ""

# 6. Test PWA files
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6️⃣  CHECKING PWA FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

PWA_FILES=(
    "pwa/login.html"
    "pwa/dashboard.html"
    "pwa/garage.html"
    "pwa/gateway.html"
    "manifest.json"
    "service-worker.js"
)

for file in "${PWA_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_status "$file"
    else
        print_error "$file MISSING!"
    fi
done

echo ""

# 7. Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $FAILED -eq 0 ]; then
    print_status "All Python imports working!"
else
    print_error "Some Python imports failed - check errors above"
fi

echo ""
echo "NEXT STEPS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Start Ollama:"
echo "   ollama serve"
echo ""
echo "2️⃣  Pull llama2 model:"
echo "   ollama pull llama2"
echo ""
echo "3️⃣  Configure .env:"
echo "   Edit .env and add your TELEGRAM_BOT_TOKEN"
echo ""
echo "4️⃣  Start the bot:"
echo "   python3 bot.py"
echo ""
echo "5️⃣  Test PWA locally:"
echo "   python3 -m http.server 8000"
echo "   Open: http://localhost:8000/pwa/login.html"
echo ""
echo "6️⃣  Deploy PWA online:"
echo "   Option A: drag taurobot-pwa-ready.zip to https://app.netlify.com/drop"
echo "   Option B: ./deploy_vercel.sh"
echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✅ FIX COMPLETED!                                ║"
echo "╚════════════════════════════════════════════════════╝"
