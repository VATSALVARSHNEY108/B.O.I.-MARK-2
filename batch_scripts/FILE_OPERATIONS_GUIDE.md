# File Operations Batch Script Guide

## Overview
The `file_operations.bat` script provides a centralized, reliable way to handle file creation, deletion, and editing operations on Windows. This batch file is integrated with the BOI AI system for maximum reliability when working with files.

## Features

### ✅ Supported Operations
1. **create** - Create a new file with optional content
2. **delete** - Delete an existing file
3. **edit** - Edit/overwrite file content
4. **append** - Append content to existing file
5. **read** - Read and display file content

### 🎯 Key Benefits
- **Reliable File Creation**: Uses native Windows `type` and `echo` commands
- **Automatic Directory Creation**: Creates parent directories if they don't exist
- **Error Handling**: Provides clear success/error messages
- **Forward Slash Support**: Accepts both forward (/) and backslashes (\\) in paths
- **Content Safety**: Handles special characters in file content

## Usage

### Command Line Syntax
```batch
file_operations.bat [operation] [filepath] [content]
```

### Examples

#### Create Empty File
```batch
file_operations.bat create "C:/Users/VATSAL VARSHNEY/OneDrive/Desktop/test.txt"
```

#### Create File with Content
```batch
file_operations.bat create "Desktop/notes.txt" "This is my note content"
```

#### Delete File
```batch
file_operations.bat delete "Desktop/test.txt"
```

#### Edit File (Overwrite)
```batch
file_operations.bat edit "Desktop/notes.txt" "Updated content"
```

#### Append to File
```batch
file_operations.bat append "Desktop/notes.txt" "Additional line"
```

#### Read File
```batch
file_operations.bat read "Desktop/notes.txt"
```

## Integration with BOI

The batch script is automatically integrated with the BOI file manager:

### Python Integration
```python
from modules.file_management.file_manager import FileManager

fm = FileManager()

# Create file (uses batch script on Windows)
result = fm.create_file("Desktop/test.txt", "Hello World")

# Delete file (uses batch script on Windows)
result = fm.delete_file("Desktop/test.txt")

# Edit file (uses batch script on Windows)
result = fm.write_to_file("Desktop/test.txt", "New content", mode="w")

# Append to file (uses batch script on Windows)
result = fm.write_to_file("Desktop/test.txt", "More content", mode="a")
```

### Voice Commands
Users can use natural language commands:
- "Create file called test.txt on Desktop"
- "Delete file Desktop/test.txt"
- "Edit file Desktop/notes.txt with new content"
- "Append to file Desktop/notes.txt"

## Technical Details

### Path Handling
- Accepts forward slashes (`/`) in file paths
- Automatically converts to Windows backslashes (`\`) internally
- Creates parent directories if they don't exist
- Handles OneDrive synced folders correctly

### Error Messages
- **SUCCESS**: Operation completed successfully
- **ERROR**: Operation failed with specific reason

### Return Codes
- `0` - Success
- `1` - Failure (with error message)

## File Manager Integration

The FileManager class (`modules/file_management/file_manager.py`) uses this batch script on Windows:

1. **Primary Method**: Calls `file_operations.bat` for Windows file operations
2. **Fallback Method**: Uses Python's built-in file operations if batch fails
3. **Cross-Platform**: Automatically uses Python methods on non-Windows systems

## Location
- Batch Script: `batch_scripts/file_operations.bat`
- File Manager: `modules/file_management/file_manager.py`
- Command Executor: `modules/core/command_executor.py`

## Advantages Over Python File Operations

1. **No Unicode Escape Issues**: Avoids Python's `\U` escape character errors
2. **Native Windows Commands**: Uses `type` and `echo` for maximum reliability
3. **Better Error Handling**: Windows provides clear file operation errors
4. **Integrated with System**: Works seamlessly with Windows file system

## Version History
- **Nov 22, 2025**: Initial release with create, delete, edit, append, and read operations
- **Nov 22, 2025**: Integrated with FileManager class and command executor
