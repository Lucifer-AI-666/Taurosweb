#!/bin/bash

# 🔒 TauroBot Permanent Deploy
# Configura TauroBot per rimanere online 24/7

echo "╔════════════════════════════════════════════════════╗"
echo "║  🔒 TauroBot Permanent Deploy                     ║"
echo "║  Rimane online anche dopo riavvio server          ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}Questo script configura:${NC}"
echo "  • Systemd service (Linux) o LaunchDaemon (macOS)"
echo "  • Avvio automatico al boot"
echo "  • Restart automatico se crasha"
echo "  • Cloudflare Tunnel permanente"
echo ""

read -p "Procedi? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Annullato."
    exit 0
fi

# Get current directory
CURRENT_DIR=$(pwd)

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo ""
    echo -e "${BLUE}🐧 Configurazione per Linux (systemd)...${NC}"
    echo ""

    # Create systemd service
    sudo tee /etc/systemd/system/taurobot.service > /dev/null <<EOF
[Unit]
Description=TauroBot 3.0 Ultimate
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CURRENT_DIR
ExecStart=/usr/bin/python3 -m http.server 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Create cloudflare tunnel service
    sudo tee /etc/systemd/system/taurobot-tunnel.service > /dev/null <<EOF
[Unit]
Description=TauroBot Cloudflare Tunnel
After=network.target taurobot.service

[Service]
Type=simple
User=$USER
ExecStart=/usr/local/bin/cloudflared tunnel --url http://localhost:8000
Restart=always
RestartSec=10
StandardOutput=append:$CURRENT_DIR/logs/tunnel.log
StandardError=append:$CURRENT_DIR/logs/tunnel.log

[Install]
WantedBy=multi-user.target
EOF

    # Create logs directory
    mkdir -p logs

    # Reload systemd
    sudo systemctl daemon-reload

    # Enable and start services
    echo -e "${CYAN}Abilitazione servizi...${NC}"
    sudo systemctl enable taurobot.service
    sudo systemctl enable taurobot-tunnel.service

    echo -e "${CYAN}Avvio servizi...${NC}"
    sudo systemctl start taurobot.service
    sudo systemctl start taurobot-tunnel.service

    sleep 5

    # Check status
    echo ""
    echo -e "${GREEN}✅ Servizi configurati!${NC}"
    echo ""
    echo -e "${CYAN}Status:${NC}"
    sudo systemctl status taurobot.service --no-pager -l
    echo ""
    sudo systemctl status taurobot-tunnel.service --no-pager -l
    echo ""

    # Get tunnel URL from logs
    sleep 5
    TUNNEL_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' logs/tunnel.log | tail -1)

    if [ ! -z "$TUNNEL_URL" ]; then
        echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║        🎉 DEPLOY PERMANENTE ATTIVO! 🎉            ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${CYAN}🌐 URL pubblico:${NC}"
        echo "   $TUNNEL_URL"
        echo ""
        echo -e "${GREEN}✅ Rimane attivo anche dopo riavvio!${NC}"
        echo -e "${GREEN}✅ Restart automatico se crasha!${NC}"
        echo ""
        echo "$TUNNEL_URL" > .taurobot_permanent_url
    fi

    echo ""
    echo -e "${YELLOW}📋 Comandi utili:${NC}"
    echo "   Status:  sudo systemctl status taurobot.service"
    echo "   Stop:    sudo systemctl stop taurobot.service taurobot-tunnel.service"
    echo "   Start:   sudo systemctl start taurobot.service taurobot-tunnel.service"
    echo "   Restart: sudo systemctl restart taurobot.service taurobot-tunnel.service"
    echo "   Logs:    sudo journalctl -u taurobot-tunnel.service -f"
    echo ""

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo -e "${BLUE}🍎 Configurazione per macOS (LaunchDaemon)...${NC}"
    echo ""

    # Create launch agent
    cat > ~/Library/LaunchAgents/com.taurobot.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.taurobot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>-m</string>
        <string>http.server</string>
        <string>8000</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$CURRENT_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$CURRENT_DIR/logs/taurobot.log</string>
    <key>StandardErrorPath</key>
    <string>$CURRENT_DIR/logs/taurobot.error.log</string>
</dict>
</plist>
EOF

    cat > ~/Library/LaunchAgents/com.taurobot.tunnel.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.taurobot.tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/cloudflared</string>
        <string>tunnel</string>
        <string>--url</string>
        <string>http://localhost:8000</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$CURRENT_DIR/logs/tunnel.log</string>
    <key>StandardErrorPath</key>
    <string>$CURRENT_DIR/logs/tunnel.error.log</string>
</dict>
</plist>
EOF

    mkdir -p logs

    # Load launch agents
    launchctl load ~/Library/LaunchAgents/com.taurobot.plist
    launchctl load ~/Library/LaunchAgents/com.taurobot.tunnel.plist

    sleep 5

    echo -e "${GREEN}✅ Servizi configurati per macOS!${NC}"
    echo ""
    echo -e "${YELLOW}📋 Comandi utili:${NC}"
    echo "   Stop:    launchctl unload ~/Library/LaunchAgents/com.taurobot.plist"
    echo "   Start:   launchctl load ~/Library/LaunchAgents/com.taurobot.plist"
    echo "   Logs:    tail -f logs/tunnel.log"
    echo ""

    # Get URL
    sleep 5
    TUNNEL_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' logs/tunnel.log | tail -1)

    if [ ! -z "$TUNNEL_URL" ]; then
        echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║        🎉 DEPLOY PERMANENTE ATTIVO! 🎉            ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${CYAN}🌐 URL pubblico:${NC}"
        echo "   $TUNNEL_URL"
        echo ""
        echo "$TUNNEL_URL" > .taurobot_permanent_url
    fi
fi

echo ""
echo -e "${CYAN}💡 Note:${NC}"
echo "   • L'URL di Cloudflare Tunnel cambia ad ogni riavvio"
echo "   • Per URL fisso permanente, considera Ngrok Pro (\$8/mese)"
echo "   • Oppure usa un dominio tuo con Cloudflare Tunnel (gratis ma richiede setup DNS)"
echo ""
