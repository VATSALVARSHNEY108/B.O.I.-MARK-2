"""
Quick Reminders Module
Provides pop-up reminders with sound alerts and scheduling
"""

import time
import threading
from datetime import datetime, timedelta
import json
import os
import uuid

class QuickReminders:
    def __init__(self):
        self.reminders_file = "data/reminders.json"
        self.active_reminders = {}
        self.reminder_threads = {}
        self.cancelled_reminders = set()
        self.load_reminders()
        
    def load_reminders(self):
        """Load reminders from file"""
        try:
            os.makedirs("data", exist_ok=True)
            if os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'r') as f:
                    data = json.load(f)
                    self.active_reminders = data
                    self._restore_active_reminders()
            else:
                self.active_reminders = {}
                self.save_reminders()
        except Exception as e:
            print(f"Error loading reminders: {e}")
            self.active_reminders = {}
    
    def save_reminders(self):
        """Save reminders to file"""
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.reminders_file, 'w') as f:
                json.dump(self.active_reminders, f, indent=2)
        except Exception as e:
            print(f"Error saving reminders: {e}")
    
    def _restore_active_reminders(self):
        """Restore active reminders on load"""
        current_time = datetime.now()
        for reminder_id, reminder in list(self.active_reminders.items()):
            if reminder.get("status") == "active":
                trigger_time = datetime.fromisoformat(reminder["trigger_time"])
                if trigger_time > current_time:
                    seconds_until = (trigger_time - current_time).total_seconds()
                    self._schedule_reminder(reminder_id, seconds_until)
                else:
                    reminder["status"] = "missed"
                    self.save_reminders()
    
    def add_reminder(self, message, delay_minutes=None, specific_time=None, date=None):
        """Add a new reminder"""
        try:
            reminder_id = str(uuid.uuid4())[:8]
            current_time = datetime.now()
            
            if specific_time:
                if date:
                    target_date = datetime.strptime(date, "%Y-%m-%d").date()
                else:
                    target_date = current_time.date()
                
                time_parts = specific_time.split(":")
                hour = int(time_parts[0])
                minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                
                trigger_time = datetime.combine(target_date, datetime.min.time().replace(hour=hour, minute=minute))
                
                if trigger_time <= current_time:
                    trigger_time += timedelta(days=1)
            
            elif delay_minutes:
                trigger_time = current_time + timedelta(minutes=int(delay_minutes))
            
            else:
                return "❌ Please specify either delay_minutes or specific_time"
            
            self.active_reminders[reminder_id] = {
                "id": reminder_id,
                "message": message,
                "created": current_time.isoformat(),
                "trigger_time": trigger_time.isoformat(),
                "status": "active"
            }
            
            self.save_reminders()
            
            seconds_until = (trigger_time - current_time).total_seconds()
            self._schedule_reminder(reminder_id, seconds_until)
            
            time_str = trigger_time.strftime("%Y-%m-%d %H:%M")
            return f"⏰ Reminder set for {time_str}\nID: {reminder_id}\nMessage: {message}"
        
        except Exception as e:
            return f"❌ Failed to add reminder: {str(e)}"
    
    def _schedule_reminder(self, reminder_id, seconds_until):
        """Schedule reminder in background thread"""
        thread = threading.Thread(target=self._trigger_reminder, args=(reminder_id, seconds_until))
        thread.daemon = True
        thread.start()
        self.reminder_threads[reminder_id] = thread
    
    def _trigger_reminder(self, reminder_id, seconds_until):
        """Trigger reminder after delay"""
        end_time = datetime.now() + timedelta(seconds=seconds_until)
        
        while datetime.now() < end_time:
            if reminder_id in self.cancelled_reminders:
                self.cancelled_reminders.discard(reminder_id)
                return
            time.sleep(1)
        
        if reminder_id in self.cancelled_reminders:
            self.cancelled_reminders.discard(reminder_id)
            return
        
        if reminder_id in self.active_reminders:
            reminder = self.active_reminders[reminder_id]
            if reminder["status"] == "active":
                print(f"\n{'='*60}")
                print(f"🔔 REMINDER ALERT!")
                print(f"{'='*60}")
                print(f"Message: {reminder['message']}")
                print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}\n")
                
                try:
                    import subprocess
                    import platform
                    
                    if platform.system() == "Windows":
                        subprocess.run([
                            'powershell', '-Command',
                            f'Add-Type -AssemblyName System.Windows.Forms; ' +
                            f'[System.Windows.Forms.MessageBox]::Show("{reminder["message"]}", "Reminder Alert", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)'
                        ], check=False)
                    elif platform.system() == "Darwin":
                        subprocess.run(['osascript', '-e', f'display notification "{reminder["message"]}" with title "Reminder Alert"'], check=False)
                    elif platform.system() == "Linux":
                        subprocess.run(['notify-send', 'Reminder Alert', reminder["message"]], check=False)
                except:
                    pass
                
                try:
                    if os.path.exists("voice_sounds/wake_word.wav"):
                        import pygame
                        pygame.mixer.init()
                        sound = pygame.mixer.Sound("voice_sounds/wake_word.wav")
                        sound.play()
                except:
                    pass
                
                reminder["status"] = "triggered"
                reminder["triggered_at"] = datetime.now().isoformat()
                self.save_reminders()
    
    def list_reminders(self, status="active"):
        """List reminders by status"""
        try:
            filtered = {rid: r for rid, r in self.active_reminders.items() if r.get("status") == status}
            
            if not filtered:
                return f"ℹ️ No {status} reminders"
            
            result = f"🔔 {status.title()} Reminders:\n" + "=" * 60 + "\n"
            
            for reminder_id, reminder in sorted(filtered.items(), key=lambda x: x[1]["trigger_time"]):
                trigger_time = datetime.fromisoformat(reminder["trigger_time"])
                time_str = trigger_time.strftime("%Y-%m-%d %H:%M")
                
                result += f"\nID: {reminder_id}\n"
                result += f"Message: {reminder['message']}\n"
                result += f"Scheduled: {time_str}\n"
                
                if status == "active":
                    now = datetime.now()
                    remaining = trigger_time - now
                    if remaining.total_seconds() > 0:
                        days = remaining.days
                        hours = remaining.seconds // 3600
                        minutes = (remaining.seconds % 3600) // 60
                        
                        time_left = ""
                        if days > 0:
                            time_left = f"{days}d {hours}h {minutes}m"
                        elif hours > 0:
                            time_left = f"{hours}h {minutes}m"
                        else:
                            time_left = f"{minutes}m"
                        
                        result += f"Time Remaining: {time_left}\n"
                
                result += "-" * 60 + "\n"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to list reminders: {str(e)}"
    
    def delete_reminder(self, reminder_id):
        """Delete a reminder"""
        try:
            if reminder_id in self.active_reminders:
                reminder = self.active_reminders[reminder_id]
                self.cancelled_reminders.add(reminder_id)
                del self.active_reminders[reminder_id]
                self.save_reminders()
                return f"✅ Deleted reminder: {reminder['message']}"
            else:
                return f"⚠️ Reminder {reminder_id} not found"
        except Exception as e:
            return f"❌ Failed to delete reminder: {str(e)}"
    
    def clear_triggered_reminders(self):
        """Clear all triggered reminders"""
        try:
            triggered = [rid for rid, r in self.active_reminders.items() if r.get("status") == "triggered"]
            
            for rid in triggered:
                del self.active_reminders[rid]
            
            self.save_reminders()
            
            if triggered:
                return f"✅ Cleared {len(triggered)} triggered reminders"
            else:
                return "ℹ️ No triggered reminders to clear"
        except Exception as e:
            return f"❌ Failed to clear reminders: {str(e)}"
    
    def snooze_reminder(self, reminder_id, minutes=10):
        """Snooze a reminder"""
        try:
            if reminder_id in self.active_reminders:
                reminder = self.active_reminders[reminder_id]
                
                self.cancelled_reminders.add(reminder_id)
                
                wait_count = 0
                while reminder_id in self.cancelled_reminders and wait_count < 30:
                    time.sleep(0.1)
                    wait_count += 1
                
                new_trigger = datetime.now() + timedelta(minutes=int(minutes))
                reminder["trigger_time"] = new_trigger.isoformat()
                reminder["status"] = "active"
                
                self.save_reminders()
                
                seconds_until = minutes * 60
                self._schedule_reminder(reminder_id, seconds_until)
                
                return f"😴 Reminder snoozed for {minutes} minutes"
            else:
                return f"⚠️ Reminder {reminder_id} not found"
        except Exception as e:
            return f"❌ Failed to snooze reminder: {str(e)}"
    
    def quick_reminder(self, message, minutes=5):
        """Quick reminder shortcut"""
        return self.add_reminder(message, delay_minutes=minutes)
    
    def daily_reminder(self, message, time="09:00"):
        """Set a daily recurring reminder (simplified version)"""
        return self.add_reminder(message, specific_time=time)

if __name__ == "__main__":
    reminders = QuickReminders()
    
    print("Testing Quick Reminders...")
    print(reminders.add_reminder("Test reminder", delay_minutes=1))
    print(reminders.list_reminders())
    
    time.sleep(2)
    print(reminders.list_reminders())
