"""
Pomodoro Timer Module
Focus timer with customizable work/break intervals
"""

import time
import json
from datetime import datetime, timedelta
from threading import Thread, Event
import os

class PomodoroTimer:
    def __init__(self):
        self.work_duration = 25  # minutes
        self.short_break = 5  # minutes
        self.long_break = 15  # minutes
        self.sessions_until_long_break = 4
        
        self.current_session = 0
        self.is_running = False
        self.is_paused = False
        self.timer_thread = None
        self.stop_event = Event()
        
        self.stats_file = "pomodoro_stats.json"
        self.load_stats()
    
    def load_stats(self):
        """Load pomodoro statistics"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            else:
                self.stats = {
                    'total_sessions': 0,
                    'total_focus_time': 0,
                    'sessions_today': 0,
                    'last_session_date': None,
                    'streak_days': 0
                }
        except Exception:
            self.stats = {
                'total_sessions': 0,
                'total_focus_time': 0,
                'sessions_today': 0,
                'last_session_date': None,
                'streak_days': 0
            }
    
    def save_stats(self):
        """Save pomodoro statistics"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            pass
    
    def start_session(self, duration=None):
        """Start a Pomodoro session"""
        if self.is_running:
            return "⚠️ A Pomodoro session is already running!"
        
        if duration:
            self.work_duration = duration
        
        self.is_running = True
        self.is_paused = False
        self.stop_event.clear()
        self.current_session += 1
        
        output = f"\n{'='*50}\n"
        output += f"🍅 POMODORO SESSION {self.current_session} STARTED\n"
        output += f"{'='*50}\n\n"
        output += f"⏰ Duration: {self.work_duration} minutes\n"
        output += f"🎯 Focus on your task!\n"
        output += f"{'='*50}\n"
        
        self.timer_thread = Thread(target=self._run_timer, args=(self.work_duration * 60, 'work'))
        self.timer_thread.daemon = True
        self.timer_thread.start()
        
        return output
    
    def start_break(self, break_type='short'):
        """Start a break session"""
        if self.is_running:
            return "⚠️ Please stop the current session first!"
        
        duration = self.long_break if break_type == 'long' else self.short_break
        
        self.is_running = True
        self.is_paused = False
        self.stop_event.clear()
        
        output = f"\n{'='*50}\n"
        output += f"☕ BREAK TIME ({break_type.upper()})\n"
        output += f"{'='*50}\n\n"
        output += f"⏰ Duration: {duration} minutes\n"
        output += f"😌 Relax and recharge!\n"
        output += f"{'='*50}\n"
        
        self.timer_thread = Thread(target=self._run_timer, args=(duration * 60, 'break'))
        self.timer_thread.daemon = True
        self.timer_thread.start()
        
        return output
    
    def pause_session(self):
        """Pause the current session"""
        if not self.is_running:
            return "⚠️ No session is running!"
        
        if self.is_paused:
            return "⚠️ Session is already paused!"
        
        self.is_paused = True
        return "⏸️ Session paused. Use 'resume pomodoro' to continue."
    
    def resume_session(self):
        """Resume a paused session"""
        if not self.is_running:
            return "⚠️ No session is running!"
        
        if not self.is_paused:
            return "⚠️ Session is not paused!"
        
        self.is_paused = False
        return "▶️ Session resumed!"
    
    def stop_session(self):
        """Stop the current session"""
        if not self.is_running:
            return "⚠️ No session is running!"
        
        self.stop_event.set()
        self.is_running = False
        self.is_paused = False
        
        return "🛑 Pomodoro session stopped."
    
    def _run_timer(self, duration_seconds, session_type):
        """Run the timer (background thread)"""
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        while time.time() < end_time and not self.stop_event.is_set():
            if not self.is_paused:
                time.sleep(1)
            else:
                time.sleep(0.5)
        
        if not self.stop_event.is_set():
            self._session_complete(session_type)
    
    def _session_complete(self, session_type):
        """Handle session completion"""
        self.is_running = False
        
        if session_type == 'work':
            self._update_stats()
            
            if self.current_session % self.sessions_until_long_break == 0:
                print(f"\n🎉 Great work! Time for a long break ({self.long_break} min)!")
            else:
                print(f"\n✅ Session complete! Take a short break ({self.short_break} min)!")
        else:
            print("\n🔔 Break is over! Ready for the next session?")
    
    def _update_stats(self):
        """Update session statistics"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if self.stats['last_session_date'] != today:
            self.stats['sessions_today'] = 0
            
            if self.stats['last_session_date']:
                last_date = datetime.strptime(self.stats['last_session_date'], "%Y-%m-%d")
                if (datetime.now() - last_date).days == 1:
                    self.stats['streak_days'] += 1
                else:
                    self.stats['streak_days'] = 1
        
        self.stats['total_sessions'] += 1
        self.stats['total_focus_time'] += self.work_duration
        self.stats['sessions_today'] += 1
        self.stats['last_session_date'] = today
        
        self.save_stats()
    
    def get_status(self):
        """Get current timer status"""
        if not self.is_running:
            return "⚠️ No Pomodoro session is currently running."
        
        status = "⏸️ PAUSED" if self.is_paused else "▶️ RUNNING"
        
        output = f"\n{'='*50}\n"
        output += f"🍅 POMODORO STATUS\n"
        output += f"{'='*50}\n\n"
        output += f"Status: {status}\n"
        output += f"Session: #{self.current_session}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def get_stats(self):
        """Get Pomodoro statistics"""
        output = f"\n{'='*50}\n"
        output += f"📊 POMODORO STATISTICS\n"
        output += f"{'='*50}\n\n"
        output += f"🍅 Total Sessions: {self.stats['total_sessions']}\n"
        output += f"⏱️  Total Focus Time: {self.stats['total_focus_time']} minutes\n"
        output += f"📅 Sessions Today: {self.stats['sessions_today']}\n"
        output += f"🔥 Current Streak: {self.stats['streak_days']} days\n"
        output += f"{'='*50}\n"
        
        return output
    
    def set_custom_duration(self, work=25, short_break=5, long_break=15):
        """Set custom durations for sessions"""
        self.work_duration = work
        self.short_break = short_break
        self.long_break = long_break
        
        output = f"\n{'='*50}\n"
        output += f"⚙️ POMODORO SETTINGS UPDATED\n"
        output += f"{'='*50}\n\n"
        output += f"Work Session: {work} minutes\n"
        output += f"Short Break: {short_break} minutes\n"
        output += f"Long Break: {long_break} minutes\n"
        output += f"{'='*50}\n"
        
        return output

if __name__ == "__main__":
    timer = PomodoroTimer()
    
    print("Testing Pomodoro Timer...")
    print(timer.get_stats())
    print(timer.set_custom_duration(1, 1, 2))
