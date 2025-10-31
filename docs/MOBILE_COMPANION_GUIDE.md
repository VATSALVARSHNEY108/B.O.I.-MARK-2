# 📱 VATSAL Mobile Companion - Complete Guide

Control your VATSAL AI Desktop Automation system from your phone!

## ✨ Features

### 🎮 Remote Control
- Execute any VATSAL command from your mobile device
- Voice commands via mobile (text-based or audio)
- Real-time command execution feedback
- Command history and activity tracking

### ⚡ Quick Actions & Shortcuts
Pre-configured one-tap actions for common tasks:

**🔒 Security:**
- Lock Screen - Instantly secure your computer

**⚡ Power:**
- Shutdown - Shut down your computer
- Restart - Restart your computer
- Sleep - Put computer to sleep

**🎵 Media Control:**
- Volume Up/Down - Control system volume
- Mute - Toggle mute
- Play/Pause Music - Control Spotify playback
- Next/Previous Track - Skip songs

**📊 Productivity:**
- Start Pomodoro - Begin a focus session
- Focus Mode - Activate focus mode
- Weather - Check weather

**📸 Utilities:**
- Take Screenshot - Capture your screen
- Open Browser - Launch Chrome

### 📸 Remote Screenshot Viewing
- Live screenshot capture from your desktop
- Optimized image compression for mobile
- Cached screenshots for quick viewing
- Adjustable quality and size settings

### 📊 System Monitoring
Real-time system stats:
- CPU usage percentage
- Memory utilization
- Disk space
- Battery status (if available)
- Network activity

### 🔔 Push Notifications
Get notified about important events:
- Command completion/failure alerts
- System alerts and errors
- Security notifications
- Custom reminders and events

**Notification Channels:**
- SMS via Twilio
- Email notifications
- Webhook notifications (custom integrations)

### 🔐 Security & Authentication
- PIN-based authentication
- Secure token system (24-hour expiration)
- API key support for third-party integrations
- Session management and revocation

### 📡 Real-Time Updates
- WebSocket-based live updates
- Instant notification of command execution
- Live system stats updates every 2 seconds
- Activity feed with recent actions

---

## 🚀 Quick Start

### 1. Start the Mobile Companion Server

The mobile companion server combines WebSocket and Mobile API:

```bash
python mobile_companion_server.py
```

This will start:
- Mobile interface at: `http://your-replit-url.repl.co/mobile`
- Desktop dashboard at: `http://your-replit-url.repl.co`
- WebSocket server for real-time updates
- Mobile API with authentication

### 2. Access from Your Phone

**Option A: Direct URL Access**
1. Open your phone's web browser
2. Navigate to: `https://your-replit-url.repl.co/mobile`
3. Bookmark for quick access

**Option B: Add to Home Screen (iOS/Android)**
1. Open the mobile URL in Safari (iOS) or Chrome (Android)
2. Tap the Share button (iOS) or Menu (Android)
3. Select "Add to Home Screen"
4. Now you have a native app-like experience!

### 3. Authenticate (Optional)

For secured endpoints (command execution, screenshots):

**Default PIN: 1234** (change in `.env` file)

To authenticate via API:
```bash
curl -X POST http://your-url/api/mobile/auth \
  -H "Content-Type: application/json" \
  -d '{"pin": "1234", "device_id": "my-phone"}'
```

This returns a token valid for 24 hours.

---

## 🔧 Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Mobile Companion Settings
MOBILE_PIN=1234                        # PIN for mobile authentication (change this!)

# Push Notifications - Twilio SMS (Optional)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
NOTIFICATION_PHONE=+1987654321         # Phone to receive notifications

# Email Notifications (Optional)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
NOTIFICATION_EMAIL=alerts@example.com  # Email to receive notifications

# Webhook Notifications (Optional)
NOTIFICATION_WEBHOOK_URL=https://your-webhook-url.com/notify

# Server Settings
SECRET_KEY=your_secret_key_here
```

### Setting Up Twilio for SMS Notifications

1. Sign up at [Twilio.com](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Get a Twilio phone number
4. Add credentials to `.env`

---

## 📱 Mobile Interface Features

### Main Screen
- **Header**: Connection status indicator
- **System Stats**: Real-time CPU, Memory, Disk usage
- **Quick Actions**: One-tap shortcuts organized by category
- **Screenshot Viewer**: Live screen capture with refresh
- **Activity Feed**: Recent command history
- **Command Input**: Text-based command execution at bottom

### Quick Actions Categories
- 🔒 **Security**: Lock, security features
- ⚡ **Power**: Shutdown, restart, sleep
- 🎵 **Media**: Music control, volume
- 📊 **Productivity**: Pomodoro, focus mode
- 🌐 **Apps**: Browser, applications
- ℹ️ **Info**: Weather, news

---

## 🔌 API Reference

### Authentication

**POST** `/api/mobile/auth`
```json
{
  "pin": "1234",
  "device_id": "my-phone"
}
```

Returns:
```json
{
  "success": true,
  "token": "eyJhbGciOi...",
  "expires_at": "2025-10-31T12:00:00",
  "device_id": "my-phone"
}
```

Use token in subsequent requests:
```
Authorization: Bearer eyJhbGciOi...
```

### System Status

**GET** `/api/mobile/status` (No auth required)

Returns current system stats:
```json
{
  "success": true,
  "timestamp": "2025-10-30T10:30:00",
  "system": {
    "cpu_percent": 45.2,
    "memory_percent": 62.8,
    "disk_percent": 75.3,
    "battery": {
      "percent": 85,
      "plugged": true
    }
  }
}
```

### Execute Command

**POST** `/api/mobile/command` (Auth required)
```json
{
  "command": "open spotify"
}
```

Returns:
```json
{
  "success": true,
  "timestamp": "2025-10-30T10:30:00",
  "command": "open spotify",
  "source": "mobile",
  "result": "Spotify opened successfully"
}
```

### Quick Actions

**GET** `/api/mobile/quick-actions?category=media`

Returns available actions:
```json
{
  "success": true,
  "actions": {
    "play_music": {
      "name": "Play Music",
      "icon": "🎵",
      "command": "play spotify",
      "category": "media"
    }
  },
  "categories": ["security", "power", "media", "productivity", "apps", "info"]
}
```

**POST** `/api/mobile/quick-action/lock_screen` (Auth required)

Execute a quick action.

### Screenshot

**GET** `/api/mobile/screenshot?quality=85&max_width=1280` (Auth required)

Returns:
```json
{
  "success": true,
  "screenshot": {
    "timestamp": "2025-10-30T10:30:00",
    "image": "base64_encoded_jpeg_data",
    "width": 1280,
    "height": 720
  }
}
```

**GET** `/api/mobile/screenshot/cached`

Returns cached screenshot (faster, no auth required for demo).

### Voice Command

**POST** `/api/mobile/voice` (Auth required)
```json
{
  "text_command": "show me the weather"
}
```

### Activity Feed

**GET** `/api/mobile/activity?limit=20` (Auth required)

Returns recent command activity.

### Push Notifications

**POST** `/api/notifications/send` (Auth required)
```json
{
  "title": "Custom Alert",
  "message": "This is a test notification",
  "priority": "high",
  "recipients": {
    "phone": "+1234567890",
    "email": "user@example.com"
  }
}
```

**GET** `/api/notifications/status`

Check which notification channels are configured.

---

## 🔄 WebSocket Events

Connect to WebSocket for real-time updates:

```javascript
const socket = io('http://your-url');

// Connection events
socket.on('connect', () => {
  console.log('Connected to VATSAL');
});

// System stats (every 2 seconds)
socket.on('system_stats', (data) => {
  console.log('CPU:', data.cpu + '%');
  console.log('Memory:', data.memory + '%');
});

// Command updates
socket.on('command_update', (data) => {
  console.log('Command:', data.command);
  console.log('Status:', data.status); // started, completed, failed
  console.log('Result:', data.result);
});

// Notifications
socket.on('notification', (data) => {
  console.log('Alert:', data.title, data.message);
});
```

---

## 🎯 Integration with VATSAL

### From Command Executor

```python
from mobile_companion_server import initialize_mobile_api, broadcaster

# Initialize mobile API with your command executor
initialize_mobile_api(your_command_executor)

# Broadcast events from your code
broadcaster.command_started("opening spotify")
broadcaster.command_completed("opening spotify", "Spotify launched")
broadcaster.notify("Task Complete", "Your automation finished", "success")
```

### From GUI App

```python
# In gui_app.py
from mobile_companion_server import broadcaster

def execute_command(self, command):
    broadcaster.command_started(command)
    try:
        result = self.executor.execute_command(command)
        broadcaster.command_completed(command, result)
    except Exception as e:
        broadcaster.command_failed(command, str(e))
```

---

## 🛡️ Security Best Practices

1. **Change Default PIN**: Update `MOBILE_PIN` in `.env`
2. **Use HTTPS**: Enable SSL for production (Replit provides this)
3. **Rotate Tokens**: Tokens expire after 24 hours
4. **Revoke Compromised Tokens**: Use `/api/mobile/auth/revoke`
5. **Monitor Activity**: Check `/api/mobile/activity` regularly
6. **Limit Command Scope**: Only expose safe commands via mobile

---

## 📊 Usage Examples

### Example 1: Lock Your Computer Remotely

**From Mobile Interface:**
1. Open mobile companion app
2. Tap "Lock Screen" quick action
3. Computer locks instantly
4. Receive notification confirmation

**Via API:**
```bash
curl -X POST http://your-url/api/mobile/quick-action/lock_screen \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Example 2: Check System Status While Away

**From Mobile Interface:**
1. Open app (stats auto-update every 5 seconds)
2. View CPU, Memory, Disk usage
3. Battery status (if laptop)

**Via API:**
```bash
curl http://your-url/api/mobile/status
```

### Example 3: Control Music from Bed

**From Mobile Interface:**
1. Scroll to Media quick actions
2. Tap "Play Music" to start Spotify
3. Tap "Next Track" to skip songs
4. Tap "Pause Music" when done

### Example 4: Voice Command from Mobile

**From Mobile Interface:**
1. Type in command input: "show me the weather"
2. Press Send
3. View result in activity feed
4. Desktop executes command and displays weather

### Example 5: Remote Screenshot

**From Mobile Interface:**
1. Scroll to Screenshot section
2. Tap "Refresh Screenshot"
3. View live screen capture from desktop
4. Zoom/pan to see details

---

## 🎨 Customization

### Add Custom Quick Actions

Edit `mobile_api.py`:

```python
def _load_quick_actions(self):
    return {
        'my_custom_action': {
            'name': 'My Custom Action',
            'icon': '🎯',
            'command': 'your custom command here',
            'category': 'custom'
        }
    }
```

### Custom Notification Triggers

Edit `mobile_companion_server.py`:

```python
# Trigger notification on specific events
if 'error' in command.lower():
    notification_service.notify_event('error', {
        'message': 'An error occurred',
        'command': command
    }, priority='high')
```

---

## 🐛 Troubleshooting

### Mobile interface not loading?
- Check that server is running on port 5000
- Verify firewall settings
- Try accessing from desktop browser first

### Commands not executing?
- Verify authentication token is valid
- Check command executor is initialized
- Review activity log for errors

### Notifications not sending?
- Check Twilio credentials in `.env`
- Verify phone number format (+1234567890)
- Check notification service status: `/api/notifications/status`

### WebSocket disconnecting?
- Check network connectivity
- Verify server is running
- Check browser console for errors

---

## 📈 Performance Tips

1. **Screenshot Quality**: Lower quality (60-70) for faster loading
2. **Screenshot Size**: Use max_width=1024 for mobile viewing
3. **Cached Screenshots**: Use cached endpoint when real-time not needed
4. **Activity Limit**: Request only needed history (limit=10)
5. **WebSocket**: Auto-reconnects on disconnect

---

## 🔮 Future Enhancements

Coming soon:
- Native mobile apps (iOS/Android)
- Biometric authentication
- Voice audio recording and processing
- Gesture controls
- Dark/Light theme toggle
- Custom dashboard layouts
- Multi-device management
- Automation scheduling from mobile
- Video streaming from desktop

---

## 📞 Support

For issues or questions:
- Check the main README.md
- Review VATSAL documentation
- Check console logs for errors
- Monitor activity feed for failures

---

## 🎉 Enjoy Your Mobile Companion!

Your VATSAL AI Desktop Automation is now in your pocket. Control your computer from anywhere, anytime!

**Creator**: Vatsal Varshney
**GitHub**: https://github.com/VATSALVARSHNEY108
**Project**: VATSAL AI Desktop Automation Controller
