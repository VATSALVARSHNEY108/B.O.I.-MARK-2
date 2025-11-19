"""
Phone Link Notification Monitor
Monitors Windows notifications from Phone Link app (calls, SMS, etc.)
"""

import os
import json
import time
import subprocess
import threading
from datetime import datetime
from typing import Dict, List, Optional, Callable
from pathlib import Path


class PhoneLinkMonitor:
    """Monitor and read notifications from Windows Phone Link"""
    
    def __init__(self, notification_callback: Optional[Callable] = None):
        """
        Initialize Phone Link notification monitor
        
        Args:
            notification_callback: Optional callback function(notification_dict) to call when new notification arrives
        """
        self.is_windows = os.name == 'nt'
        self.notifications = []
        self.max_notifications = 100
        self.is_monitoring = False
        self.monitor_thread = None
        self.notification_callback = notification_callback
        
        # Create data directory for storing notifications
        self.data_dir = Path("data/phone_link_notifications")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.notifications_file = self.data_dir / "notifications.json"
        
        # Load existing notifications
        self._load_notifications()
        
        print("📱 Phone Link Monitor initialized")
    
    def _load_notifications(self):
        """Load notifications from file"""
        if self.notifications_file.exists():
            try:
                with open(self.notifications_file, 'r', encoding='utf-8') as f:
                    self.notifications = json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load notifications: {e}")
                self.notifications = []
    
    def _save_notifications(self):
        """Save notifications to file"""
        try:
            with open(self.notifications_file, 'w', encoding='utf-8') as f:
                json.dump(self.notifications[-self.max_notifications:], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Could not save notifications: {e}")
    
    def get_notifications_via_powershell(self) -> List[Dict]:
        """
        Get Windows notifications using PowerShell
        Reads from Windows Action Center
        """
        if not self.is_windows:
            return []
        
        # PowerShell script to read Action Center notifications
        ps_script = """
        Add-Type -AssemblyName System.Runtime.WindowsRuntime
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

        $notifications = @()
        
        try {
            # Get all toast notifications from Action Center
            $toastHistory = [Windows.UI.Notifications.ToastNotificationManager]::History
            $notifications = $toastHistory.GetHistory()
            
            foreach ($toast in $notifications) {
                $xml = $toast.Content.GetXml()
                
                # Extract app name
                $appId = $toast.Tag
                
                # Parse XML to get notification details
                Write-Output "---NOTIFICATION_START---"
                Write-Output "AppId: $($toast.Tag)"
                Write-Output "Group: $($toast.Group)"
                Write-Output "Time: $($toast.ExpirationTime)"
                Write-Output "XML: $xml"
                Write-Output "---NOTIFICATION_END---"
            }
        } catch {
            Write-Output "Error: $_"
        }
        """
        
        try:
            result = subprocess.run(
                ['powershell', '-Command', ps_script],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse the output
            notifications = []
            current_notif = {}
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                if line == "---NOTIFICATION_START---":
                    current_notif = {}
                elif line == "---NOTIFICATION_END---":
                    if current_notif:
                        notifications.append(current_notif)
                    current_notif = {}
                elif ': ' in line:
                    key, value = line.split(': ', 1)
                    current_notif[key] = value
            
            return notifications
            
        except Exception as e:
            print(f"⚠️ Error reading notifications: {e}")
            return []
    
    def get_phone_link_notifications(self) -> List[Dict]:
        """
        Get notifications specifically from Phone Link app
        Filters for SMS, calls, and other phone notifications
        """
        all_notifications = self.get_notifications_via_powershell()
        
        # Filter for Phone Link related notifications
        phone_notifications = []
        phone_link_identifiers = [
            'YourPhone',
            'Microsoft.YourPhone',
            'PhoneLink',
            'Windows.PhoneLink'
        ]
        
        for notif in all_notifications:
            app_id = notif.get('AppId', '')
            group = notif.get('Group', '')
            
            # Check if it's from Phone Link
            if any(identifier.lower() in app_id.lower() or identifier.lower() in group.lower() 
                   for identifier in phone_link_identifiers):
                phone_notifications.append(notif)
        
        return phone_notifications
    
    def parse_notification_content(self, notification: Dict) -> Dict:
        """
        Parse notification XML to extract useful information
        
        Args:
            notification: Raw notification dict with XML
            
        Returns:
            Parsed notification with title, message, sender, etc.
        """
        parsed = {
            'timestamp': notification.get('Time', datetime.now().isoformat()),
            'app': notification.get('AppId', 'Unknown'),
            'group': notification.get('Group', ''),
            'type': 'unknown',
            'title': '',
            'message': '',
            'sender': '',
            'raw_xml': notification.get('XML', '')
        }
        
        # Try to parse XML content
        xml_content = notification.get('XML', '')
        
        # Simple XML parsing (looking for common tags)
        if '<text>' in xml_content:
            # Extract text elements
            import re
            text_matches = re.findall(r'<text[^>]*>([^<]+)</text>', xml_content)
            
            if len(text_matches) >= 1:
                parsed['title'] = text_matches[0]
            if len(text_matches) >= 2:
                parsed['message'] = text_matches[1]
            if len(text_matches) >= 3:
                parsed['sender'] = text_matches[2]
        
        # Determine notification type based on content
        if 'call' in xml_content.lower() or 'calling' in xml_content.lower():
            parsed['type'] = 'call'
        elif 'sms' in xml_content.lower() or 'message' in xml_content.lower():
            parsed['type'] = 'sms'
        elif 'missed' in xml_content.lower():
            parsed['type'] = 'missed_call'
        
        return parsed
    
    def check_new_notifications(self) -> List[Dict]:
        """
        Check for new Phone Link notifications
        Returns only new notifications since last check
        """
        current_notifications = self.get_phone_link_notifications()
        
        # Parse all notifications
        parsed_notifications = [
            self.parse_notification_content(n) 
            for n in current_notifications
        ]
        
        # Filter for new ones
        existing_ids = {
            f"{n.get('timestamp')}_{n.get('message')}" 
            for n in self.notifications
        }
        
        new_notifications = [
            n for n in parsed_notifications
            if f"{n.get('timestamp')}_{n.get('message')}" not in existing_ids
        ]
        
        # Add new notifications to history
        if new_notifications:
            self.notifications.extend(new_notifications)
            self.notifications = self.notifications[-self.max_notifications:]
            self._save_notifications()
            
            # Call callback if provided
            if self.notification_callback:
                for notif in new_notifications:
                    try:
                        self.notification_callback(notif)
                    except Exception as e:
                        print(f"⚠️ Notification callback error: {e}")
        
        return new_notifications
    
    def start_monitoring(self, check_interval: int = 5):
        """
        Start monitoring for new notifications in background
        
        Args:
            check_interval: Seconds between checks (default: 5)
        """
        if self.is_monitoring:
            return {"success": False, "message": "Already monitoring"}
        
        def monitor_loop():
            print(f"📱 Started monitoring Phone Link notifications (checking every {check_interval}s)")
            while self.is_monitoring:
                try:
                    new_notifs = self.check_new_notifications()
                    if new_notifs:
                        print(f"📱 {len(new_notifs)} new Phone Link notification(s)")
                        for notif in new_notifs:
                            print(f"  📨 {notif['type']}: {notif['title']} - {notif['message']}")
                except Exception as e:
                    print(f"⚠️ Monitor error: {e}")
                
                time.sleep(check_interval)
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        return {
            "success": True,
            "message": f"Monitoring started (interval: {check_interval}s)"
        }
    
    def stop_monitoring(self):
        """Stop monitoring for notifications"""
        if not self.is_monitoring:
            return {"success": False, "message": "Not currently monitoring"}
        
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        
        return {"success": True, "message": "Monitoring stopped"}
    
    def get_recent_notifications(self, limit: int = 10, notif_type: Optional[str] = None) -> List[Dict]:
        """
        Get recent notifications
        
        Args:
            limit: Maximum number to return
            notif_type: Filter by type ('sms', 'call', 'missed_call', etc.)
        
        Returns:
            List of recent notifications
        """
        notifications = self.notifications
        
        # Filter by type if specified
        if notif_type:
            notifications = [n for n in notifications if n.get('type') == notif_type]
        
        return notifications[-limit:]
    
    def get_unread_count(self) -> Dict:
        """Get count of unread messages by type"""
        # Count notifications by type
        type_counts = {}
        for notif in self.notifications:
            notif_type = notif.get('type', 'unknown')
            type_counts[notif_type] = type_counts.get(notif_type, 0) + 1
        
        return {
            "success": True,
            "total": len(self.notifications),
            "by_type": type_counts
        }
    
    def clear_notifications(self) -> Dict:
        """Clear all stored notifications"""
        self.notifications = []
        self._save_notifications()
        return {"success": True, "message": "Notifications cleared"}


def create_phone_link_monitor(callback: Optional[Callable] = None):
    """Factory function to create PhoneLinkMonitor instance"""
    return PhoneLinkMonitor(notification_callback=callback)


# For testing
if __name__ == "__main__":
    print("📱 Phone Link Notification Monitor Test")
    print("=" * 60)
    
    monitor = PhoneLinkMonitor()
    
    # Check for notifications
    print("\n🔍 Checking for Phone Link notifications...")
    notifications = monitor.get_phone_link_notifications()
    
    if notifications:
        print(f"✅ Found {len(notifications)} notifications:")
        for i, notif in enumerate(notifications[:5], 1):
            parsed = monitor.parse_notification_content(notif)
            print(f"\n{i}. {parsed['type'].upper()}")
            print(f"   Title: {parsed['title']}")
            print(f"   Message: {parsed['message']}")
            print(f"   Sender: {parsed['sender']}")
            print(f"   Time: {parsed['timestamp']}")
    else:
        print("ℹ️ No Phone Link notifications found")
    
    # Show recent stored notifications
    recent = monitor.get_recent_notifications(5)
    if recent:
        print(f"\n📋 Recent notifications ({len(recent)}):")
        for notif in recent:
            print(f"  • {notif['type']}: {notif['message']}")
