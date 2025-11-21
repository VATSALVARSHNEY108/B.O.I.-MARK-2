# 📱 Phone Link Notification Monitor

## Overview
Access and monitor your Phone Link notifications (SMS, calls, etc.) from BOI (Barely Obeys Instructions), batch files, or Python scripts!

---

## 🎯 Features

✅ **Read Phone Link Notifications** - Access SMS, calls, and missed call notifications  
✅ **Background Monitoring** - Automatically monitor for new notifications  
✅ **Command Line Access** - Use batch files to check notifications  
✅ **BOI Integration** - Ask BOI to read your messages  
✅ **Python API** - Full programmatic access to Phone Link notifications

---

## 🗣️ Voice Commands for BOI

Just say:

- **"Check phone notifications"** - Check for new notifications
- **"Read my messages"** - Same as above
- **"Show recent messages"** - Display recent notifications
- **"How many messages do I have?"** - Get notification counts
- **"Start monitoring notifications"** - Enable background monitoring
- **"Stop monitoring notifications"** - Disable monitoring

---

## 💻 Batch File Usage

Run the batch file from command line:

```batch
REM Check for new notifications
cd batch_scripts\automation
phone_link_notifications.bat check

REM Show recent notifications
phone_link_notifications.bat recent

REM Start continuous monitoring (Ctrl+C to stop)
phone_link_notifications.bat monitor

REM Show notification counts
phone_link_notifications.bat count

REM Clear stored notifications
phone_link_notifications.bat clear
```

---

## 🐍 Python API Usage

### Basic Usage

```python
from modules.communication.phone_link_monitor import PhoneLinkMonitor

# Create monitor
monitor = PhoneLinkMonitor()

# Check for new notifications
new_notifications = monitor.check_new_notifications()
for notif in new_notifications:
    print(f"{notif['type']}: {notif['message']}")

# Get recent notifications
recent = monitor.get_recent_notifications(limit=10)

# Get only SMS notifications
sms_only = monitor.get_recent_notifications(limit=5, notif_type='sms')

# Get notification counts
counts = monitor.get_unread_count()
print(f"Total: {counts['total']}")
print(f"By type: {counts['by_type']}")
```

### Background Monitoring

```python
from modules.communication.phone_link_monitor import PhoneLinkMonitor

def on_new_notification(notification):
    """Callback when new notification arrives"""
    print(f"📱 New {notification['type']}: {notification['message']}")

# Create monitor with callback
monitor = PhoneLinkMonitor(notification_callback=on_new_notification)

# Start monitoring (checks every 5 seconds)
monitor.start_monitoring(check_interval=5)

# Let it run...
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    monitor.stop_monitoring()
```

---

## 📊 Notification Types

The system detects these notification types:

- `sms` - Text messages
- `call` - Incoming calls
- `missed_call` - Missed calls
- `unknown` - Other notifications

---

## 📁 Data Storage

Notifications are automatically saved to:
```
data/phone_link_notifications/notifications.json
```

Up to 100 recent notifications are stored.

---

## ⚙️ How It Works

1. **Windows Action Center** - Reads notifications from Windows Action Center
2. **PowerShell** - Uses PowerShell to access notification APIs
3. **Filtering** - Filters for Phone Link specific notifications
4. **Parsing** - Extracts sender, message, title, and type
5. **Storage** - Saves to JSON for history

---

## 🔧 Requirements

- ✅ Windows 10/11
- ✅ Phone Link app installed and paired
- ✅ Phone connected to Phone Link
- ✅ Python 3.x

---

## 💡 Example Use Cases

### 1. Auto-Reply to Important Messages
```python
monitor = PhoneLinkMonitor()
new_sms = monitor.check_new_notifications()

for sms in new_sms:
    if sms['type'] == 'sms' and 'urgent' in sms['message'].lower():
        # Trigger auto-reply via BOI
        print(f"📱 Urgent message from {sms['sender']}")
```

### 2. Log All Notifications
```python
import logging

def log_notification(notif):
    logging.info(f"Phone notification: {notif['type']} - {notif['message']}")

monitor = PhoneLinkMonitor(notification_callback=log_notification)
monitor.start_monitoring()
```

### 3. Check Messages on Schedule
```python
import schedule

def check_messages():
    monitor = PhoneLinkMonitor()
    new_msgs = monitor.check_new_notifications()
    if new_msgs:
        print(f"📱 {len(new_msgs)} new messages!")

schedule.every(10).minutes.do(check_messages)
```

---

## 🚀 Quick Start

1. **Test from command line:**
   ```batch
   python scripts/phone_link_notifications_cli.py check
   ```

2. **Use batch file:**
   ```batch
   batch_scripts\automation\phone_link_notifications.bat recent
   ```

3. **Ask BOI:**
   ```
   "Check my phone notifications"
   ```

---

## 🐛 Troubleshooting

**No notifications found?**
- Ensure Phone Link is installed and running
- Make sure your phone is connected
- Try sending a test SMS to your phone first

**Notifications not updating?**
- Phone Link must be actively syncing
- Check Windows Action Center has notifications
- Restart Phone Link app

**PowerShell errors?**
- Run as Administrator if needed
- Check PowerShell execution policy
- Ensure Windows notifications are enabled

---

## 📝 Notes

- Notifications are read-only (can't send replies yet)
- Requires active Phone Link connection
- Limited to notifications in Windows Action Center
- Some notification details may be limited by Phone Link

---

## 🎉 Enjoy!

You can now monitor your phone notifications directly from your desktop using BOI, batch files, or Python!
