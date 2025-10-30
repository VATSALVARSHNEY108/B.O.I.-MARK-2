# 🌐 Real-Time WebSocket Dashboard Guide

## Overview

VATSAL now includes **real-time WebSocket connections** for live monitoring and remote control! Watch your automation system work in real-time from any web browser.

## ✨ Features

### 📡 Real-Time Updates
- **Live command execution** - See commands as they're processed
- **System monitoring** - CPU, Memory, and Disk usage updated every 2 seconds
- **Instant notifications** - Get notified about events immediately
- **Activity feed** - Complete history of all commands and results

### 🎯 Remote Access
- **Web-based dashboard** - Access from any browser
- **Mobile-friendly** - Works on phones and tablets
- **Cross-platform** - No installation needed on client devices
- **Secure WebSocket** - Real-time bidirectional communication

### 💻 Live System Stats
- **CPU Usage** - Real-time processor utilization with visual bars
- **Memory Usage** - RAM consumption tracking
- **Disk Usage** - Storage space monitoring
- **Network Activity** - Track data sent/received

## 🚀 Getting Started

### Starting the WebSocket Server

The WebSocket server runs automatically when you start your project. It serves:
- **Dashboard**: http://localhost:5000
- **Health endpoint**: http://localhost:5000/api/health

### Accessing the Dashboard

1. **Start the WebSocket Server workflow** (if not already running)
2. **Open your browser** to http://localhost:5000
3. **Watch real-time updates** as you use VATSAL

### Using the Dashboard

#### Connection Status
- 🟢 **Green dot** = Connected
- 🔴 **Red dot** = Disconnected

#### System Statistics Cards
- View live CPU, Memory, and Disk usage
- Visual progress bars show utilization
- Updates automatically every 2 seconds

#### Send Commands
- Type commands directly in the dashboard
- Press Enter or click "Send Command"
- See execution in real-time in the activity feed

#### Activity Feed
- Shows all commands being executed
- Color-coded status:
  - **Blue** = Pending
  - **Yellow** = Started
  - **Green** = Completed
  - **Red** = Failed
- Displays timestamps, commands, and results

## 🔧 Technical Details

### WebSocket Events

**Server → Client Events:**
- `connection_response` - Sent when client connects
- `system_stats` - System metrics (CPU, RAM, disk)
- `command_update` - Command execution updates
- `command_history` - Historical commands
- `notification` - Important notifications
- `system_event` - System-level events

**Client → Server Events:**
- `execute_command` - Send command for execution
- `ping` - Keep-alive heartbeat

### Integration with GUI App

The GUI automatically broadcasts to connected web clients:
- **Command started** - When you execute a command
- **Command completed** - With results
- **Command failed** - With error details

### Architecture

```
┌─────────────────┐
│   GUI App       │
│  (gui_app.py)   │
└────────┬────────┘
         │
         │ WebSocket Client
         ▼
┌─────────────────┐
│ WebSocket Server│
│(port 5000)      │
└────────┬────────┘
         │
         │ Socket.IO
         ▼
┌─────────────────┐
│  Web Dashboard  │
│   (Browser)     │
└─────────────────┘
```

## 🎨 Dashboard Features

### Modern Dark Theme
- Beautiful gradient design
- Smooth animations
- Responsive layout
- Professional look

### Real-Time Notifications
- Toast-style popups
- Color-coded by severity:
  - 🔵 Info
  - 🟢 Success
  - 🟡 Warning
  - 🔴 Error

### Smooth Animations
- Slide-in effects for new activities
- Pulse animation for connection status
- Progress bar transitions

## 🌟 Use Cases

### 1. Remote Monitoring
Monitor your automation system from anywhere:
- Check if tasks are running
- View system performance
- See command history

### 2. Debugging
Watch what's happening in real-time:
- See exact command flow
- Catch errors as they occur
- Understand system behavior

### 3. Team Collaboration
Multiple people can monitor the same system:
- Share dashboard URL
- Everyone sees same updates
- Coordinate automation tasks

### 4. Mobile Control
Control VATSAL from your phone:
- Send commands on-the-go
- Check system status
- Monitor from anywhere

## 📊 Example Workflow

1. **Start VATSAL GUI** on your computer
2. **Open dashboard** in your browser (or phone)
3. **Execute command** from GUI or dashboard
4. **Watch real-time updates** flow through:
   - Command appears in activity feed
   - Status changes: Pending → Started → Completed
   - System stats update continuously
5. **Get notifications** for important events

## 🔐 Security Notes

- Server runs on localhost (127.0.0.1) by default
- For remote access, configure firewall rules
- Consider adding authentication for production use
- WebSocket connections are not encrypted by default

## 🛠️ Advanced Configuration

### Custom Port
Edit `websocket_server.py`:
```python
socketio.run(app, host='0.0.0.0', port=YOUR_PORT)
```

### Remote Access
To access from other devices on your network:
1. Find your local IP address
2. Access dashboard at `http://YOUR_IP:5000`
3. Ensure firewall allows connections

### Multiple Clients
The server supports unlimited simultaneous connections. Each client gets:
- Real-time updates
- Synchronized view
- Independent connection status

## 📝 API Reference

### REST Endpoints

**GET /** - Dashboard page

**GET /api/health** - Server health check
```json
{
  "status": "online",
  "clients": 2,
  "time": "2024-10-30T12:34:56.789"
}
```

### WebSocket Events

**Emit from Client:**
```javascript
socket.emit('execute_command', {
  command: "Take screenshot"
});
```

**Receive from Server:**
```javascript
socket.on('command_update', (data) => {
  console.log(data.command);  // "Take screenshot"
  console.log(data.status);   // "completed"
  console.log(data.result);   // Result message
});
```

## 🎯 Next Steps

This is just the beginning! Future enhancements could include:
- User authentication
- Command scheduling from dashboard
- Custom dashboards
- Mobile app
- Multi-user chat
- File upload/download
- Video streaming
- And much more!

## 🆘 Troubleshooting

**Dashboard won't connect:**
- Check WebSocket Server workflow is running
- Verify port 5000 is not in use
- Check browser console for errors

**No real-time updates:**
- Ensure GUI app is running with WebSocket integration
- Check connection status indicator
- Refresh the page

**Slow updates:**
- Check network connection
- Verify system isn't overloaded
- Try reducing update frequency

---

**Enjoy your real-time automation dashboard!** 🚀
