# Taurosweb - TauroBot 3.0 Ultimate

![Avatar del proprietario](https://avatars.githubusercontent.com/u/198739241?s=48&v=4)

## Descrizione
Taurosweb è il sito ufficiale di **TauroBot 3.0 Ultimate**, un bot AI avanzato per Telegram che integra Ollama, memoria intelligente, sintesi vocale e un'anima hacker. Progettato per offrire un'esperienza interattiva, personalizzata e potente agli utenti Telegram.

---

## Caratteristiche principali
- **Integrazione con Ollama:** Gestione avanzata delle conversazioni con memoria contestuale.
- **Memoria persistente:** Capacità di ricordare informazioni tra le sessioni per una migliore continuità.
- **Sintesi vocale:** Supporto per la conversione testo-voce per risposte vocali.
- **Anima hacker:** Funzionalità avanzate e personalizzabili per utenti esperti.
- **Compatibilità Telegram:** Facile integrazione e utilizzo tramite la piattaforma Telegram.

---

## Stato del progetto
- ✅ **Implementazione completata!**
- Repository pubblico su GitHub
- Bot completamente funzionale con tutti i componenti
- Codice pronto per l'uso in produzione
- Ultimo aggiornamento: Ottobre 2025

---

## Installazione

⚠️ **Per istruzioni dettagliate di installazione, vedi [INSTALL.md](INSTALL.md)**

### Quick Start

1. Clona il repository:
   ```bash
   git clone https://github.com/Lucifer-AI-666/Taurosweb.git
   cd Taurosweb
   ```
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura le variabili d'ambiente:
   ```bash
   cp .env.example .env
   # Modifica .env con il tuo TELEGRAM_BOT_TOKEN
   ```
4. Avvia Ollama:
   ```bash
   ollama serve
   ```
5. Avvia il bot:
   ```bash
   python bot.py
   ```

Per maggiori dettagli, consulta la [guida di installazione completa](INSTALL.md).

---

## Configurazione

Il bot si configura tramite due file principali:

### File .env (richiesto)
Copia `.env.example` in `.env` e configura:
- `TELEGRAM_BOT_TOKEN` - Token del bot Telegram (da @BotFather)
- `OLLAMA_HOST` - Indirizzo server Ollama (default: http://localhost:11434)
- `OLLAMA_MODEL` - Modello AI da usare (default: llama2)
- Altri parametri opzionali per logging, memoria, ecc.

### File config.yml (opzionale)
Personalizza parametri avanzati:
- Configurazione AI (temperatura, max tokens, context window)
- Impostazioni memoria (ritenzione, salvataggio automatico)
- Parametri sintesi vocale (lingua, velocità, volume)
- Limiti e rate limiting

Vedi [INSTALL.md](INSTALL.md) per dettagli completi.

---

## Uso

### Avvio del Bot
```bash
python bot.py
```

### Comandi Telegram Disponibili
- `/start` - Avvia il bot e mostra il messaggio di benvenuto
- `/help` - Mostra aiuto e lista comandi
- `/clear` - Cancella la memoria della conversazione
- `/stats` - Mostra statistiche sulla memoria
- `/voice` - Abilita/disabilita risposte vocali

### Interazione
Invia semplicemente un messaggio al bot su Telegram e ti risponderà utilizzando:
- 🧠 Intelligenza artificiale (tramite Ollama)
- 💾 Memoria persistente delle conversazioni passate
- 🔊 Risposte vocali (opzionale)

### Test
Esegui i test per verificare l'installazione:
```bash
python test_bot.py
```

---

## Struttura del Progetto

```
Taurosweb/
├── bot.py                      # Bot Telegram principale
├── memory.py                   # Sistema memoria persistente
├── voice.py                    # Sistema sintesi vocale (TTS)
├── test_bot.py                 # Suite di test
├── config.yml                  # Configurazione bot
├── requirements.txt            # Dipendenze Python
├── .env.example                # Template variabili d'ambiente
├── .gitignore                  # File esclusi da git
├── README.md                   # Questo file
├── INSTALL.md                  # Guida installazione dettagliata
├── LICENSE                     # Licenza MIT
├── SECURITY.md                 # Policy di sicurezza
├── MessageEvent.js             # Componente React Native
├── remixed-daaaa90c (10).html  # Interfaccia web
└── AnouarLauncher[1].apk       # APK Android (placeholder)
```

---

## Contributi

Contributi e miglioramenti sono benvenuti!

Per contribuire:
1. Fai fork del repository.
2. Crea un branch per la tua feature o correzione.
3. Invia una pull request descrivendo le modifiche apportate.

---

## Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file LICENSE per maggiori dettagli.

---

## Contatti

Per domande o supporto, apri una issue su GitHub o contatta gli sviluppatori tramite Telegram.

---

*Taurosweb - Il tuo bot AI avanzato per Telegram con memoria, sintesi vocale e anima hacker.*

[Visita il repository su GitHub](https://github.com/Lucifer-AI-666/Taurosweb)
