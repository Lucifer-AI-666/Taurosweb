# 📱 TauroBot Android - APK Esclusiva

**App Android per controllare TauroBot da ovunque nel mondo** 🌍

> Perché anche chi ha i soldini merita di controllare il proprio bot da smartphone! 💰📱

---

## 🎯 Il Concetto

**TU ovunque** → **Smartphone Android** → **TauroBot a casa**

```
┌──────────────────┐
│   Tu in giro     │
│   📱 Android     │
└────────┬─────────┘
         │ 4G/5G/WiFi
         ▼
    ┌────────────┐
    │  Internet  │
    └─────┬──────┘
          │
          ▼
  ┌───────────────┐
  │ Casa tua      │
  │ 💻 TauroBot   │
  │ 🤖 Bot attivo │
  └───────────────┘
```

**Cosa puoi fare dall'app:**
- ✅ Avviare/fermare il bot
- ✅ Vedere log in tempo reale
- ✅ Modificare configurazioni
- ✅ Esportare/importare database
- ✅ Terminal SSH completo
- ✅ Aggiornare da GitHub
- ✅ Monitorare stats (CPU, RAM, uptime)

---

## 🚀 Build APK (Sul Tuo PC)

### Requisiti

**Software necessari:**
- Node.js 16+ (https://nodejs.org)
- Java JDK 11+
- Android SDK (o Android Studio)
- Git

**Verifica installazione:**
```bash
node --version   # v16.x o superiore
java --version   # 11.x o superiore
echo $ANDROID_HOME  # Path all'SDK Android
```

### Step 1: Setup Android SDK

**Opzione A: Android Studio (Consigliato)**
1. Scarica Android Studio: https://developer.android.com/studio
2. Installa e apri
3. SDK Manager → Install:
   - Android SDK Platform 33
   - Android SDK Build-Tools 33.0.0
   - Android SDK Platform-Tools

**Opzione B: Solo SDK Tools**
```bash
# Linux/macOS
wget https://dl.google.com/android/repository/commandlinetools-linux-latest.zip
unzip commandlinetools-linux-latest.zip -d ~/android-sdk
export ANDROID_HOME=~/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/bin

# macOS (Homebrew)
brew install android-sdk
```

**Aggiungi al PATH:**
```bash
# Aggiungi a ~/.bashrc o ~/.zshrc
export ANDROID_HOME=~/Android/Sdk  # O il tuo path
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin

# Ricarica
source ~/.bashrc  # o source ~/.zshrc
```

### Step 2: Install Dependencies

```bash
cd Taurosweb/android
npm install
```

### Step 3: Build!

**Debug APK (per testare):**
```bash
./build_apk.sh
# Scegli opzione 1 (Debug)
```

**Release APK (per distribuzione):**
```bash
./build_apk.sh
# Scegli opzione 2 (Release)
```

**Output:**
```
✅ APK pronta in:
   android/app/build/outputs/apk/debug/app-debug.apk  (DEBUG)
   android/app/build/outputs/apk/release/TauroBot-v3.0.0-release.apk  (RELEASE)
```

---

## 📲 Installazione su Android

### Metodo 1: USB (Più veloce)

```bash
# Connetti telefono via USB
# Attiva "Debug USB" nelle Impostazioni Developer

# Verifica connessione
adb devices
# List of devices attached
# 1234567890ABCDEF    device

# Installa APK
adb install android/app/build/outputs/apk/debug/app-debug.apk

# ✅ App installata!
```

### Metodo 2: Download Diretto

1. Copia APK su Google Drive / Dropbox
2. Apri link da telefono Android
3. Scarica APK
4. Apri file → "Installa" (permetti "Fonti sconosciute")
5. ✅ App installata!

### Metodo 3: QR Code

```bash
# Genera QR code con link APK
npm install -g qrcode-terminal
qrcode-terminal "http://tuo-server.com/app.apk"

# Scansiona con telefono → Download → Installa
```

---

## 🌍 Setup Accesso Remoto

**Per collegarti da ovunque, serve esporre il tuo TauroBot locale a internet.**

### Opzione 1: Ngrok (Più facile, gratis per uso personale)

**Sul PC dove gira TauroBot:**

```bash
# Installa ngrok
# Linux/macOS:
brew install ngrok
# O scarica da: https://ngrok.com/download

# Registrati su ngrok.com e ottieni auth token

# Avvia tunnel
ngrok http 3000

# Output:
# Forwarding  https://abc123.ngrok.io -> http://localhost:3000
```

**Nell'app Android:**
- Host: `abc123.ngrok.io`
- Porta: `443` (HTTPS)
- ✅ Connesso!

**⚠️ Limitazione:** URL cambia ad ogni restart (gratis). URL fisso = piano a pagamento ($8/mese).

### Opzione 2: Cloudflare Tunnel (Gratis, URL fisso!)

```bash
# Installa cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Login
cloudflared tunnel login

# Crea tunnel
cloudflared tunnel create taurobot
# Output: Tunnel ID: 12345-67890-...

# Configura
cat > ~/.cloudflared/config.yml <<EOF
tunnel: 12345-67890-...
credentials-file: ~/.cloudflared/12345-67890-....json

ingress:
  - hostname: taurobot.tuodominio.com
    service: http://localhost:3000
  - service: http_status:404
EOF

# Avvia tunnel
cloudflared tunnel run taurobot

# ✅ Ora raggiungibile da: https://taurobot.tuodominio.com
```

**Nell'app Android:**
- Host: `taurobot.tuodominio.com`
- Porta: `443`
- ✅ Connesso da ovunque!

### Opzione 3: Port Forwarding Router (Se hai IP pubblico)

**Sul router di casa:**
1. Accedi a pannello router (es: 192.168.1.1)
2. Trova "Port Forwarding" / "NAT"
3. Crea regola:
   - Porta esterna: `8080`
   - Porta interna: `3000`
   - IP: `192.168.1.X` (IP del PC con TauroBot)
4. Salva

**Trova IP pubblico:**
```bash
curl ifconfig.me
# Es: 93.45.123.45
```

**Nell'app Android:**
- Host: `93.45.123.45`
- Porta: `8080`
- ✅ Connesso!

**⚠️ Sicurezza:** Aggiungi autenticazione (password nell'app) o usa VPN!

### Opzione 4: VPN (Più sicuro)

**Setup WireGuard sul PC:**
```bash
sudo apt install wireguard

# Genera chiavi
wg genkey | tee privatekey | wg pubkey > publickey

# Configura
sudo nano /etc/wireguard/wg0.conf
```

**Configura VPN su Android:**
1. Installa WireGuard app
2. Importa configurazione
3. Connetti VPN
4. Ora puoi usare IP locale (192.168.1.X) nell'app!

---

## 🎮 Uso dell'App

### Admin Panel

Apri app → **Admin Panel**

**Funzionalità:**
- 📊 Status: Bot online/offline, uptime, stats
- ⚡ Quick Actions: Start/Stop/Restart bot
- ⚙️ Config: Cambia model Ollama, abilita voice
- 📋 Logs: Vedi log in tempo reale
- 💾 Database: Export/import dati
- 🔄 Updates: Pull da GitHub, check updates

### Terminal Remoto

Apri app → **Terminal**

**Comandi utili:**
```bash
# Status bot
status

# Avvia bot
python bot.py &

# Ferma bot
pkill -f bot.py

# Vedi log live
tail -f logs/bot.log

# Spazio disco
df -h

# RAM libera
free -h

# Processi
ps aux

# Aggiorna da Git
git pull

# Restart server
sudo reboot
```

**Quick Commands:**
- Tap su bottoni per comandi rapidi
- Scrivi comando custom e premi ▶️

### Il Garage - Project Manager

Apri app → **Il Garage** 🚗

**La tua officina per gestire TUTTI i progetti:**
- 📊 Dashboard unificata: Vedi tutti i tuoi progetti in un colpo d'occhio
- 🚀 Multi-project support: Non solo TauroBot, aggiungi qualsiasi progetto!
- ⚠️ Problem detection: Rileva problemi automaticamente (test falliti, dipendenze obsolete, memoria alta)
- 💻 Quick access: Apri terminal e admin panel per ogni progetto
- 📈 Health monitoring: Ogni progetto ha uno score di salute in tempo reale
- ⏱️ Real-time stats: CPU, RAM, uptime per ogni progetto
- 🎯 Direct navigation: Vai direttamente al file/linea con il problema

**Tipi di progetti supportati:**
- 🤖 Telegram Bot
- 🌐 Web App
- 🔌 REST API
- 🧠 Machine Learning
- 📦 Qualsiasi altro progetto

**Come funziona:**
1. Apri "Il Garage" dalla dashboard o admin panel
2. TauroBot è già presente di default
3. Clicca "➕ Aggiungi Nuovo Progetto"
4. Inserisci: nome, tipo, path, comando di start
5. Boom! 💥 Il tuo progetto appare nella griglia
6. Monitora salute, problemi, e controlla tutto da un unico posto

**Auto-scanning intelligente:**
- Ogni 30 secondi il Garage scansiona tutti i progetti
- Rileva problemi comuni (memoria elevata, test falliti, vulnerabilità)
- Ti porta direttamente al file/linea del problema
- Suggerisce il fix da applicare

**Filters:**
- 📁 Tutti i progetti
- ▶️ Solo quelli in esecuzione
- ⚠️ Solo quelli con problemi
- ✅ Solo quelli "healthy" (salute >80%)

**Example workflow:**
```
1. Hai 5 progetti: TauroBot, WebApp, API, MLModel, TestBot
2. Il Garage rileva che TestBot ha 3 test falliti
3. Clicchi sul problema → Ti dice: test_api.py:78
4. Clicchi "Vai al Fix" → Apre il file
5. Risolvi il bug
6. Health score sale da 60% a 100% ✅
```

**💡 Pro tip:** Usa il Garage come "mission control" per tutti i tuoi side projects!

---

## 🔒 Sicurezza

### Protezione Base

**Nell'app, usa password forte:**
```bash
# In terminal remoto, crea utente dedicato
sudo useradd -m taurobot-remote
sudo passwd taurobot-remote
# Inserisci password complessa
```

### HTTPS (Obbligatorio se esponi a internet)

**Con Ngrok:** HTTPS automatico ✅

**Con Cloudflare:** HTTPS automatico ✅

**Con Port Forwarding:** Usa Caddy reverse proxy:

```bash
# Installa Caddy
sudo apt install caddy

# Configura
sudo nano /etc/caddy/Caddyfile
```

```
taurobot.tuodominio.com {
    reverse_proxy localhost:3000
}
```

```bash
sudo systemctl restart caddy
# ✅ HTTPS automatico con Let's Encrypt!
```

### Firewall

```bash
# Permetti solo porte necessarie
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 3000/tcp # TauroBot (solo se port forwarding)
sudo ufw enable
```

### Autenticazione App

**Nell'app, abilita password:**
- Settings → Require Password: ON
- Ogni volta che apri app = chiedi password

---

## 🎨 Personalizzazione APK

### Cambia Icona

```bash
# Sostituisci icone in:
android/app/src/main/res/
├── mipmap-hdpi/ic_launcher.png     (72x72)
├── mipmap-mdpi/ic_launcher.png     (48x48)
├── mipmap-xhdpi/ic_launcher.png    (96x96)
├── mipmap-xxhdpi/ic_launcher.png   (144x144)
└── mipmap-xxxhdpi/ic_launcher.png  (192x192)
```

### Cambia Nome App

**In `capacitor.config.json`:**
```json
{
  "appName": "Il Mio TauroBot Pro",
  "appId": "com.miodominio.taurobot"
}
```

### Cambia Colori

**In `android/app/src/main/res/values/colors.xml`:**
```xml
<color name="colorPrimary">#667eea</color>
<color name="colorAccent">#764ba2</color>
```

### Rebuild dopo modifiche

```bash
./build_apk.sh
```

---

## 🐛 Troubleshooting

### "ANDROID_HOME not set"

```bash
export ANDROID_HOME=~/Android/Sdk
# Aggiungi a ~/.bashrc per permanente
```

### "adb: command not found"

```bash
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

### "Gradle build failed"

```bash
# Pulisci cache
cd android
./gradlew clean

# Rebuild
./gradlew assembleDebug
```

### "Device unauthorized"

```bash
# Su telefono: "Autorizza debug USB" → OK
# Poi:
adb kill-server
adb start-server
adb devices
```

### App crasha all'avvio

```bash
# Vedi log Android
adb logcat | grep TauroBot

# O in Android Studio:
# View → Tool Windows → Logcat
```

### Non si connette da remoto

1. ✅ Tunnel/VPN attivo?
   ```bash
   curl http://localhost:3000  # Sul server
   curl https://abc123.ngrok.io  # Da fuori
   ```

2. ✅ Firewall?
   ```bash
   sudo ufw status
   # Se 3000 bloccata: sudo ufw allow 3000
   ```

3. ✅ Bot running?
   ```bash
   ps aux | grep bot.py
   ```

---

## 📊 Performance

**Dimensione APK:**
- Debug: ~8 MB
- Release (minified): ~5 MB

**Requisiti Android:**
- Android 6.0+ (API 23)
- RAM: 100MB
- Storage: 20MB

**Consumi:**
- Standby: <1% batteria/ora
- Uso attivo: ~5% batteria/ora
- Dati: ~1MB/sessione

---

## 🚀 Features Roadmap

- [ ] Notifiche push per eventi bot
- [ ] Widget home screen (stats bot)
- [ ] Dark mode
- [ ] Multi-bot support
- [ ] Backup automatico su cloud
- [ ] Fingerprint/Face unlock
- [ ] Export logs in PDF
- [ ] Chat diretta con bot dall'app

---

## 💎 Pro Tips

### Avvio Automatico Bot su Server

**Crea systemd service:**

```bash
sudo nano /etc/systemd/system/taurobot.service
```

```ini
[Unit]
Description=TauroBot 3.0
After=network.target

[Service]
Type=simple
User=tuo-user
WorkingDirectory=/home/tuo-user/Taurosweb
ExecStart=/usr/bin/python3 /home/tuo-user/Taurosweb/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable taurobot
sudo systemctl start taurobot

# ✅ Bot parte all'avvio del server!
```

### Notifiche Android Quando Bot Va Offline

**Installa monitoring script:**

```bash
# Script che controlla ogni 5 min
*/5 * * * * curl http://localhost:3000 || curl -X POST "https://api.pushover.net/1/messages.json" --data "token=YOUR_TOKEN&user=YOUR_USER&message=TauroBot offline!"
```

### Accesso SSH dall'App

**Installa Termux sul telefono:**
1. Installa Termux da F-Droid
2. `pkg install openssh`
3. `ssh user@tuo-server.com`
4. Controllo completo via SSH!

---

## 📄 Licenza

MIT - Fai quello che vuoi! 🎉

---

**TL;DR:**
1. `cd android && ./build_apk.sh`
2. Installa APK su telefono
3. Setup ngrok/cloudflare per accesso remoto
4. Apri app → Connetti → Controlla bot da ovunque! 🌍

**Hai i soldini? Hai anche il controllo totale!** 💰📱✨

---

*Built with 💰 for premium users*
*Android 6.0+ compatible*
*Open source, auditable, privacy-first*
