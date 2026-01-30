"""
TauroBot 3.0 Ultimate - Bot AI avanzato per Telegram
Integra Ollama, memoria intelligente, sintesi vocale e anima hacker
"""

import os
import logging
import asyncio
from datetime import datetime
from typing import Optional, Dict, List, Any
import yaml
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import httpx

from memory import MemorySystem
from voice import VoiceSystem
from rate_limiter import RateLimiter
from i18n import i18n, get_text, get_available_languages, is_supported_language


# Configurazione logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TauroBot:
    """Bot AI avanzato per Telegram"""
    
    def __init__(self):
        # Carica variabili d'ambiente
        load_dotenv()
        
        # Configurazione
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama2')
        
        # Carica config.yml
        self.config = self._load_config()
        
        # Inizializza sistemi
        self.memory = MemorySystem(
            memory_file=os.getenv('MEMORY_FILE', 'memory/conversations.json'),
            max_size=int(os.getenv('MAX_MEMORY_SIZE', '1000'))
        )
        
        self.voice = VoiceSystem(
            language=os.getenv('TTS_LANGUAGE', 'it'),
            rate=self.config.get('voice', {}).get('rate', 150),
            volume=self.config.get('voice', {}).get('volume', 1.0)
        )
        
        # Client HTTP per Ollama
        self.http_client: httpx.AsyncClient = httpx.AsyncClient(timeout=60.0)
        
        # Admin users
        admin_ids = os.getenv('ADMIN_USER_IDS', '')
        self.admin_users: List[int] = [int(x.strip()) for x in admin_ids.split(',') if x.strip().isdigit()]
        
        # Rate limiter
        limits = self.config.get('limits', {})
        self.rate_limiter = RateLimiter(
            max_requests=limits.get('rate_limit_messages', 30),
            window_seconds=limits.get('rate_limit_window', 60),
            block_duration=60
        )
        
        # Aggiungi admin alla whitelist del rate limiter
        for admin_id in self.admin_users:
            self.rate_limiter.add_to_whitelist(admin_id)
        
    def _load_config(self) -> Dict[str, Any]:
        """Carica configurazione da config.yml"""
        try:
            if os.path.exists('config.yml'):
                with open('config.yml', 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Errore nel caricamento config.yml: {e}")
        return {}
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler per il comando /start"""
        user = update.effective_user
        welcome_message = (
            f"🐂 Ciao {user.first_name}! Sono TauroBot 3.0 Ultimate!\n\n"
            "Sono un bot AI avanzato con:\n"
            "• 🧠 Intelligenza artificiale Ollama\n"
            "• 💾 Memoria persistente delle conversazioni\n"
            "• 🔊 Sintesi vocale\n"
            "• 🥷 Anima hacker\n\n"
            "Comandi disponibili:\n"
            "/start - Avvia il bot\n"
            "/help - Mostra aiuto\n"
            "/clear - Cancella memoria conversazione\n"
            "/stats - Statistiche memoria\n"
            "/voice - Abilita/disabilita sintesi vocale\n\n"
            "Inviami un messaggio e ti risponderò!"
        )
        await update.message.reply_text(welcome_message)
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler per il comando /help"""
        help_text = (
            "🐂 *TauroBot 3.0 Ultimate - Aiuto*\n\n"
            "*Comandi base:*\n"
            "/start - Avvia il bot\n"
            "/help - Mostra questo messaggio\n"
            "/clear - Cancella la tua memoria conversazione\n"
            "/stats - Mostra statistiche memoria\n"
            "/voice - Abilita/disabilita risposte vocali\n\n"
            "*Come funziono:*\n"
            "• Inviami un messaggio e ti risponderò usando AI\n"
            "• Ricordo le nostre conversazioni passate\n"
            "• Posso rispondere con messaggi vocali\n"
            "• Sono sempre in modalità hacker 🥷\n\n"
            "*Suggerimenti:*\n"
            "• Fammi domande complesse\n"
            "• Chiedi aiuto su coding, tecnologia, etc.\n"
            "• Usa /clear se vuoi ricominciare da zero"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
        
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler per il comando /clear"""
        user_id = update.effective_user.id
        if self.memory.clear_user_memory(user_id):
            await self.memory.save_memory()
            await update.message.reply_text("✅ Memoria conversazione cancellata!")
        else:
            await update.message.reply_text("ℹ️ Nessuna memoria da cancellare.")
            
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler per il comando /stats"""
        stats = self.memory.get_stats()
        user_id = update.effective_user.id
        user_messages = len(self.memory.get_conversation(user_id))
        
        stats_text = (
            f"📊 *Statistiche Memoria*\n\n"
            f"*Tue statistiche:*\n"
            f"• Messaggi salvati: {user_messages}\n\n"
            f"*Statistiche globali:*\n"
            f"• Utenti totali: {stats['total_users']}\n"
            f"• Messaggi totali: {stats['total_messages']}\n"
            f"• Media msg/utente: {stats['average_messages_per_user']:.1f}"
        )
        await update.message.reply_text(stats_text, parse_mode='Markdown')
        
    async def voice_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler per il comando /voice"""
        user_id = update.effective_user.id
        lang = i18n.get_user_language(user_id)
        
        # Toggle voice preference (stored in context)
        if 'voice_enabled' not in context.user_data:
            context.user_data['voice_enabled'] = True
        else:
            context.user_data['voice_enabled'] = not context.user_data['voice_enabled']
            
        if context.user_data['voice_enabled']:
            await update.message.reply_text(get_text('voice.enabled', lang))
        else:
            await update.message.reply_text(get_text('voice.disabled', lang))
            
    async def lang_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler per il comando /lang - cambia lingua"""
        user_id = update.effective_user.id
        current_lang = i18n.get_user_language(user_id)
        
        # Se è stato specificato un codice lingua
        if context.args and len(context.args) > 0:
            new_lang = context.args[0].lower()
            
            if is_supported_language(new_lang):
                i18n.set_user_language(user_id, new_lang)
                lang_name = get_available_languages().get(new_lang, new_lang)
                await update.message.reply_text(
                    get_text('language.changed', new_lang, lang=lang_name)
                )
            else:
                langs = ', '.join(get_available_languages().keys())
                await update.message.reply_text(
                    get_text('language.not_supported', current_lang, langs=langs)
                )
        else:
            # Mostra lingue disponibili
            text = get_text('language.title', current_lang) + "\n\n"
            for code, name in get_available_languages().items():
                marker = " ✓" if code == current_lang else ""
                text += f"{name}{marker}\n"
            text += f"\nUsa: /lang <codice> (es. /lang en)"
            await update.message.reply_text(text, parse_mode='Markdown')
        
    async def query_ollama(self, prompt: str, context_messages: Optional[List[Dict[str, Any]]] = None) -> Optional[str]:
        """Interroga Ollama per ottenere una risposta AI"""
        try:
            # Prepara i messaggi con contesto
            messages = []
            
            # System message
            messages.append({
                "role": "system",
                "content": "Sei TauroBot 3.0 Ultimate, un assistente AI avanzato con anima hacker. "
                          "Sei competente, diretto e hai un approccio tecnico alle cose. "
                          "Rispondi in italiano in modo chiaro e utile."
            })
            
            # Aggiungi contesto se disponibile
            if context_messages:
                for msg in context_messages[-5:]:  # Ultimi 5 messaggi
                    messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
            
            # Aggiungi il prompt corrente
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Chiamata API Ollama
            url = f"{self.ollama_host}/api/chat"
            payload = {
                "model": self.ollama_model,
                "messages": messages,
                "stream": False
            }
            
            response = await self.http_client.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return data.get('message', {}).get('content', 'Scusa, non ho capito.')
            
        except Exception as e:
            logger.error(f"Errore query Ollama: {e}")
            return f"❌ Errore nel contattare l'AI: {str(e)}"
            
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler per i messaggi degli utenti"""
        user_id = update.effective_user.id
        user_message = update.message.text
        lang = i18n.get_user_language(user_id)
        
        # Check rate limit
        allowed, wait_seconds = self.rate_limiter.check(user_id)
        if not allowed:
            await update.message.reply_text(
                get_text('errors.rate_limited', lang, seconds=wait_seconds)
            )
            return
            
        # Registra richiesta per rate limiting
        self.rate_limiter.record(user_id)
        
        # Salva messaggio utente in memoria
        self.memory.add_message(user_id, "user", user_message)
        
        # Mostra "sta scrivendo..."
        await update.message.chat.send_action("typing")
        
        # Ottieni contesto conversazione
        context_messages = self.memory.get_conversation(user_id, limit=10)
        
        # Interroga Ollama
        response = await self.query_ollama(user_message, context_messages)
        
        # Salva risposta in memoria
        self.memory.add_message(user_id, "assistant", response)
        
        # Salva memoria
        await self.memory.save_memory()
        
        # Invia risposta testuale
        await update.message.reply_text(response)
        
        # Se voice è abilitato, invia anche audio
        if context.user_data.get('voice_enabled', False) and self.config.get('voice', {}).get('tts_enabled', True):
            await update.message.chat.send_action("record_voice")
            
            # Genera file audio
            audio_file = f"temp_voice_{user_id}_{datetime.now().timestamp()}.mp3"
            audio_path = await self.voice.text_to_speech(response, audio_file)
            
            if audio_path and os.path.exists(audio_path):
                try:
                    with open(audio_path, 'rb') as audio:
                        await update.message.reply_voice(audio)
                finally:
                    # Pulisci file temporaneo
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                        
    async def post_init(self, application: Application):
        """Inizializzazione post-startup"""
        await self.memory.load_memory()
        logger.info("TauroBot 3.0 avviato!")
        
    async def post_shutdown(self, application: Application):
        """Cleanup pre-shutdown"""
        await self.memory.save_memory()
        await self.http_client.aclose()
        self.voice.cleanup()
        logger.info("TauroBot 3.0 arrestato.")
        
    def run(self):
        """Avvia il bot"""
        if not self.token:
            logger.error("TELEGRAM_BOT_TOKEN non configurato!")
            return
            
        # Crea application
        application = Application.builder().token(self.token).build()
        
        # Registra handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("clear", self.clear_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("voice", self.voice_command))
        application.add_handler(CommandHandler("lang", self.lang_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Post init/shutdown hooks
        application.post_init = self.post_init
        application.post_shutdown = self.post_shutdown
        
        # Avvia bot
        logger.info("Avvio TauroBot 3.0 Ultimate...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Entry point"""
    bot = TauroBot()
    bot.run()


if __name__ == '__main__':
    main()
