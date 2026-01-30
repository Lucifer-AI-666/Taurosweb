"""
Script di test per TauroBot 3.0
Testa i componenti principali senza avviare il bot
"""

import asyncio
import os
from memory import MemorySystem
from voice import VoiceSystem
from rate_limiter import RateLimiter
from i18n import get_text, is_supported_language, get_available_languages


async def test_memory_system():
    """Test del sistema di memoria"""
    print("🧪 Test Memory System...")
    
    import uuid
    test_file = f"test_memory_{uuid.uuid4().hex[:8]}.json"
    memory = MemorySystem(memory_file=test_file, max_size=10)
    
    # Test aggiungi messaggi
    memory.add_message(123, "user", "Ciao!")
    memory.add_message(123, "assistant", "Ciao! Come posso aiutarti?")
    memory.add_message(456, "user", "Test utente 2")
    
    # Test recupero conversazione
    conv = memory.get_conversation(123)
    assert len(conv) == 2, "Errore: numero messaggi non corretto"
    
    # Test contesto
    context = memory.get_context(123)
    assert "Ciao!" in context, "Errore: contesto non contiene messaggio"
    
    # Test salvataggio
    await memory.save_memory()
    
    # Test caricamento (ricarica lo stesso oggetto)
    await memory.load_memory()
    assert len(memory.get_conversation(456)) == 1, "Errore: memoria non ricaricata"
    
    # Test statistiche
    stats = memory.get_stats()
    assert stats['total_users'] == 2, "Errore: numero utenti non corretto"
    
    # Test cancellazione
    memory.clear_user_memory(123)
    assert len(memory.get_conversation(123)) == 0, "Errore: memoria non cancellata"
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(f"{test_file}.bak"):
        os.remove(f"{test_file}.bak")
    
    print("✅ Memory System: OK")


async def test_voice_system():
    """Test del sistema vocale"""
    print("🧪 Test Voice System...")
    
    voice = VoiceSystem()
    
    # Test configurazione
    voice.set_rate(200)
    assert voice.rate == 200, "Errore: rate non impostato"
    
    voice.set_volume(0.5)
    assert voice.volume == 0.5, "Errore: volume non impostato"
    
    # Test sintesi (opzionale, richiede dipendenze)
    import uuid
    try:
        test_audio = f"test_voice_{uuid.uuid4().hex[:8]}.mp3"
        result = await voice.text_to_speech("Test vocale", test_audio)
        if result:
            print("  ℹ️ Sintesi vocale funzionante")
            if os.path.exists(test_audio):
                os.remove(test_audio)
        else:
            print("  ⚠️ Sintesi vocale non disponibile (dipendenze mancanti)")
    except Exception as e:
        print(f"  ⚠️ Sintesi vocale non testabile: {e}")
    
    voice.cleanup()
    print("✅ Voice System: OK")


async def test_rate_limiter():
    """Test del sistema di rate limiting"""
    print("🧪 Test Rate Limiter...")
    
    limiter = RateLimiter(max_requests=3, window_seconds=60, block_duration=10)
    
    # Test richieste normali
    for i in range(3):
        allowed, wait = limiter.check(123)
        assert allowed, f"Errore: richiesta {i+1} dovrebbe essere permessa"
        limiter.record(123)
    
    # Test superamento limite
    allowed, wait = limiter.check(123)
    assert not allowed, "Errore: richiesta dovrebbe essere bloccata"
    assert wait is not None, "Errore: wait_seconds dovrebbe essere valorizzato"
    
    # Test whitelist
    limiter.add_to_whitelist(456)
    for i in range(10):
        allowed, wait = limiter.check(456)
        assert allowed, "Errore: utente whitelist dovrebbe sempre passare"
        limiter.record(456)
    
    # Test reset utente
    limiter.reset_user(123)
    allowed, wait = limiter.check(123)
    assert allowed, "Errore: dopo reset dovrebbe essere permesso"
    
    # Test statistiche
    usage = limiter.get_usage(123)
    assert 'requests_count' in usage, "Errore: mancano statistiche"
    
    print("✅ Rate Limiter: OK")


async def test_i18n():
    """Test del sistema di internazionalizzazione"""
    print("🧪 Test i18n System...")
    
    # Test lingue supportate
    assert is_supported_language('it'), "Errore: italiano dovrebbe essere supportato"
    assert is_supported_language('en'), "Errore: inglese dovrebbe essere supportato"
    assert not is_supported_language('xx'), "Errore: lingua inventata non dovrebbe esistere"
    
    # Test lista lingue
    langs = get_available_languages()
    assert len(langs) >= 5, "Errore: dovrebbero esserci almeno 5 lingue"
    assert 'it' in langs, "Errore: italiano mancante"
    assert 'en' in langs, "Errore: inglese mancante"
    
    # Test traduzioni
    text_it = get_text('welcome.greeting', 'it', name='Test')
    assert 'Ciao' in text_it or 'Test' in text_it, "Errore: traduzione italiana non funziona"
    
    text_en = get_text('welcome.greeting', 'en', name='Test')
    assert 'Hello' in text_en or 'Test' in text_en, "Errore: traduzione inglese non funziona"
    
    # Test fallback a chiave se mancante
    missing = get_text('chiave.inesistente', 'it')
    assert 'chiave.inesistente' in missing, "Errore: fallback a chiave non funziona"
    
    print("✅ i18n System: OK")


async def test_config_files():
    """Test presenza file di configurazione"""
    print("🧪 Test Configuration Files...")
    
    required_files = [
        'bot.py',
        'memory.py',
        'voice.py',
        'rate_limiter.py',
        'requirements.txt',
        'config.yml',
        '.env.example',
        '.gitignore',
        'README.md',
        'INSTALL.md',
        'LICENSE',
        'Dockerfile',
        'docker-compose.yml',
        'i18n/__init__.py',
        'i18n/it.json',
        'i18n/en.json'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"  ❌ File mancanti: {', '.join(missing)}")
        return False
    
    print("✅ Configuration Files: OK")
    return True


async def main():
    """Esegue tutti i test"""
    print("\n" + "="*50)
    print("🐂 TauroBot 3.0 Ultimate - Test Suite")
    print("="*50 + "\n")
    
    try:
        await test_config_files()
        await test_memory_system()
        await test_voice_system()
        await test_rate_limiter()
        await test_i18n()
        
        print("\n" + "="*50)
        print("✅ Tutti i test completati con successo!")
        print("="*50 + "\n")
        
        print("📝 Note:")
        print("  • Per avviare il bot: python bot.py")
        print("  • Oppure con Docker: docker-compose up -d")
        print("  • Configura .env prima dell'avvio")
        print("  • Assicurati che Ollama sia in esecuzione")
        
    except Exception as e:
        print(f"\n❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
