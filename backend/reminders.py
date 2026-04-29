"""
TauroBot 3.0 - Sistema di Reminder/Notifiche
Gestisce promemoria programmati per gli utenti
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
import re
import aiofiles


@dataclass
class Reminder:
    """Rappresenta un singolo reminder"""
    id: str
    user_id: int
    chat_id: int
    message: str
    trigger_time: str  # ISO format
    created_at: str
    is_recurring: bool = False
    recurrence_interval: Optional[int] = None  # minuti
    is_completed: bool = False


class ReminderSystem:
    """
    Sistema di gestione reminder per il bot.
    Supporta reminder singoli e ricorrenti.
    """
    
    def __init__(self, storage_file: str = "memory/reminders.json"):
        self.storage_file = storage_file
        self.reminders: Dict[str, Reminder] = {}
        self._callback: Optional[Callable] = None
        self._check_task: Optional[asyncio.Task] = None
        self._running = False
        self._ensure_directory()
        
    def _ensure_directory(self) -> None:
        """Crea la directory se non esiste"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        
    def set_callback(self, callback: Callable[[Reminder], Any]) -> None:
        """Imposta la callback da chiamare quando scatta un reminder"""
        self._callback = callback
        
    async def load_reminders(self) -> bool:
        """Carica i reminder dal file"""
        try:
            if os.path.exists(self.storage_file):
                async with aiofiles.open(self.storage_file, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    data = json.loads(content)
                    for rid, rdata in data.items():
                        self.reminders[rid] = Reminder(**rdata)
                return True
        except Exception as e:
            print(f"Errore caricamento reminders: {e}")
        return False
        
    async def save_reminders(self) -> bool:
        """Salva i reminder su file"""
        try:
            data = {rid: asdict(r) for rid, r in self.reminders.items()}
            async with aiofiles.open(self.storage_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        except Exception as e:
            print(f"Errore salvataggio reminders: {e}")
        return False
        
    def add_reminder(
        self,
        user_id: int,
        chat_id: int,
        message: str,
        trigger_time: datetime,
        is_recurring: bool = False,
        recurrence_interval: Optional[int] = None
    ) -> Reminder:
        """
        Aggiunge un nuovo reminder.
        
        Args:
            user_id: ID utente Telegram
            chat_id: ID chat dove inviare
            message: Messaggio del reminder
            trigger_time: Quando far scattare il reminder
            is_recurring: Se è ricorrente
            recurrence_interval: Intervallo in minuti per ricorrenza
            
        Returns:
            Il reminder creato
        """
        reminder_id = f"rem_{user_id}_{datetime.now().timestamp()}"
        
        reminder = Reminder(
            id=reminder_id,
            user_id=user_id,
            chat_id=chat_id,
            message=message,
            trigger_time=trigger_time.isoformat(),
            created_at=datetime.now().isoformat(),
            is_recurring=is_recurring,
            recurrence_interval=recurrence_interval
        )
        
        self.reminders[reminder_id] = reminder
        return reminder
        
    def get_user_reminders(self, user_id: int) -> List[Reminder]:
        """Ottiene tutti i reminder attivi di un utente"""
        return [
            r for r in self.reminders.values()
            if r.user_id == user_id and not r.is_completed
        ]
        
    def delete_reminder(self, reminder_id: str) -> bool:
        """Elimina un reminder"""
        if reminder_id in self.reminders:
            del self.reminders[reminder_id]
            return True
        return False
        
    def complete_reminder(self, reminder_id: str) -> None:
        """Segna un reminder come completato"""
        if reminder_id in self.reminders:
            reminder = self.reminders[reminder_id]
            
            if reminder.is_recurring and reminder.recurrence_interval:
                # Aggiorna al prossimo trigger
                current = datetime.fromisoformat(reminder.trigger_time)
                next_trigger = current + timedelta(minutes=reminder.recurrence_interval)
                reminder.trigger_time = next_trigger.isoformat()
            else:
                reminder.is_completed = True
                
    async def check_reminders(self) -> List[Reminder]:
        """
        Controlla quali reminder devono scattare.
        
        Returns:
            Lista di reminder da triggerare
        """
        now = datetime.now()
        triggered = []
        
        for reminder in list(self.reminders.values()):
            if reminder.is_completed:
                continue
                
            trigger_time = datetime.fromisoformat(reminder.trigger_time)
            
            if trigger_time <= now:
                triggered.append(reminder)
                
                if self._callback:
                    try:
                        await self._callback(reminder)
                    except Exception as e:
                        print(f"Errore callback reminder: {e}")
                        
                self.complete_reminder(reminder.id)
                
        if triggered:
            await self.save_reminders()
            
        return triggered
        
    async def start_checker(self, interval: int = 30) -> None:
        """Avvia il controllo periodico dei reminder"""
        self._running = True
        
        while self._running:
            try:
                await self.check_reminders()
            except Exception as e:
                print(f"Errore nel checker reminders: {e}")
            
            await asyncio.sleep(interval)
            
    def stop_checker(self) -> None:
        """Ferma il checker"""
        self._running = False
        if self._check_task:
            self._check_task.cancel()
            
    def cleanup_completed(self) -> int:
        """Rimuove i reminder completati"""
        to_remove = [
            rid for rid, r in self.reminders.items()
            if r.is_completed
        ]
        
        for rid in to_remove:
            del self.reminders[rid]
            
        return len(to_remove)


def parse_reminder_time(text: str) -> Optional[datetime]:
    """
    Parsa una stringa di tempo in italiano/inglese.
    
    Esempi supportati:
    - "tra 5 minuti" / "in 5 minutes"
    - "tra 1 ora" / "in 1 hour"
    - "domani alle 10" / "tomorrow at 10"
    - "tra 30 secondi" / "in 30 seconds"
    
    Returns:
        datetime o None se non parsabile
    """
    text = text.lower().strip()
    now = datetime.now()
    
    # Pattern: tra X minuti/ore/secondi
    patterns = [
        (r'tra (\d+) minut[io]', 'minutes'),
        (r'tra (\d+) or[ae]', 'hours'),
        (r'tra (\d+) second[io]', 'seconds'),
        (r'tra (\d+) giorn[io]', 'days'),
        (r'in (\d+) minute?s?', 'minutes'),
        (r'in (\d+) hours?', 'hours'),
        (r'in (\d+) seconds?', 'seconds'),
        (r'in (\d+) days?', 'days'),
    ]
    
    for pattern, unit in patterns:
        match = re.search(pattern, text)
        if match:
            value = int(match.group(1))
            if unit == 'minutes':
                return now + timedelta(minutes=value)
            elif unit == 'hours':
                return now + timedelta(hours=value)
            elif unit == 'seconds':
                return now + timedelta(seconds=value)
            elif unit == 'days':
                return now + timedelta(days=value)
    
    # Pattern: domani alle HH:MM
    tomorrow_match = re.search(r'domani alle? (\d{1,2})(?::(\d{2}))?', text)
    if tomorrow_match:
        hour = int(tomorrow_match.group(1))
        minute = int(tomorrow_match.group(2) or 0)
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # Pattern: tomorrow at HH:MM
    tomorrow_en = re.search(r'tomorrow at (\d{1,2})(?::(\d{2}))?', text)
    if tomorrow_en:
        hour = int(tomorrow_en.group(1))
        minute = int(tomorrow_en.group(2) or 0)
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    return None
