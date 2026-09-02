 #🔒 Tor Controller Pro v1.0

**Developer:** [@S_MOKE_R](https://t.me/S_MOKE_R)  
**GitHub:** [https://github.com/S-MOKE-R](https://github.com/S-MOKE-R)  
**Telegram:** [https://t.me/S_MOKE_R](https://t.me/S_MOKE_R)  
**Channel:** [https://t.me/VOID_SMOKER](https://t.me/VOID_SMOKER)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-green)](https://www.linux.org/)

**Tor Controller Pro** is a free, open-source GUI tool that helps you manage Tor proxy connections with ease. It's designed to be simple, fast, and privacy-focused.

---

## 💻 System Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Linux (Ubuntu, Mint, Kali, Debian), Windows 10/11, macOS 10.15+ |
| **Python** | 3.8 or higher |
| **RAM** | 512 MB minimum (1 GB recommended) |
| **Disk Space** | 50 MB for the app + Tor installation |
| **Network** | Internet connection for Tor network access |

---

## 🎯 What is This Tool?

This is a **FREE proxy manager** that lets you:

- Connect/disconnect to Tor with one click
- See your real IP and Tor IP side by side
- Get a new Tor identity instantly
- Set auto-disconnect timers
- Download files through Tor via proxychains
- 4 themes: Dark, Light, Hacker, Blue

**It does NOT require any paid API or subscription. It's completely FREE.**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **One-Click Connect** | Toggle Tor proxy on/off instantly |
| **IP Display** | Shows Real IP and Tor IP side by side |
| **Copy to Clipboard** | Copy any IP with one click |
| **New Identity** | Get a new Tor exit node instantly |
| **Auto-Off Timer** | Set a timer to auto-disconnect Tor |
| **Quick Presets** | 5, 10, 15, 30, 60 minute timers |
| **Connection Logs** | Real-time logging with color coding |
| **Export Logs** | Save logs to a file |
| **4 Themes** | Dark, Light, Hacker, Blue |
| **Download Helper** | Download files through Tor via proxychains |
| **Cross-platform** | Works on Linux, Windows, macOS |
| **100% Free** | No subscriptions, no hidden fees |

---

## 🚀 Installation

Below are four separate installation options. Choose the one that fits your platform.

### Option 1: One-Click Installer (Recommended)

```bash
git clone https://github.com/S-MOKE-R/tor-controller.git
cd tor-controller
chmod +x install.sh
./install.sh
```

---

### Option 2: Linux Manual Installation

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-tk python3-pip tor privoxy proxychains4 -y

# Install Python packages
pip3 install -r requirements.txt
# or individually:
# pip3 install requests psutil pyperclip pillow

# Run the app
python3 tor_controller.py
```

---

### Option 3: Windows Installation

```powershell
# Install Python from python.org (check "Add to PATH")

# Open Command Prompt or PowerShell as Administrator
pip install -r requirements.txt
# or: pip install requests psutil pyperclip pillow

# Download tor_controller.py from GitHub and run:
python tor_controller.py
```

---

### Option 4: macOS Installation

```bash
# Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python3 tor

# Install Python packages
pip3 install -r requirements.txt
# or: pip3 install requests psutil pyperclip pillow

# Run the app
python3 tor_controller.py
```

---

## 🔧 Configuration

### Linux (Tor & Privoxy)

```bash
# Start Tor
sudo systemctl start tor
sudo systemctl enable tor

# Start Privoxy (HTTP proxy)
sudo systemctl start privoxy
sudo systemctl enable privoxy
```

### Windows Configuration

```powershell
# Download and install Tor Browser from https://www.torproject.org/
# Run Tor in the background — the app expects SOCKS5 at 127.0.0.1:9050
```

### macOS Configuration

```bash
# Start Tor as a service
brew services start tor
```

---

## 🎯 Usage

Launch the App

```bash
python3 tor_controller.py
```

Quick Actions

| Button | Action |
|---|---|
| 🔒 CONNECT TO TOR | Enable Tor proxy |
| 🔓 DISCONNECT FROM TOR | Disable Tor proxy |
| 🔄 New Identity | Get a new Tor exit node |
| 📊 Refresh IP | Update IP display |
| 📋 Copy Current | Copy IP to clipboard |
| ⚙️ Settings | Configure auto-start |

Commands

| Command | Description |
|---|---|
| CONNECT TO TOR | Enable Tor proxy |
| DISCONNECT FROM TOR | Disable Tor proxy |
| Timer | Auto-disconnect after set time |
| Download Helper | Download files via proxychains |

---

## 🛠️ Troubleshooting

Error: "proxychains4 not found"

```bash
# Linux
sudo apt install proxychains4 -y

# macOS
brew install proxychains-ng
```

Error: "Tor is not running"

```bash
# Linux
sudo systemctl start tor

# macOS
brew services start tor

# Windows
# Start Tor Browser from the start menu
```

Error: "No module named tkinter"

```bash
# Linux
sudo apt install python3-tk -y

# Windows/macOS
# tkinter is included with Python by default
```

---

## 📁 Project Structure

```
tor-controller/
├── tor_controller.py   # Main application
├── README.md           # Documentation
├── LICENSE             # MIT License
├── requirements.txt    # Python dependencies
└── install.sh          # One-click installer
```

## 👨‍💻 Credits

| Platform | Link |
|---|---|
| Developer | @S_MOKE_R |
| GitHub | S-MOKE-R |
| Telegram | @S_MOKE_R |
| Channel | VOID_SMOKER |
| Powered By | Tor Project |

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

⭐ Support

If you find this useful, please star the repository on GitHub!
