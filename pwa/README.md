# 📱 TauroBot 3.0 - Progressive Web App

**PWA con autenticazione locale e integrazione Hybrid Security**

## 🚀 Caratteristiche

### ✅ Privacy-First Authentication
- **100% Locale:** Credenziali salvate solo su `localStorage` del tuo dispositivo
- **SHA-256 Hashing:** Password hashate con crypto browser-native
- **Zero Server:** Nessuna chiamata a server esterni per login/registrazione
- **Session Management:** Sessioni valide 24 ore con `sessionStorage`

### 🔒 Security Features
- Service Worker per funzionamento offline
- HTTPS required (per PWA standard)
- Password minimum 6 caratteri
- Username minimum 3 caratteri
- Auto-logout dopo 24h

### 🎨 UI/UX
- Design moderno con gradients
- Animazioni fluide
- Responsive (mobile-first)
- Dark mode ready
- Installabile come app nativa

## 📂 Struttura File

```
pwa/
├── login.html       # Pagina login/registrazione
├── dashboard.html   # Dashboard utente autenticato
└── README.md        # Questa documentazione
```

## 🛠️ Installazione

### 1. Servi con HTTPS

**Opzione A: GitHub Pages (Consigliato)**
```bash
# Push su GitHub
git push origin main

# Abilita GitHub Pages nelle Settings
# Pages → Source → main branch → /root
```

**Opzione B: Server locale con HTTPS**
```bash
# Con Python
python -m http.server 8000 --bind localhost

# O con npx http-server
npx http-server -p 8000 --ssl
```

### 2. Apri nel Browser

```
https://your-domain.github.io/pwa/login.html
```

### 3. Installa PWA

**Su Desktop:**
- Chrome/Edge: Icona "Installa" nella barra URL
- Firefox: Menu → "Installa come app"

**Su Mobile (Android/iOS):**
- Chrome Android: Menu → "Aggiungi a schermata Home"
- Safari iOS: Condividi → "Aggiungi a Home"

## 🔐 Come Funziona l'Autenticazione

### Registrazione

```javascript
// 1. Utente inserisce username e password
username: "mario"
password: "secret123"

// 2. Password viene hashata con SHA-256
passwordHash = sha256("secret123")
// → "2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b"

// 3. Dati salvati in localStorage
localStorage.setItem('taurobot_user_mario', {
  username: "mario",
  passwordHash: "2bb80d537...",
  createdAt: 1700000000000,
  profile: { displayName: "mario", avatar: "🐂" }
})

// ✅ NESSUN dato inviato a server esterni!
```

### Login

```javascript
// 1. Utente inserisce credenziali
username: "mario"
password: "secret123"

// 2. Hash della password inserita
inputHash = sha256("secret123")

// 3. Confronto con hash salvato
stored = localStorage.getItem('taurobot_user_mario')
if (stored.passwordHash === inputHash) {
  // Login success!

  // 4. Crea sessione temporanea
  sessionStorage.setItem('taurobot_session', {
    username: "mario",
    loginTime: Date.now(),
    token: randomToken()
  })

  // 5. Redirect a dashboard
  window.location.href = "/pwa/dashboard.html"
}
```

### Logout

```javascript
// Rimuove sessione
sessionStorage.removeItem('taurobot_session')

// Redirect a login
window.location.href = "/pwa/login.html"
```

## 📊 Dashboard Features

### Overview Tab
- Tempo sessione attivo
- Status sistemi ibridi (NET'ALIS + NEXUS)
- Privacy score (sempre 10/10!)

### NET'ALIS Tab
- Integrazione con quantum-neural sandbox
- Avvia componente React in sandbox
- Stats real-time

### NEXUS Tab
- Info su Reinforcement Learning
- Privacy Guardian status
- Richiede backend Python (opzionale)

### Activity Tab
- Log attività in tempo reale
- Timestamp di ogni azione
- Ultime 20 attività salvate

## 🔧 Personalizzazione

### Cambiare Avatar

Modifica in `dashboard.html`:

```javascript
const userData = {
  ...
  profile: {
    displayName: username,
    avatar: '🐂'  // <-- Cambia emoji qui
  }
}
```

### Cambiare Tema

Modifica gradients in `login.html` e `dashboard.html`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Cambia con i tuoi colori preferiti */
```

### Estendere Session Timeout

In `dashboard.html`:

```javascript
// Da 24 ore a 7 giorni
if (Date.now() - session.loginTime > 604800000) { // 7 giorni
  ...
}
```

## 🧪 Testing

### Test Registrazione
1. Apri `login.html`
2. Clicca "Registrati"
3. Inserisci:
   - Username: `testuser`
   - Password: `test123`
   - Conferma: `test123`
4. Clicca "Registrati"
5. ✅ Dovresti vedere messaggio di successo

### Test Login
1. Inserisci credenziali create sopra
2. Clicca "Accedi"
3. ✅ Redirect a dashboard

### Test Offline
1. Apri DevTools → Application → Service Workers
2. Spunta "Offline"
3. Ricarica pagina
4. ✅ PWA dovrebbe funzionare da cache

### Test Installazione
1. Desktop Chrome: cerca icona "+" nella barra URL
2. Clicca "Installa"
3. ✅ App si apre in finestra standalone

## 🐛 Troubleshooting

### PWA non si installa
- ✅ Verifica HTTPS attivo
- ✅ Controlla `manifest.json` valido
- ✅ Service Worker registrato correttamente

### Login non funziona
- ✅ Apri DevTools → Console
- ✅ Verifica `localStorage` non pieno (quota ~10MB)
- ✅ Cancella cache e riprova

### Dashboard redirect a login
- ✅ Sessione scaduta (>24h)
- ✅ `sessionStorage` cancellato
- ✅ Rifare login

### Service Worker non aggiorna
```javascript
// In DevTools → Application → Service Workers
// Clicca "Unregister" → Ricarica pagina
```

## 📜 Privacy Policy Template

```markdown
# TauroBot 3.0 PWA - Privacy Policy

## Dati Raccolti
- Username (scelto da te)
- Password (hashata SHA-256, mai in chiaro)

## Dove Sono Salvati
- **localStorage** del TUO browser
- **sessionStorage** del TUO browser
- Zero server remoti

## Condivisione Dati
NESSUNA. I tuoi dati NON lasciano mai il tuo dispositivo.

## Eliminazione Dati
```javascript
// Apri DevTools → Console → Esegui:
localStorage.clear()
sessionStorage.clear()
// Tutti i dati eliminati istantaneamente
```

## Contatti
Per domande: apri issue su GitHub
```

## 🚀 Roadmap

- [ ] Biometric authentication (fingerprint/face ID)
- [ ] Multi-device sync (P2P, no server)
- [ ] Encrypted backup export
- [ ] 2FA locale (TOTP)
- [ ] Dark mode toggle
- [ ] Custom themes
- [ ] PWA push notifications

## 📄 License

MIT - Vedi LICENSE nel root del progetto

## 🤝 Contributing

Contributi benvenuti! Questa PWA è parte del progetto TauroBot 3.0.

---

**Versione:** 2.0.0
**Last Updated:** 2025-11-15
**Status:** ✅ Production Ready
