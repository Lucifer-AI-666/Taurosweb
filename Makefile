.PHONY: help install run test clean setup

help:
	@echo "TauroBot 3.0 Ultimate - Makefile Commands"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup    - Initial setup (create venv, install deps, create .env)"
	@echo "  make install  - Install/update dependencies"
	@echo "  make run      - Run the Telegram bot"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Clean temporary files and cache"
	@echo "  make help     - Show this help message"
	@echo ""

setup: .env venv
	@echo "✅ Setup completato! Modifica il file .env con il tuo token."

.env:
	@if [ ! -f .env ]; then \
		echo "Creazione file .env..."; \
		cp .env.example .env; \
		echo "⚠️  IMPORTANTE: Modifica .env con il tuo TELEGRAM_BOT_TOKEN"; \
	fi

venv:
	@if [ ! -d venv ]; then \
		echo "Creazione virtual environment..."; \
		python3 -m venv venv; \
	fi

install: venv
	@echo "Installazione dipendenze..."
	@. venv/bin/activate && pip install --upgrade pip > /dev/null 2>&1
	@. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Dipendenze installate!"

run: venv .env
	@echo "🚀 Avvio TauroBot 3.0 Ultimate..."
	@. venv/bin/activate && python bot.py

test: venv
	@echo "🧪 Esecuzione test..."
	@. venv/bin/activate && python test_bot.py

clean:
	@echo "🧹 Pulizia file temporanei..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@find . -type f -name "temp_voice_*.mp3" -delete 2>/dev/null || true
	@echo "✅ Pulizia completata!"
