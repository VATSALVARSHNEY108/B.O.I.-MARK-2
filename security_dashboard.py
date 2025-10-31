"""
🛡️ Security Dashboard
Central management for all enhanced security features
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from enhanced_biometric_auth import BiometricAuthenticationSystem
from two_factor_authentication import TwoFactorAuthentication
from encrypted_storage_manager import EncryptedStorageManager
from activity_monitoring import ActivityMonitoringSystem
from sandbox_mode import SandboxMode

class SecurityDashboard:
    """
    Unified security dashboard for managing all security features:
    - Biometric Authentication
    - Two-Factor Authentication (2FA)
    - Encrypted Storage
    - Activity Monitoring
    - Sandbox Mode
    """
    
    def __init__(self, app_name: str = "VATSAL AI Assistant"):
        self.app_name = app_name
        self.dashboard_dir = "security_dashboard"
        self.config_file = os.path.join(self.dashboard_dir, "dashboard_config.json")
        self.audit_log_file = os.path.join(self.dashboard_dir, "audit_log.json")
        
        os.makedirs(self.dashboard_dir, exist_ok=True)
        
        self.biometric_auth = BiometricAuthenticationSystem()
        self.two_factor_auth = TwoFactorAuthentication(app_name=app_name)
        self.encrypted_storage = EncryptedStorageManager()
        self.activity_monitor = ActivityMonitoringSystem()
        self.sandbox = SandboxMode()
        
        self.config = self._load_config()
        self.audit_log = self._load_audit_log()
        
        self.current_user = None
        self.authenticated = False
        self.auth_methods_used = []
    
    def _load_config(self) -> Dict:
        """Load dashboard configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "require_biometric": False,
            "require_2fa": True,
            "require_both": False,
            "auto_encrypt_enabled": False,
            "activity_monitoring_enabled": True,
            "sandbox_default_active": False,
            "session_timeout_minutes": 30,
            "security_level": "medium"
        }
    
    def _save_config(self):
        """Save dashboard configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _load_audit_log(self) -> List:
        """Load security audit log"""
        if os.path.exists(self.audit_log_file):
            try:
                with open(self.audit_log_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_audit_log(self):
        """Save security audit log"""
        try:
            with open(self.audit_log_file, 'w') as f:
                json.dump(self.audit_log[-500:], f, indent=2)
        except Exception as e:
            print(f"Error saving audit log: {e}")
    
    def _log_audit_event(self, event_type: str, details: Dict, severity: str = "info"):
        """Log security audit event"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user": self.current_user,
            "severity": severity,
            "details": details
        }
        self.audit_log.append(entry)
        self._save_audit_log()
    
    def authenticate_user(self, user_id: str, use_biometric: bool = False, use_2fa: bool = False, totp_token: Optional[str] = None) -> Dict:
        """
        Authenticate user using configured security methods
        
        Args:
            user_id: User identifier
            use_biometric: Use biometric authentication
            use_2fa: Use two-factor authentication
            totp_token: 2FA TOTP token if using 2FA
        
        Returns:
            Dict with authentication result
        """
        print("\n🔐 Starting Enhanced Authentication")
        print("=" * 50)
        
        auth_results = {
            "biometric": None,
            "2fa": None
        }
        
        if use_biometric or self.config["require_biometric"]:
            print("\n👤 Step 1: Biometric Authentication")
            bio_result = self.biometric_auth.authenticate_face()
            auth_results["biometric"] = bio_result
            
            if not bio_result["success"]:
                self._log_audit_event(
                    "authentication_failed",
                    {"method": "biometric", "user_id": user_id},
                    "warning"
                )
                return {
                    "success": False,
                    "message": "Biometric authentication failed",
                    "auth_results": auth_results
                }
            
            self.auth_methods_used.append("biometric")
            print(f"✅ Biometric authentication successful")
        
        if use_2fa or self.config["require_2fa"]:
            print("\n🔑 Step 2: Two-Factor Authentication")
            
            if totp_token:
                tfa_result = self.two_factor_auth.verify_totp(user_id, totp_token)
                auth_results["2fa"] = tfa_result
                
                if not tfa_result["success"]:
                    self._log_audit_event(
                        "authentication_failed",
                        {"method": "2fa", "user_id": user_id},
                        "warning"
                    )
                    return {
                        "success": False,
                        "message": "2FA verification failed",
                        "auth_results": auth_results
                    }
                
                self.auth_methods_used.append("2fa")
                print(f"✅ 2FA authentication successful")
            else:
                return {
                    "success": False,
                    "message": "2FA token required but not provided",
                    "auth_results": auth_results
                }
        
        self.authenticated = True
        self.current_user = user_id
        
        self._log_audit_event(
            "authentication_success",
            {
                "user_id": user_id,
                "methods": self.auth_methods_used
            },
            "info"
        )
        
        if self.config["activity_monitoring_enabled"]:
            self.activity_monitor.start_monitoring()
        
        print(f"\n✅ Authentication Complete!")
        print(f"   User: {user_id}")
        print(f"   Methods: {', '.join(self.auth_methods_used)}")
        
        return {
            "success": True,
            "user_id": user_id,
            "auth_methods": self.auth_methods_used,
            "message": "Authentication successful"
        }
    
    def enroll_user(self, user_id: str, user_email: str, enroll_biometric: bool = True, enable_2fa: bool = True) -> Dict:
        """
        Enroll a new user with security features
        
        Args:
            user_id: Unique user identifier
            user_email: User email address
            enroll_biometric: Enroll biometric authentication
            enable_2fa: Enable two-factor authentication
        
        Returns:
            Dict with enrollment results
        """
        print(f"\n📝 Enrolling User: {user_email}")
        print("=" * 50)
        
        enrollment_results = {
            "biometric": None,
            "2fa": None
        }
        
        if enroll_biometric:
            print("\n👤 Biometric Enrollment")
            bio_result = self.biometric_auth.enroll_face(user_id, user_email)
            enrollment_results["biometric"] = bio_result
            
            if not bio_result["success"]:
                print(f"⚠️  Biometric enrollment warning: {bio_result['message']}")
        
        if enable_2fa:
            print("\n🔑 2FA Enrollment")
            tfa_result = self.two_factor_auth.enable_2fa(user_id, user_email)
            enrollment_results["2fa"] = tfa_result
            
            if tfa_result["success"]:
                print(f"\n📱 2FA Setup Instructions:")
                print(f"   1. Open your authenticator app")
                print(f"   2. Scan the QR code saved at: {tfa_result['qr_code_path']}")
                print(f"   3. Save these backup codes:")
                for i, code in enumerate(tfa_result['backup_codes'], 1):
                    print(f"      {i}. {code}")
        
        self._log_audit_event(
            "user_enrolled",
            {
                "user_id": user_id,
                "email": user_email,
                "biometric_enrolled": enrollment_results["biometric"]["success"] if enrollment_results["biometric"] else False,
                "2fa_enabled": enrollment_results["2fa"]["success"] if enrollment_results["2fa"] else False
            },
            "info"
        )
        
        print(f"\n✅ User Enrollment Complete!")
        
        return {
            "success": True,
            "enrollment_results": enrollment_results,
            "message": "User enrolled successfully"
        }
    
    def get_comprehensive_security_status(self) -> Dict:
        """Get comprehensive security status across all features"""
        biometric_stats = self.biometric_auth.get_authentication_stats()
        tfa_stats = self.two_factor_auth.get_statistics()
        storage_status = self.encrypted_storage.get_encryption_status()
        activity_stats = self.activity_monitor.get_activity_stats()
        threat_summary = self.activity_monitor.get_threat_summary(hours=24)
        sandbox_status = self.sandbox.get_sandbox_status()
        
        return {
            "dashboard_info": {
                "app_name": self.app_name,
                "security_level": self.config["security_level"],
                "current_user": self.current_user,
                "authenticated": self.authenticated
            },
            "biometric_authentication": {
                "enrolled_users": biometric_stats["enrolled_users_count"],
                "total_attempts": biometric_stats["total_attempts"],
                "success_rate": biometric_stats["success_rate"]
            },
            "two_factor_authentication": {
                "total_users": tfa_stats["total_users"],
                "enabled_users": tfa_stats["enabled_users"],
                "success_rate": tfa_stats["success_rate"]
            },
            "encrypted_storage": {
                "enabled": storage_status["enabled"],
                "encrypted_files": storage_status["encrypted_files_count"],
                "algorithm": storage_status["algorithm"]
            },
            "activity_monitoring": {
                "active": activity_stats["monitoring_active"],
                "total_activities": activity_stats["total_activities_logged"],
                "threats_detected": activity_stats["total_threats_detected"]
            },
            "threat_summary_24h": {
                "total_threats": threat_summary["total_threats"],
                "critical": threat_summary["critical_threats"],
                "high": threat_summary["high_threats"]
            },
            "sandbox": {
                "active": sandbox_status["active"],
                "session_id": sandbox_status["session_id"]
            }
        }
    
    def enable_full_security(self, user_id: str, user_email: str) -> Dict:
        """
        Enable all security features at once
        
        Args:
            user_id: User identifier
            user_email: User email
        
        Returns:
            Dict with setup results
        """
        print("\n🛡️  Enabling Full Security Suite")
        print("=" * 60)
        
        enrollment = self.enroll_user(user_id, user_email, enroll_biometric=True, enable_2fa=True)
        
        self.encrypted_storage.enable_auto_encryption()
        
        self.activity_monitor.start_monitoring()
        self.activity_monitor.enable_auto_response()
        
        self.config["require_biometric"] = True
        self.config["require_2fa"] = True
        self.config["auto_encrypt_enabled"] = True
        self.config["activity_monitoring_enabled"] = True
        self.config["security_level"] = "maximum"
        self._save_config()
        
        self._log_audit_event(
            "full_security_enabled",
            {"user_id": user_id, "email": user_email},
            "info"
        )
        
        print("\n✅ Full Security Suite Enabled!")
        print("   ✓ Biometric Authentication")
        print("   ✓ Two-Factor Authentication")
        print("   ✓ Encrypted Storage")
        print("   ✓ Activity Monitoring")
        print("   ✓ Sandbox Mode Available")
        
        return {
            "success": True,
            "enrollment": enrollment,
            "security_level": "maximum",
            "message": "Full security suite enabled successfully"
        }
    
    def generate_security_report(self) -> str:
        """Generate comprehensive security report"""
        status = self.get_comprehensive_security_status()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          🛡️  SECURITY DASHBOARD REPORT                       ║
╚══════════════════════════════════════════════════════════════╝

📋 Application: {status['dashboard_info']['app_name']}
🔒 Security Level: {status['dashboard_info']['security_level'].upper()}
👤 Current User: {status['dashboard_info']['current_user'] or 'Not Authenticated'}
✓ Authenticated: {status['dashboard_info']['authenticated']}

╔══════════════════════════════════════════════════════════════╗
║  BIOMETRIC AUTHENTICATION                                    ║
╚══════════════════════════════════════════════════════════════╝
• Enrolled Users: {status['biometric_authentication']['enrolled_users']}
• Total Attempts: {status['biometric_authentication']['total_attempts']}
• Success Rate: {status['biometric_authentication']['success_rate']:.1f}%

╔══════════════════════════════════════════════════════════════╗
║  TWO-FACTOR AUTHENTICATION (2FA)                             ║
╚══════════════════════════════════════════════════════════════╝
• Total Users: {status['two_factor_authentication']['total_users']}
• Enabled Users: {status['two_factor_authentication']['enabled_users']}
• Success Rate: {status['two_factor_authentication']['success_rate']:.1f}%

╔══════════════════════════════════════════════════════════════╗
║  ENCRYPTED STORAGE                                           ║
╚══════════════════════════════════════════════════════════════╝
• Status: {'ENABLED' if status['encrypted_storage']['enabled'] else 'DISABLED'}
• Encrypted Files: {status['encrypted_storage']['encrypted_files']}
• Algorithm: {status['encrypted_storage']['algorithm']}

╔══════════════════════════════════════════════════════════════╗
║  ACTIVITY MONITORING                                         ║
╚══════════════════════════════════════════════════════════════╝
• Monitoring: {'ACTIVE' if status['activity_monitoring']['active'] else 'INACTIVE'}
• Total Activities: {status['activity_monitoring']['total_activities']}
• Threats Detected: {status['activity_monitoring']['threats_detected']}

╔══════════════════════════════════════════════════════════════╗
║  THREAT SUMMARY (Last 24 Hours)                              ║
╚══════════════════════════════════════════════════════════════╝
• Total Threats: {status['threat_summary_24h']['total_threats']}
• Critical: {status['threat_summary_24h']['critical']}
• High: {status['threat_summary_24h']['high']}

╔══════════════════════════════════════════════════════════════╗
║  SANDBOX MODE                                                ║
╚══════════════════════════════════════════════════════════════╝
• Status: {'ACTIVE' if status['sandbox']['active'] else 'INACTIVE'}
• Session: {status['sandbox']['session_id'] or 'None'}

╔══════════════════════════════════════════════════════════════╗
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return report
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            self._log_audit_event(
                "user_logout",
                {"user_id": self.current_user},
                "info"
            )
        
        self.current_user = None
        self.authenticated = False
        self.auth_methods_used = []
        
        self.biometric_auth.logout()
        
        print("🔓 Logged out successfully")


if __name__ == "__main__":
    print("🛡️  Security Dashboard")
    print("=" * 60)
    
    dashboard = SecurityDashboard()
    
    print(dashboard.generate_security_report())
    
    print("\n" + "=" * 60)
    print("✅ Security dashboard ready!")
