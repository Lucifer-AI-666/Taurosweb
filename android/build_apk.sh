#!/bin/bash

# 📱 TauroBot APK Builder
# Crea APK Android personalizzata per gestione sistema

echo "📱 TauroBot Ultimate - Android APK Builder"
echo "==========================================="
echo "💎 Premium Edition - Solo per te!"
echo ""

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found${NC}"
    echo "   Install: https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}✅ Node.js found:${NC} $(node --version)"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ npm found:${NC} $(npm --version)"

# Check Java (required for Android build)
if ! command -v java &> /dev/null; then
    echo -e "${RED}❌ Java not found${NC}"
    echo "   Install JDK 11 or later"
    echo "   Ubuntu: sudo apt install openjdk-11-jdk"
    echo "   macOS: brew install openjdk@11"
    exit 1
fi
echo -e "${GREEN}✅ Java found:${NC} $(java -version 2>&1 | head -n 1)"

# Check Android SDK
if [ -z "$ANDROID_HOME" ]; then
    echo -e "${YELLOW}⚠️  ANDROID_HOME not set${NC}"
    echo "   Install Android Studio or SDK tools"
    echo "   Then export ANDROID_HOME=/path/to/sdk"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✅ Android SDK:${NC} $ANDROID_HOME"
fi

# Vai alla directory android
cd "$(dirname "$0")"

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    npm install
fi

# Sync Capacitor
echo -e "${BLUE}🔄 Syncing Capacitor...${NC}"
npx cap sync android

# Choose build type
echo ""
echo "Select build type:"
echo "1) Debug APK (fast, for testing)"
echo "2) Release APK (signed, for production)"
read -p "Choice [1-2]: " choice

case $choice in
    1)
        echo -e "${BLUE}🔨 Building DEBUG APK...${NC}"
        cd android
        ./gradlew assembleDebug

        if [ $? -eq 0 ]; then
            APK_PATH="app/build/outputs/apk/debug/app-debug.apk"
            echo ""
            echo -e "${GREEN}✅ APK BUILD SUCCESSFUL!${NC}"
            echo -e "${GREEN}📱 APK Location:${NC}"
            echo "   $(pwd)/$APK_PATH"
            echo ""
            echo -e "${YELLOW}Install on device:${NC}"
            echo "   adb install $APK_PATH"
        else
            echo -e "${RED}❌ Build failed${NC}"
            exit 1
        fi
        ;;
    2)
        echo -e "${BLUE}🔨 Building RELEASE APK...${NC}"

        # Check keystore
        if [ ! -f "keystore.jks" ]; then
            echo -e "${YELLOW}⚠️  Keystore not found. Creating new keystore...${NC}"
            keytool -genkey -v -keystore keystore.jks \
                    -alias taurobot \
                    -keyalg RSA \
                    -keysize 2048 \
                    -validity 10000 \
                    -storepass taurobot123 \
                    -keypass taurobot123 \
                    -dname "CN=TauroBot, OU=Dev, O=TauroBot, L=Rome, S=Italy, C=IT"
            echo -e "${GREEN}✅ Keystore created${NC}"
        fi

        cd android
        ./gradlew assembleRelease

        if [ $? -eq 0 ]; then
            APK_PATH="app/build/outputs/apk/release/app-release-unsigned.apk"
            SIGNED_APK="app/build/outputs/apk/release/TauroBot-v3.0.0-release.apk"

            # Sign APK
            echo -e "${BLUE}✍️  Signing APK...${NC}"
            jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
                     -keystore ../keystore.jks \
                     -storepass taurobot123 \
                     $APK_PATH taurobot

            # Zipalign
            echo -e "${BLUE}📦 Optimizing APK...${NC}"
            zipalign -v 4 $APK_PATH "$SIGNED_APK"

            echo ""
            echo -e "${GREEN}✅ RELEASE APK BUILD SUCCESSFUL!${NC}"
            echo -e "${GREEN}📱 APK Location:${NC}"
            echo "   $(pwd)/$SIGNED_APK"
            echo ""
            echo -e "${YELLOW}Install on device:${NC}"
            echo "   adb install $SIGNED_APK"
            echo ""
            echo -e "${YELLOW}Size:${NC} $(du -h "$SIGNED_APK" | cut -f1)"
        else
            echo -e "${RED}❌ Build failed${NC}"
            exit 1
        fi
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Build completed!${NC}"
echo ""
echo "Next steps:"
echo "1. Connect Android device via USB"
echo "2. Enable USB debugging on device"
echo "3. Run: adb devices (to verify connection)"
echo "4. Install APK with command above"
echo ""
echo "💎 Enjoy your exclusive TauroBot app!"
