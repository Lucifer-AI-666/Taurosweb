# 🐂 TauroBot 3.0 Ultimate - Guida per Tutti

**Cos'è? Un sistema completo per gestire bot Telegram e progetti, con privacy al 100%**

> Scritto in modo semplice, senza paroloni tecnici! 😊

---

## 📖 Indice

1. [Cos'è TauroBot](#cosè-taurobot)
2. [Cosa fa](#cosa-fa)
3. [Come funziona](#come-funziona)
4. [Le parti principali](#le-parti-principali)
5. [Come si usa](#come-si-usa)
6. [La privacy](#la-privacy)
7. [FAQ - Domande frequenti](#faq)

---

## Cos'è TauroBot?

**TauroBot è come un assistente digitale che:**
- Risponde su Telegram (come ChatGPT, ma TUO e PRIVATO)
- Funziona sul TUO computer (nessuno legge le tue chat)
- Ha un'intelligenza artificiale LOCALE (non manda dati in giro)
- Si può controllare da smartphone con un'app dedicata

**In parole povere:** È come avere ChatGPT che gira sul tuo computer, senza che nessuno legga quello che scrivi.

---

## Cosa fa?

### 1. **Bot Telegram Intelligente** 🤖

Puoi chattare con il bot su Telegram e lui ti risponde usando l'intelligenza artificiale.

**Esempio:**
```
Tu: "Spiegami cos'è Python"
Bot: "Python è un linguaggio di programmazione..."

Tu: "Ricordi cosa ti ho chiesto prima?"
Bot: "Sì, mi hai chiesto di spiegarti Python..."
```

**Ha memoria!** Si ricorda le conversazioni precedenti.

### 2. **Il Garage - Gestisci Tutti i Progetti** 🚗

Immagina un cruscotto dove vedi TUTTI i tuoi progetti (siti web, bot, programmi) in un colpo d'occhio.

**Come un cruscotto auto:**
- Vedi quali girano e quali sono fermi (🟢/🔴)
- Vedi se ci sono problemi (⚠️)
- Puoi avviarli o fermarli con un click
- Vedi quanto consumano (CPU, RAM)

**Esempio pratico:**
```
┌─────────────────┬─────────────────┐
│ MioSitoWeb      │ BotTelegram2    │
│ 🟢 Attivo       │ 🔴 Fermo        │
│ Salute: 95%     │ Salute: 100%    │
│ ⚠️ 1 Problema   │ ✅ Tutto OK     │
└─────────────────┴─────────────────┘
```

Click sul problema → Ti dice ESATTAMENTE dove e cosa sistemare!

### 3. **Gateway Mode - Tu come Ponte** 📡

Immagina di avere un'antenna sul balcone:
- Internet ← **TU (antenna)** ← Bot (in casa, isolato)

**Perché?**
- Il bot non ha accesso diretto a internet
- TU fai da "filtro" - decidi cosa passa e cosa no
- Proteggi le tue informazioni personali

**Come funziona:**
1. Qualcuno chiede qualcosa al bot
2. La richiesta passa da TE
3. TU decidi se farla passare
4. Blocchi le cose pericolose (email, password, ecc.)

### 4. **App Android** 📱

Un'app solo per te per controllare tutto dal telefono:
- **Admin Panel:** Avvia/ferma il bot, vedi statistiche
- **Terminal:** Dai comandi al computer da remoto
- **Il Garage:** Gestisci tutti i progetti anche fuori casa

**Esempio:**
Sei al bar → Apri l'app → Vedi che un progetto è fermo → Lo riavvii → Tutto risolto!

---

## Come funziona?

### Il Sistema è Fatto di 3 Pezzi:

#### 1️⃣ **Il Bot** (bot.py)
Il "cervello" che risponde su Telegram.

**Cosa fa:**
- Riceve messaggi da Telegram
- Chiede all'intelligenza artificiale (Ollama) la risposta
- Ti manda la risposta
- Si ricorda le conversazioni

**Esempio di conversazione:**
```
Tu su Telegram: "Ciao!"
↓
Bot riceve il messaggio
↓
Bot chiede a Ollama: "Come rispondo a 'Ciao'?"
↓
Ollama risponde: "Rispondi con un saluto amichevole"
↓
Bot ti scrive: "Ciao! Come posso aiutarti?"
```

#### 2️⃣ **L'Intelligenza Artificiale** (Ollama)
È come ChatGPT, ma gira sul TUO computer.

**Perché è importante:**
- ✅ Nessuno legge le tue chat (privacy 100%)
- ✅ Nessun abbonamento mensile
- ✅ Funziona anche senza internet (dopo installazione)
- ❌ Richiede un computer decente (consiglia 8GB RAM)

**Modelli disponibili:**
- **Llama 2** (7GB) - Buono, bilanciato
- **Mistral** (4GB) - Più leggero, veloce
- **Phi** (2.7GB) - Leggerissimo per PC vecchi
- **CodeLlama** (7GB) - Specializzato in programmazione

#### 3️⃣ **L'Interfaccia Web** (PWA)
Un sito che apri nel browser come un'app.

**Pagine principali:**

**a) Login** 🔐
- Username e password (salvati SOLO sul tuo PC)
- Password criptata con SHA-256 (impossibile recuperarla)
- Nessun server esterno, tutto locale

**b) Dashboard** 📊
- Vedi statistiche in tempo reale
- Quanto tempo sei connesso
- Quanti messaggi hai scambiato
- Sistemi di sicurezza attivi

**c) Il Garage** 🚗 ← **LA NOVITÀ!**
- Vedi tutti i tuoi progetti
- Aggiungi nuovi progetti
- Monitora salute e problemi
- Avvia/ferma progetti con un click

**d) Gateway** 📡
- Modalità "antenna sul balcone"
- Filtri traffico in entrata/uscita
- Blocca informazioni personali

**e) Admin Panel** ⚙️
- Controlla il bot da remoto
- Cambia impostazioni
- Vedi log e errori

**f) Terminal** 💻
- Come un "prompt dei comandi" ma da browser
- Dai comandi al computer da lontano
- Utile per fare manutenzione

---

## Le Parti Principali

### 🔒 **Sicurezza (NET'ALIS e NEXUS)**

**Cosa fanno?**
Sono due "guardiani" che proteggono il tuo sistema.

#### NET'ALIS - Il Guardiano Quantistico 🧠

**In parole semplici:**
Immagina un poliziotto che controlla tutti i dati che entrano ed escono.

**Cosa fa:**
- Simula 16 "bit quantistici" (come piccoli detective)
- Analizza il traffico in tempo reale
- Rileva comportamenti strani
- Si auto-aggiorna per migliorare

**Esempio:**
```
Dato normale:    "Ciao come stai?"      → ✅ OK
Dato sospetto:   "DROP TABLE users;"    → ⚠️ BLOCCATO (tentativo SQL injection)
```

#### NEXUS - Il Guardiano Intelligente 🤖

**In parole semplici:**
Un sistema che impara dai propri errori e migliora nel tempo.

**Cosa fa:**
- Usa "apprendimento automatico" (machine learning)
- Impara quali comportamenti sono pericolosi
- Blocca email, telefoni, carte di credito nel traffico
- Si evolve geneticamente (come la selezione naturale)

**Esempio:**
```
Prima settimana:  Blocca 60% minacce
Dopo un mese:     Blocca 95% minacce (ha imparato!)
```

**Cosa rilevano insieme:**

| Cosa | NET'ALIS | NEXUS |
|------|----------|-------|
| Email nascoste nei dati | ✅ | ✅ |
| Numeri di telefono | ✅ | ✅ |
| Carte di credito | ✅ | ✅ |
| Attacchi hacker (SQL injection) | ✅ | ✅ |
| Password in chiaro | ✅ | ✅ |
| Comportamenti anomali | ✅ | ✅ |

---

## Come Si Usa?

### 📥 **Installazione (Solo la Prima Volta)**

#### Su Linux:

**1. Scarica il progetto:**
```bash
git clone https://github.com/Lucifer-AI-666/Taurosweb.git
cd Taurosweb
```

**2. Installa i programmi necessari:**
```bash
# Python (probabilmente già installato)
sudo apt install python3 python3-pip

# Ollama (l'intelligenza artificiale)
curl https://ollama.ai/install.sh | sh
```

**3. Installa le librerie Python:**
```bash
pip install -r requirements.txt
```

**4. Configura il token Telegram:**
- Apri il file `.env`
- Metti il tuo token Telegram (lo prendi da @BotFather)

**5. Scarica il modello AI:**
```bash
ollama pull llama2
```

**Fatto!** Installazione completa! ✅

#### Su macOS:

È uguale, ma c'è uno script automatico:
```bash
./start_bot_macos.sh
```

Installa tutto da solo (Homebrew, Python, Ollama, ecc.)!

---

### ▶️ **Avvio Normale**

**Ogni volta che vuoi usare TauroBot:**

**1. Avvia Ollama** (l'intelligenza artificiale):
```bash
ollama serve
```

**2. Avvia il bot** (in un'altra finestra):
```bash
./start_bot.sh
```

**3. Apri il browser:**
```
http://localhost:8000/pwa/login.html
```

**4. Fai login** e inizia a usare!

---

### 🎮 **Uso Quotidiano**

#### **Per chattare con il bot su Telegram:**

1. Apri Telegram
2. Cerca il tuo bot (quello che hai creato)
3. Inizia a scrivere!

```
Tu: Ciao!
Bot: Ciao! Come posso aiutarti oggi?

Tu: Dimmi una barzelletta
Bot: Perché i programmatori confondono Halloween e Natale?
     Perché Oct 31 = Dec 25! 🎃=🎄

Tu: Non ho capito...
Bot: È un gioco di parole sui numeri ottali e decimali...
     [spiega in dettaglio]
```

#### **Per gestire progetti con Il Garage:**

**Scenario 1 - Vedi tutto in un colpo d'occhio:**

1. Apri `http://localhost:8000/pwa/garage.html`
2. Vedi tutti i tuoi progetti:

```
┌──────────────────────────────────────┐
│ 🚗 Il Garage                         │
├──────────────────────────────────────┤
│ [5] Progetti  [3] Attivi  [1] Problema│
└──────────────────────────────────────┘

┌─────────────┬─────────────┬─────────────┐
│ TauroBot    │ MioSitoWeb  │ APIServer   │
│ 🟢 Running  │ 🟢 Running  │ 🔴 Stopped  │
│ 95% ▓▓▓▓▓▓▓▓▓░│ 78% ▓▓▓▓▓▓▓░░│ 100% ▓▓▓▓▓▓▓▓▓▓│
│             │ ⚠️ Test falliti│           │
└─────────────┴─────────────┴─────────────┘
```

**Scenario 2 - Aggiungi un nuovo progetto:**

1. Click su "➕ Aggiungi Nuovo Progetto"
2. Compila il form:

```
Nome: Il Mio Blog
Tipo: Web App
Path: /home/user/blog
URL: http://localhost:3000
Comando start: npm start
Descrizione: Il mio blog personale in React
```

3. Click "Salva" → Boom! Progetto aggiunto! 💥

**Scenario 3 - Risolvi un problema:**

1. Vedi "⚠️ 1 Problema" su un progetto
2. Click sul problema
3. Ti appare:

```
╔════════════════════════════════════════╗
║ ⚠️ Test Falliti                        ║
╠════════════════════════════════════════╣
║ 3 test non passano in test_api.py     ║
║                                        ║
║ File: /home/user/MioSitoWeb/test_api.py║
║ Linea: 78                              ║
║                                        ║
║ Fix suggerito:                         ║
║ Controlla gli assert sui codici HTTP  ║
║                                        ║
║ [Chiudi]  [Vai al Fix] ←              ║
╚════════════════════════════════════════╝
```

4. Click "Vai al Fix"
5. Si apre il file esatto alla linea con l'errore!

---

### 📱 **App Android**

**Per controllarti da smartphone:**

**1. Build dell'APK** (solo prima volta):
```bash
cd android
./build_apk.sh
# Scegli: 2) Release APK
```

**2. Installa sul telefono:**
```bash
adb install -r app-release.apk
```

**3. Usa l'app:**
- Apri l'app
- Fai login (stesso username/password del web)
- Accedi a tutte le funzioni:
  - 🚗 Il Garage
  - ⚙️ Admin Panel
  - 💻 Terminal
  - 📊 Dashboard

**Esempio pratico:**

Sei in treno → Il sito è fermo → Apri l'app → Vai su Il Garage → Click "▶️ Start" → Tutto risolto! 🚀

---

## La Privacy

### 🔒 **Perché è Sicuro al 100%?**

**1. Tutto sul TUO computer**
- Nessun server esterno
- Nessuna "nuvola" (cloud)
- Tutti i dati salvati sul tuo PC
- Zero dipendenze da aziende tipo Google/Amazon

**2. Password criptate**
- Quando fai login, la password viene "hashata" (SHA-256)
- Significa: trasformata in codice irreversibile
- Anche se qualcuno ruba il database, non può leggere la password

**Esempio:**
```
Password vera:    "tauro2024"
Salvata come:     "7a8f3b2c... (64 caratteri incomprensibili)"

Impossibile tornare indietro!
Da "7a8f3b2c..." NON puoi risalire a "tauro2024"
```

**3. Nessuna chiamata esterna**
- L'AI gira sul tuo PC (Ollama)
- Nessun dato mandato a ChatGPT, Google, ecc.
- Le tue chat restano TUE

**4. Gateway Mode filtra tutto**
- Blocca email, telefoni, carte di credito
- Prima che escano dal tuo PC
- Tu hai controllo totale

**5. Sistemi di sicurezza (NET'ALIS + NEXUS)**
- Due guardiani sempre attivi
- Analizzano traffico 24/7
- Bloccano minacce in tempo reale

### 📊 **Privacy Score: 10/10**

| Criterio | Score | Perché |
|----------|-------|--------|
| Crittografia | 10/10 | SHA-256, standard militare |
| Storage locale | 10/10 | Zero cloud, tutto sul tuo PC |
| API esterne | 10/10 | Nessuna chiamata esterna |
| Tracking | 10/10 | Zero analytics, zero cookies |
| Anonimato | 10/10 | Nessun dato personale richiesto |
| Controllo utente | 10/10 | Sei TU il padrone dei dati |

**Confronto con alternative:**

| Sistema | Dove girano i dati | Privacy |
|---------|-------------------|---------|
| ChatGPT | Server OpenAI (USA) | 3/10 |
| Google Assistant | Server Google | 2/10 |
| Alexa | Server Amazon | 2/10 |
| **TauroBot** | **TUO PC** | **10/10** ✅ |

---

## FAQ - Domande Frequenti

### ❓ **È difficile da installare?**

**No!** Se sai aprire il Terminale e copiare comandi, ce la fai.

Tempo richiesto: 10-15 minuti

### ❓ **Quanto spazio occupa?**

**Totale: ~8-10 GB**
- Ollama: ~7GB (modello Llama2)
- TauroBot: ~50MB
- Dipendenze Python: ~500MB

### ❓ **Serve un computer potente?**

**Consigliato:**
- CPU: 4 core o più
- RAM: 8GB minimo (16GB ideale)
- Spazio disco: 10GB liberi

**Ma funziona anche su PC più vecchi:**
- Usa modello Phi (2.7GB invece di 7GB)
- Sarà più lento ma funziona!

### ❓ **Funziona su Windows?**

**Sì!** Ma devi installare:
1. Python 3 (da Microsoft Store)
2. Ollama (da ollama.ai)
3. Git (opzionale)

Oppure usa WSL (Windows Subsystem for Linux) - funziona benissimo!

### ❓ **Posso usarlo senza Ollama?**

**Sì, ma:**
- Il bot Telegram NON funziona (serve Ollama per le risposte)
- Tutto il resto funziona:
  - Il Garage ✅
  - Gateway Mode ✅
  - Admin Panel ✅
  - Terminal ✅
  - Dashboard ✅

### ❓ **È gratis?**

**SÌ! 100% GRATIS!**
- Nessun abbonamento
- Nessun costo nascosto
- Codice open source (puoi modificarlo)
- Nessuna pubblicità

### ❓ **Posso accedere da fuori casa?**

**Sì!** Con questi metodi:

**1. Ngrok** (il più facile):
```bash
ngrok http 8000
# Ti dà un link tipo: https://abc123.ngrok.io
```

**2. Cloudflare Tunnel**:
```bash
cloudflared tunnel --url http://localhost:8000
```

**3. VPN casalinga**:
- Installa WireGuard/OpenVPN sul tuo PC
- Connettiti alla VPN da fuori
- Accedi a localhost:8000

**4. Port forwarding**:
- Apri porta 8000 sul router
- Accedi via IP pubblico

### ❓ **È sicuro per uso professionale?**

**Dipende:**

✅ **SÌ se:**
- Usi per test/sviluppo personale
- Usi in rete locale (casa/ufficio)
- Non devi rispettare normative aziendali

❌ **NO se:**
- Devi avere backup automatici
- Serve alta disponibilità (99.9% uptime)
- Serve supporto tecnico certificato

Per uso professionale pesante → Considera soluzioni aziendali.

### ❓ **Posso vendere progetti fatti con TauroBot?**

**SÌ!** Licenza MIT:
- Puoi usarlo commercialmente
- Puoi modificarlo
- Puoi venderlo
- Devi solo mantenere la licenza originale

### ❓ **Quanta corrente consuma?**

**Consumo tipico:**
- In idle (fermo): ~5-10W
- Quando risponde: ~50-100W (per qualche secondo)

**Costo elettrico stimato:**
- 24h acceso al mese: ~2-3€
- Solo quando serve: ~0.50€ al mese

### ❓ **Si può migliorare?**

**CERTO!** È open source!

**Idee per il futuro:**
- [ ] Supporto multi-lingua
- [ ] Integrazione con WhatsApp
- [ ] Backup automatici
- [ ] Grafici storici delle performance
- [ ] Notifiche push più avanzate
- [ ] Supporto Docker per installazione facile
- [ ] Integrazione con GitHub Actions

**Contribuisci su:** https://github.com/Lucifer-AI-666/Taurosweb

---

## 🎯 In Sintesi

### TauroBot è:

✅ **Un bot Telegram intelligente con memoria**
✅ **Un gestore multi-progetto (Il Garage)**
✅ **Un sistema di sicurezza (NET'ALIS + NEXUS)**
✅ **Un'app Android per controllo remoto**
✅ **100% privato - tutto sul tuo PC**
✅ **Gratis e open source**
✅ **Facile da usare**

### Non è:

❌ Un servizio cloud
❌ Un abbonamento mensile
❌ Complicato da capire
❌ Invasivo della privacy
❌ Legato a Google/Amazon/Microsoft

---

## 🚀 Prossimi Passi

**Se vuoi iniziare:**

1. **Installa** seguendo la guida sopra (10 min)
2. **Avvia** con `./start_bot.sh`
3. **Apri** il browser su `localhost:8000/pwa/login.html`
4. **Registrati** (username + password)
5. **Esplora** Il Garage e tutte le funzioni!

**Se hai domande:**
- Leggi la documentazione completa: `README.md`
- Guarda il report tecnico: `PRIVACY_SECURITY_REPORT.md`
- Guarda il test report: `TEST_REPORT.md`

**Se vuoi aiutare:**
- Segnala bug su GitHub Issues
- Contribuisci con codice (Pull Request)
- Condividi con amici che tengono alla privacy!

---

## 📞 Supporto

**Hai problemi?**

1. Controlla i log: `logs/bot.log`
2. Guarda la guida installazione: `INSTALL.md`
3. Per macOS: `INSTALL_MACOS.md`
4. Apri un Issue su GitHub

**Ricorda:** TauroBot è un progetto personale/educativo.
Non c'è supporto 24/7, ma la community aiuta! 💪

---

**Creato con ❤️ per chi ama la privacy**

**Versione:** 3.0.0-garage
**Data:** Novembre 2025
**Licenza:** MIT

🐂 **TauroBot - La tua privacy, il tuo controllo!** 🔒

---

*P.S.: Se ti è piaciata questa guida, condividila! Più persone usano software che rispetta la privacy, meglio è per tutti! 🌟*
