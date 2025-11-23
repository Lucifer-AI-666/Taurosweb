#!/bin/bash

# 🚀 TauroBot Online Deploy - ONE CLICK MAGIC!
# Rende TauroBot accessibile da QUALSIASI posto con un link pubblico

echo "╔════════════════════════════════════════════════════╗"
echo "║  🚀 TauroBot Online Deploy - ONE CLICK!           ║"
echo "║  Rendi il tuo bot accessibile da OVUNQUE          ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check se siamo nella directory giusta
if [ ! -f "bot.py" ]; then
    echo -e "${RED}❌ Errore: Esegui questo script dalla directory Taurosweb!${NC}"
    exit 1
fi

echo -e "${CYAN}Scegli il metodo di deploy:${NC}"
echo ""
echo "1) 🆓 Cloudflare Tunnel (GRATIS, veloce, sicuro) - CONSIGLIATO!"
echo "2) 🆓 Ngrok (GRATIS con limitazioni)"
echo "3) 💰 Ngrok Premium (con dominio custom, \$8/mese)"
echo "4) 🌐 Deploy PWA su Vercel (GRATIS, solo frontend)"
echo ""
read -p "Scelta (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  🆓 Cloudflare Tunnel - GRATIS E ILLIMITATO!      ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
        echo ""

        # Check if cloudflared is installed
        if ! command -v cloudflared &> /dev/null; then
            echo -e "${YELLOW}📦 Installazione Cloudflare Tunnel...${NC}"

            # Detect OS
            if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                # Linux
                wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
                sudo dpkg -i cloudflared-linux-amd64.deb
                rm cloudflared-linux-amd64.deb
            elif [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                brew install cloudflare/cloudflare/cloudflared
            else
                echo -e "${RED}❌ OS non supportato. Installa manualmente da:${NC}"
                echo "   https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
                exit 1
            fi

            echo -e "${GREEN}✅ Cloudflare Tunnel installato!${NC}"
        else
            echo -e "${GREEN}✅ Cloudflare Tunnel già installato!${NC}"
        fi

        echo ""
        echo -e "${BLUE}🚀 Avvio servizi...${NC}"
        echo ""

        # Start HTTP server
        echo -e "${CYAN}1️⃣ Avvio HTTP Server (porta 8000)...${NC}"
        python3 -m http.server 8000 > /tmp/tauro_http.log 2>&1 &
        HTTP_PID=$!
        echo $HTTP_PID > /tmp/tauro_http.pid
        sleep 2

        if ps -p $HTTP_PID > /dev/null; then
            echo -e "${GREEN}   ✅ HTTP Server avviato (PID: $HTTP_PID)${NC}"
        else
            echo -e "${RED}   ❌ Errore avvio HTTP Server${NC}"
            exit 1
        fi

        # Start Cloudflare Tunnel
        echo ""
        echo -e "${CYAN}2️⃣ Avvio Cloudflare Tunnel...${NC}"
        echo -e "${YELLOW}   ⏳ Attendere 5-10 secondi...${NC}"
        echo ""

        cloudflared tunnel --url http://localhost:8000 > /tmp/tauro_tunnel.log 2>&1 &
        TUNNEL_PID=$!
        echo $TUNNEL_PID > /tmp/tauro_tunnel.pid

        # Wait for tunnel to start and get URL
        sleep 8

        # Extract URL from logs
        TUNNEL_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/tauro_tunnel.log | head -1)

        if [ -z "$TUNNEL_URL" ]; then
            # Try alternative grep
            TUNNEL_URL=$(grep "trycloudflare.com" /tmp/tauro_tunnel.log | grep -oP 'https://[^\s]+' | head -1)
        fi

        echo ""
        echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║           🎉 DEPLOY COMPLETATO! 🎉                 ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
        echo ""

        if [ ! -z "$TUNNEL_URL" ]; then
            echo -e "${PURPLE}🌐 Il tuo TauroBot è online su:${NC}"
            echo ""
            echo -e "${CYAN}   $TUNNEL_URL${NC}"
            echo ""
            echo -e "${YELLOW}📱 Link diretti:${NC}"
            echo "   Login:     $TUNNEL_URL/pwa/login.html"
            echo "   🚗 Garage: $TUNNEL_URL/pwa/garage.html"
            echo "   Dashboard: $TUNNEL_URL/pwa/dashboard.html"
            echo "   Admin:     $TUNNEL_URL/android/admin.html"
            echo ""
            echo -e "${GREEN}✅ Accessibile da QUALSIASI dispositivo nel mondo!${NC}"
            echo -e "${GREEN}✅ Connessione sicura HTTPS automatica!${NC}"
            echo -e "${GREEN}✅ Completamente GRATUITO!${NC}"
            echo ""

            # Save URL to file
            echo "$TUNNEL_URL" > .taurobot_public_url
            echo "Login: $TUNNEL_URL/pwa/login.html" >> .taurobot_public_url
            echo "Garage: $TUNNEL_URL/pwa/garage.html" >> .taurobot_public_url

            echo -e "${BLUE}💾 URL salvato in: .taurobot_public_url${NC}"
        else
            echo -e "${YELLOW}⚠️  Tunnel avviato ma URL non rilevato automaticamente${NC}"
            echo -e "${YELLOW}   Controlla i log: tail -f /tmp/tauro_tunnel.log${NC}"
        fi

        echo ""
        echo -e "${CYAN}📊 Status dei servizi:${NC}"
        echo "   HTTP Server PID: $HTTP_PID"
        echo "   Tunnel PID: $TUNNEL_PID"
        echo ""
        echo -e "${YELLOW}ℹ️  Per fermare tutto:${NC}"
        echo "   kill $HTTP_PID $TUNNEL_PID"
        echo ""
        echo -e "${YELLOW}ℹ️  Il tunnel rimane attivo finché non chiudi il terminale!${NC}"
        echo -e "${YELLOW}   Per tunnel permanente, usa: ./deploy_permanent.sh${NC}"
        echo ""

        # Keep script running
        echo -e "${GREEN}✅ Servizi attivi! Premi Ctrl+C per fermare.${NC}"
        echo ""

        # Show live logs
        echo -e "${CYAN}📋 Log in tempo reale (Ctrl+C per uscire):${NC}"
        tail -f /tmp/tauro_tunnel.log
        ;;

    2)
        echo ""
        echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  🆓 Ngrok Free - Con limitazioni                  ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
        echo ""

        # Check if ngrok is installed
        if ! command -v ngrok &> /dev/null; then
            echo -e "${YELLOW}📦 Installazione Ngrok...${NC}"

            if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
                echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
                sudo apt update && sudo apt install ngrok
            elif [[ "$OSTYPE" == "darwin"* ]]; then
                brew install ngrok/ngrok/ngrok
            fi

            echo -e "${GREEN}✅ Ngrok installato!${NC}"
        fi

        echo ""
        echo -e "${YELLOW}⚠️  Ngrok FREE ha limiti:${NC}"
        echo "   - URL cambia ad ogni riavvio"
        echo "   - Limite di 40 connessioni/minuto"
        echo "   - Session timeout dopo 2 ore"
        echo ""
        echo -e "${CYAN}Per rimuovere limiti: ngrok.com (da \$8/mese)${NC}"
        echo ""

        read -p "Hai già un account Ngrok? (y/n): " has_account

        if [ "$has_account" == "y" ]; then
            read -p "Inserisci il tuo authtoken: " authtoken
            ngrok config add-authtoken $authtoken
        else
            echo ""
            echo -e "${YELLOW}1. Vai su: https://dashboard.ngrok.com/signup${NC}"
            echo -e "${YELLOW}2. Registrati (gratis)${NC}"
            echo -e "${YELLOW}3. Copia il tuo authtoken${NC}"
            echo ""
            read -p "Authtoken: " authtoken
            ngrok config add-authtoken $authtoken
        fi

        # Start HTTP server
        echo ""
        echo -e "${BLUE}🚀 Avvio servizi...${NC}"
        python3 -m http.server 8000 > /tmp/tauro_http.log 2>&1 &
        HTTP_PID=$!
        sleep 2

        # Start ngrok
        echo -e "${CYAN}Avvio Ngrok tunnel...${NC}"
        ngrok http 8000 > /tmp/tauro_ngrok.log 2>&1 &
        NGROK_PID=$!

        sleep 5

        # Get URL from ngrok API
        NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -oP '"public_url":"https://[^"]+' | head -1 | cut -d'"' -f4)

        echo ""
        echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║           🎉 DEPLOY COMPLETATO! 🎉                 ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${PURPLE}🌐 Il tuo TauroBot è online su:${NC}"
        echo ""
        echo -e "${CYAN}   $NGROK_URL${NC}"
        echo ""
        echo "   Login: $NGROK_URL/pwa/login.html"
        echo "   Garage: $NGROK_URL/pwa/garage.html"
        echo ""
        echo -e "${YELLOW}⚠️  Questo URL cambia ad ogni riavvio!${NC}"
        echo -e "${YELLOW}   Per URL fisso, upgrade a Ngrok Pro (\$8/mese)${NC}"
        echo ""

        echo "$NGROK_URL" > .taurobot_public_url

        echo -e "${GREEN}✅ Servizi attivi! Premi Ctrl+C per fermare.${NC}"

        # Keep running
        wait
        ;;

    3)
        echo ""
        echo -e "${PURPLE}╔════════════════════════════════════════════════════╗${NC}"
        echo -e "${PURPLE}║  💰 Ngrok Premium - Dominio Personalizzato        ║${NC}"
        echo -e "${PURPLE}╚════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${CYAN}Prezzo: \$8/mese (o \$96/anno)${NC}"
        echo ""
        echo -e "${GREEN}✅ Vantaggi:${NC}"
        echo "   • Dominio custom (es: taurobot.ngrok.io)"
        echo "   • URL fisso che non cambia MAI"
        echo "   • Nessun limite di connessioni"
        echo "   • Nessun timeout"
        echo "   • IP whitelisting"
        echo "   • Autenticazione integrata"
        echo ""
        echo -e "${YELLOW}📝 Setup:${NC}"
        echo "   1. Vai su: https://dashboard.ngrok.com/billing/subscription"
        echo "   2. Sottoscrivi Piano Pro"
        echo "   3. Configura dominio custom"
        echo "   4. Torna qui con il dominio"
        echo ""
        read -p "Hai già il piano Pro e il dominio? (y/n): " has_pro

        if [ "$has_pro" == "y" ]; then
            read -p "Inserisci il tuo dominio (es: taurobot.ngrok.io): " custom_domain
            read -p "Inserisci il tuo authtoken Pro: " authtoken

            ngrok config add-authtoken $authtoken

            # Start services
            python3 -m http.server 8000 > /tmp/tauro_http.log 2>&1 &
            HTTP_PID=$!
            sleep 2

            # Start ngrok with custom domain
            ngrok http --domain=$custom_domain 8000 &
            NGROK_PID=$!

            sleep 5

            echo ""
            echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
            echo -e "${GREEN}║           🎉 DEPLOY PREMIUM ATTIVO! 🎉            ║${NC}"
            echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
            echo ""
            echo -e "${PURPLE}🌐 Il tuo TauroBot è su:${NC}"
            echo ""
            echo -e "${CYAN}   https://$custom_domain${NC}"
            echo ""
            echo "   Login: https://$custom_domain/pwa/login.html"
            echo "   Garage: https://$custom_domain/pwa/garage.html"
            echo ""
            echo -e "${GREEN}✅ URL PERMANENTE - Non cambia mai!${NC}"
            echo -e "${GREEN}✅ Nessun limite!${NC}"
            echo ""

            wait
        else
            echo ""
            echo -e "${BLUE}👉 Vai su: https://dashboard.ngrok.com/billing/subscription${NC}"
            echo ""
        fi
        ;;

    4)
        echo ""
        echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  🌐 Deploy PWA su Vercel - GRATIS!                ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${YELLOW}📝 Questo metodo deploya SOLO il frontend (PWA)${NC}"
        echo -e "${YELLOW}   Il bot Telegram rimane sul tuo PC${NC}"
        echo ""

        # Check if vercel CLI is installed
        if ! command -v vercel &> /dev/null; then
            echo -e "${CYAN}📦 Installazione Vercel CLI...${NC}"
            npm install -g vercel
            echo -e "${GREEN}✅ Vercel CLI installato!${NC}"
        fi

        echo ""
        echo -e "${CYAN}🚀 Deploy su Vercel...${NC}"
        echo ""

        # Create vercel.json if not exists
        cat > vercel.json <<EOF
{
  "version": 2,
  "name": "taurobot-pwa",
  "builds": [
    {
      "src": "pwa/**",
      "use": "@vercel/static"
    },
    {
      "src": "android/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/\$1"
    }
  ]
}
EOF

        # Deploy
        vercel --prod

        echo ""
        echo -e "${GREEN}✅ Deploy completato!${NC}"
        echo ""
        echo -e "${YELLOW}📝 Note importanti:${NC}"
        echo "   • La PWA è online su Vercel"
        echo "   • Il bot Telegram serve ancora Ollama locale"
        echo "   • Usa Cloudflare Tunnel per esporre il bot"
        echo ""
        ;;

    *)
        echo -e "${RED}❌ Scelta non valida!${NC}"
        exit 1
        ;;
esac
