# 📥 Installation Guide - Terminal Chat

Terminal Chat can be installed in multiple ways depending on your needs and technical expertise.

---

## 🚀 Quick Install (Recommended)

### Option 1: pip Install (Python users)

**Requirements:** Python 3.8 or higher

```bash
pip install terminal-chat
```

Then run from anywhere:
```bash
terminal-chat
```

---

### Option 2: Standalone Executable (No Python needed!)

**For non-technical users or those without Python installed.**

1. **Download** the executable for your platform:
   - 🪟 Windows: `terminal-chat-windows.exe`
   - 🐧 Linux: `terminal-chat-linux`
   - 🍎 macOS: `terminal-chat-macos`

2. **Run** the executable:
   - Windows: Double-click `terminal-chat-windows.exe`
   - Linux/macOS: `./terminal-chat-linux` (or `./terminal-chat-macos`)

**Note:** On Linux/macOS, you may need to make it executable first:
```bash
chmod +x terminal-chat-linux
```

---

## 🔧 Advanced Installation

### From Source (Developers)

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/Terminal-Chat-Program.git
cd Terminal-Chat-Program
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run directly:**
```bash
python3 bin/terminal-chat.py
```

---

### Using Docker

1. **Pull the image:**
```bash
docker pull terminalchat/terminal-chat
```

2. **Run:**
```bash
docker run -it -p 4444:4444 terminalchat/terminal-chat
```

---

## 🛠️ Building from Source

### Build pip Package

```bash
python3 setup.py sdist bdist_wheel
pip install dist/terminal-chat-*.whl
```

### Build Standalone Executable

```bash
python3 build_executable.py
```

This will create a platform-specific executable in the `dist/` folder.

---

## 📋 System Requirements

**Minimum:**
- Python 3.8+ (for pip install or source)
- 50 MB disk space
- Terminal/Command line access
- Network connection (for chat functionality)

**Standalone Executables:**
- No Python required
- 20-50 MB disk space (executable size)
- Modern OS (Windows 10+, Linux kernel 3.2+, macOS 10.13+)

---

## 🌍 Language Support

Terminal Chat supports multiple languages:
- 🇬🇧 English
- 🇩🇪 German (Deutsch)

Language selection appears at startup.

---

## ✅ Verify Installation

Test your installation:

```bash
terminal-chat --version
```

Or just run:
```bash
terminal-chat
```

You should see the language selection screen.

---

## 🆘 Troubleshooting

### pip install fails

**Issue:** `pip: command not found`
- **Solution:** Install Python 3.8+ from python.org

**Issue:** Permission denied
- **Solution:** Use `pip install --user terminal-chat`

### Executable won't run

**Issue:** "Permission denied" (Linux/macOS)
- **Solution:** Run `chmod +x terminal-chat-linux`

**Issue:** Windows Defender warning
- **Solution:** Click "More info" → "Run anyway" (the app is safe)

**Issue:** "Cannot execute binary file"
- **Solution:** Download the correct executable for your platform

### Connection issues

**Issue:** Cannot connect to server
- **Solution:** Check firewall settings, ensure port 4444 is open

---

## 📚 Next Steps

After installation, check out:
- [User Manual](docs/USER_MANUAL.txt) - Complete usage guide
- [Quick Start](bin/instructions.txt) - English quick start
- [Schnellstart](bin/anleitung.txt) - German quick start

---

## 💬 Need Help?

- 📖 Read the [README.md](README.md)
- 🐛 Report issues on GitHub
- 💡 Check the [documentation](docs/)

Happy chatting! 🎉