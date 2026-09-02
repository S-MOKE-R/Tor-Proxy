# 🔒 Tor Controller Pro v1.0

**Developer:** [@S_MOKE_R](https://t.me/S_MOKE_R)  
**GitHub:** [https://github.com/S-MOKE-R](https://github.com/S-MOKE-R)  
**Telegram:** [https://t.me/S_MOKE_R](https://t.me/S_MOKE_R)  
**Channel:** [https://t.me/VOID_SMOKER](https://t.me/VOID_SMOKER)

A professional Tor proxy manager with a modern GUI for Linux, Windows, and macOS.

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

---

## 🚀 Installation

### Linux (Debian/Ubuntu/Mint/Kali)

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-tk python3-pip tor privoxy proxychains4 -y
pip3 install requests psutil pyperclip pillow

# Download the script
wget -O tor_controller.py https://raw.githubusercontent.com/S-MOKE-R/tor-controller/main/tor_controller.py

# Run
python3 tor_controller.py
Windows
powershell
# Install Python from python.org (make sure to check "Add to PATH")
# Then open Command Prompt or PowerShell as Administrator

# Install dependencies
pip install requests psutil pyperclip pillow

# Download the script
curl -o tor_controller.py https://raw.githubusercontent.com/S-MOKE-R/tor-controller/main/tor_controller.py

# Run
python tor_controller.py
Note: Tor must be installed separately on Windows:

Download Tor from https://www.torproject.org/download/

Run Tor in the background

The app will connect to Tor on 127.0.0.1:9050

macOS
bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python3 tor

# Install Python packages
pip3 install requests psutil pyperclip pillow

# Download the script
curl -o tor_controller.py https://raw.githubusercontent.com/S-MOKE-R/tor-controller/main/tor_controller.py

# Run
python3 tor_controller.py
🔧 Configuration
Linux (Tor & Privoxy)
bash
# Start Tor
sudo systemctl start tor
sudo systemctl enable tor

# Start Privoxy (HTTP proxy)
sudo systemctl start privoxy
sudo systemctl enable privoxy
Windows (Manual Setup)
Install Tor Browser from https://www.torproject.org/

Run Tor in the background

The app will use 127.0.0.1:9050 as the SOCKS5 proxy

macOS (Manual Setup)
bash
# Start Tor
brew services start tor

# The app will use 127.0.0.1:9050 as the SOCKS5 proxy
🎯 Usage
Launch the App
bash
python3 tor_controller.py
Quick Actions
Button	Action
🔄 New Identity	Get a new Tor exit node
📊 Refresh IP	Update IP display
📋 Copy Current	Copy IP to clipboard
⚙️ Settings	Configure auto-start
📝 Commands
Command	Description
CONNECT TO TOR	Enable Tor proxy
DISCONNECT FROM TOR	Disable Tor proxy
Timer	Auto-disconnect after set time
Download Helper	Download files via proxychains
⚙️ Modes
Normal Mode
Connects/disconnects Tor proxy

Shows IP addresses

Timer and presets

Advanced Mode
New identity

Download helper

Log export

📁 Project Structure
text
tor-controller/
├── tor_controller.py   # Main application
├── README.md           # Documentation
├── LICENSE             # MIT License
└── requirements.txt    # Python dependencies
🛠️ Troubleshooting
Error: "proxychains4 not found"
bash
# Linux
sudo apt install proxychains4 -y

# macOS
brew install proxychains-ng
Error: "Tor is not running"
bash
# Linux
sudo systemctl start tor

# macOS
brew services start tor

# Windows
# Start Tor Browser from the start menu
Error: "No module named tkinter"
bash
# Linux
sudo apt install python3-tk -y

# Windows/macOS
# tkinter is included with Python by default
👨‍💻 Credits
Platform	Link
Developer	@S_MOKE_R
GitHub	S-MOKE-R
Telegram	@S_MOKE_R
Channel	VOID_SMOKER
Powered By	Tor Project
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

💬 Support
For support, questions, or contributions:

Join the Telegram channel: https://t.me/VOID_SMOKER

Open an issue on GitHub: Issues

Fork the repository: Fork

⭐ Star the Project
If you find this useful, please star the repository on GitHub!
