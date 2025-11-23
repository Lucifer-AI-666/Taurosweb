#!/bin/bash

# 🌐 Deploy PWA su Vercel - GRATIS E PERMANENTE!

echo "╔════════════════════════════════════════════════════╗"
echo "║  🌐 Deploy TauroBot PWA su Vercel                 ║"
echo "║  URL permanente GRATIS!                           ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}📦 Installazione Vercel CLI...${NC}"
    npm install -g vercel

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Vercel CLI installato!${NC}"
    else
        echo -e "${RED}❌ Errore installazione. Prova manualmente:${NC}"
        echo "   npm install -g vercel"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Vercel CLI già installato!${NC}"
fi

echo ""
echo -e "${CYAN}📝 Cosa verrà deployato:${NC}"
echo "   • PWA (Login, Dashboard, Garage, Gateway)"
echo "   • Admin Panel Android"
echo "   • Terminal Remoto"
echo "   • Sistemi sicurezza (NET'ALIS, NEXUS)"
echo "   • Service Worker & Manifest"
echo ""
echo -e "${YELLOW}⚠️  NON verrà deployato:${NC}"
echo "   • Bot Telegram (rimane sul tuo PC)"
echo "   • File .env (segreti)"
echo "   • Memoria conversazioni"
echo ""

read -p "Procedi con il deploy? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Deploy annullato."
    exit 0
fi

echo ""
echo -e "${BLUE}🚀 Deploy in corso...${NC}"
echo ""

# Deploy to production
vercel --prod

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║        🎉 DEPLOY COMPLETATO! 🎉                    ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}🌐 La tua PWA è online!${NC}"
    echo ""
    echo -e "${YELLOW}📱 Vercel ti ha dato un URL tipo:${NC}"
    echo "   https://taurobot-xyz123.vercel.app"
    echo ""
    echo -e "${GREEN}✅ URL permanente - Non cambia MAI!${NC}"
    echo -e "${GREEN}✅ HTTPS automatico!${NC}"
    echo -e "${GREEN}✅ CDN globale velocissimo!${NC}"
    echo -e "${GREEN}✅ Completamente GRATIS!${NC}"
    echo ""
    echo -e "${CYAN}📋 Link diretti:${NC}"
    echo "   Login:     https://tuo-url.vercel.app/"
    echo "   Dashboard: https://tuo-url.vercel.app/pwa/dashboard.html"
    echo "   🚗 Garage: https://tuo-url.vercel.app/pwa/garage.html"
    echo "   Admin:     https://tuo-url.vercel.app/android/admin.html"
    echo ""
    echo -e "${YELLOW}💡 Prossimi passi:${NC}"
    echo "   1. Apri l'URL dal browser"
    echo "   2. Registrati (username + password)"
    echo "   3. Accedi al Garage e aggiungi progetti!"
    echo ""
    echo -e "${CYAN}🔧 Dominio personalizzato (opzionale):${NC}"
    echo "   • Vai su: vercel.com/dashboard"
    echo "   • Settings → Domains"
    echo "   • Aggiungi: tuodominio.com (se lo possiedi)"
    echo ""
    echo -e "${BLUE}📊 Dashboard Vercel:${NC}"
    echo "   https://vercel.com/dashboard"
    echo ""
else
    echo -e "${RED}❌ Errore durante il deploy${NC}"
    echo "Controlla i log sopra per dettagli"
    exit 1
fi
