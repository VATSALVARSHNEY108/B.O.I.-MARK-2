#!/usr/bin/env python3
"""
Phone Link Notifications CLI
Command-line interface for Phone Link notification monitoring
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from modules.communication.phone_link_monitor import PhoneLinkMonitor


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "check"
    
    monitor = PhoneLinkMonitor()
    
    if action == "check":
        print("🔍 Checking for new notifications...")
        new_notifs = monitor.check_new_notifications()
        
        if new_notifs:
            print(f"✅ Found {len(new_notifs)} new notification(s):")
            for notif in new_notifs:
                print(f"\n📱 {notif['type'].upper()}")
                print(f"   Title: {notif['title']}")
                print(f"   Message: {notif['message']}")
                print(f"   Sender: {notif['sender']}")
        else:
            print("ℹ️ No new notifications")
    
    elif action == "recent":
        recent = monitor.get_recent_notifications(10)
        print(f"📋 Recent notifications ({len(recent)}):")
        for i, notif in enumerate(recent, 1):
            print(f"\n{i}. {notif['type'].upper()} - {notif.get('timestamp', 'N/A')}")
            print(f"   {notif['title']}")
            print(f"   {notif['message']}")
    
    elif action == "monitor":
        print("📱 Starting continuous monitoring... (Press Ctrl+C to stop)")
        monitor.start_monitoring(5)
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            print("\n✅ Monitoring stopped")
    
    elif action == "clear":
        monitor.clear_notifications()
        print("✅ Notifications cleared")
    
    elif action == "count":
        counts = monitor.get_unread_count()
        print(f"📊 Total notifications: {counts['total']}")
        print("By type:")
        for notif_type, count in counts['by_type'].items():
            print(f"  • {notif_type}: {count}")
    
    else:
        print(f"❌ Unknown action: {action}")
        print("\nAvailable actions:")
        print("  check   - Check for new notifications")
        print("  recent  - Show recent notifications")
        print("  monitor - Start continuous monitoring")
        print("  count   - Show notification counts")
        print("  clear   - Clear stored notifications")


if __name__ == "__main__":
    main()
