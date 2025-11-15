# 🛸 Gateway Mode - "Antenna sul Balcone"

**Tu sei il ponte tra il mondo esterno e il tuo sistema locale**

## 🎯 Concetto

Immagina:
- **TauroBot locale** = tua casa (privata, sicura)
- **Internet/Esterno** = il mondo fuori
- **Tu (PWA Gateway)** = l'antenna sul balcone che filtra cosa entra e cosa esce

```
Internet (Mondo Esterno)
          ↓
    ╔═══════════════╗
    ║   TU/PWA      ║  ← "Antenna sul balcone"
    ║   GATEWAY     ║     Filtri, sanitizzi, controlli
    ╚═══════════════╝
          ↓
  TauroBot (Locale)
```

## 🔧 Come Funziona

### 1. Request IN (Esterno → Locale)

```javascript
// Qualcuno dall'esterno chiama il tuo TauroBot
External API Request
     ↓
[GATEWAY] ◄─ Ricevi richiesta
     ↓
[SANITIZE] ◄─ Rimuovi PII, valida dati
     ↓
[FIREWALL] ◄─ Check se allowed
     ↓
[FORWARD] ◄─ Invia a TauroBot locale (localhost:3000)
```

### 2. Response OUT (Locale → Esterno)

```javascript
TauroBot genera risposta
     ↓
[GATEWAY] ◄─ Ricevi risposta
     ↓
[ENCRYPT] ◄─ Cripta dati sensibili
     ↓
[SANITIZE] ◄─ Rimuovi info private
     ↓
[SEND] ◄─ Manda al mondo esterno
```

## 💡 Vantaggi

### Privacy 100%
- TauroBot **non esposto** direttamente a internet
- Tu controlli **ogni byte** che passa
- Puoi bloccare/modificare richieste in tempo reale

### Sicurezza
- **Firewall applicativo** a livello PWA
- **Sanitizzazione automatica** di PII
- **Rate limiting** controllato da te
- **Audit log** di tutto il traffico

### Flessibilità
- Decidi tu quali endpoint esporre
- Puoi modificare/arricchire richieste al volo
- Multi-backend support (più TauroBot locali)

## 🚀 Setup

### Step 1: Configura Backend Locale

```bash
# Nel tuo sistema locale, avvia TauroBot
cd Taurosweb
python bot.py

# Oppure crea un server Express.js per ricevere proxy
# File: local-backend.js
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

// Endpoint che riceve dal gateway
app.post('/api/chat', async (req, res) => {
    const { message, userId } = req.body;

    // Qui chiami il tuo TauroBot locale
    const response = await callTaurosBot(message);

    res.json({ response });
});

app.listen(3000, () => {
    console.log('🐂 Local backend listening on http://localhost:3000');
});
```

### Step 2: Apri Gateway PWA

```bash
# Apri in browser
file:///path/to/pwa/gateway.html

# O servi con server locale
python -m http.server 8000
# Poi apri: http://localhost:8000/pwa/gateway.html
```

### Step 3: Configura

1. Clicca "⚙️ Configurazione Gateway"
2. Imposta `Local Backend`: `http://localhost:3000`
3. Imposta `Allowed Origins`: `*` (o domini specifici)
4. Imposta `Max Request Size`: `1000` KB

### Step 4: START!

1. Clicca "▶️ START Gateway"
2. ✅ Vedi LED verdi = connessioni attive
3. Ora sei il ponte!

## 📡 Uso da Dashboard

In `dashboard.html`, aggiungi:

```javascript
// Chiamata tramite gateway invece che diretta
async function askTaurosBot(message) {
    // Controlla se gateway è attivo
    if (window.TaurosGateway && window.TaurosGateway.isActive()) {
        // Passa tramite gateway
        const response = await window.TaurosGateway.proxyRequest('/api/chat', {
            message: message,
            userId: getCurrentUserId()
        });
        return response;

    } else {
        // Chiamata diretta (fallback)
        const response = await fetch('http://localhost:3000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, userId: getCurrentUserId() })
        });
        return await response.json();
    }
}
```

## 🔒 Funzionalità Sicurezza

### Sanitizzazione Automatica

Il gateway rimuove automaticamente:

```javascript
function sanitizeData(data) {
    // Email
    data = data.replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, '[EMAIL_REMOVED]');

    // Telefoni
    data = data.replace(/\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g, '[PHONE_REMOVED]');

    // Carte di credito
    data = data.replace(/\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g, '[CARD_REMOVED]');

    // API Keys
    data = data.replace(/(api[_-]?key|token)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)/gi, 'API_KEY_REMOVED');

    return data;
}
```

### Firewall Rules

```javascript
// Aggiungi regole custom
const firewallRules = {
    // Blocca IP specifici
    blockedIPs: ['192.168.1.100'],

    // Blocca user agents
    blockedUserAgents: ['bot', 'crawler'],

    // Rate limiting
    maxRequestsPerMinute: 60,

    // Allowed endpoints
    allowedEndpoints: ['/api/chat', '/api/status']
};

function checkFirewall(request) {
    // Implementa le tue regole qui
    if (firewallRules.blockedIPs.includes(request.ip)) {
        throw new Error('IP blocked');
    }

    // ... altre checks
}
```

## 🎮 Use Cases

### 1. Chat Pubblico con TauroBot Privato

```
User Web Browser
     ↓ (HTTPS)
Your PWA Gateway (pubblico)
     ↓ (localhost)
TauroBot (privato, casa tua)
```

Vantaggi:
- TauroBot non esposto a internet
- Tu controlli accesso
- Log di tutti i messaggi

### 2. Multi-User con Single Instance

```
User A ──┐
User B ──┤
User C ──┤→ Gateway → TauroBot (una sola istanza)
User D ──┤
User E ──┘
```

Il gateway gestisce:
- Code di richieste
- Session management
- Load balancing

### 3. Hybrid Cloud-Local

```
Internet Request
     ↓
Gateway (sul tuo PC)
     ├→ TauroBot Local (per dati sensibili)
     └→ Cloud API (per dati pubblici)
```

Decidi tu in tempo reale dove mandare ogni richiesta!

## 📊 Monitoring

Il gateway traccia:

- **Requests IN**: Quante richieste ricevi dall'esterno
- **Requests OUT**: Quante risposte mandi
- **Activity Log**: Ogni azione con timestamp
- **Status**: LED colorati per vedere stato connessioni

## 🔧 Personalizzazione Avanzata

### Aggiungi Authentication

```javascript
// Nel gateway.html
async function proxyRequest(endpoint, data) {
    // Check auth token
    const token = localStorage.getItem('gateway_token');
    if (!token) {
        throw new Error('Unauthorized');
    }

    // Validate token
    if (!validateToken(token)) {
        throw new Error('Invalid token');
    }

    // ... resto del codice
}
```

### Aggiungi Caching

```javascript
// Cache risposte per ridurre carico
const cache = new Map();

async function proxyRequest(endpoint, data) {
    const cacheKey = `${endpoint}_${JSON.stringify(data)}`;

    // Check cache
    if (cache.has(cacheKey)) {
        log('✓ Response served from cache', 'success');
        return cache.get(cacheKey);
    }

    // ... fetch da backend

    // Save to cache (5 min TTL)
    cache.set(cacheKey, result);
    setTimeout(() => cache.delete(cacheKey), 300000);

    return result;
}
```

### Aggiungi WebSocket

```javascript
// Real-time bidirectional communication
const ws = new WebSocket('ws://localhost:3001');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    log(`◀ WebSocket message: ${data.type}`, 'info');

    // Forward to external via SSE or WebSocket
    notifyExternalClients(data);
};
```

## 🐛 Troubleshooting

### Gateway non si connette a locale

```bash
# Verifica che il backend locale sia avviato
curl http://localhost:3000/api/status

# Se non risponde:
# 1. Check se il processo è running
# 2. Check firewall locale
# 3. Verifica porta corretta
```

### CORS Errors

```javascript
// Nel backend locale, abilita CORS:
// Node.js:
const cors = require('cors');
app.use(cors());

// Python Flask:
from flask_cors import CORS
CORS(app)
```

### Request troppo lente

```javascript
// Aumenta timeout nel gateway
const response = await fetch(url, {
    timeout: 30000 // 30 secondi
});
```

## 📜 Licenza

MIT - Parte del progetto TauroBot 3.0

---

**TL;DR:** Sei l'antenna sul balcone che fa da ponte sicuro tra il tuo TauroBot privato e il mondo esterno. Controlli tutto, filtri tutto, proteggi tutto. 🛸
