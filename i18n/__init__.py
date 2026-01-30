"""
TauroBot 3.0 - Sistema di Internazionalizzazione (i18n)
Supporto multilingua per il bot
"""

import json
import os
from typing import Dict, Optional

# Directory delle traduzioni
TRANSLATIONS_DIR = os.path.dirname(os.path.abspath(__file__))

# Cache delle traduzioni caricate
_translations_cache: Dict[str, Dict[str, str]] = {}

# Lingua di default
DEFAULT_LANGUAGE = 'it'

# Lingue supportate
SUPPORTED_LANGUAGES = ['it', 'en', 'es', 'fr', 'de']


def load_language(lang_code: str) -> Dict[str, str]:
    """
    Carica le traduzioni per una lingua specifica.
    
    Args:
        lang_code: Codice lingua (es. 'it', 'en')
        
    Returns:
        Dizionario con le traduzioni
    """
    if lang_code in _translations_cache:
        return _translations_cache[lang_code]
    
    lang_file = os.path.join(TRANSLATIONS_DIR, f'{lang_code}.json')
    
    if not os.path.exists(lang_file):
        # Fallback alla lingua default
        lang_file = os.path.join(TRANSLATIONS_DIR, f'{DEFAULT_LANGUAGE}.json')
        lang_code = DEFAULT_LANGUAGE
    
    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            translations = json.load(f)
            _translations_cache[lang_code] = translations
            return translations
    except (json.JSONDecodeError, IOError) as e:
        print(f"Errore nel caricamento traduzioni {lang_code}: {e}")
        return {}


def get_text(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """
    Ottiene una stringa tradotta.
    
    Args:
        key: Chiave della traduzione (es. 'welcome_message')
        lang: Codice lingua
        **kwargs: Variabili per la formattazione
        
    Returns:
        Stringa tradotta e formattata
    """
    translations = load_language(lang)
    
    # Supporta chiavi annidate con dot notation (es. 'commands.start')
    keys = key.split('.')
    value = translations
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, None)
        else:
            value = None
            break
    
    if value is None:
        # Fallback: prova con la lingua default
        if lang != DEFAULT_LANGUAGE:
            return get_text(key, DEFAULT_LANGUAGE, **kwargs)
        # Se anche il default fallisce, ritorna la chiave
        return key
    
    # Formatta la stringa con i parametri
    try:
        return value.format(**kwargs) if kwargs else value
    except KeyError:
        return value


def t(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """Alias breve per get_text()"""
    return get_text(key, lang, **kwargs)


def get_available_languages() -> Dict[str, str]:
    """
    Ottiene la lista delle lingue disponibili.
    
    Returns:
        Dizionario {codice: nome_nativo}
    """
    return {
        'it': '🇮🇹 Italiano',
        'en': '🇬🇧 English',
        'es': '🇪🇸 Español',
        'fr': '🇫🇷 Français',
        'de': '🇩🇪 Deutsch'
    }


def is_supported_language(lang_code: str) -> bool:
    """Verifica se una lingua è supportata"""
    return lang_code in SUPPORTED_LANGUAGES


class I18n:
    """
    Classe helper per gestire le traduzioni per un utente specifico.
    """
    
    def __init__(self, default_lang: str = DEFAULT_LANGUAGE):
        self.default_lang = default_lang
        self.user_languages: Dict[int, str] = {}
    
    def set_user_language(self, user_id: int, lang: str) -> bool:
        """Imposta la lingua per un utente"""
        if is_supported_language(lang):
            self.user_languages[user_id] = lang
            return True
        return False
    
    def get_user_language(self, user_id: int) -> str:
        """Ottiene la lingua di un utente"""
        return self.user_languages.get(user_id, self.default_lang)
    
    def translate(self, user_id: int, key: str, **kwargs) -> str:
        """Traduce una stringa per un utente specifico"""
        lang = self.get_user_language(user_id)
        return get_text(key, lang, **kwargs)
    
    def t(self, user_id: int, key: str, **kwargs) -> str:
        """Alias breve per translate()"""
        return self.translate(user_id, key, **kwargs)


# Istanza globale per uso semplificato
i18n = I18n()
