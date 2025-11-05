"""
Timer & Stopwatch Module
Provides countdown timer, stopwatch, and time tracking features
"""

import time
import threading
from datetime import datetime, timedelta
import json
import os

class TimerStopwatch:
    def __init__(self):
        self.active_timers = {}
        self.cancelled_timers = set()
        self.stopwatch_start = None
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0
        self.lap_times = []
        self.timer_callbacks = []
        
    def start_timer(self, duration_seconds, name="Timer", callback=None):
        """Start a countdown timer"""
        try:
            timer_id = f"timer_{len(self.active_timers) + 1}"
            end_time = datetime.now() + timedelta(seconds=duration_seconds)
            
            self.active_timers[timer_id] = {
                "name": name,
                "duration": duration_seconds,
                "end_time": end_time,
                "started": datetime.now(),
                "callback": callback
            }
            
            thread = threading.Thread(target=self._run_timer, args=(timer_id,))
            thread.daemon = True
            thread.start()
            
            hours = duration_seconds // 3600
            minutes = (duration_seconds % 3600) // 60
            seconds = duration_seconds % 60
            
            time_str = ""
            if hours > 0:
                time_str = f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                time_str = f"{minutes}m {seconds}s"
            else:
                time_str = f"{seconds}s"
            
            return f"⏰ Timer '{name}' started for {time_str}\nTimer ID: {timer_id}"
        except Exception as e:
            return f"❌ Failed to start timer: {str(e)}"
    
    def _run_timer(self, timer_id):
        """Run timer in background thread"""
        timer = self.active_timers.get(timer_id)
        if not timer:
            if timer_id in self.cancelled_timers:
                self.cancelled_timers.discard(timer_id)
            return
        
        while datetime.now() < timer["end_time"]:
            if timer_id in self.cancelled_timers:
                self.cancelled_timers.discard(timer_id)
                return
            time.sleep(1)
        
        if timer_id in self.cancelled_timers:
            self.cancelled_timers.discard(timer_id)
            return
        
        if timer["callback"]:
            timer["callback"](timer["name"])
        
        self.timer_callbacks.append({
            "timer_id": timer_id,
            "name": timer["name"],
            "completed": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        print(f"\n{'='*60}")
        print(f"⏰ TIMER ALERT!")
        print(f"{'='*60}")
        print(f"Timer: {timer['name']}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        if timer_id in self.active_timers:
            del self.active_timers[timer_id]
    
    def stop_timer(self, timer_id):
        """Stop a running timer"""
        try:
            if timer_id in self.active_timers:
                timer = self.active_timers[timer_id]
                self.cancelled_timers.add(timer_id)
                del self.active_timers[timer_id]
                return f"⏹️ Timer '{timer['name']}' stopped"
            else:
                return f"⚠️ Timer {timer_id} not found"
        except Exception as e:
            return f"❌ Failed to stop timer: {str(e)}"
    
    def list_timers(self):
        """List all active timers"""
        try:
            if not self.active_timers:
                return "ℹ️ No active timers"
            
            result = "⏰ Active Timers:\n" + "=" * 50 + "\n"
            for timer_id, timer in self.active_timers.items():
                remaining = (timer["end_time"] - datetime.now()).total_seconds()
                if remaining > 0:
                    hours = int(remaining // 3600)
                    minutes = int((remaining % 3600) // 60)
                    seconds = int(remaining % 60)
                    
                    time_left = ""
                    if hours > 0:
                        time_left = f"{hours}h {minutes}m {seconds}s"
                    elif minutes > 0:
                        time_left = f"{minutes}m {seconds}s"
                    else:
                        time_left = f"{seconds}s"
                    
                    result += f"\n{timer_id}: {timer['name']}\n"
                    result += f"  Time Remaining: {time_left}\n"
            
            result += "=" * 50
            return result
        except Exception as e:
            return f"❌ Failed to list timers: {str(e)}"
    
    def start_stopwatch(self):
        """Start the stopwatch"""
        try:
            if self.stopwatch_running:
                return "⚠️ Stopwatch is already running"
            
            self.stopwatch_start = time.time()
            self.stopwatch_running = True
            self.lap_times = []
            
            return "▶️ Stopwatch started"
        except Exception as e:
            return f"❌ Failed to start stopwatch: {str(e)}"
    
    def stop_stopwatch(self):
        """Stop the stopwatch"""
        try:
            if not self.stopwatch_running:
                return "⚠️ Stopwatch is not running"
            
            self.stopwatch_elapsed += time.time() - self.stopwatch_start
            self.stopwatch_running = False
            
            elapsed_str = self._format_elapsed(self.stopwatch_elapsed)
            return f"⏹️ Stopwatch stopped at {elapsed_str}"
        except Exception as e:
            return f"❌ Failed to stop stopwatch: {str(e)}"
    
    def pause_stopwatch(self):
        """Pause the stopwatch"""
        try:
            if not self.stopwatch_running:
                return "⚠️ Stopwatch is not running"
            
            self.stopwatch_elapsed += time.time() - self.stopwatch_start
            self.stopwatch_running = False
            
            elapsed_str = self._format_elapsed(self.stopwatch_elapsed)
            return f"⏸️ Stopwatch paused at {elapsed_str}"
        except Exception as e:
            return f"❌ Failed to pause stopwatch: {str(e)}"
    
    def resume_stopwatch(self):
        """Resume the stopwatch"""
        try:
            if self.stopwatch_running:
                return "⚠️ Stopwatch is already running"
            
            self.stopwatch_start = time.time()
            self.stopwatch_running = True
            
            return "▶️ Stopwatch resumed"
        except Exception as e:
            return f"❌ Failed to resume stopwatch: {str(e)}"
    
    def reset_stopwatch(self):
        """Reset the stopwatch"""
        try:
            self.stopwatch_start = None
            self.stopwatch_running = False
            self.stopwatch_elapsed = 0
            self.lap_times = []
            
            return "🔄 Stopwatch reset"
        except Exception as e:
            return f"❌ Failed to reset stopwatch: {str(e)}"
    
    def lap_stopwatch(self):
        """Record a lap time"""
        try:
            if not self.stopwatch_running:
                return "⚠️ Stopwatch is not running"
            
            current_time = self.stopwatch_elapsed + (time.time() - self.stopwatch_start)
            lap_number = len(self.lap_times) + 1
            
            if self.lap_times:
                lap_time = current_time - sum(self.lap_times)
            else:
                lap_time = current_time
            
            self.lap_times.append(lap_time)
            
            lap_str = self._format_elapsed(lap_time)
            total_str = self._format_elapsed(current_time)
            
            return f"🏁 Lap {lap_number}: {lap_str} (Total: {total_str})"
        except Exception as e:
            return f"❌ Failed to record lap: {str(e)}"
    
    def get_stopwatch_time(self):
        """Get current stopwatch time"""
        try:
            if self.stopwatch_running:
                current_time = self.stopwatch_elapsed + (time.time() - self.stopwatch_start)
            else:
                current_time = self.stopwatch_elapsed
            
            elapsed_str = self._format_elapsed(current_time)
            status = "Running" if self.stopwatch_running else "Paused"
            
            result = f"⏱️ Stopwatch: {elapsed_str} ({status})"
            
            if self.lap_times:
                result += f"\n\nLap Times:\n" + "=" * 50
                for i, lap_time in enumerate(self.lap_times, 1):
                    lap_str = self._format_elapsed(lap_time)
                    result += f"\nLap {i}: {lap_str}"
                result += "\n" + "=" * 50
            
            return result
        except Exception as e:
            return f"❌ Failed to get stopwatch time: {str(e)}"
    
    def _format_elapsed(self, seconds):
        """Format elapsed time as HH:MM:SS.ms"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 100)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}.{milliseconds:02d}"
    
    def quick_timer(self, minutes):
        """Quick timer shortcut for common durations"""
        try:
            duration = int(minutes) * 60
            return self.start_timer(duration, f"{minutes} minute timer")
        except Exception as e:
            return f"❌ Failed to start quick timer: {str(e)}"
    
    def pomodoro_timer(self, work_minutes=25, break_minutes=5):
        """Start a Pomodoro work session"""
        try:
            duration = int(work_minutes) * 60
            return self.start_timer(duration, f"Pomodoro - {work_minutes} min work")
        except Exception as e:
            return f"❌ Failed to start Pomodoro timer: {str(e)}"

if __name__ == "__main__":
    timer = TimerStopwatch()
    
    print("Testing Timer & Stopwatch...")
    print(timer.start_timer(5, "Test Timer"))
    print(timer.list_timers())
    
    print("\nTesting Stopwatch...")
    print(timer.start_stopwatch())
    time.sleep(2)
    print(timer.lap_stopwatch())
    time.sleep(1)
    print(timer.get_stopwatch_time())
    print(timer.stop_stopwatch())
