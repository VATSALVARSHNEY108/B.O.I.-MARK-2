# Desktop File & Folder Automator - Usage Guide

## Overview
This tool scans your Windows desktop, analyzes your files and folders, stores the data, and helps you automate desktop organization.

## How It Works

### 1. Automatic Desktop Scanning
When you run the script, it will:
- Scan your entire desktop
- Count all files and folders
- Analyze file types and sizes
- Save this data to `desktop_data.json`

### 2. Interactive Menu
After scanning, you get 6 options:

**Option 1: Download/Setup batch file controller**
- Prepares the batch file for use
- Shows where the batch file is located
- Option to launch it immediately

**Option 2: View detailed file analysis**
- Shows all files on your desktop
- Displays file sizes and types
- Lists first 20 files with details

**Option 3: Re-scan desktop**
- Scans your desktop again
- Updates the saved data
- Useful if you've added/removed files

**Option 4: Launch desktop automation (batch file)**
- Directly runs the batch file
- Opens the automation menu
- Quick access to file organization

**Option 5: View saved desktop history**
- Shows previously saved desktop data
- Compare with current state
- Track changes over time

**Option 6: Exit**
- Closes the program
- Data remains saved

## Features

### Desktop Analysis
- **Total Files & Folders**: Complete count
- **File Types**: Breakdown by extension (.txt, .pdf, etc.)
- **Total Size**: Human-readable format (KB, MB, GB)
- **Folder Contents**: Item count per folder

### Data Storage
- All scan data saved to `desktop_data.json`
- Includes timestamps
- Full file paths and metadata
- Persistent across sessions

### Batch File Integration
- Seamless connection to desktop automation
- Launch directly from menu
- One-click access to organization tools

## Running the Script

### From Command Prompt/PowerShell:
```bash
cd C:\Users\VATSAL VARSHNEY\PycharmProjects\DesktopAutomator2
python desktop_sync_manager.py
```

### From File Explorer:
- Double-click `desktop_sync_manager.py`
- Make sure Python is installed and associated with .py files

## Requirements

1. **Batch File**: Download `desktop_file_controller.bat` from Replit
2. **Python**: Version 3.x installed
3. **Windows**: Works on Windows OS

## Saved Data Location
- `desktop_data.json` - Complete desktop scan data
- `downloads_ready.txt` - Batch file instructions
- Both files saved in script directory

## Tips

- Run regularly to track desktop changes
- Use Option 5 to see historical data
- Combine with batch file for full automation
- Data persists between runs
