# Modular Structure for Vibe Cozy Chat

## Overview

The codebase has been organized into a modular structure for better maintainability, testing, and understanding.

## Directory Structure

```
src/
├── cozy_secure_chat.py          ← Original monolithic version (WORKING)
├── lib/                          ← Reusable library modules
│   ├── __init__.py              - Library exports
│   ├── utils.py                 - Utilities & constants
│   ├── encryption.py            - Encryption/decryption
│   ├── server.py                - ChatServer class (TODO)
│   └── client.py                - ChatClient class (TODO)
└── modular/                      ← Modular version
    ├── cozy_secure_chat_modular.py  - Entry point using lib/
    └── MODULAR_STRUCTURE.md     - This file
```

## Modules Created

### ✅ lib/utils.py
- **Purpose**: Common utilities and constants
- **Contents**:
  - ANSI color codes (BLUE, GREEN, YELLOW, RED, CYAN, MAGENTA, RESET)
  - `timestamp()` function
- **Size**: 20 lines
- **Dependencies**: datetime

### ✅ lib/encryption.py  
- **Purpose**: Encryption/decryption functionality
- **Contents**:
  - `Encryption` class
  - `encrypt(text)` method
  - `decrypt(encrypted_text)` method
- **Size**: 76 lines
- **Dependencies**: subprocess, sys, utils

### 🚧 lib/server.py (To Be Created)
- **Purpose**: Server-side functionality
- **Contents**:
  - `ChatServer` class (~330 lines)
  - Client handling
  - Message broadcasting
  - File transfer handling
  - Command processing
  - Logging
- **Dependencies**: socket, threading, os, shutil, logging, utils, encryption

### 🚧 lib/client.py (To Be Created)
- **Purpose**: Client-side functionality
- **Contents**:
  - `ChatClient` class (~230 lines)
  - Message sending/receiving
  - File transfer
  - Color-coded display
  - Command processing
- **Dependencies**: socket, threading, os, base64, utils, encryption

### 🚧 modular/cozy_secure_chat_modular.py (To Be Created)
- **Purpose**: Main entry point using modular components
- **Contents**:
  - Import from lib/
  - `main()` function
  - Command-line argument parsing
- **Size**: ~50 lines
- **Dependencies**: lib.server, lib.client, sys

## Benefits of Modular Structure

### 🎯 Maintainability
- Each module has a single responsibility
- Easier to locate and fix bugs
- Changes isolated to specific modules

### 🧪 Testability
- Individual components can be tested separately
- Mock dependencies easily
- Better test coverage

### 📚 Readability
- Smaller, focused files
- Clear module boundaries
- Better documentation possibilities

### 🔄 Reusability
- Encryption module can be used elsewhere
- Server/Client classes as libraries
- Utils shared across project

### 👥 Collaboration
- Multiple developers can work on different modules
- Less merge conflicts
- Clear ownership boundaries

## Module Responsibilities

```
┌─────────────────────────────────────────────┐
│         cozy_secure_chat_modular.py         │
│              (Entry Point)                  │
│  - Parse arguments                          │
│  - Initialize server/client                 │
└──────────────┬──────────────┬───────────────┘
               │              │
        ┌──────▼──────┐  ┌───▼──────┐
        │   Server    │  │  Client  │
        │             │  │          │
        │ - Listen    │  │ - Connect│
        │ - Broadcast │  │ - Send   │
        │ - Handle    │  │ - Receive│
        └──────┬──────┘  └────┬─────┘
               │              │
               └──────┬───────┘
                      │
            ┌─────────▼──────────┐
            │    Encryption      │
            │                    │
            │ - encrypt()        │
            │ - decrypt()        │
            └─────────┬──────────┘
                      │
            ┌─────────▼──────────┐
            │      Utils         │
            │                    │
            │ - Colors           │
            │ - timestamp()      │
            └────────────────────┘
```

## Usage

### Original Version (Still Works!)
```bash
python3 src/cozy_secure_chat.py listen 4444 pass123 Admin
python3 src/cozy_secure_chat.py connect localhost 4444 pass123 Alice
```

### Modular Version (After completing TODO items)
```bash
python3 src/modular/cozy_secure_chat_modular.py listen 4444 pass123 Admin
python3 src/modular/cozy_secure_chat_modular.py connect localhost 4444 pass123 Alice
```

### As Library
```python
from lib import ChatServer, ChatClient, Encryption

# Create server
server = ChatServer(4444, "password", "Admin")
server.run()

# Or create client
client = ChatClient("localhost", 4444, "password", "Alice")
client.run()
```

## Migration Path

1. ✅ **Phase 1**: Extract utils and encryption (DONE)
2. 🚧 **Phase 2**: Extract server class
3. 🚧 **Phase 3**: Extract client class
4. 🚧 **Phase 4**: Create modular entry point
5. 🚧 **Phase 5**: Update tests to test modules
6. 🚧 **Phase 6**: Update documentation

## Testing Strategy

### Unit Tests for Each Module
```python
# tests/test_encryption.py
from lib.encryption import Encryption

def test_encrypt_decrypt():
    enc = Encryption("password")
    encrypted = enc.encrypt("hello")
    decrypted = enc.decrypt(encrypted)
    assert decrypted == "hello"

# tests/test_utils.py
from lib.utils import timestamp

def test_timestamp_format():
    ts = timestamp()
    assert len(ts) == 8
    assert ts[2] == ':'
```

### Integration Tests
```python
# tests/test_integration.py
from lib import ChatServer, ChatClient

def test_server_client_communication():
    # Test server-client message exchange
    pass
```

## Notes

- **Original file preserved**: `src/cozy_secure_chat.py` remains unchanged
- **Gradual migration**: Can be done incrementally
- **Backwards compatible**: Old code continues to work
- **Future proof**: Easy to add new features as modules

## Next Steps

To complete the modularization:

1. Extract `ChatServer` class to `lib/server.py`
2. Extract `ChatClient` class to `lib/client.py`  
3. Create `modular/cozy_secure_chat_modular.py` entry point
4. Update tests to import from lib/
5. Update documentation

Each step can be done independently without breaking the original version!