@echo off
REM TauroBot 3.0 Ultimate - Run Script for Windows
REM This script helps you easily start the Telegram bot

echo.
echo TauroBot 3.0 Ultimate - Launcher
echo ====================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: File .env non trovato!
    echo Copiando .env.example in .env...
    copy .env.example .env
    echo File .env creato.
    echo.
    echo IMPORTANTE: Modifica il file .env con il tuo TELEGRAM_BOT_TOKEN!
    echo    Ottieni il token da @BotFather su Telegram
    echo.
    pause
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment non trovato. Creazione in corso...
    python -m venv venv
    echo Virtual environment creato.
)

REM Activate virtual environment
echo Attivazione virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installazione/aggiornamento dipendenze...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

echo.
echo Dipendenze installate!
echo.

REM Check if Ollama is running (basic check)
echo Verifica connessione Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo Ollama e' raggiungibile
) else (
    echo WARNING: Ollama non sembra essere in esecuzione
    echo    Avvia Ollama con: ollama serve
    echo    Oppure scarica da: https://ollama.ai
    echo.
    pause
)

echo.
echo Avvio TauroBot 3.0 Ultimate...
echo    Premi Ctrl+C per fermare il bot
echo.
echo ====================================
echo.

REM Run the bot
python bot.py
