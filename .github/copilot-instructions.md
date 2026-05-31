# Copilot Instructions for Taurosweb – TauroBot 3.0 Ultimate

## Project Overview
**Taurosweb** is the repository for **TauroBot 3.0 Ultimate**, an advanced Telegram bot integrating Ollama AI, persistent memory, text-to-speech, rate limiting, and a PWA web interface.

## Tech Stack
- **Language:** Python 3.11
- **Bot framework:** `python-telegram-bot` 20.x (async)
- **AI backend:** `ollama` (local LLM)
- **Testing:** `pytest` with `pytest-asyncio` and `pytest-cov`
- **Linting/formatting:** `flake8`, `black` (line length 120), `isort`, `mypy`
- **Security scanning:** `bandit`
- **Containerisation:** Docker / docker-compose
- **Frontend:** Vanilla HTML/JS PWA (`index.html`, `service-worker.js`, `manifest.json`)
- **i18n:** JSON files under `i18n/` (IT, EN, ES, FR, DE, ar_ma)

## Code Style
- Follow **PEP 8** with a maximum line length of **120 characters**.
- Format all Python files with **Black** (`black --line-length 120`).
- Sort imports with **isort** (compatible with Black profile: `isort --profile black`).
- Use **type hints** throughout Python code; check with `mypy --ignore-missing-imports`.
- Write docstrings for all public functions and classes.

## Architecture Conventions
- `bot.py` — main Telegram bot entry point (async handlers using `python-telegram-bot`).
- `memory.py` — persistent conversation memory layer.
- `voice.py` — text-to-speech (TTS) integration.
- `rate_limiter.py` — anti-spam / rate-limiting logic.
- `run.py` / `run.sh` — startup scripts; do not add business logic here.
- `config.yml` — runtime configuration (AI parameters, memory settings, TTS, rate limits); prefer adding new settings here over hardcoding values.
- `.env` / `.env.example` — secrets and environment-specific variables; **never commit real secrets**.

## Testing
- Tests live in `test_bot.py`. Run with:
  ```bash
  pytest test_bot.py -v --cov=. --cov-report=xml
  ```
- Use `pytest-asyncio` for async test functions.
- Aim for meaningful coverage on `bot.py`, `memory.py`, `voice.py`, and `rate_limiter.py`.
- Do **not** remove or weaken existing tests.

## Dependencies
- Manage Python dependencies in `requirements.txt`.
- When adding a new package, pin it to a specific version (e.g. `httpx==0.25.2`).
- Check for known vulnerabilities before adding new packages.

## Security
- Never commit secrets, tokens, or API keys. Use `.env` and GitHub Secrets.
- Follow the guidelines in `SECURITY.md`.
- All new code must pass `bandit` without high-severity findings.

## i18n
- All user-facing strings must be externalised in the appropriate `i18n/<lang>.json` files.
- Italian (`it.json`) is the default locale.

## Docker
- The `Dockerfile` targets Python 3.11-slim; keep the image minimal.
- `docker-compose.yml` orchestrates the bot and the Ollama service.
- Test Docker builds locally before pushing changes to the `main` branch.

## Pull Requests
- Target the `main` branch for production-ready changes; use `develop` for work-in-progress.
- Ensure CI passes (lint → test → security → Docker build) before requesting a review.
- Describe changes clearly in Italian or English in the PR description.
