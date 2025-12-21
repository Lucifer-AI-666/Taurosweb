.PHONY: help install run test clean dev

help:
	@echo "TauroBot 3.0 Ultimate - Makefile Commands"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make install  - Install/update Python dependencies"
	@echo "  make run      - Run the Telegram bot (uses run.py)"
	@echo "  make dev      - Run bot directly (no checks)"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Clean temporary files and cache"
	@echo "  make help     - Show this help message"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	@python3 -m pip install --upgrade pip > /dev/null 2>&1 || pip install --upgrade pip
	@python3 -m pip install -r requirements.txt || pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

run:
	@python3 run.py || python run.py

dev:
	@echo "🔧 Starting bot in development mode..."
	@python3 bot.py || python bot.py

test:
	@echo "🧪 Running tests..."
	@python3 test_bot.py || python test_bot.py

clean:
	@echo "🧹 Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@find . -type f -name "temp_voice_*.mp3" -delete 2>/dev/null || true
	@echo "✅ Cleanup completed!"
