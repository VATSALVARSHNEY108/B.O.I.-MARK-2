# 🛡️ Enhanced Security Features

## Overview

BOI (Barely Obeys Instructions) Assistant now includes a comprehensive security suite with multiple layers of protection:

1. **Biometric Authentication** 🔐
2. **Two-Factor Authentication (2FA)** 🔑
3. **Encrypted Storage** 🔒
4. **Activity Monitoring** 👁️
5. **Sandbox Mode** 🧪

---

## 1. Biometric Authentication

### Features
- **Face Recognition** using OpenCV with LBPH algorithm
- **Fingerprint Authentication** framework (hardware sensor support)
- Enrollment with multiple face samples (30+ for accuracy)
- Configurable confidence threshold
- Session management with timeout

### Usage

```python
from enhanced_biometric_auth import BiometricAuthenticationSystem

bio_auth = BiometricAuthenticationSystem()

# Enroll a user
result = bio_auth.enroll_face("user123", "John Doe", num_samples=30)

# Authenticate
auth_result = bio_auth.authenticate_face(confidence_threshold=70)

if auth_result["success"]:
    print(f"Welcome {auth_result['user_name']}!")
```

### Configuration
- Confidence threshold: Lower = more strict (default: 70)
- Session timeout: 30 minutes (configurable)
- Max failed attempts: 3 before lockout

---

## 2. Two-Factor Authentication (2FA)

### Features
- **TOTP** (Time-Based One-Time Password) compatible with:
  - Google Authenticator
  - Authy
  - Microsoft Authenticator
  - Any RFC 6238 compliant app
- QR code generation for easy setup
- Backup recovery codes (10 codes per user)
- Code regeneration support

### Usage

```python
from two_factor_authentication import TwoFactorAuthentication

tfa = TwoFactorAuthentication(app_name="BOI (Barely Obeys Instructions)")

# Enable 2FA for a user
result = tfa.enable_2fa("user123", "user@example.com")

# User scans QR code from: result['qr_code_path']
# Save backup codes: result['backup_codes']

# Verify TOTP token
verification = tfa.verify_totp("user123", "123456")

if verification["success"]:
    print("2FA verified!")
```

### Setup Steps
1. Enable 2FA for user → generates secret & QR code
2. User scans QR code with authenticator app
3. User enters 6-digit code to verify setup
4. Save backup codes in secure location

---

## 3. Encrypted Storage

### Features
- **AES-256-GCM** encryption for all data files
- Transparent encryption/decryption
- Password-based key derivation (PBKDF2)
- Encrypted backups with integrity verification
- Support for JSON, TXT, DAT, LOG files

### Usage

```python
from encrypted_storage_manager import EncryptedStorageManager

storage = EncryptedStorageManager(master_password="secure_password")

# Encrypt a single file
result = storage.encrypt_file("sensitive_data.json", keep_original=False)

# Encrypt entire directory
result = storage.encrypt_directory("data/", recursive=True)

# Decrypt file
result = storage.decrypt_file("sensitive_data.json.encrypted")

# Create encrypted backup
backup = storage.create_encrypted_backup(
    ["file1.json", "file2.txt"],
    backup_name="important_backup"
)

# Enable auto-encryption
storage.enable_auto_encryption()
```

### Security Features
- 480,000 PBKDF2 iterations (OWASP 2025 recommendation)
- SHA-256 checksums for integrity verification
- Secure key storage with file permissions (chmod 600)
- Automatic backup rotation

---

## 4. Activity Monitoring

### Features
- Real-time process monitoring
- Failed authentication tracking
- Unusual activity detection
- Resource usage alerts (CPU/Memory)
- Automated threat response
- Comprehensive activity logging

### Threat Detection
- Multiple failed login attempts
- Suspicious process names (hack, crack, malware, etc.)
- High CPU/Memory usage (>90% for 5+ minutes)
- Rapid file access patterns
- Privilege escalation attempts

### Usage

```python
from activity_monitoring import ActivityMonitoringSystem

monitor = ActivityMonitoringSystem()

# Start monitoring
monitor.start_monitoring()

# Log custom activity
monitor.log_activity(
    "file_access",
    {"path": "/etc/passwd", "action": "read"},
    user_id="user123"
)

# Get threat summary
threats = monitor.get_threat_summary(hours=24)
print(f"Threats in last 24h: {threats['total_threats']}")

# Enable auto-response
monitor.enable_auto_response()

# Block suspicious processes
monitor.add_blocked_process("malicious_app")
```

### Risk Levels
- **Low**: Normal activity
- **Medium**: Potentially suspicious
- **High**: Likely security issue
- **Critical**: Immediate threat requiring action

---

## 5. Sandbox Mode

### Features
- Isolated test environment
- Command simulation (no actual execution)
- Virtual filesystem
- Session-based testing
- Rollback capabilities
- Safe command whitelisting

### Usage

```python
from sandbox_mode import SandboxMode

sandbox = SandboxMode()

# Start sandbox session
session = sandbox.start_sandbox("test_automation")

# Simulate command execution
result = sandbox.execute_command("rm -rf /important_data", simulate=True)
# Output: [SIMULATED] Command would execute: rm -rf /important_data

# Create virtual files for testing
sandbox.create_virtual_file("test.txt", "Test content")

# Execute safe commands
sandbox.execute_command("echo 'Hello World'", simulate=False)

# Get session log
log = sandbox.get_session_log()

# Rollback all changes
sandbox.rollback_session()

# End session
sandbox.end_sandbox(keep_session=False)
```

### Safety Features
- Blocked dangerous commands (rm -rf, format, shutdown, etc.)
- Safe command whitelist (echo, ls, cat, grep, etc.)
- Virtual filesystem isolation
- Command logging for audit
- Automatic rollback on errors

---

## Security Dashboard

### Unified Management

```python
from security_dashboard import SecurityDashboard

dashboard = SecurityDashboard(app_name="BOI (Barely Obeys Instructions)")

# Enroll user with all security features
enrollment = dashboard.enroll_user(
    "user123",
    "user@example.com",
    enroll_biometric=True,
    enable_2fa=True
)

# Authenticate with multiple factors
auth = dashboard.authenticate_user(
    "user123",
    use_biometric=True,
    use_2fa=True,
    totp_token="123456"
)

# Enable full security suite
dashboard.enable_full_security("user123", "user@example.com")

# Generate security report
print(dashboard.generate_security_report())

# Get comprehensive status
status = dashboard.get_comprehensive_security_status()
```

### Security Report Example

```
╔══════════════════════════════════════════════════════════════╗
║          🛡️  SECURITY DASHBOARD REPORT                       ║
╚══════════════════════════════════════════════════════════════╝

📋 Application: BOI (Barely Obeys Instructions) Assistant
🔒 Security Level: MAXIMUM
👤 Current User: user123
✓ Authenticated: True

╔══════════════════════════════════════════════════════════════╗
║  BIOMETRIC AUTHENTICATION                                    ║
╚══════════════════════════════════════════════════════════════╝
• Enrolled Users: 5
• Total Attempts: 127
• Success Rate: 94.5%

╔══════════════════════════════════════════════════════════════╗
║  TWO-FACTOR AUTHENTICATION (2FA)                             ║
╚══════════════════════════════════════════════════════════════╝
• Total Users: 5
• Enabled Users: 5
• Success Rate: 98.2%

... [Additional sections]
```

---

## Best Practices

### 1. Biometric Authentication
- Enroll in good lighting conditions
- Capture diverse face angles (30+ samples recommended)
- Re-enroll if accuracy drops
- Use appropriate confidence threshold (70-80 for balance)

### 2. Two-Factor Authentication
- **Always save backup codes** in secure location
- Regenerate backup codes after using 5+ codes
- Don't share TOTP secrets
- Use valid_window=1 for clock drift tolerance

### 3. Encrypted Storage
- Use strong master password (12+ characters)
- Never store master password in code
- Create regular encrypted backups
- Test decryption before deleting originals

### 4. Activity Monitoring
- Review threat logs daily
- Adjust thresholds based on normal usage
- Whitelist known safe processes
- Enable auto-response only after testing

### 5. Sandbox Mode
- Always test new automations in sandbox first
- Review session logs before production
- Keep important sessions for reference
- Use rollback liberally during testing

---

## Security Levels

### Low Security
- Password only
- Basic activity logging

### Medium Security (Default)
- 2FA required
- Activity monitoring enabled
- Encrypted storage optional

### High Security
- Biometric OR 2FA required
- All files encrypted at rest
- Real-time threat monitoring
- Auto-response enabled

### Maximum Security
- Biometric AND 2FA required
- All data encrypted
- Continuous monitoring
- Auto-response + sandbox mode

---

## Troubleshooting

### Biometric Authentication Issues
**Problem**: Face not recognized
- **Solution**: Increase confidence threshold or re-enroll with more samples

**Problem**: Camera not accessible
- **Solution**: Check camera permissions and ensure no other app is using it

### 2FA Issues
**Problem**: TOTP code rejected
- **Solution**: Check system time synchronization (TOTP is time-sensitive)

**Problem**: Lost authenticator device
- **Solution**: Use backup recovery codes

### Encrypted Storage Issues
**Problem**: Decryption fails
- **Solution**: Verify master password and ensure key file exists

**Problem**: Encrypted files corrupted
- **Solution**: Restore from encrypted backup

### Activity Monitoring Issues
**Problem**: Too many false positives
- **Solution**: Adjust threat thresholds and whitelist known processes

**Problem**: High CPU usage
- **Solution**: Increase monitoring interval (edit _monitoring_loop sleep time)

---

## API Reference

### BiometricAuthenticationSystem
- `enroll_face(user_id, user_name, num_samples=30)`
- `authenticate_face(confidence_threshold=70)`
- `enroll_fingerprint(user_id, user_name, fingerprint_data)`
- `authenticate_fingerprint(fingerprint_data)`
- `is_session_valid()`
- `logout()`
- `get_authentication_stats()`

### TwoFactorAuthentication
- `enable_2fa(user_id, user_email)`
- `verify_totp(user_id, token, mark_verified=True)`
- `verify_backup_code(user_id, backup_code)`
- `regenerate_backup_codes(user_id, current_token)`
- `disable_2fa(user_id, token)`
- `get_user_status(user_id)`
- `get_statistics()`

### EncryptedStorageManager
- `encrypt_file(file_path, keep_original=True)`
- `decrypt_file(encrypted_file_path, output_path=None)`
- `encrypt_directory(directory_path, recursive=True)`
- `decrypt_directory(directory_path, recursive=True)`
- `create_encrypted_backup(source_files, backup_name=None)`
- `restore_backup(backup_name, restore_path)`
- `enable_auto_encryption()`
- `get_encryption_status()`

### ActivityMonitoringSystem
- `start_monitoring()`
- `stop_monitoring()`
- `log_activity(activity_type, details, user_id=None)`
- `get_threat_summary(hours=24)`
- `get_activity_stats()`
- `add_blocked_process(process_name)`
- `enable_auto_response()`

### SandboxMode
- `start_sandbox(session_name=None)`
- `execute_command(command, simulate=True)`
- `create_virtual_file(filename, content)`
- `read_virtual_file(filename)`
- `list_virtual_files()`
- `get_session_log()`
- `rollback_session()`
- `end_sandbox(keep_session=False)`

### SecurityDashboard
- `authenticate_user(user_id, use_biometric, use_2fa, totp_token)`
- `enroll_user(user_id, user_email, enroll_biometric, enable_2fa)`
- `enable_full_security(user_id, user_email)`
- `get_comprehensive_security_status()`
- `generate_security_report()`
- `logout()`

---

## License

These security features are part of the BOI (Barely Obeys Instructions) Assistant project.

## Support

For security-related issues or questions, please refer to the main project documentation.

---

**Remember**: Security is only as strong as its weakest link. Use all features together for maximum protection! 🛡️
