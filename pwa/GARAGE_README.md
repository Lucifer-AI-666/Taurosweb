# 🚗 Il Garage - Multi-Project Manager

**La tua officina digitale per gestire tutti i progetti da un unico posto**

> Perché chi ha più di un progetto merita un posto per organizzarli tutti! 🛠️

---

## 🎯 Il Concetto

**Il Garage è il tuo "mission control" per tutti i side projects.**

Invece di dover:
- ❌ Aprire 10 terminal diverse
- ❌ Ricordarti quali progetti girano
- ❌ Cercare manualmente i problemi nei log
- ❌ Gestire ogni progetto separatamente

Con Il Garage puoi:
- ✅ Vedere TUTTI i progetti in una dashboard unificata
- ✅ Monitorare salute, CPU, RAM, uptime in tempo reale
- ✅ Rilevare problemi automaticamente
- ✅ Andare direttamente al file/linea con l'errore
- ✅ Avviare/fermare progetti con un click
- ✅ Accedere al terminal e admin panel di ogni progetto

---

## 🚀 Features

### 1. Dashboard Unificata

```
┌────────────────────────────────────────────────────┐
│  🚗 Il Garage - Dashboard                          │
├────────────────────────────────────────────────────┤
│  [5] Progetti Totali  [3] Running  [2] Problemi   │
└────────────────────────────────────────────────────┘

┌─────────────┬─────────────┬─────────────┐
│ TauroBot    │ WebApp      │ API Server  │
│ 🟢 Running  │ 🟢 Running  │ 🔴 Stopped  │
│ Health: 95% │ Health: 78% │ Health: 100%│
│             │ ⚠️ 1 Issue  │             │
└─────────────┴─────────────┴─────────────┘
```

**Statistiche globali:**
- Numero totale progetti
- Progetti attivi/inattivi
- Problemi complessivi
- Salute media del "parco progetti"

### 2. Multi-Project Support

**Tipi supportati:**
- 🤖 **Telegram Bot** - TauroBot, altri bot
- 🌐 **Web App** - React, Vue, Angular, PWA
- 🔌 **REST API** - Express, FastAPI, Flask
- 🧠 **Machine Learning** - Modelli PyTorch, TensorFlow
- 📦 **Altro** - Qualsiasi progetto con path e comando start

**Aggiungi progetto in 30 secondi:**
1. Click su "➕ Aggiungi Nuovo Progetto"
2. Compila form:
   - Nome: `MioProgettoFigo`
   - Tipo: `Web App`
   - Path: `/home/user/MioProgettoFigo`
   - URL: `http://localhost:3000`
   - Start cmd: `npm start`
   - Descrizione: `Il mio side project incredibile`
3. Salva → Boom! 💥

### 3. Problem Detection Automatica

**Il Garage scansiona continuamente e rileva:**

| Problema | Descrizione | Severity |
|----------|-------------|----------|
| **Memoria elevata** | RAM usage sopra soglia | ⚠️ Warning |
| **Dipendenze obsolete** | CVE security issues | 🔴 High |
| **Test falliti** | Unit/integration test fail | 🔴 Critical |
| **Porta occupata** | Conflitto porte | ⚠️ Warning |
| **Build errors** | Compilazione fallita | 🔴 Critical |
| **CPU alta** | Uso CPU >80% persistente | ⚠️ Warning |

**Auto-scan ogni 30 secondi:**
- Controlla log per errori
- Monitora risorse (CPU, RAM)
- Verifica dipendenze con vulnerabilità note
- Simula esecuzione test (se configurati)

### 4. Direct Navigation ai Problemi

**Esempio workflow:**

```
1. Garage rileva: "3 test falliti in test_api.py"

2. Click sul problema → Modal con dettagli:
   ┌────────────────────────────────────────┐
   │ ⚠️ Test Falliti                        │
   ├────────────────────────────────────────┤
   │ Descrizione:                           │
   │ 3 test non passano in test_api.py     │
   │                                        │
   │ File: /home/user/MyAPI/tests/test_api.py│
   │ Linea: 78                              │
   │                                        │
   │ Fix suggerito:                         │
   │ Controlla gli assert sui codici HTTP  │
   │ 401 - autenticazione potrebbe essere  │
   │ cambiata                               │
   │                                        │
   │ [Chiudi]  [Vai al Fix] ←              │
   └────────────────────────────────────────┘

3. Click "Vai al Fix" → Apre editor sul file esatto

4. Risolvi bug → Health score sale 60% → 100% ✅
```

### 5. Real-Time Monitoring

**Per ogni progetto:**
- **Status**: 🟢 Running / 🔴 Stopped / 🟡 Idle
- **Health**: Score 0-100% (basato su problemi, risorse, uptime)
- **Uptime**: Tempo di esecuzione continua
- **CPU**: Uso processore in %
- **RAM**: Memoria utilizzata in MB
- **Last commit**: Ultimo commit Git

**Aggiornamento automatico ogni 10 secondi.**

### 6. Quick Actions

**Per ogni progetto nella griglia:**

```
┌─────────────────────────────────────┐
│ 🤖 TauroBot 3.0 Ultimate           │
│ 🟢 RUNNING                          │
│ Health: ▓▓▓▓▓▓▓▓▓░ 95%            │
│                                     │
│ 📁 /home/user/Taurosweb            │
│ ⏱️ Uptime: 2h 34m                  │
│ 💻 CPU/RAM: 12% / 245MB            │
│                                     │
│ [💻 Terminal] [⚙️ Admin] [⏸️ Stop] │
└─────────────────────────────────────┘
```

**Azioni disponibili:**
- **Terminal**: Apri terminal remoto per quel progetto
- **Admin**: Apri admin panel specifico
- **Start/Stop**: Avvia o ferma il progetto

### 7. Smart Filters

**Filtra i progetti visualizzati:**
- 📁 **Tutti**: Mostra tutti i progetti
- ▶️ **In Esecuzione**: Solo progetti running
- ⚠️ **Con Problemi**: Solo progetti con issue
- ✅ **Healthy**: Solo progetti con health >80%

---

## 🎨 UI/UX

### Design Principles

1. **At-a-glance visibility**: Vedi stato di TUTTO in un colpo d'occhio
2. **Color coding**: Verde=ok, Giallo=warning, Rosso=critico
3. **Direct actions**: 1 click per fare qualsiasi cosa
4. **Mobile-first**: Funziona perfettamente su smartphone
5. **Offline-capable**: Cached via Service Worker

### Visual Indicators

**Health Bar:**
```
Health: ▓▓▓▓▓▓▓▓▓░ 95%  → Verde (80-100%)
Health: ▓▓▓▓▓░░░░░ 50%  → Giallo (50-79%)
Health: ▓░░░░░░░░░ 10%  → Rosso (0-49%)
```

**Status Badges:**
- 🟢 **RUNNING** → Progetto attivo
- 🔴 **STOPPED** → Progetto fermo
- 🟡 **IDLE** → In attesa (es: server senza traffico)

**Card Border:**
- **Verde**: Tutto ok, nessun problema
- **Giallo**: Warning presenti, check consigliato
- **Rosso**: Problemi critici, azione richiesta

---

## 💾 Storage

**Dove sono salvati i progetti?**

Tutto in `localStorage` del browser:

```javascript
localStorage.setItem('garage_projects', JSON.stringify([
  {
    id: 'taurobot',
    name: 'TauroBot 3.0 Ultimate',
    type: 'bot',
    status: 'running',
    health: 95,
    path: '/home/user/Taurosweb',
    url: 'http://localhost:8000',
    startCmd: 'python bot.py',
    description: 'Bot Telegram con AI locale',
    lastCommit: 'Add bot startup script',
    problems: [],
    uptime: '2h 34m',
    cpu: '12%',
    ram: '245MB'
  },
  // ... altri progetti
]));
```

**TauroBot è sempre presente** - viene ricreato automaticamente se manca.

---

## 🔧 Integrazione con TauroBot

### Da Admin Panel

Nel `android/admin.html` c'è una card dedicata:

```html
┌─────────────────────────────────────┐
│ 🚗 Il Garage - Project Manager     │
│                                     │
│ Gestisci tutti i tuoi progetti da  │
│ un unico posto                      │
│                                     │
│ [🚗 Apri Il Garage]                │
└─────────────────────────────────────┘
```

### Da Dashboard PWA

Nel `pwa/dashboard.html` c'è un tab:

```
[📊 Overview] [🧠 NET'ALIS] [🤖 NEXUS] [📝 Activity] [🚗 Il Garage]
                                                        ↑
                                               Tab viola highlight
```

### Service Worker

Il Garage è cached per funzionamento offline:

```javascript
const CACHE_NAME = 'taurobot-v3.0.0-garage';
const urlsToCache = [
  '/pwa/garage.html',  // ← Il Garage
  // ... altri file
];
```

---

## 🎓 Use Cases

### 1. Sviluppatore con 5 side projects

**Scenario:**
- TauroBot (bot Telegram)
- Portfolio (React website)
- Blog API (FastAPI)
- ML Model (PyTorch)
- Test Automation (Selenium)

**Problema:** Ogni giorno devi:
1. Aprire 5 terminal diverse
2. Fare `cd` in 5 directory diverse
3. Eseguire `python bot.py`, `npm start`, `uvicorn main:app`, etc.
4. Controllare log di ognuno
5. Ricordarti quale gira e quale no

**Soluzione con Il Garage:**
1. Apri `http://localhost:8000/pwa/garage.html`
2. Vedi tutti e 5 in una griglia
3. Click "Start" su quelli che servono
4. Vedi subito chi ha problemi
5. Click su problema → Vai al fix

**Tempo risparmiato:** Da 15 minuti a 30 secondi. ⚡

### 2. Team che condivide progetti

**Scenario:**
Team di 3 dev lavorano su 10 microservizi.

**Problema:**
- "Quale servizio sta girando?"
- "Chi ha rotto il build?"
- "Perché l'API non risponde?"

**Soluzione:**
1. Ogni dev ha Il Garage con gli stessi 10 progetti
2. Filtro "Con Problemi" → Vede subito quali servizi sono broken
3. Click su problema → Vede file/linea esatta
4. Risolve e committa
5. Altri dev aggiornano e vedono health score salire

### 3. Monitoraggio production

**Scenario:**
Hai 3 servizi in produzione su VPS remoto.

**Problema:**
Non vuoi SSH ogni volta per controllare status.

**Soluzione:**
1. Installa APK Android con Il Garage
2. Configura remote access (ngrok/cloudflare)
3. Apri Garage da smartphone ovunque nel mondo
4. Vedi real-time CPU, RAM, uptime
5. Se qualcosa va giù → Riavvia con un tap

---

## 🛣️ Roadmap Future Features

- [ ] **Git integration**: Auto-pull, push, commit count
- [ ] **Docker support**: Gestisci container da Garage
- [ ] **CI/CD triggers**: Trigger build/deploy da interfaccia
- [ ] **Team collaboration**: Condividi progetti via cloud
- [ ] **Alerting**: Notifiche push quando progetto va offline
- [ ] **Logs viewer**: Vedi log completi inline senza aprire terminal
- [ ] **Performance graphs**: Grafici storici CPU/RAM
- [ ] **Auto-fix suggestions**: AI suggerisce fix per problemi comuni
- [ ] **Project templates**: Clona struttura progetto esistente
- [ ] **Backup/Restore**: Esporta/importa setup completo

---

## 🎮 Shortcuts & Tips

### Keyboard Shortcuts (Desktop)

- `Ctrl + N` → Nuovo progetto
- `Ctrl + F` → Focus su search
- `Ctrl + R` → Refresh tutti i progetti
- `Ctrl + 1-4` → Cambia filtro

### Pro Tips

**1. Naming convention:**
Usa nomi descrittivi per riconoscere subito i progetti:
- ✅ `TauroBot-Prod`
- ✅ `Portfolio-v2-React`
- ✅ `MLModel-ImageClassifier`
- ❌ `bot`
- ❌ `test`

**2. Health monitoring:**
Fai pull dal Garage ogni mattina:
- Vedi quali progetti hanno problemi accumulati overnight
- Risolvi prima di iniziare a codare

**3. Resource management:**
Se un progetto usa troppa RAM:
- Il Garage te lo segnala
- Ferma i progetti che non usi
- Libera risorse per quelli attivi

**4. Use tags/emojis:**
Aggiungi emoji nei nomi per categorizzare:
- 🤖 Bot
- 🌐 Web
- 🔌 API
- 🧠 ML
- 🧪 Test

---

## 📊 Metrics & Analytics

### Stats Tracked

**Per progetto:**
- Total uptime (lifetime)
- Crash count
- Average CPU usage
- Peak RAM usage
- Problems detected (historical)
- Last accessed timestamp

**Globali:**
- Total projects managed
- Total problems fixed
- Average health score trend
- Most used project type

### Example Dashboard

```
╔═══════════════════════════════════════════════╗
║  🚗 Il Garage - Analytics                     ║
╠═══════════════════════════════════════════════╣
║  Progetti gestiti: 12                         ║
║  Problemi risolti (mese): 47                  ║
║  Salute media: 87%                            ║
║  Uptime totale: 234h 12m                      ║
║                                               ║
║  Top 3 progetti più usati:                    ║
║  1. TauroBot (89h)                            ║
║  2. WebApp (56h)                              ║
║  3. API (34h)                                 ║
╚═══════════════════════════════════════════════╝
```

---

## 🔐 Security & Privacy

### Data Storage

✅ **100% Local:** Tutti i dati in `localStorage`
✅ **Zero server:** Nessuna chiamata a backend esterni
✅ **No tracking:** Nessuna analytics esterna
✅ **Offline-first:** Funziona senza internet

### Sensitive Data

**Non memorizzare nel Garage:**
- ❌ Password o token
- ❌ API keys
- ❌ Credenziali database

**Il Garage salva solo:**
- ✅ Path dei progetti
- ✅ Comandi di start (pubblici)
- ✅ URL locali
- ✅ Metriche di performance

---

## 📄 Licenza

MIT - Fai quello che vuoi! 🎉

---

**TL;DR:**
Il Garage è come "Task Manager" di Windows, ma per i tuoi progetti di sviluppo.
Vedi tutto, controlli tutto, risolvi tutto. Da un unico posto. 🚗💨

---

*Built with 💰 for developers with too many side projects*
*Compatible with: Chrome, Firefox, Safari, Edge, Android WebView*
*Works offline via Service Worker*

**Hai un garage pieno di progetti? Ora hai il Garage per organizzarli!** 🛠️✨
