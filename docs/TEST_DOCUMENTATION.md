# Test Documentation - Cozy Secure Chat

## Overview

This document describes the test suite for the Cozy Secure Chat application. The test suite consists of 20 comprehensive unit and integration tests that validate the core functionality of the encrypted chat system.

## Test File

**File:** `test_chat.py`
**Location:** `vibe-cozy-chat/test_chat.py`
**Lines of Code:** 340
**Test Framework:** Python's built-in `unittest`

## Running the Tests

### Standard Execution

```bash
cd vibe-cozy-chat
python3 test_chat.py
```

### With pytest (Optional)

If you have pytest installed:

```bash
python3 -m pytest test_chat.py -v
```

### With Coverage (Optional)

To run tests with coverage reporting:

```bash
python3 -m pytest test_chat.py --cov=cozy_secure_chat --cov-report=html
```

## Test Categories

### 1. Encryption Tests (`TestEncryption`)

**Purpose:** Validate the encryption and decryption functionality using OpenSSL AES-256-CBC.

| Test Name | Description | Validates |
|-----------|-------------|-----------|
| `test_encrypt_decrypt_simple_message` | Basic encryption/decryption | Core encryption functionality works |
| `test_encrypt_decrypt_long_message` | Long message handling | Large messages encrypt/decrypt correctly |
| `test_encrypt_special_characters` | Special character support | Symbols (!@#$%^&*) are preserved |
| `test_encrypt_unicode` | Unicode character support | International characters (中文, العربية, 🎉) work |
| `test_wrong_password_fails` | Password validation | Wrong password cannot decrypt messages |
| `test_empty_message` | Empty string handling | Edge case: empty strings are handled |
| `test_newlines_removed_from_encrypted` | Output format | Encrypted output has no line breaks |

**Expected Results:** All 7 tests should pass, confirming that encryption works correctly for various input types.

### 2. Client Tests (`TestChatClient`)

**Purpose:** Validate client initialization and color assignment system.

| Test Name | Description | Validates |
|-----------|-------------|-----------|
| `test_client_initialization` | Client setup | Client initializes with correct parameters |
| `test_color_assignment_own_user` | Self-coloring | User sees their own messages in blue |
| `test_color_assignment_admin` | Admin coloring | Admin messages always appear in magenta |
| `test_color_assignment_consistency` | Color persistence | Same user always gets the same color |
| `test_color_assignment_different_users` | Color variety | Different users get different colors |

**Expected Results:** All 5 tests should pass, confirming that the color coding system works as designed.

### 3. Server Tests (`TestChatServer`)

**Purpose:** Validate server initialization and core functionality.

| Test Name | Description | Validates |
|-----------|-------------|-----------|
| `test_server_initialization` | Server setup | Server initializes with correct port, folders, logging |
| `test_broadcast_message_encryption` | Broadcast functionality | Messages are encrypted before broadcasting |

**Expected Results:** All 2 tests should pass, confirming server starts correctly and can encrypt messages.

### 4. File Operation Tests (`TestFileOperations`)

**Purpose:** Validate file handling capabilities.

| Test Name | Description | Validates |
|-----------|-------------|-----------|
| `test_file_exists` | File I/O | Reading and writing files works |
| `test_base64_encoding` | Base64 encoding | File data can be encoded/decoded for transfer |

**Expected Results:** All 2 tests should pass, confirming file operations work correctly.

### 5. Integration Tests (`TestIntegration`)

**Purpose:** Validate system-level functionality.

| Test Name | Description | Validates |
|-----------|-------------|-----------|
| `test_server_starts_and_stops` | Server lifecycle | Server can start and stop cleanly |
| `test_timestamp_format` | Timestamp utility | Timestamp format is correct (HH:MM:SS) |

**Expected Results:** All 2 tests should pass, confirming basic integration works.

### 6. Utility Tests (`TestUtilityFunctions`)

**Purpose:** Validate helper functions.

| Test Name | Description | Validates |
|-----------|-------------|-----------|
| `test_timestamp_returns_string` | Return type | Timestamp function returns a string |
| `test_timestamp_format` | Format validation | Timestamp components are valid |

**Expected Results:** All 2 tests should pass, confirming utility functions work correctly.

## Test Coverage Summary

```
Total Tests: 20
├── Encryption Tests: 7
├── Client Tests: 5
├── Server Tests: 2
├── File Operation Tests: 2
├── Integration Tests: 2
└── Utility Tests: 2
```

## Expected Output

When all tests pass, you should see:

```
----------------------------------------------------------------------
Ran 20 tests in 0.4s

OK

======================================================================
Tests run: 20
Successes: 20
Failures: 0
Errors: 0
======================================================================
```

## Dependencies

### Required
- Python 3.6+
- OpenSSL command-line tool
- Standard Python libraries: `unittest`, `socket`, `threading`, `tempfile`, `base64`

### Optional
- `pytest` - For alternative test runner
- `pytest-cov` - For coverage reporting

## Test Environment

Tests create temporary directories and files during execution:
- Temporary directories are created using Python's `tempfile` module
- All temporary files are cleaned up after tests complete
- Tests run in isolated environments to prevent interference

## Continuous Integration

These tests are designed to be run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    cd vibe-cozy-chat
    python3 test_chat.py
```

## Troubleshooting

### OpenSSL Errors

If you see OpenSSL-related errors:
- Ensure OpenSSL is installed: `openssl version`
- Check that `openssl` is in your PATH
- Verify OpenSSL supports AES-256-CBC: `openssl enc -list`

### Import Errors

If you see import errors:
- Ensure you're running tests from the correct directory
- Check that `cozy_secure_chat.py` is in the same directory as `test_chat.py`

### Test Failures

If tests fail:
1. Check the error message for specific failure details
2. Verify your Python version: `python3 --version`
3. Ensure all dependencies are installed
4. Check that no other processes are using test ports (5555, 5556, 6000)

## Contributing

When adding new features to the chat application:
1. Write tests for the new functionality
2. Ensure all existing tests still pass
3. Update this documentation with new test descriptions
4. Run the full test suite before submitting changes

## Test Maintenance

- Tests should be run before each release
- Add new tests when bugs are discovered
- Keep test documentation up to date
- Review and refactor tests periodically

## Contact

For issues with tests or test documentation, please refer to the main project documentation or submit an issue report.

---

**Last Updated:** November 2, 2025  
**Test Suite Version:** 1.0  
**Compatibility:** Python 3.6+