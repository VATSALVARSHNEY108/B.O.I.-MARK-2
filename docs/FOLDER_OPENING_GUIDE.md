# 📂 Folder Opening Feature Guide

## Overview
The AI Desktop Automation Controller now includes intelligent folder opening capabilities that work across Windows, macOS, and Linux. You can open folders on your Desktop, in common locations, or any custom path using natural language commands.

---

## 🎯 Features

### 1. Open Desktop Folder
Open the Desktop folder or any folder within it.

**Commands:**
- "Open my Desktop"
- "Show me Desktop"
- "Open Desktop folder"

**Action:** `open_desktop`

**Example:**
```python
from command_executor import CommandExecutor

executor = CommandExecutor()
result = executor.execute_single_action("open_desktop", {})
```

---

### 2. Open Specific Desktop Folder
Open a specific folder that's on your Desktop.

**Commands:**
- "Open Projects folder on Desktop"
- "Open the TestFolder from Desktop"
- "Show me the Work folder on my Desktop"

**Action:** `open_desktop_folder`

**Parameters:**
- `folder_name` (optional): Name of the folder on Desktop

**Example:**
```python
# Open a specific folder on Desktop
result = executor.execute_single_action("open_desktop_folder", {
    "folder_name": "Projects"
})

# Or open Desktop itself
result = executor.execute_single_action("open_desktop_folder", {})
```

---

### 3. Open Any Folder (Smart Search)
Open folders from common locations or custom paths. The system automatically searches:
- Desktop
- Documents
- Downloads
- Home directory
- Subdirectories in these locations

**Commands:**
- "Open Documents folder"
- "Open Downloads"
- "Show me my Pictures folder"
- "Open the Projects folder"

**Action:** `open_folder`

**Parameters:**
- `folder_name` (string): Name of folder to search for
- OR
- `folder_path` (string): Full path to folder

**Examples:**
```python
# Search for folder by name
result = executor.execute_single_action("open_folder", {
    "folder_name": "Documents"
})

# Open folder by full path
result = executor.execute_single_action("open_folder", {
    "folder_path": "/home/user/custom/path"
})

# Expand home directory
result = executor.execute_single_action("open_folder", {
    "folder_path": "~/Projects"
})
```

---

## 🚀 How It Works

### Search Algorithm
When you provide a folder name, the system searches in this order:

1. **Desktop** - `~/Desktop`
2. **Documents** - `~/Documents`
3. **Downloads** - `~/Downloads`
4. **Home Directory** - `~`
5. **Desktop/[folder_name]** - Subdirectory on Desktop
6. **Documents/[folder_name]** - Subdirectory in Documents
7. **Downloads/[folder_name]** - Subdirectory in Downloads

The first matching location is opened.

### Cross-Platform Support

**Windows:**
- Uses Windows Explorer (`explorer.exe`)
- Desktop path: `C:\Users\[username]\Desktop`

**macOS:**
- Uses Finder (`open` command)
- Desktop path: `/Users/[username]/Desktop`

**Linux:**
- Uses default file manager (`xdg-open`)
- Desktop path: `/home/[username]/Desktop`
- Falls back to home directory if Desktop doesn't exist

---

## 💡 Natural Language Examples

The AI understands various ways to express folder opening:

### Opening Desktop
```
✅ "Open my Desktop"
✅ "Show Desktop"
✅ "Open Desktop folder"
✅ "Open the Desktop"
```

### Opening Desktop Subfolders
```
✅ "Open Projects folder on Desktop"
✅ "Show me the Work folder from Desktop"
✅ "Open TestFolder on my Desktop"
✅ "Open Desktop/Projects"
```

### Opening Common Folders
```
✅ "Open Documents"
✅ "Open my Documents folder"
✅ "Show me Downloads"
✅ "Open the Pictures folder"
```

### Opening Custom Paths
```
✅ "Open /home/user/projects"
✅ "Open ~/workspace"
✅ "Show me C:\Users\John\Projects"
```

---

## 🔧 Technical Details

### GUI Automation Methods

```python
from gui_automation import GUIAutomation

gui = GUIAutomation()

# Get Desktop path for current OS
desktop_path = gui.get_desktop_path()

# Open folder by path or name
success = gui.open_folder(
    folder_path="/path/to/folder"  # OR
    folder_name="FolderName"
)

# Open Desktop folder specifically
success = gui.open_desktop_folder(
    folder_name="Projects"  # Optional
)
```

### Command Executor Actions

```python
from command_executor import CommandExecutor

executor = CommandExecutor()

# Action: open_desktop
result = executor.execute_single_action("open_desktop", {})

# Action: open_desktop_folder
result = executor.execute_single_action("open_desktop_folder", {
    "folder_name": "Projects"  # Optional
})

# Action: open_folder
result = executor.execute_single_action("open_folder", {
    "folder_name": "Documents"  # OR folder_path
})
```

### Response Format

All folder opening actions return:

```python
{
    "success": True/False,
    "message": "Descriptive message"
}
```

**Success Example:**
```python
{
    "success": True,
    "message": "Opened Desktop folder: Projects"
}
```

**Failure Example:**
```python
{
    "success": False,
    "message": "Folder 'NonExistent' not found on Desktop"
}
```

---

## 🎨 Use Cases

### 1. Quick Desktop Access
```python
# Open Desktop to see all files
executor.execute_single_action("open_desktop", {})
```

### 2. Project Management
```python
# Open your Projects folder on Desktop
executor.execute_single_action("open_desktop_folder", {
    "folder_name": "Projects"
})
```

### 3. File Organization
```python
# Open Downloads to organize files
executor.execute_single_action("open_folder", {
    "folder_name": "Downloads"
})
```

### 4. Custom Workflows
```python
# Open specific project directory
executor.execute_single_action("open_folder", {
    "folder_path": "~/Development/MyApp"
})
```

---

## ⚠️ Error Handling

The system provides clear error messages:

### Folder Not Found
```
⚠️ Folder 'Projects' not found on Desktop
  Searched: /home/user/Desktop/Projects
```

### Path Does Not Exist
```
⚠️ Path does not exist: /invalid/path
```

### Search Failed
```
⚠️ Folder 'Unknown' not found in common locations
```

---

## 🧪 Demo Mode

In environments without GUI support (like Replit), the system runs in demo mode:

```
[DEMO] Would open folder: /home/runner/Desktop/Projects
```

The feature will work normally on actual desktop systems with GUI support.

---

## 📊 Integration

### With Workflow Templates

```python
# Save a workflow that opens multiple folders
workflow_steps = [
    {"action": "open_desktop", "parameters": {}},
    {"action": "open_folder", "parameters": {"folder_name": "Documents"}},
    {"action": "open_folder", "parameters": {"folder_name": "Downloads"}}
]

executor.execute_workflow(workflow_steps)
```

### With Voice Commands

```python
# Voice command gets parsed by Gemini AI
user_says = "Open my Desktop folder"
# AI translates to: {"action": "open_desktop", "parameters": {}}
```

### With Smart Automation

```python
# Part of daily routine workflow
daily_routine = [
    {"action": "open_desktop", "parameters": {}},
    {"action": "open_folder", "parameters": {"folder_name": "Projects"}},
    {"action": "open_app", "parameters": {"app_name": "VSCode"}}
]
```

---

## 🔮 Future Enhancements

Planned improvements:
- Recursive folder search in all subdirectories
- Recent folders history
- Favorite folders quick access
- Bulk folder operations
- Folder creation integration
- Smart folder suggestions based on usage patterns

---

## 💬 Support

For issues or questions:
1. Check if the folder exists at the expected location
2. Verify Desktop path is correct for your OS
3. Try using full path instead of folder name
4. Ensure file manager is installed (Linux: `xdg-open`)

**Common Solutions:**

**Linux - Desktop not found:**
```bash
mkdir -p ~/Desktop
```

**Permissions issue:**
```bash
chmod +x [folder_path]
```

---

## ✅ Summary

The folder opening feature provides:

✅ **Cross-platform support** - Windows, macOS, Linux  
✅ **Smart search** - Automatically finds folders  
✅ **Desktop integration** - Quick access to Desktop folders  
✅ **Natural language** - Intuitive voice commands  
✅ **Error handling** - Clear feedback messages  
✅ **Demo mode** - Works in any environment  

**Enjoy seamless folder navigation with your AI Desktop Automation Controller!** 🚀
