"""
Habit Tracker Module
Daily habit checklist with streak tracking and statistics
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class HabitTracker:
    def __init__(self):
        self.habits_file = "data/habits.json"
        self.habits = {}
        self.completions = {}
        self.load_habits()
    
    def load_habits(self):
        """Load habits from file"""
        try:
            os.makedirs("data", exist_ok=True)
            if os.path.exists(self.habits_file):
                with open(self.habits_file, 'r') as f:
                    data = json.load(f)
                    self.habits = data.get("habits", {})
                    self.completions = data.get("completions", {})
            else:
                self.habits = {}
                self.completions = {}
                self.save_habits()
        except Exception as e:
            print(f"Error loading habits: {e}")
            self.habits = {}
            self.completions = {}
    
    def save_habits(self):
        """Save habits to file"""
        try:
            os.makedirs("data", exist_ok=True)
            data = {
                "habits": self.habits,
                "completions": self.completions
            }
            with open(self.habits_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving habits: {e}")
    
    def add_habit(self, name, category="general", goal_frequency="daily", target_count=1):
        """Add a new habit to track"""
        try:
            habit_id = name.lower().replace(" ", "_")
            
            if habit_id in self.habits:
                return f"⚠️ Habit '{name}' already exists"
            
            self.habits[habit_id] = {
                "name": name,
                "category": category,
                "goal_frequency": goal_frequency,
                "target_count": target_count,
                "created": datetime.now().strftime("%Y-%m-%d"),
                "active": True
            }
            
            self.save_habits()
            return f"✅ Added habit: {name} ({goal_frequency})"
        
        except Exception as e:
            return f"❌ Failed to add habit: {str(e)}"
    
    def complete_habit(self, habit_id, date=None):
        """Mark a habit as completed for today or specific date"""
        try:
            if habit_id not in self.habits:
                return f"⚠️ Habit '{habit_id}' not found"
            
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            if habit_id not in self.completions:
                self.completions[habit_id] = []
            
            if date not in self.completions[habit_id]:
                self.completions[habit_id].append(date)
                self.save_habits()
                
                habit_name = self.habits[habit_id]["name"]
                streak = self.get_streak(habit_id)
                
                return f"✅ Completed: {habit_name}\n🔥 Current Streak: {streak} days"
            else:
                return f"ℹ️ Habit already completed today"
        
        except Exception as e:
            return f"❌ Failed to complete habit: {str(e)}"
    
    def uncomplete_habit(self, habit_id, date=None):
        """Unmark a habit completion"""
        try:
            if habit_id not in self.habits:
                return f"⚠️ Habit '{habit_id}' not found"
            
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            if habit_id in self.completions and date in self.completions[habit_id]:
                self.completions[habit_id].remove(date)
                self.save_habits()
                
                habit_name = self.habits[habit_id]["name"]
                return f"↩️ Unmarked: {habit_name} for {date}"
            else:
                return f"ℹ️ Habit not completed on {date}"
        
        except Exception as e:
            return f"❌ Failed to uncomplete habit: {str(e)}"
    
    def get_streak(self, habit_id):
        """Calculate current streak for a habit"""
        try:
            if habit_id not in self.completions or not self.completions[habit_id]:
                return 0
            
            completions = sorted(self.completions[habit_id], reverse=True)
            today = datetime.now().date()
            streak = 0
            
            current_date = today
            for completion_str in completions:
                completion_date = datetime.strptime(completion_str, "%Y-%m-%d").date()
                
                if completion_date == current_date:
                    streak += 1
                    current_date -= timedelta(days=1)
                elif completion_date < current_date:
                    break
            
            return streak
        
        except Exception as e:
            return 0
    
    def get_longest_streak(self, habit_id):
        """Calculate longest streak for a habit"""
        try:
            if habit_id not in self.completions or not self.completions[habit_id]:
                return 0
            
            completions = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in self.completions[habit_id]])
            
            max_streak = 1
            current_streak = 1
            
            for i in range(1, len(completions)):
                if (completions[i] - completions[i-1]).days == 1:
                    current_streak += 1
                    max_streak = max(max_streak, current_streak)
                else:
                    current_streak = 1
            
            return max_streak
        
        except Exception as e:
            return 0
    
    def list_habits(self, category=None):
        """List all habits with their status"""
        try:
            if not self.habits:
                return "ℹ️ No habits tracked yet"
            
            filtered_habits = self.habits
            if category:
                filtered_habits = {hid: h for hid, h in self.habits.items() if h.get("category") == category}
            
            if not filtered_habits:
                return f"ℹ️ No habits in category '{category}'"
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            result = "📊 Habit Tracker:\n" + "=" * 60 + "\n"
            
            for habit_id, habit in filtered_habits.items():
                if not habit.get("active", True):
                    continue
                
                completed_today = habit_id in self.completions and today in self.completions[habit_id]
                streak = self.get_streak(habit_id)
                longest = self.get_longest_streak(habit_id)
                total_completions = len(self.completions.get(habit_id, []))
                
                status_icon = "✅" if completed_today else "⬜"
                
                result += f"\n{status_icon} {habit['name']}"
                result += f" ({habit['category']})\n"
                result += f"   🔥 Streak: {streak} days | 🏆 Best: {longest} days | 📈 Total: {total_completions}\n"
            
            result += "=" * 60
            return result
        
        except Exception as e:
            return f"❌ Failed to list habits: {str(e)}"
    
    def today_checklist(self):
        """Show today's habit checklist"""
        try:
            if not self.habits:
                return "ℹ️ No habits tracked yet"
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            result = f"📋 Daily Habit Checklist - {today}\n" + "=" * 60 + "\n"
            
            completed_count = 0
            total_count = 0
            
            for habit_id, habit in self.habits.items():
                if not habit.get("active", True):
                    continue
                
                total_count += 1
                completed_today = habit_id in self.completions and today in self.completions[habit_id]
                
                if completed_today:
                    completed_count += 1
                    status = "✅"
                else:
                    status = "⬜"
                
                result += f"{status} {habit['name']}\n"
            
            result += "=" * 60 + "\n"
            result += f"Progress: {completed_count}/{total_count} habits completed"
            
            if completed_count == total_count and total_count > 0:
                result += " 🎉 All done!"
            
            return result
        
        except Exception as e:
            return f"❌ Failed to show checklist: {str(e)}"
    
    def get_statistics(self):
        """Get overall habit statistics"""
        try:
            if not self.habits:
                return "ℹ️ No habits tracked yet"
            
            result = "📊 Habit Statistics:\n" + "=" * 60 + "\n"
            
            total_habits = len([h for h in self.habits.values() if h.get("active", True)])
            today = datetime.now().strftime("%Y-%m-%d")
            completed_today = sum(1 for hid in self.habits if hid in self.completions and today in self.completions[hid])
            
            result += f"\n📌 Active Habits: {total_habits}\n"
            result += f"✅ Completed Today: {completed_today}/{total_habits}\n\n"
            
            result += "Top Performers:\n"
            result += "-" * 60 + "\n"
            
            habit_stats = []
            for habit_id, habit in self.habits.items():
                if not habit.get("active", True):
                    continue
                
                streak = self.get_streak(habit_id)
                longest = self.get_longest_streak(habit_id)
                total = len(self.completions.get(habit_id, []))
                
                habit_stats.append({
                    "name": habit["name"],
                    "streak": streak,
                    "longest": longest,
                    "total": total
                })
            
            habit_stats.sort(key=lambda x: x["streak"], reverse=True)
            
            for i, stat in enumerate(habit_stats[:5], 1):
                result += f"{i}. {stat['name']}\n"
                result += f"   🔥 Streak: {stat['streak']} | 🏆 Best: {stat['longest']} | 📈 Total: {stat['total']}\n"
            
            result += "=" * 60
            return result
        
        except Exception as e:
            return f"❌ Failed to get statistics: {str(e)}"
    
    def delete_habit(self, habit_id):
        """Delete a habit"""
        try:
            if habit_id in self.habits:
                habit_name = self.habits[habit_id]["name"]
                del self.habits[habit_id]
                if habit_id in self.completions:
                    del self.completions[habit_id]
                self.save_habits()
                return f"✅ Deleted habit: {habit_name}"
            else:
                return f"⚠️ Habit '{habit_id}' not found"
        except Exception as e:
            return f"❌ Failed to delete habit: {str(e)}"

if __name__ == "__main__":
    tracker = HabitTracker()
    
    print("Testing Habit Tracker...")
    print(tracker.add_habit("Morning Exercise", "health"))
    print(tracker.add_habit("Read 30 min", "learning"))
    print(tracker.complete_habit("morning_exercise"))
    print(tracker.today_checklist())
    print(tracker.get_statistics())
