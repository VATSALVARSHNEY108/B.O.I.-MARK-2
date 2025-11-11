# 📂 VATSAL AI Batch File System

This folder contains Windows batch (.bat) files that create desktop files for time/date and reminders that your VATSAL AI can read and interact with.

## 🎯 What This Does

- **Creates visible files on your Desktop** that show current time/date and your reminders
- **VATSAL AI can read these files** and tell you what's in them
- **Simple reminder system** that saves to a text file
- **No API needed** - works completely offline using batch files

---

## 📁 Files Included

### 1. `show_time_date.bat`
**Creates a desktop file with current date and time**

**Usage:**
1. Double-click the file
2. It creates `CURRENT_TIME.txt` on your Desktop
3. Ask VATSAL AI: *"read desktop time"* or *"what does the desktop time file say?"*

**What it creates:**
```
================================================
          CURRENT DATE AND TIME                
================================================

Date: 11/11/2025
Time: 14:30:45

Day of Week: Mon

Last Updated: Mon 11/11/2025  2:30:45.67 PM
================================================
```

---

### 2. `auto_update_time.bat`
**Automatically updates the time file every 60 seconds**

**Usage:**
1. Double-click the file
2. Leave the window running in the background
3. The desktop time file updates automatically every minute
4. Press `Ctrl+C` to stop

**Perfect for:** Keeping an always-updated time display on your desktop that AI can read!

---

### 3. `reminder_system.bat`
**Interactive reminder management system**

**Usage:**
1. Double-click the file
2. Choose from menu:
   - **1** - Add New Reminder
   - **2** - View All Reminders
   - **3** - Clear All Reminders
   - **4** - Exit

**What it creates:**
`REMINDERS.txt` on your Desktop with all your reminders

**Example reminder file:**
```
[11/11/2025 02:30:45.67 PM]
Reminder: Call mom tomorrow
Due: 5pm
------------------------------------------------

[11/11/2025 02:35:12.34 PM]
Reminder: Finish project report
Due: Friday
------------------------------------------------
```

---

## 🤖 Using with VATSAL AI

Once you've run the batch files, you can ask VATSAL AI to interact with them:

### Reading Desktop Time
```
You: "read desktop time"
AI: 📅 Date: 11/11/2025
    🕐 Time: 14:30:45
    📆 Day: Mon
```

```
You: "what does the desktop time say?"
AI: [Shows current time from desktop file]
```

### Managing Reminders

**View Reminders:**
```
You: "show my reminders"
You: "what are my reminders?"
You: "read reminder file"
```

**Add Reminder:**
```
You: "add reminder to call mom"
You: "remind me to finish report by Friday"
You: "create reminder buy groceries"
```

The AI will add it to the desktop REMINDERS.txt file automatically!

---

## 🎨 How It Works

### Architecture:
1. **Batch Files (.bat)** → Create/Update text files on Desktop
2. **Desktop Text Files** → Store time/date and reminders
3. **Python Module** (`modules/batch_file_reader.py`) → Reads the text files
4. **VATSAL AI** → Interprets your commands and reads/writes to these files

### Flow Example:
```
User runs batch file → Creates REMINDERS.txt
User asks AI "show reminders" → AI reads REMINDERS.txt
AI responds with formatted reminder list
```

---

## ✨ Advanced Features

### Auto-Run on Startup (Optional)
To have the time file always updated:

1. Press `Win + R`
2. Type: `shell:startup`
3. Copy `auto_update_time.bat` into that folder
4. Time file will auto-update every time Windows starts!

### Editing Reminder File Manually
You can also edit `REMINDERS.txt` directly:
- Open in Notepad
- Add your own reminders in the same format
- VATSAL AI will read them!

---

## 🔧 Troubleshooting

**Problem:** Desktop files not appearing
- **Solution:** Make sure you're running the .bat files by double-clicking them
- Check your Desktop folder

**Problem:** AI can't read the files
- **Solution:** Ensure the files exist on Desktop
- File names must be exactly: `CURRENT_TIME.txt` and `REMINDERS.txt`

**Problem:** Batch file closes immediately
- **Solution:** This is normal! Check your Desktop for the created files

---

## 📝 Notes

- These batch files work on **Windows only**
- **Compatible with all modern Windows versions** (uses PowerShell for date/time)
- Files are created in your Desktop folder (`%USERPROFILE%\Desktop`)
- VATSAL AI can read these files on **any platform** (Windows, Linux, Mac) as long as the files exist
- You can create these files manually if batch files don't work
- **No admin rights required** - works with standard user permissions

---

## 🚀 Quick Start Guide

**5-Minute Setup:**

1. Run `show_time_date.bat` → Creates time file on Desktop
2. Run `reminder_system.bat` → Add 2-3 test reminders
3. Ask VATSAL AI: *"read desktop time"*
4. Ask VATSAL AI: *"show my reminders"*
5. Ask VATSAL AI: *"add reminder test the system"*
6. Check Desktop - you'll see the new reminder!

**That's it!** You now have a fully functional time/reminder system that your AI can read and manage! 🎉
