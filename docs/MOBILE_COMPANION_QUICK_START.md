# 📱 Mobile Companion - Quick Start

Get started with VATSAL Mobile Companion in 60 seconds!

## 🚀 Start the Server

The Mobile Companion Server is already configured as a workflow. Simply ensure it's running:

1. Check that "Mobile Companion Server" workflow is active
2. If not, click "Run" on the workflow

The server runs on port 5000 and provides both mobile and desktop interfaces.

## 📱 Access from Your Phone

### Method 1: Direct URL
1. Get your Replit URL (e.g., `https://your-repl-name.your-username.repl.co`)
2. On your phone, open: `https://your-repl-name.your-username.repl.co/mobile`
3. Bookmark it for quick access!

### Method 2: Add to Home Screen (Recommended)
**iOS:**
1. Open the mobile URL in Safari
2. Tap the Share button (📤)
3. Scroll and tap "Add to Home Screen"
4. Tap "Add" - now you have an app icon!

**Android:**
1. Open the mobile URL in Chrome
2. Tap the menu (⋮)
3. Tap "Add to Home screen"
4. Tap "Add" - icon appears on your home screen!

## 🎮 What You Can Do

### ⚡ Quick Actions (One-Tap Control)
Tap any quick action button to instantly:
- 🔒 Lock your screen
- ⚡ Shutdown/Restart/Sleep computer
- 🔊 Control volume (up, down, mute)
- 🎵 Control music playback
- 📸 Take screenshots
- 🎯 Start focus mode/Pomodoro
- 🌤️ Check weather

### 📊 Monitor Your System
See real-time stats:
- CPU usage
- Memory usage
- Disk space
- Updates every 5 seconds

### 💬 Voice Commands
Type any command at the bottom:
- "show me the weather"
- "open spotify"
- "lock screen"
- Any VATSAL command!

### 📸 View Your Screen
- Tap "Refresh Screenshot" to capture your desktop
- View and zoom the live screenshot
- Perfect for checking what's happening remotely

## 🔐 Security (Optional)

### Default PIN: 1234

**To change it:**
1. Go to Secrets in Replit (🔒 icon)
2. Add/Edit: `MOBILE_PIN` = `your-new-pin`
3. Restart the Mobile Companion Server

### Authentication
Some features require authentication:
- Command execution
- Screenshot capture
- Activity viewing

The mobile interface handles this automatically via tokens.

## 🔔 Push Notifications (Optional)

Get SMS alerts for important events:

1. Sign up at [Twilio.com](https://www.twilio.com)
2. Add to your Replit Secrets:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_PHONE_NUMBER`
   - `NOTIFICATION_PHONE` (your phone to receive alerts)
3. Restart server

Now you'll get SMS when:
- Commands complete/fail
- System errors occur
- Security alerts happen

## 📡 Live Updates

The mobile interface updates in real-time via WebSocket:
- System stats refresh every 2 seconds
- Command execution appears instantly
- Notifications pop up automatically
- Activity feed updates live

## 💡 Pro Tips

1. **Bookmark the mobile URL** for instant access
2. **Add to home screen** for app-like experience
3. **Use quick actions** for common tasks (faster than typing)
4. **Keep it open** to monitor your system remotely
5. **Use voice commands** when you need something specific

## 🎯 Common Use Cases

**From Your Couch:**
- "Play music" → Start Spotify
- "Next song" → Skip tracks
- "Volume down" → Adjust audio

**Before Sleep:**
- Tap "Lock Screen"
- Tap "Sleep Computer"

**While Away:**
- Check system stats (is it running?)
- View screenshot (what's on screen?)
- Execute commands remotely

**In Meeting:**
- Quickly mute your computer
- Start focus mode
- Check if tasks completed

## 🆘 Troubleshooting

**Can't access mobile URL?**
- Ensure Mobile Companion Server workflow is running
- Check you're using the correct Replit URL
- Try refreshing the page

**Commands not working?**
- Authentication may have expired (reload page)
- Check that VATSAL is running (GUI App workflow)
- Commands execute on desktop, not mobile

**No system stats?**
- Wait 5 seconds for first update
- Check WebSocket connection status (top of page)
- Refresh the page

**Screenshot not working?**
- This feature requires desktop environment with display
- In Replit's headless mode, screenshots are limited
- Works perfectly on local installations

## 🎉 That's It!

You're now controlling your VATSAL desktop automation from your phone! 

For more details, see [MOBILE_COMPANION_GUIDE.md](MOBILE_COMPANION_GUIDE.md)

---

**Enjoy your mobile companion!** 📱✨
