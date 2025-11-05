"""
Sistema di memoria persistente per TauroBot 3.0
Gestisce la memorizzazione delle conversazioni e del contesto
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from utils import FileManager, DateTimeHelper, get_logger

logger = get_logger(__name__)


class MemorySystem:
    """Gestisce la memoria persistente del bot"""
    
    def __init__(self, memory_file: str = "memory/conversations.json", max_size: int = 1000):
        self.memory_file = memory_file
        self.max_size = max_size
        self.conversations: Dict[int, List[Dict]] = {}
        self._ensure_directory()
        
    def _ensure_directory(self):
        """Crea la directory memory se non esiste"""
        FileManager.ensure_directory(self.memory_file)
        
    async def load_memory(self) -> bool:
        """Carica la memoria dal file"""
        try:
            if FileManager.file_exists(self.memory_file):
                content = await FileManager.async_read_file(self.memory_file)
                if content:
                    data = json.loads(content)
                    # Converti le chiavi da stringa a int
                    self.conversations = {int(k): v for k, v in data.get('conversations', {}).items()}
                    return True
        except Exception as e:
            logger.error(f"Errore nel caricamento della memoria: {e}")
            return False
        return False
        
    async def save_memory(self) -> bool:
        """Salva la memoria sul file"""
        try:
            # Crea un backup
            if FileManager.file_exists(self.memory_file):
                backup_file = f"{self.memory_file}.bak"
                FileManager.safe_remove(backup_file)
                os.rename(self.memory_file, backup_file)
            
            # Salva i dati
            data = {
                'conversations': {str(k): v for k, v in self.conversations.items()},
                'last_updated': DateTimeHelper.get_timestamp()
            }
            
            content = json.dumps(data, indent=2, ensure_ascii=False)
            return await FileManager.async_write_file(self.memory_file, content)
        except Exception as e:
            logger.error(f"Errore nel salvataggio della memoria: {e}")
            return False
            
    def add_message(self, user_id: int, role: str, content: str):
        """Aggiunge un messaggio alla conversazione"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
            
        message = {
            'role': role,
            'content': content,
            'timestamp': DateTimeHelper.get_timestamp()
        }
        
        self.conversations[user_id].append(message)
        
        # Limita la dimensione della memoria
        if len(self.conversations[user_id]) > self.max_size:
            self.conversations[user_id] = self.conversations[user_id][-self.max_size:]
            
    def get_conversation(self, user_id: int, limit: Optional[int] = None) -> List[Dict]:
        """Recupera la conversazione di un utente"""
        if user_id not in self.conversations:
            return []
            
        conv = self.conversations[user_id]
        if limit:
            return conv[-limit:]
        return conv
        
    def get_context(self, user_id: int, max_messages: int = 10) -> str:
        """Ottiene il contesto recente formattato per l'AI"""
        conversation = self.get_conversation(user_id, limit=max_messages)
        
        if not conversation:
            return ""
            
        context_parts = []
        for msg in conversation:
            role = msg['role']
            content = msg['content']
            context_parts.append(f"{role}: {content}")
            
        return "\n".join(context_parts)
        
    def clear_user_memory(self, user_id: int) -> bool:
        """Cancella la memoria di un utente specifico"""
        if user_id in self.conversations:
            del self.conversations[user_id]
            return True
        return False
        
    def cleanup_old_conversations(self, days: int = 30):
        """Rimuove conversazioni vecchie"""
        cutoff_date = datetime.now() - timedelta(days=days)
        users_to_remove = []
        
        for user_id, messages in self.conversations.items():
            if messages:
                last_message_time = DateTimeHelper.timestamp_to_datetime(messages[-1]['timestamp'])
                if last_message_time < cutoff_date:
                    users_to_remove.append(user_id)
                    
        for user_id in users_to_remove:
            del self.conversations[user_id]
            
        return len(users_to_remove)
        
    def get_stats(self) -> Dict:
        """Ottiene statistiche sulla memoria"""
        total_users = len(self.conversations)
        total_messages = sum(len(conv) for conv in self.conversations.values())
        
        return {
            'total_users': total_users,
            'total_messages': total_messages,
            'average_messages_per_user': total_messages / total_users if total_users > 0 else 0
        }
