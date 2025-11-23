# 🚀 Deploy TauroBot Online - Guida Completa

**Rendi TauroBot accessibile da OVUNQUE con un link pubblico!**

---

## 🎯 Metodi Disponibili

| Metodo | Costo | Velocità | URL Fisso | Difficoltà |
|--------|-------|----------|-----------|------------|
| **Cloudflare Tunnel** | 🆓 GRATIS | ⚡⚡⚡ | ❌ Cambia | ⭐ Facilissimo |
| **Ngrok Free** | 🆓 GRATIS | ⚡⚡ | ❌ Cambia | ⭐⭐ Facile |
| **Ngrok Pro** | 💰 $8/mese | ⚡⚡⚡ | ✅ Permanente | ⭐⭐ Facile |
| **Vercel/Netlify** | 🆓 GRATIS | ⚡⚡⚡ | ✅ Permanente | ⭐⭐⭐ Medio |
| **VPS Custom** | 💰 $5-10/mese | ⚡⚡⚡ | ✅ Permanente | ⭐⭐⭐⭐ Avanzato |

---

## 🆓 Metodo 1: Cloudflare Tunnel (CONSIGLIATO!)

**✅ Vantaggi:**
- Completamente GRATIS
- Nessun limite di traffico
- HTTPS automatico
- Velocissimo (CDN globale)
- Un solo comando!

**❌ Svantaggi:**
- URL cambia ad ogni riavvio (tipo: `abc123.trycloudflare.com`)

### 🚀 Deploy ONE CLICK

```bash
./deploy_online.sh
# Scegli opzione 1 (Cloudflare Tunnel)
```

**Fatto!** In 30 secondi hai il link pubblico! 🎉

### Output Esempio:
```
╔════════════════════════════════════════════════════╗
║           🎉 DEPLOY COMPLETATO! 🎉                 ║
╚════════════════════════════════════════════════════╝

🌐 Il tuo TauroBot è online su:

   https://abc123-def456.trycloudflare.com

📱 Link diretti:
   Login:     https://abc123-def456.trycloudflare.com/pwa/login.html
   🚗 Garage: https://abc123-def456.trycloudflare.com/pwa/garage.html
   Dashboard: https://abc123-def456.trycloudflare.com/pwa/dashboard.html
   Admin:     https://abc123-def456.trycloudflare.com/android/admin.html

✅ Accessibile da QUALSIASI dispositivo nel mondo!
✅ Connessione sicura HTTPS automatica!
✅ Completamente GRATUITO!
```

### Deploy Permanente (24/7):

Se vuoi che rimanga online anche dopo il riavvio:

```bash
./deploy_permanent.sh
```

Questo:
- Configura systemd service (Linux) o LaunchDaemon (macOS)
- Avvio automatico al boot
- Restart automatico se crasha
- Tunnel sempre attivo

**Nota:** L'URL cambia comunque ad ogni riavvio del server. Per URL fisso → vedi Ngrok Pro o VPS.

---

## 🆓 Metodo 2: Ngrok Free

**✅ Vantaggi:**
- Gratis
- Interfaccia web di monitoring

**❌ Svantaggi:**
- Limite 40 connessioni/minuto
- Timeout dopo 2 ore
- URL cambia ad ogni avvio

### Setup:

```bash
./deploy_online.sh
# Scegli opzione 2 (Ngrok Free)
```

**Primo avvio:**
1. Vai su https://dashboard.ngrok.com/signup
2. Registrati (gratis)
3. Copia il tuo authtoken
4. Incollalo quando richiesto

**Fatto!**

---

## 💰 Metodo 3: Ngrok Pro (URL Fisso)

**Prezzo:** $8/mese (o $96/anno con sconto)

**✅ Vantaggi:**
- **URL permanente** personalizzato (es: `taurobot.ngrok.io`)
- Nessun limite di connessioni
- Nessun timeout
- IP whitelisting
- Autenticazione integrata
- Support professionale

### Setup:

1. **Sottoscrivi piano Pro:**
   - Vai su https://dashboard.ngrok.com/billing/subscription
   - Scegli "Pro" → $8/mese
   - Configura pagamento

2. **Configura dominio custom:**
   - Dashboard → Domains → Reserve Domain
   - Scegli: `tuonome.ngrok.io`

3. **Deploy:**
   ```bash
   ./deploy_online.sh
   # Scegli opzione 3 (Ngrok Pro)
   # Inserisci il tuo dominio custom
   ```

**Risultato:**
```
https://taurobot.ngrok.io  ← URL PERMANENTE!
```

Non cambia MAI, anche dopo riavvio! 🎯

---

## 🌐 Metodo 4: Vercel/Netlify (Solo PWA)

**GRATIS per sempre!**

**✅ Vantaggi:**
- Hosting gratuito illimitato
- CDN globale ultra-veloce
- HTTPS automatico
- Dominio custom gratis (tipo: `taurobot.vercel.app`)
- Deploy automatico da GitHub

**❌ Svantaggi:**
- Solo frontend (PWA)
- Il bot Telegram deve girare ancora sul tuo PC

### Setup Vercel:

```bash
# 1. Installa Vercel CLI
npm install -g vercel

# 2. Deploy
./deploy_online.sh
# Scegli opzione 4 (Vercel)

# 3. Login con GitHub
# Follow prompts
```

**Risultato:**
- PWA online su: `https://taurobot-xyz.vercel.app`
- Il Garage, Dashboard, ecc. accessibili pubblicamente
- Il bot Telegram gira ancora sul tuo PC (usa Cloudflare Tunnel separato)

### Setup Netlify (alternativa):

```bash
# Installa Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod

# Follow prompts
```

**Domain Custom:**

Su Vercel/Netlify puoi collegare il TUO dominio:
- Compri dominio su Namecheap (~$10/anno)
- Lo colleghi a Vercel/Netlify (gratis)
- Risultato: `https://taurobot.tuodominio.com`

---

## 🖥️ Metodo 5: VPS (Controllo Totale)

**Per chi vuole il massimo controllo.**

**Prezzo:** $5-10/mese
- DigitalOcean Droplet: $6/mese
- Linode: $5/mese
- Hetzner: €4/mese
- Railway: Free tier (poi $5/mese)

**✅ Vantaggi:**
- Controllo totale
- IP fisso permanente
- Dominio custom
- Ollama gira sul server (non serve PC sempre acceso)
- Backup automatici

**❌ Svantaggi:**
- Richiede conoscenze Linux
- Setup più complesso
- Manutenzione periodica

### Setup VPS (DigitalOcean esempio):

**1. Crea Droplet:**
```
- Vai su digitalocean.com
- Create → Droplets
- Scegli: Ubuntu 22.04, Basic $6/mese, 1GB RAM
- Create Droplet
```

**2. SSH nel server:**
```bash
ssh root@your_droplet_ip
```

**3. Installa TauroBot:**
```bash
# Clone repo
git clone https://github.com/Lucifer-AI-666/Taurosweb.git
cd Taurosweb

# Installa dipendenze
./start_bot.sh  # Installa tutto automaticamente

# Configura .env con il tuo token

# Avvia permanentemente
./deploy_permanent.sh
```

**4. Dominio (opzionale):**
```
- Compra dominio su Namecheap/Cloudflare
- Aggiungi record DNS:
  Type: A
  Name: @
  Value: your_droplet_ip

- Accedi su: https://tuodominio.com
```

**Costo totale:** $6/mese VPS + $10/anno dominio = ~$7/mese

---

## 📊 Confronto Dettagliato

### Per Uso Personale / Test:

**Cloudflare Tunnel** 🏆
- Gratis
- Veloce
- Zero config
- Perfetto per test/sviluppo

### Per Condividere con Amici:

**Ngrok Free** 🏆
- Gratis
- Facile condividere link
- Va bene per sessioni brevi

### Per Uso Professionale:

**Ngrok Pro** 🏆
- $8/mese
- URL permanente
- Affidabile

### Per Portfolio / Demo:

**Vercel** 🏆
- Gratis
- Bellissimo dominio
- Deploy da GitHub

### Per Produzione 24/7:

**VPS** 🏆
- $6/mese
- Massima affidabilità
- Controllo totale

---

## 🔒 Sicurezza

### Cloudflare Tunnel / Ngrok:

✅ **Sicuro di default:**
- Traffic criptato end-to-end
- Nessuna porta aperta sul router
- Protezione DDoS automatica

⚠️ **Ricorda:**
- Usa password forti sul login PWA
- Attiva 2FA se disponibile
- Non condividere il link pubblicamente

### Vercel / Netlify:

✅ **Molto sicuro:**
- Solo file statici (HTML/CSS/JS)
- Nessun backend esposto
- CDN con protezione DDoS

### VPS:

⚠️ **Richiede setup sicurezza:**
```bash
# Firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Fail2ban (protezione brute force)
sudo apt install fail2ban

# SSL con Let's Encrypt
sudo certbot --nginx -d tuodominio.com
```

---

## 💡 Raccomandazioni

### Scenario: "Voglio solo testare"
→ **Cloudflare Tunnel** (opzione 1)
- Tempo: 30 secondi
- Costo: $0

### Scenario: "Uso quotidiano per me"
→ **Cloudflare Tunnel Permanente**
- Tempo: 2 minuti
- Costo: $0

### Scenario: "Condivido con team/amici"
→ **Ngrok Pro**
- Tempo: 5 minuti
- Costo: $8/mese

### Scenario: "Portfolio professionale"
→ **Vercel + Dominio Custom**
- Tempo: 10 minuti
- Costo: $10/anno (solo dominio)

### Scenario: "Startup / Business"
→ **VPS + Dominio**
- Tempo: 30 minuti
- Costo: ~$7/mese

---

## 🚨 Troubleshooting

### Problema: "URL non funziona"

**Cloudflare Tunnel:**
```bash
# Check se il tunnel è attivo
ps aux | grep cloudflared

# Vedi log
tail -f /tmp/tauro_tunnel.log

# Riavvia
pkill cloudflared
cloudflared tunnel --url http://localhost:8000
```

**Ngrok:**
```bash
# Check se ngrok è attivo
ps aux | grep ngrok

# Apri dashboard web
http://localhost:4040

# Riavvia
pkill ngrok
ngrok http 8000
```

### Problema: "502 Bad Gateway"

Il server locale non risponde:
```bash
# Check se HTTP server gira
ps aux | grep "http.server"

# Se no, avvialo
python3 -m http.server 8000
```

### Problema: "Connection timeout"

Firewall che blocca:
```bash
# Linux - disabilita firewall temporaneamente
sudo ufw disable

# Se risolve, apri solo porta 8000
sudo ufw allow 8000/tcp
sudo ufw enable
```

---

## 📱 Accesso da Smartphone

Dopo il deploy, dal telefono:

1. Apri browser (Chrome, Safari)
2. Vai su: `https://tuo-url-pubblico/pwa/login.html`
3. **Aggiungi a Home Screen** (PWA):
   - iPhone: Condividi → Aggiungi a Home
   - Android: Menu → Installa app

Ora hai l'app TauroBot sul telefono! 📱✨

---

## 🎓 Best Practices

### 1. **Backup prima di deploy:**
```bash
# Backup configurazione
cp .env .env.backup
cp -r memory memory_backup
```

### 2. **Usa HTTPS sempre:**
- Cloudflare/Ngrok lo fanno automaticamente
- Su VPS, usa Let's Encrypt

### 3. **Monitora risorse:**
```bash
# CPU/RAM usage
htop

# Log errori
tail -f logs/bot.log
```

### 4. **Update regolari:**
```bash
git pull
pip install -r requirements.txt --upgrade
```

---

## 💰 Costi Riepilogo

| Soluzione | Setup | Mensile | Annuale | Totale 1° Anno |
|-----------|-------|---------|---------|----------------|
| Cloudflare Tunnel | $0 | $0 | $0 | **$0** 🏆 |
| Ngrok Free | $0 | $0 | $0 | **$0** 🏆 |
| Ngrok Pro | $0 | $8 | $96 | **$96** |
| Vercel + Dominio | $10 | $0 | $10 | **$20** 🏆 |
| VPS + Dominio | $10 | $6 | $72 | **$82** |

**Consiglio:** Inizia con Cloudflare Tunnel (gratis). Se ti serve URL permanente, passa a Ngrok Pro o VPS.

---

## 🎯 Quick Start

**Più facile in assoluto:**

```bash
# 1. Deploy ONE CLICK
./deploy_online.sh

# 2. Scegli opzione 1 (Cloudflare)

# 3. Aspetta 30 secondi

# 4. Copia il link che ti dà

# 5. Apri dal telefono → Done! 🎉
```

**Tempo totale:** 1 minuto

---

## 📞 Supporto

**Problemi con deploy?**

1. Controlla i log: `tail -f /tmp/tauro_tunnel.log`
2. Riavvia tutto: `pkill cloudflared && ./deploy_online.sh`
3. Apri Issue su GitHub con log completi

**Domande frequenti?** Leggi `GUIDA_SEMPLICE.md`

---

**Creato per rendere TauroBot accessibile OVUNQUE! 🌍**

**Versione:** 3.0.0-garage
**Data:** Novembre 2025

🐂 **Da localhost al mondo intero in 30 secondi!** 🚀
