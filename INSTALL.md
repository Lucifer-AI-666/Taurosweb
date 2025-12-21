# Guida di Installazione e Configurazione - TauroBot 3.0 Ultimate

## Prerequisiti

- Python 3.8 o superiore
- Ollama installato e in esecuzione
- Account Telegram e Bot Token

## Installazione

### 1. Clona il Repository

```bash
git clone https://github.com/Lucifer-AI-666/Taurosweb.git
cd Taurosweb
```

### 2. Crea un Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

### 3. Installa le Dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configura Ollama

Assicurati che Ollama sia in esecuzione:

```bash
# Installa Ollama (se non già installato)
# Visita: https://ollama.ai

# Scarica un modello (es. llama2)
ollama pull llama2

# Avvia Ollama
ollama serve
```

### 5. Configura il Bot Telegram

1. Crea un bot su Telegram tramite [@BotFather](https://t.me/BotFather)
2. Ottieni il token del bot
3. Copia il file `.env.example` in `.env`:

```bash
cp .env.example .env
```

4. Modifica `.env` con i tuoi dati:

```env
TELEGRAM_BOT_TOKEN=il_tuo_token_qui
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

### 6. Personalizza la Configurazione (Opzionale)

Modifica `config.yml` per personalizzare:
- Parametri dell'AI (temperatura, max tokens)
- Impostazioni memoria
- Configurazione voce
- Limiti e rate limiting

## Avvio del Bot

### Metodo Facile (Consigliato) 🚀

**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```cmd
run.bat
```

Lo script automaticamente:
- ✅ Crea il virtual environment se non esiste
- ✅ Installa/aggiorna le dipendenze
- ✅ Crea il file .env se mancante
- ✅ Verifica che Ollama sia raggiungibile
- ✅ Avvia il bot

### Metodo con Makefile

```bash
make setup      # Prima volta: crea venv e .env
make install    # Installa dipendenze
make run        # Avvia il bot
make test       # Esegui test
make clean      # Pulisci file temporanei
```

### Metodo Manuale

```bash
python bot.py
```

Il bot sarà attivo e risponderà ai messaggi su Telegram!

## Comandi Disponibili

- `/start` - Avvia il bot e mostra il messaggio di benvenuto
- `/help` - Mostra l'aiuto e i comandi disponibili
- `/clear` - Cancella la memoria della tua conversazione
- `/stats` - Mostra statistiche sulla memoria
- `/voice` - Abilita/disabilita le risposte vocali

## Struttura del Progetto

```
Taurosweb/
├── bot.py              # Bot principale
├── memory.py           # Sistema di memoria persistente
├── voice.py            # Sistema sintesi vocale
├── config.yml          # Configurazione bot
├── requirements.txt    # Dipendenze Python
├── .env.example        # Template variabili d'ambiente
├── .gitignore          # File da escludere da git
├── README.md           # Documentazione principale
└── memory/             # Directory memoria (creata automaticamente)
```

## Risoluzione Problemi

### Il bot non risponde

1. Verifica che Ollama sia in esecuzione: `curl http://localhost:11434/api/tags`
2. Controlla il token Telegram nel file `.env`
3. Verifica i log del bot per errori

### Errore "Model not found"

```bash
ollama pull llama2  # o il modello specificato in .env
```

### Errore sintesi vocale

La sintesi vocale richiede dipendenze di sistema. Su Linux:

```bash
sudo apt-get install espeak ffmpeg libespeak1
```

## Sviluppo

Per contribuire al progetto:

1. Fai fork del repository
2. Crea un branch per la tua feature
3. Committa le modifiche
4. Invia una pull request

## Licenza

MIT License - Vedi il file LICENSE per dettagli
