#!/bin/bash
# Tor Controller Pro Installer
# Developer: @S_MOKE_R
# GitHub: https://github.com/S-MOKE-R

echo "=========================================="
echo "🔒 Tor Controller Pro Installer"
echo "=========================================="
echo "Developer: @S_MOKE_R"
echo "GitHub: https://github.com/S-MOKE-R"
echo "Telegram: https://t.me/S_MOKE_R"
echo "=========================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  This installer is for Linux only."
    echo "For Windows/macOS, please follow manual instructions in README.md"
    exit 1
fi

echo "📦 Checking dependencies..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Installing..."
    sudo apt update
    sudo apt install python3 python3-pip -y
else
    echo "✅ Python3 found"
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Installing..."
    sudo apt install python3-pip -y
else
    echo "✅ pip3 found"
fi

# Check tkinter
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "❌ tkinter not found. Installing..."
    sudo apt install python3-tk -y
else
    echo "✅ tkinter found"
fi

# Check Tor
if ! command -v tor &> /dev/null; then
    echo "❌ Tor not found. Installing..."
    sudo apt install tor -y
else
    echo "✅ Tor found"
fi

# Check proxychains
if ! command -v proxychains4 &> /dev/null; then
    echo "❌ proxychains4 not found. Installing..."
    sudo apt install proxychains4 -y
else
    echo "✅ proxychains4 found"
fi

echo ""
echo "📦 Installing Python packages..."

# Try to install with --break-system-packages (newer Python), fallback to --user
pip3 install requests psutil pyperclip pillow --break-system-packages 2>/dev/null || pip3 install requests psutil pyperclip pillow --user

echo ""
echo "🔧 Configuring services..."

# Start Tor
echo "Starting Tor service..."
sudo systemctl start tor 2>/dev/null || echo "⚠️  Could not start Tor. You may need to start it manually: sudo systemctl start tor"

# Enable Tor to start on boot
sudo systemctl enable tor 2>/dev/null || echo "⚠️  Could not enable Tor. You may need to enable it manually: sudo systemctl enable tor"

# Start Privoxy
echo "Starting Privoxy service..."
sudo systemctl start privoxy 2>/dev/null || echo "⚠️  Could not start Privoxy. You may need to start it manually: sudo systemctl start privoxy"

# Enable Privoxy to start on boot
sudo systemctl enable privoxy 2>/dev/null || echo "⚠️  Could not enable Privoxy. You may need to enable it manually: sudo systemctl enable privoxy"

echo ""
echo "🖥️  Creating desktop shortcut..."

# Create desktop shortcut
cat > ~/.local/share/applications/tor-controller.desktop << EOF
[Desktop Entry]
Name=Tor Controller Pro
Comment=Free Tor Proxy Manager
Exec=python3 /home/$USER/tor-controller/tor_controller.py
Icon=network-vpn
Terminal=false
Type=Application
Categories=Network;Utility;
StartupNotify=true
EOF

chmod +x ~/.local/share/applications/tor-controller.desktop

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "🔒 Tor Controller Pro v1.0"
echo "Developer: @S_MOKE_R"
echo "GitHub: https://github.com/S-MOKE-R"
echo ""
echo "🚀 To launch the app:"
echo "   python3 ~/tor-controller/tor_controller.py"
echo ""
echo "📌 Or find it in your application menu: 'Tor Controller Pro'"
echo ""
echo "=========================================="
