"""
Batch File Reader Module for BOI (Barely Obeys Instructions)
Reads time/date and reminders from desktop batch file outputs
"""

import os
from pathlib import Path
from datetime import datetime


class BatchFileReader:
    """Read data from batch file outputs on desktop"""
    
    def __init__(self):
        self.desktop = self._get_desktop_path()
        self.time_file = self.desktop / "CURRENT_TIME.txt"
        self.reminder_file = self.desktop / "REMINDERS.txt"
    
    def _get_desktop_path(self) -> Path:
        """Get the desktop path (cross-platform)"""
        if os.name == 'nt':
            desktop = Path(os.path.expanduser("~")) / "Desktop"
        else:
            desktop = Path(os.path.expanduser("~")) / "Desktop"
            if not desktop.exists():
                desktop = Path(os.path.expanduser("~"))
        return desktop
    
    def read_desktop_time(self) -> dict:
        """Read time and date from desktop file created by batch script"""
        try:
            if not self.time_file.exists():
                return {
                    "success": False,
                    "message": "Time file not found on desktop. Please run 'show_time_date.bat' first.",
                    "file_path": str(self.time_file)
                }
            
            content = self.time_file.read_text(encoding='utf-8', errors='ignore')
            
            lines = content.split('\n')
            date_line = ""
            time_line = ""
            day_line = ""
            updated_line = ""
            
            for line in lines:
                if "Date:" in line:
                    date_line = line.split("Date:")[-1].strip()
                elif "Time:" in line:
                    time_line = line.split("Time:")[-1].strip()
                elif "Day of Week:" in line:
                    day_line = line.split("Day of Week:")[-1].strip()
                elif "Last Updated:" in line:
                    updated_line = line.split("Last Updated:")[-1].strip()
            
            return {
                "success": True,
                "date": date_line,
                "time": time_line,
                "day_of_week": day_line,
                "last_updated": updated_line,
                "full_content": content,
                "message": f"📅 Date: {date_line}\n🕐 Time: {time_line}\n📆 Day: {day_line}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error reading time file: {str(e)}",
                "error": str(e)
            }
    
    def read_reminders(self) -> dict:
        """Read all reminders from desktop file"""
        try:
            if not self.reminder_file.exists():
                return {
                    "success": False,
                    "message": "No reminders file found. Please run 'reminder_system.bat' to create reminders.",
                    "reminders": [],
                    "count": 0
                }
            
            content = self.reminder_file.read_text(encoding='utf-8', errors='ignore')
            
            if not content.strip():
                return {
                    "success": True,
                    "message": "No reminders found. The reminder file is empty.",
                    "reminders": [],
                    "count": 0
                }
            
            reminders = self._parse_reminders(content)
            
            return {
                "success": True,
                "message": f"Found {len(reminders)} reminder(s)",
                "reminders": reminders,
                "count": len(reminders),
                "full_content": content
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error reading reminders: {str(e)}",
                "error": str(e),
                "reminders": [],
                "count": 0
            }
    
    def _parse_reminders(self, content: str) -> list:
        """Parse reminder content into structured list"""
        reminders = []
        lines = content.split('\n')
        
        current_reminder = {}
        for line in lines:
            line = line.strip()
            
            if line.startswith('['):
                if current_reminder:
                    reminders.append(current_reminder)
                current_reminder = {
                    "timestamp": line.strip('[]'),
                    "text": "",
                    "due": ""
                }
            elif line.startswith('Reminder:'):
                current_reminder["text"] = line.replace('Reminder:', '').strip()
            elif line.startswith('Due:'):
                current_reminder["due"] = line.replace('Due:', '').strip()
            elif line == '------------------------------------------------':
                if current_reminder:
                    reminders.append(current_reminder)
                    current_reminder = {}
        
        if current_reminder and current_reminder.get("text"):
            reminders.append(current_reminder)
        
        return reminders
    
    def format_reminders_for_display(self, reminders: list) -> str:
        """Format reminders for nice display"""
        if not reminders:
            return "📝 No reminders found."
        
        output = f"📝 **{len(reminders)} Reminder(s)**\n\n"
        
        for i, reminder in enumerate(reminders, 1):
            output += f"**{i}.** {reminder.get('text', 'No text')}\n"
            if reminder.get('due'):
                output += f"   ⏰ Due: {reminder['due']}\n"
            output += f"   📅 Added: {reminder.get('timestamp', 'Unknown')}\n"
            output += "\n"
        
        return output
    
    def add_reminder_via_python(self, text: str, due_time: str = "") -> dict:
        """Add a reminder directly from Python (alternative to batch file)"""
        try:
            timestamp = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
            
            reminder_text = f"\n[{timestamp}]\n"
            reminder_text += f"Reminder: {text}\n"
            if due_time:
                reminder_text += f"Due: {due_time}\n"
            reminder_text += "------------------------------------------------\n"
            
            with open(self.reminder_file, 'a', encoding='utf-8') as f:
                f.write(reminder_text)
            
            return {
                "success": True,
                "message": f"✅ Reminder added: {text}",
                "reminder": {
                    "text": text,
                    "due": due_time,
                    "timestamp": timestamp
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error adding reminder: {str(e)}",
                "error": str(e)
            }


batch_reader = BatchFileReader()


if __name__ == "__main__":
    print("Testing Batch File Reader...")
    print("\n1. Reading Desktop Time:")
    time_data = batch_reader.read_desktop_time()
    print(time_data.get("message"))
    
    print("\n2. Reading Reminders:")
    reminder_data = batch_reader.read_reminders()
    print(reminder_data.get("message"))
    if reminder_data.get("reminders"):
        print(batch_reader.format_reminders_for_display(reminder_data["reminders"]))
