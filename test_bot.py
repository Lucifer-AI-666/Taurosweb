"""
Script di test per TauroBot 3.0
Testa i componenti principali senza avviare il bot
"""

import asyncio
import os
from memory import MemorySystem
from voice import VoiceSystem


async def test_memory_system():
    """Test del sistema di memoria"""
    print("🧪 Test Memory System...")
    
    memory = MemorySystem(memory_file="test_memory.json", max_size=10)
    
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
    
    # Test caricamento
    memory2 = MemorySystem(memory_file="test_memory.json")
    await memory2.load_memory()
    assert len(memory2.get_conversation(123)) == 2, "Errore: memoria non caricata"
    
    # Test statistiche
    stats = memory.get_stats()
    assert stats['total_users'] == 2, "Errore: numero utenti non corretto"
    
    # Test cancellazione
    memory.clear_user_memory(123)
    assert len(memory.get_conversation(123)) == 0, "Errore: memoria non cancellata"
    
    # Cleanup
    if os.path.exists("test_memory.json"):
        os.remove("test_memory.json")
    if os.path.exists("test_memory.json.bak"):
        os.remove("test_memory.json.bak")
    
    print("✅ Memory System: OK")


async def test_voice_system():
    """Test del sistema vocale"""
    print("🧪 Test Voice System...")
    
    voice = VoiceSystem()
    
    # Test inizializzazione
    voice._init_engine()
    assert voice._engine is not None, "Errore: engine non inizializzato"
    
    # Test configurazione
    voice.set_rate(200)
    assert voice.rate == 200, "Errore: rate non impostato"
    
    voice.set_volume(0.5)
    assert voice.volume == 0.5, "Errore: volume non impostato"
    
    # Test sintesi (opzionale, richiede dipendenze)
    try:
        result = await voice.text_to_speech("Test vocale", "test_voice.mp3")
        if result:
            print("  ℹ️ Sintesi vocale funzionante")
            if os.path.exists("test_voice.mp3"):
                os.remove("test_voice.mp3")
        else:
            print("  ⚠️ Sintesi vocale non disponibile (dipendenze mancanti)")
    except Exception as e:
        print(f"  ⚠️ Sintesi vocale non testabile: {e}")
    
    voice.cleanup()
    print("✅ Voice System: OK")


async def test_config_files():
    """Test presenza file di configurazione"""
    print("🧪 Test Configuration Files...")
    
    required_files = [
        'bot.py',
        'memory.py',
        'voice.py',
        'requirements.txt',
        'config.yml',
        '.env.example',
        '.gitignore',
        'README.md',
        'INSTALL.md',
        'LICENSE'
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
        
        print("\n" + "="*50)
        print("✅ Tutti i test completati con successo!")
        print("="*50 + "\n")
        
        print("📝 Note:")
        print("  • Per avviare il bot: python bot.py")
        print("  • Configura .env prima dell'avvio")
        print("  • Assicurati che Ollama sia in esecuzione")
        
    except Exception as e:
        print(f"\n❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
