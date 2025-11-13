# VATSAL Web GUI

Modern HTML/CSS/JavaScript interface for the VATSAL AI System.

## Features

- **Modern Design**: Clean, responsive interface matching the VATSAL brand
- **Real-time Updates**: Live date/time display and status indicators
- **Command Execution**: Execute VATSAL commands through the web interface
- **Console Output**: View responses and logs in an organized console
- **Theme Toggle**: Switch between light and dark themes
- **Status Controls**: Toggle VATSAL and Self-Operating modes
- **API Integration**: REST API endpoints for backend communication

## Project Structure

```
web_gui/
├── server.py              # Flask server
├── static/
│   ├── css/
│   │   └── style.css     # Modern CSS styling
│   └── js/
│       └── main.js       # Frontend JavaScript
├── templates/
│   └── index.html        # Main HTML interface
└── README.md
```

## Running the Web GUI

### Standalone Mode
```bash
cd web_gui
python server.py
```

### VNC Display Mode
The web GUI can be displayed in a VNC environment alongside the main VATSAL GUI system.

## API Endpoints

- `GET /` - Main web interface
- `POST /api/execute` - Execute VATSAL commands
- `GET /api/status` - Get system status
- `POST /api/clear` - Clear console
- `GET /health` - Health check

## Usage

1. Open the web interface at http://localhost:5000
2. Enter commands in the command input field
3. Click "Execute" or press Enter to run commands
4. View responses in the output console
5. Use the utility buttons for additional functions
6. Toggle theme with the theme button

## Features Coming Soon

- Voice input/output integration
- Advanced settings panel
- Volume controls
- Power management options
- Real-time notifications
- Command history
- Auto-complete suggestions

## Integration with VATSAL Core

The web GUI is designed to integrate seamlessly with the main VATSAL AI system. When the backend is connected, commands will be processed through the VATSAL core engine.

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

## Dependencies

- Flask
- Flask-CORS

Install with:
```bash
pip install flask flask-cors
```
