# Vibe Cozy Chat v1.1.0 Release Notes

**Release Date:** November 2, 2025  
**Repository:** https://github.com/maxron84/vibe-cozy-chat

## 🎉 What's New

### New Features

#### `/help` Command
- Interactive help menu for all users (server and clients)
- Color-coded display with comprehensive command list
- Easy-to-read formatted output
- Accessible anytime during chat session

#### `/inbox` Command for Clients
- Clients can now view their received files
- Previously only available on server
- Better file management visibility

### Bug Fixes

#### Fixed `src/data/` Recreation Issue
- Resolved persistent folder creation bug
- Client now correctly calculates path to root `data/` folder
- Eliminates unwanted directory structure

### Improvements

#### Documentation Reorganization
- **Quick Reference:** `bin/instructions.txt` and `bin/anleitung.txt`
- **Detailed Guides:** `docs/USER_MANUAL.txt` and `docs/BENUTZER_HANDBUCH.txt`
- All documentation updated with correct file paths
- Cross-references added between documents

#### Updated Command Table
All commands now documented in README with examples:
- `/list` - List shared files
- `/inbox` - View received files
- `/outbox` - View files ready to upload
- `/upload <file>` - Upload public file
- `/upload <file> @user` - Upload private file
- `/download <file>` - Download file
- `/help` - Show help menu
- `/quit` - Exit chat

## 📦 Installation

### Quick Start
```bash
git clone https://github.com/maxron84/vibe-cozy-chat.git
cd vibe-cozy-chat
python3 bin/vibe-chat.py
```

### Docker Deployment
```bash
git clone https://github.com/maxron84/vibe-cozy-chat.git
cd vibe-cozy-chat
cp .env.example .env
nano .env  # Set strong password
docker-compose up -d
```

## 🧪 Testing

All 27 tests pass successfully:
```bash
python3 tests/test_chat.py
# Expected: Ran 27 tests in ~0.3s - OK
```

## ⚠️ Security Notice

**IMPORTANT: Private Networks Only**

This application is designed for **trusted, private networks** only (home LANs, office networks, VPNs). Do not expose to public internet without:
- VPN tunnel
- Reverse proxy with TLS
- Rate limiting
- Additional hardening

See [Security Documentation](docs/SECURITY.md) for details.

## 📚 Documentation

- **[README](README.md)** - Complete project overview
- **[User Manual (EN)](docs/USER_MANUAL.txt)** - Detailed usage guide
- **[Benutzerhandbuch (DE)](docs/BENUTZER_HANDBUCH.txt)** - Deutsche Anleitung
- **[Quick Reference (EN)](bin/instructions.txt)** - Command cheat sheet
- **[Schnellreferenz (DE)](bin/anleitung.txt)** - Befehlsübersicht
- **[CHANGELOG](docs/CHANGELOG.md)** - Version history
- **[Security Policy](docs/SECURITY.md)** - Security guidelines

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 🐛 Bug Reports

Found a bug? Please [open an issue](https://github.com/maxron84/vibe-cozy-chat/issues/new?template=bug_report.md) with:
- Detailed description
- Steps to reproduce
- Your environment details
- Error messages/logs

## 💡 Feature Requests

Have an idea? [Request a feature](https://github.com/maxron84/vibe-cozy-chat/issues/new?template=feature_request.md)!

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🤖 AI Generation Notice

This project is 100% AI-generated using:
- **AI:** Anthropic Claude Sonnet 4.5
- **Tool:** VS Codium with Roo Code extension
- **Method:** Prompt-driven development
- **Human Input:** Prompts and direction only

## 🙏 Acknowledgments

- Python's excellent standard library
- OpenSSL for encryption capabilities
- The open-source community
- All users and contributors

## 🔗 Links

- **Repository:** https://github.com/maxron84/vibe-cozy-chat
- **Issues:** https://github.com/maxron84/vibe-cozy-chat/issues
- **Discussions:** https://github.com/maxron84/vibe-cozy-chat/discussions

---

**Happy Chatting! 🎉**

Made with ❤️ by AI (Claude Sonnet 4.5) + Human prompts