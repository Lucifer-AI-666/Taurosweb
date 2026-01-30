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
from reminders import ReminderSystem, parse_reminder_time, Reminder


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
        
        # Sistema reminder
        self.reminders = ReminderSystem()
        
        # Riferimento all'application per i reminder
        self._application: Optional[Application] = None
        
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
            "• 🥷 Anima hacker\n"
            "• 🌍 Multi-lingua\n\n"
            "Comandi disponibili:\n"
            "/start - Avvia il bot\n"
            "/help - Mostra aiuto\n"
            "/clear - Cancella memoria conversazione\n"
            "/stats - Statistiche memoria\n"
            "/voice - Abilita/disabilita sintesi vocale\n"
            "/lang - Cambia lingua\n"
            "/code - Genera codice\n"
            "/translate - Traduci testo\n\n"
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
    
    def _should_respond_in_group(self, update: Update, bot_username: str) -> bool:
        """
        Determina se il bot deve rispondere in un gruppo.
        Risponde solo se:
        - È menzionato (@botname)
        - È una risposta a un suo messaggio
        """
        message = update.message
        
        # Chat privata: rispondi sempre
        if message.chat.type == 'private':
            return True
        
        # Gruppo: controlla menzione o reply
        text = message.text or ""
        
        # Menzionato con @
        if f"@{bot_username}" in text:
            return True
        
        # È una risposta a un messaggio del bot
        if message.reply_to_message:
            if message.reply_to_message.from_user:
                if message.reply_to_message.from_user.username == bot_username:
                    return True
        
        return False
            
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler per i messaggi degli utenti (privati e gruppi)"""
        user_id = update.effective_user.id
        user_message = update.message.text
        lang = i18n.get_user_language(user_id)
        
        # Ottieni username del bot
        bot_username = context.bot.username or "TauroBot"
        
        # In gruppo, rispondi solo se menzionato o in reply
        if not self._should_respond_in_group(update, bot_username):
            return
        
        # Rimuovi la menzione dal messaggio
        clean_message = user_message.replace(f"@{bot_username}", "").strip()
        if not clean_message:
            clean_message = user_message
        
        # Check rate limit
        allowed, wait_seconds = self.rate_limiter.check(user_id)
        if not allowed:
            await update.message.reply_text(
                get_text('errors.rate_limited', lang, seconds=wait_seconds)
            )
            return
            
        # Registra richiesta per rate limiting
        self.rate_limiter.record(user_id)
        
        # Salva messaggio utente in memoria (usa messaggio pulito)
        self.memory.add_message(user_id, "user", clean_message)
        
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
                        
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler per il comando /admin - Dashboard amministratore"""
        user_id = update.effective_user.id
        lang = i18n.get_user_language(user_id)
        
        # Verifica se è admin
        if user_id not in self.admin_users:
            await update.message.reply_text(get_text('errors.not_authorized', lang))
            return
        
        # Statistiche memoria
        stats = self.memory.get_stats()
        
        # Statistiche rate limiter
        total_users_limited = len([u for u in self.rate_limiter._user_data.values() if u.violations > 0])
        
        admin_text = (
            "🛡️ *ADMIN DASHBOARD*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 *Statistiche Memoria:*\n"
            f"• Utenti totali: `{stats['total_users']}`\n"
            f"• Messaggi totali: `{stats['total_messages']}`\n"
            f"• Media msg/utente: `{stats['average_messages_per_user']:.1f}`\n\n"
            "🛡️ *Rate Limiting:*\n"
            f"• Limite: `{self.rate_limiter.max_requests}` msg/{self.rate_limiter.window_seconds}s\n"
            f"• Utenti con violazioni: `{total_users_limited}`\n\n"
            "⚙️ *Configurazione:*\n"
            f"• Modello AI: `{self.ollama_model}`\n"
            f"• Host Ollama: `{self.ollama_host}`\n"
            f"• Admin IDs: `{len(self.admin_users)}`\n\n"
            "🌍 *Lingue attive:* IT, EN, ES, FR, DE\n\n"
            "📝 *Comandi Admin:*\n"
            "/admin - Questa dashboard\n"
            "/admin broadcast <msg> - Invia a tutti (TODO)\n"
            "/admin reset <user_id> - Reset rate limit"
        )
        await update.message.reply_text(admin_text, parse_mode='Markdown')
        
    async def code_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler per il comando /code - Genera codice"""
        user_id = update.effective_user.id
        lang = i18n.get_user_language(user_id)
        
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "💻 *Uso:* `/code <linguaggio> <descrizione>`\n\n"
                "*Esempi:*\n"
                "• `/code python leggi un file JSON`\n"
                "• `/code javascript fetch API REST`\n"
                "• `/code bash script backup`",
                parse_mode='Markdown'
            )
            return
        
        language = context.args[0]
        description = ' '.join(context.args[1:])
        
        # Check rate limit
        allowed, wait_seconds = self.rate_limiter.check(user_id)
        if not allowed:
            await update.message.reply_text(
                get_text('errors.rate_limited', lang, seconds=wait_seconds)
            )
            return
        self.rate_limiter.record(user_id)
        
        await update.message.chat.send_action("typing")
        
        prompt = f"""Genera codice {language} per: {description}

Rispondi SOLO con il codice, ben formattato e commentato. 
Non aggiungere spiegazioni prima o dopo il codice.
Inizia direttamente con ```{language}"""
        
        response = await self.query_ollama(prompt)
        await update.message.reply_text(response, parse_mode='Markdown')
        
    async def translate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler per il comando /translate - Traduzione"""
        user_id = update.effective_user.id
        lang = i18n.get_user_language(user_id)
        
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "🌐 *Uso:* `/translate <lingua> <testo>`\n\n"
                "*Esempi:*\n"
                "• `/translate en Ciao, come stai?`\n"
                "• `/translate es Buongiorno a tutti`\n"
                "• `/translate de Grazie mille`\n\n"
                "*Lingue:* en, es, fr, de, it, pt, zh, ja, ko, ru, ar, darija",
                parse_mode='Markdown'
            )
            return
        
        target_lang = context.args[0].lower()
        text_to_translate = ' '.join(context.args[1:])
        
        # Check rate limit
        allowed, wait_seconds = self.rate_limiter.check(user_id)
        if not allowed:
            await update.message.reply_text(
                get_text('errors.rate_limited', lang, seconds=wait_seconds)
            )
            return
        self.rate_limiter.record(user_id)
        
        await update.message.chat.send_action("typing")
        
        lang_names = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'zh': 'Chinese', 'ja': 'Japanese',
            'ko': 'Korean', 'ru': 'Russian', 'ar': 'Arabic', 'darija': 'Darija'
        } 
        
        target_name = lang_names.get(target_lang, target_lang)
        
        prompt = f"""Translate the following text to {target_name}. 
Reply ONLY with the translation, nothing else.

Text: {text_to_translate}"""
        
        response = await self.query_ollama(prompt)
        
        result = (
            f"🌐 *Traduzione in {target_name}:*\n\n"
            f"{response}"
        )
        await update.message.reply_text(result, parse_mode='Markdown')
        
    async def remind_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler per il comando /remind - Imposta promemoria"""
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        lang = i18n.get_user_language(user_id)
        
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "⏰ *Uso:* `/remind <quando> <messaggio>`\n\n"
                "*Esempi:*\n"
                "• `/remind tra 5 minuti Chiamare Mario`\n"
                "• `/remind tra 1 ora Meeting importante`\n"
                "• `/remind domani alle 9 Sveglia!`\n"
                "• `/remind in 30 minutes Check email`\n\n"
                "*Altri comandi:*\n"
                "• `/remind list` - Mostra i tuoi promemoria\n"
                "• `/remind delete <id>` - Elimina un promemoria",
                parse_mode='Markdown'
            )
            return
        
        # Comando list
        if context.args[0].lower() == 'list':
            user_reminders = self.reminders.get_user_reminders(user_id)
            if not user_reminders:
                await update.message.reply_text("📭 Non hai promemoria attivi.")
                return
            
            text = "⏰ *I tuoi promemoria:*\n\n"
            for i, rem in enumerate(user_reminders, 1):
                trigger = datetime.fromisoformat(rem.trigger_time)
                text += f"{i}. `{rem.id[:12]}...`\n"
                text += f"   📝 {rem.message}\n"
                text += f"   🕐 {trigger.strftime('%d/%m/%Y %H:%M')}\n\n"
            
            await update.message.reply_text(text, parse_mode='Markdown')
            return
        
        # Comando delete
        if context.args[0].lower() == 'delete' and len(context.args) > 1:
            rem_id = context.args[1]
            # Cerca reminder che inizia con l'ID parziale
            found = None
            for rid in self.reminders.reminders:
                if rid.startswith(rem_id) or rem_id in rid:
                    found = rid
                    break
            
            if found and self.reminders.delete_reminder(found):
                await self.reminders.save_reminders()
                await update.message.reply_text("✅ Promemoria eliminato!")
            else:
                await update.message.reply_text("❌ Promemoria non trovato.")
            return
        
        # Parse tempo e messaggio
        full_text = ' '.join(context.args)
        trigger_time = parse_reminder_time(full_text)
        
        if not trigger_time:
            await update.message.reply_text(
                "❌ Non ho capito quando vuoi il promemoria.\n"
                "Prova con: `tra 5 minuti`, `tra 1 ora`, `domani alle 10`",
                parse_mode='Markdown'
            )
            return
        
        # Estrai il messaggio (rimuovi la parte del tempo)
        message = full_text
        time_patterns = [
            r'tra \d+ minut[io]', r'tra \d+ or[ae]', r'tra \d+ second[io]',
            r'tra \d+ giorn[io]', r'in \d+ minutes?', r'in \d+ hours?',
            r'in \d+ seconds?', r'in \d+ days?', r'domani alle? \d{1,2}(?::\d{2})?',
            r'tomorrow at \d{1,2}(?::\d{2})?'
        ]
        import re
        for pattern in time_patterns:
            message = re.sub(pattern, '', message, flags=re.IGNORECASE).strip()
        
        if not message:
            message = "Promemoria!"
        
        # Crea il reminder
        reminder = self.reminders.add_reminder(
            user_id=user_id,
            chat_id=chat_id,
            message=message,
            trigger_time=trigger_time
        )
        await self.reminders.save_reminders()
        
        await update.message.reply_text(
            f"✅ *Promemoria impostato!*\n\n"
            f"📝 {message}\n"
            f"🕐 {trigger_time.strftime('%d/%m/%Y alle %H:%M')}",
            parse_mode='Markdown'
        )
        
    async def _send_reminder_notification(self, reminder: Reminder) -> None:
        """Invia la notifica di un reminder"""
        if self._application:
            try:
                await self._application.bot.send_message(
                    chat_id=reminder.chat_id,
                    text=f"⏰ *PROMEMORIA!*\n\n{reminder.message}",
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Errore invio reminder: {e}")
                        
    async def post_init(self, application: Application) -> None:
        """Inizializzazione post-startup"""
        self._application = application
        await self.memory.load_memory()
        await self.reminders.load_reminders()
        
        # Imposta callback per reminder
        self.reminders.set_callback(self._send_reminder_notification)
        
        # Avvia checker reminder in background
        asyncio.create_task(self.reminders.start_checker(interval=30))
        
        logger.info("TauroBot 3.0 avviato!")
        
    async def post_shutdown(self, application: Application):
        """Cleanup pre-shutdown"""
        self.reminders.stop_checker()
        await self.reminders.save_reminders()
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
        application.add_handler(CommandHandler("admin", self.admin_command))
        application.add_handler(CommandHandler("code", self.code_command))
        application.add_handler(CommandHandler("translate", self.translate_command))
        application.add_handler(CommandHandler("remind", self.remind_command))
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
