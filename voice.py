"""
Modulo di sintesi vocale per TauroBot 3.0
Gestisce la conversione testo-voce
"""

import pyttsx3
import os
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
from utils import FileManager, ErrorHandler, get_logger

logger = get_logger(__name__)


class VoiceSystem:
    """Gestisce la sintesi vocale (TTS)"""
    
    def __init__(self, language: str = 'it', rate: int = 150, volume: float = 1.0):
        self.language = language
        self.rate = rate
        self.volume = volume
        self.executor = ThreadPoolExecutor(max_workers=2)
        self._engine = None
        
    def _init_engine(self):
        """Inizializza il motore TTS"""
        if self._engine is None:
            self._engine = pyttsx3.init()
            self._engine.setProperty('rate', self.rate)
            self._engine.setProperty('volume', self.volume)
            
            # Imposta la voce italiana se disponibile
            voices = self._engine.getProperty('voices')
            for voice in voices:
                if self.language in voice.languages or 'italian' in voice.name.lower():
                    self._engine.setProperty('voice', voice.id)
                    break
                    
    def _synthesize(self, text: str, output_file: str) -> bool:
        """Sintetizza il testo e salva in un file audio"""
        try:
            self._init_engine()
            self._engine.save_to_file(text, output_file)
            self._engine.runAndWait()
            return FileManager.file_exists(output_file)
        except Exception as e:
            logger.error(f"Errore nella sintesi vocale: {e}")
            return False
            
    async def text_to_speech(self, text: str, output_file: str) -> Optional[str]:
        """
        Converte testo in audio (async)
        
        Args:
            text: Testo da convertire
            output_file: Path del file audio di output
            
        Returns:
            Path del file audio se successo, None altrimenti
        """
        try:
            # Esegui la sintesi in un thread separato per non bloccare
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(
                self.executor,
                self._synthesize,
                text,
                output_file
            )
            
            if success:
                return output_file
            return None
        except Exception as e:
            logger.error(f"Errore in text_to_speech: {e}")
            return None
            
    def set_rate(self, rate: int):
        """Imposta la velocità di pronuncia"""
        self.rate = rate
        if self._engine:
            self._engine.setProperty('rate', rate)
            
    def set_volume(self, volume: float):
        """Imposta il volume (0.0 - 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        if self._engine:
            self._engine.setProperty('volume', self.volume)
            
    def cleanup(self):
        """Pulisce le risorse"""
        if self._engine:
            try:
                self._engine.stop()
            except:
                pass
        self.executor.shutdown(wait=False)
        
    def __del__(self):
        """Distruttore"""
        self.cleanup()
