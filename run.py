#!/usr/bin/env python3
"""
TauroBot 3.0 Ultimate - Python Run Script
Simple wrapper to run the bot with proper error handling and setup checks
"""

import os
import sys
import subprocess
import shutil
import re
from pathlib import Path


def check_env_file():
    """Check if .env file exists and is configured"""
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("Creating .env from .env.example...")
        
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ .env file created.")
            print("")
            print("⚠️  IMPORTANT: You need to configure .env before running the bot:")
            print("1. Get a bot token from @BotFather on Telegram")
            print("2. Edit .env file and set TELEGRAM_BOT_TOKEN")
            print("3. Make sure Ollama is running (ollama serve)")
            print("")
            return False
        else:
            print("❌ Error: .env.example not found!")
            return False
    
    # Check if token is configured
    with open('.env', 'r') as f:
        content = f.read()
        # Look for TELEGRAM_BOT_TOKEN line with a value that's not the placeholder
        token_match = re.search(r'^\s*TELEGRAM_BOT_TOKEN\s*=\s*(.+?)\s*$', content, re.MULTILINE)
        if not token_match or token_match.group(1) in ('', 'your_telegram_bot_token_here'):
            print("⚠️  Warning: TELEGRAM_BOT_TOKEN not configured in .env!")
            print("Please edit .env and set your bot token from @BotFather")
            print("")
            return False
    
    return True


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import telegram
        import ollama
        import yaml
        from dotenv import load_dotenv
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error installing dependencies")
            return False


def create_directories():
    """Create necessary directories"""
    Path('memory').mkdir(exist_ok=True)
    Path('logs').mkdir(exist_ok=True)


def main():
    """Main entry point"""
    print("🐂 TauroBot 3.0 Ultimate - Run Script")
    print("=" * 50)
    print("")
    
    # Check environment file
    if not check_env_file():
        print("")
        print("Please configure .env and run this script again.")
        sys.exit(1)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        print("❌ Dependency check failed")
        sys.exit(1)
    print("✅ Dependencies OK")
    print("")
    
    # Create directories
    create_directories()
    
    # Run the bot
    print("🚀 Launching TauroBot 3.0 Ultimate...")
    print("   Press Ctrl+C to stop")
    print("")
    
    try:
        # Import and run the bot
        try:
            from bot import main as bot_main
        except ImportError as e:
            print(f"❌ Error: Could not import bot module: {e}")
            print("Make sure bot.py exists in the current directory")
            sys.exit(1)
        
        bot_main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error running bot: {e}")
        print("\nPlease check:")
        print("1. .env file is properly configured")
        print("2. Ollama is running (ollama serve)")
        print("3. Your bot token is valid")
        sys.exit(1)


if __name__ == '__main__':
    main()
