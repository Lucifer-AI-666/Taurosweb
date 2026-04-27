# Copilot Instructions for Taurosweb / TauroBot 3.0 Ultimate

## Project Overview

Taurosweb is the official website and codebase for **TauroBot 3.0 Ultimate**, an advanced AI-powered Telegram bot that integrates Ollama for conversational AI, persistent memory, text-to-speech, rate limiting, multi-language support (i18n), reminder systems, and a Progressive Web App (PWA) frontend.

Primary language: **Python 3.11**. Comments and documentation are primarily in **Italian**.

---

## Repository Structure

```
Taurosweb/
├── bot.py               # Main Telegram bot (TauroBot class, command/message handlers)
├── memory.py            # Persistent memory system (conversation history per user)
├── voice.py             # Text-to-speech system (pyttsx3)
├── rate_limiter.py      # Anti-spam / rate limiting logic
├── reminders.py         # Reminder system (scheduling messages)
├── run.py               # Entry-point script to start the bot
├── run.sh               # Bash entry-point script
├── setup.sh             # Automated setup script
├── config.yml           # Bot configuration (Ollama, memory, voice, rate limits)
├── requirements.txt     # Python dependencies
├── .env.example         # Template for required environment variables
├── test_bot.py          # pytest test suite
├── i18n/                # Multi-language translation files (it, en, es, fr, de)
├── index.html           # PWA web interface
├── manifest.json        # PWA manifest
├── service-worker.js    # PWA service worker
├── generate_pwa_icons.py# PWA icon generator
├── Dockerfile           # Docker build file
├── docker-compose.yml   # Docker Compose (bot + Ollama service)
└── .github/
    └── workflows/
        ├── ci.yml       # CI/CD: lint, test, security, Docker build, release
        └── blank.yml
```

---

## Key Dependencies

- `python-telegram-bot==20.7` — Telegram Bot API client (async)
- `ollama==0.1.6` — Local LLM integration via Ollama
- `python-dotenv==1.0.0` — Environment variable loading
- `pyyaml==6.0.1` — YAML config parsing
- `pyttsx3==2.90` — Text-to-speech
- `SpeechRecognition==3.10.0` — Speech recognition
- `aiofiles==23.2.1` — Async file I/O
- `httpx==0.25.2` — Async HTTP client

---

## Environment Variables

Defined in `.env` (copy from `.env.example`):

- `TELEGRAM_BOT_TOKEN` — Required. Telegram bot token from @BotFather.
- `OLLAMA_HOST` — Ollama server URL (default: `http://localhost:11434`)
- `OLLAMA_MODEL` — AI model name (default: `llama2`)

---

## Development Conventions

- **Python style:** Follow PEP 8. Line length max 120 characters (as configured in CI flake8).
- **Formatting:** Code is formatted with `black` and imports sorted with `isort`.
- **Type hints:** Use type annotations where possible; mypy is run in CI with `--ignore-missing-imports`.
- **Async:** All Telegram handlers are `async def`. Use `asyncio` patterns consistently.
- **Config:** Read bot settings from `config.yml` using PyYAML. Runtime secrets come from `.env`.
- **Logging:** Use the standard `logging` module. Logger name should match the module name.
- **Comments and docstrings:** Write in Italian to match the existing codebase style.
- **Error handling:** Use `try/except` blocks with appropriate logging; avoid swallowing exceptions silently.

---

## Testing

Run the test suite with:

```bash
pytest test_bot.py -v
```

CI also collects coverage:

```bash
pytest test_bot.py -v --cov=. --cov-report=xml
```

When adding new features, add corresponding tests in `test_bot.py` following the existing patterns.

---

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on every push/PR to `main` or `develop`:

1. **Lint:** flake8, black (check), isort (check), mypy
2. **Test:** pytest with coverage (uploaded to Codecov)
3. **Security:** bandit scan
4. **Docker:** Build and push to GHCR (only on `main` push)
5. **Release:** Create GitHub release on version tags (`v*`)

---

## Docker

Build and run locally:

```bash
docker-compose up -d
docker exec -it ollama ollama pull llama2
docker-compose logs -f taurobot
```

---

## Copilot Agent Tips

- When modifying `bot.py`, keep all Telegram handlers registered in the `setup_handlers` method (or equivalent) of the `TauroBot` class.
- When adding new commands, register them with both `CommandHandler` and update the help text returned by `/help`.
- When adding new i18n strings, add them to **all** locale files in `i18n/` (`it.json`, `en.json`, `es.json`, `fr.json`, `de.json`).
- Do not commit secrets or tokens. The `.env` file is in `.gitignore`.
- When changing `requirements.txt`, also update `Dockerfile` if the install step needs changes.
- Always run `black .` and `isort .` before committing Python changes.
