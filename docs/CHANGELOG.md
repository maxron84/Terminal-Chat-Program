# Changelog

All notable changes to Vibe Cozy Chat will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-02

### Added
- `/help` command for all users with formatted menu display
- `/inbox` command for clients to view received files
- Color-coded help menu with comprehensive command list
- User-friendly command reference accessible in-app
- `docker-rebuild.sh` script for Docker troubleshooting

### Fixed
- Fixed `src/data/` recreation bug in client path calculation
- Client now correctly uses root `data/` folder (3 levels up instead of 2)
- Prevented unwanted folder creation during execution
- **Docker deployment issues fixed:**
  - Server now detects non-interactive mode (Docker/background)
  - Fixed stdin reading causing container restarts
  - Fixed environment variable expansion in docker-compose command
  - Containers now start and run stably
- **Improved password mismatch detection:**
  - Clear, formatted error messages when wrong password used
  - Explains issue and provides actionable solutions
  - Helps users quickly identify and fix connection problems

### Changed
- Reorganized documentation structure:
  - `bin/` now contains quick reference cards (instructions.txt, anleitung.txt)
  - `docs/` now contains detailed user manuals (USER_MANUAL.txt, BENUTZER_HANDBUCH.txt)
- Updated all documentation to reference correct file paths
- Updated launcher path references to `./bin/vibe-chat.py`
- Improved user experience with clearer command organization

### Documentation
- Cross-references added between documentation files
- README updated with new file paths and `/help` command
- Command table updated with all available commands
- All repository URLs updated to maxron84

---

## [1.0.0] - 2025-11-02

### 🎉 Initial Release

First public release of Vibe Cozy Chat - a secure, encrypted terminal-based chat application.

### Added

#### Core Features
- Multi-client chat room with real-time messaging
- End-to-end AES-256-CBC encryption
- User authentication via shared password
- Unique username enforcement
- Color-coded messages per user
- Join/leave notifications

#### File Sharing
- Direct file transfer (`/send` command)
- Public file sharing via shared folder
- Private file sharing with `@username` syntax
- Permission-based file access control
- Upload/download commands
- Inbox/outbox folder system

#### Security
- AES-256-CBC message encryption
- PBKDF2 key derivation
- Permission tracking system
- File access control
- Complete server-side logging

#### Docker Support
- Production-ready docker-compose.yml
- Development docker-compose.dev.yml
- Optimized Dockerfile
- Health checks
- Resource limits
- Named volumes for persistence
- Multi-stage configuration

#### User Interface
- Interactive Python launcher (bin/vibe-chat.py)
- Color-coded terminal output
- Command-based interface
- Real-time message display
- File transfer progress indication

#### Documentation
- Comprehensive README with AI disclosure
- Security warnings for private networks
- Docker deployment guide
- Multi-language support (EN/DE)
- Quick start guides
- Architecture documentation
- Test documentation
- Security assessment

#### Testing
- 27 unit and integration tests
- 100% test pass rate
- Coverage for all major features
- Encryption tests
- File permission tests
- Client/server tests

#### Internationalization
- English documentation
- German documentation (Deutsch)
- Multi-language command reference

### Technical Details

#### Languages & Tools
- Python 3.6+ (stdlib only, no external dependencies)
- Docker & Docker Compose
- OpenSSL for encryption

#### Architecture
- Modular library structure
- Separate client/server modules
- File permissions manager
- Encryption abstraction layer
- Utility functions

#### File Structure
```
Terminal-Chat-Program/
├── bin/              - Launchers and quick starts
├── src/
│   ├── lib/          - Core library modules
│   ├── modular/      - Entry point
│   └── legacy/       - Original version
├── tests/            - Test suite
├── docs/             - Documentation
├── data/             - User data folders
└── Docker files      - Container deployment
```

### ⚠️ Important Notes

- **Private Networks Only** - Not for public internet
- **No TLS/SSL** - Transport layer not encrypted
- **Password-based** - Single shared password
- **Educational** - Great for learning, not for production security

### Known Limitations

- No TLS/SSL transport encryption
- No user account system
- No rate limiting
- Basic input validation
- Single password for all users

### 🤖 AI Generation Notice

This entire project (code, docs, tests, Docker configs) was created using:
- AI: Anthropic Claude Sonnet 4.5
- Tool: VS Codium with Roo Code extension
- Method: 100% prompt-driven development
- Human contribution: Prompts only, no code

---

## [Unreleased]

### Planned for v2.0

- [ ] TLS/SSL transport encryption
- [ ] User authentication system
- [ ] Session management
- [ ] Rate limiting
- [ ] Enhanced input validation
- [ ] Web-based GUI
- [ ] Mobile app support

### Planned for v3.0

- [ ] End-to-end encryption enhancement
- [ ] Multi-factor authentication
- [ ] Voice chat support
- [ ] Video sharing
- [ ] Plugin system
- [ ] Advanced monitoring

---

## Version History

### [1.1.0] - 2025-11-02
- Added `/help` command with formatted menu
- Fixed `src/data/` recreation bug
- Reorganized documentation structure
- Updated all repository URLs
- 27 tests passing

### [1.0.0] - 2025-11-02
- Initial public release
- Complete feature set
- Full documentation
- Docker support
- 27 passing tests

---

## Links

- [Repository](https://github.com/maxron84/Terminal-Chat-Program)
- [Documentation](docs/)
- [Security Policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [License](LICENSE)

---

**Note**: This project is 100% AI-generated. All versions and changes are tracked here for transparency.