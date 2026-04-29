"""
TauroBot 3.0 - Sistema di Rate Limiting
Protegge il bot da abusi limitando le richieste per utente
"""

import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple
from functools import wraps
import asyncio


@dataclass
class RateLimitInfo:
    """Informazioni sul rate limit per un utente"""
    timestamps: list = field(default_factory=list)
    blocked_until: float = 0.0
    violations: int = 0


class RateLimiter:
    """
    Rate limiter per controllare la frequenza dei messaggi.
    
    Implementa un algoritmo sliding window per contare i messaggi
    in una finestra temporale.
    """
    
    def __init__(
        self,
        max_requests: int = 30,
        window_seconds: int = 60,
        block_duration: int = 60,
        max_violations: int = 3
    ):
        """
        Inizializza il rate limiter.
        
        Args:
            max_requests: Numero massimo di richieste nella finestra
            window_seconds: Durata della finestra in secondi
            block_duration: Durata del blocco in secondi dopo violazione
            max_violations: Numero di violazioni prima del blocco prolungato
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.block_duration = block_duration
        self.max_violations = max_violations
        
        # Storage per utente: {user_id: RateLimitInfo}
        self._user_data: Dict[int, RateLimitInfo] = defaultdict(RateLimitInfo)
        
        # Whitelist utenti (admin, etc.)
        self._whitelist: set = set()
        
    def add_to_whitelist(self, user_id: int) -> None:
        """Aggiunge un utente alla whitelist (no rate limit)"""
        self._whitelist.add(user_id)
        
    def remove_from_whitelist(self, user_id: int) -> None:
        """Rimuove un utente dalla whitelist"""
        self._whitelist.discard(user_id)
        
    def is_whitelisted(self, user_id: int) -> bool:
        """Verifica se un utente è nella whitelist"""
        return user_id in self._whitelist
        
    def _cleanup_old_timestamps(self, user_id: int, current_time: float) -> None:
        """Rimuove i timestamp fuori dalla finestra temporale"""
        data = self._user_data[user_id]
        cutoff = current_time - self.window_seconds
        data.timestamps = [ts for ts in data.timestamps if ts > cutoff]
        
    def check(self, user_id: int) -> Tuple[bool, Optional[int]]:
        """
        Verifica se un utente può inviare un messaggio.
        
        Args:
            user_id: ID dell'utente Telegram
            
        Returns:
            Tuple (allowed, wait_seconds):
            - allowed: True se l'utente può procedere
            - wait_seconds: Secondi da attendere se bloccato, None altrimenti
        """
        # Whitelist bypass
        if self.is_whitelisted(user_id):
            return True, None
            
        current_time = time.time()
        data = self._user_data[user_id]
        
        # Check se l'utente è bloccato
        if current_time < data.blocked_until:
            wait = int(data.blocked_until - current_time) + 1
            return False, wait
            
        # Pulisci timestamp vecchi
        self._cleanup_old_timestamps(user_id, current_time)
        
        # Check rate limit
        if len(data.timestamps) >= self.max_requests:
            # Utente ha superato il limite
            data.violations += 1
            
            # Calcola durata blocco (aumenta con le violazioni)
            block_multiplier = min(data.violations, self.max_violations)
            block_time = self.block_duration * block_multiplier
            
            data.blocked_until = current_time + block_time
            return False, int(block_time)
            
        # Utente può procedere
        return True, None
        
    def record(self, user_id: int) -> None:
        """
        Registra una richiesta per un utente.
        
        Chiamare dopo che l'utente ha passato il check.
        """
        if not self.is_whitelisted(user_id):
            self._user_data[user_id].timestamps.append(time.time())
            
    def get_usage(self, user_id: int) -> Dict:
        """
        Ottiene le statistiche di utilizzo per un utente.
        
        Returns:
            Dict con requests_count, window_seconds, limit, remaining
        """
        if self.is_whitelisted(user_id):
            return {
                'requests_count': 0,
                'window_seconds': self.window_seconds,
                'limit': float('inf'),
                'remaining': float('inf'),
                'whitelisted': True
            }
            
        self._cleanup_old_timestamps(user_id, time.time())
        data = self._user_data[user_id]
        
        return {
            'requests_count': len(data.timestamps),
            'window_seconds': self.window_seconds,
            'limit': self.max_requests,
            'remaining': max(0, self.max_requests - len(data.timestamps)),
            'violations': data.violations,
            'whitelisted': False
        }
        
    def reset_user(self, user_id: int) -> None:
        """Resetta le statistiche di un utente"""
        if user_id in self._user_data:
            del self._user_data[user_id]
            
    def reset_all(self) -> None:
        """Resetta tutte le statistiche"""
        self._user_data.clear()


def rate_limit(limiter: RateLimiter):
    """
    Decoratore per applicare rate limiting a handler Telegram.
    
    Usage:
        limiter = RateLimiter(max_requests=30, window_seconds=60)
        
        @rate_limit(limiter)
        async def handle_message(update, context):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(self_or_update, update_or_context, context=None):
            # Supporta sia metodi di classe che funzioni standalone
            if context is None:
                update = self_or_update
                context = update_or_context
                self = None
            else:
                self = self_or_update
                update = update_or_context
            
            user_id = update.effective_user.id
            allowed, wait_seconds = limiter.check(user_id)
            
            if not allowed:
                await update.message.reply_text(
                    f"⚠️ Troppi messaggi! Attendi {wait_seconds} secondi."
                )
                return
                
            # Registra la richiesta
            limiter.record(user_id)
            
            # Esegui l'handler originale
            if self is not None:
                return await func(self, update, context)
            else:
                return await func(update, context)
                
        return wrapper
    return decorator


class AsyncRateLimiter:
    """
    Versione async-safe del rate limiter con lock.
    Da usare in ambienti con alta concorrenza.
    """
    
    def __init__(self, *args, **kwargs):
        self._limiter = RateLimiter(*args, **kwargs)
        self._lock = asyncio.Lock()
        
    async def check(self, user_id: int) -> Tuple[bool, Optional[int]]:
        async with self._lock:
            return self._limiter.check(user_id)
            
    async def record(self, user_id: int) -> None:
        async with self._lock:
            self._limiter.record(user_id)
            
    def add_to_whitelist(self, user_id: int) -> None:
        self._limiter.add_to_whitelist(user_id)
        
    def is_whitelisted(self, user_id: int) -> bool:
        return self._limiter.is_whitelisted(user_id)
