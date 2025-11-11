"""
Quick Information Module
Provides instant responses for date, time, and weather without web search
"""

from datetime import datetime
import calendar


class QuickInfo:
    """Quick access to date, time, and basic information"""
    
    def __init__(self):
        pass
    
    def get_current_time(self, format_type="12hour"):
        """Get current time in various formats"""
        now = datetime.now()
        
        if format_type == "12hour":
            time_str = now.strftime("%I:%M:%S %p")
        else:
            time_str = now.strftime("%H:%M:%S")
        
        output = f"\n{'='*50}\n"
        output += f"🕐 CURRENT TIME\n"
        output += f"{'='*50}\n\n"
        output += f"⏰ Time (12-hour): {now.strftime('%I:%M:%S %p')}\n"
        output += f"⏰ Time (24-hour): {now.strftime('%H:%M:%S')}\n"
        output += f"📅 Day: {now.strftime('%A')}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def get_current_date(self, detailed=True):
        """Get current date with details"""
        now = datetime.now()
        
        output = f"\n{'='*50}\n"
        output += f"📅 CURRENT DATE\n"
        output += f"{'='*50}\n\n"
        
        if detailed:
            # Calculate day of year
            day_of_year = now.timetuple().tm_yday
            days_in_year = 366 if calendar.isleap(now.year) else 365
            days_remaining = days_in_year - day_of_year
            
            # Calculate week number
            week_number = now.isocalendar()[1]
            
            output += f"📆 Full Date: {now.strftime('%A, %B %d, %Y')}\n"
            output += f"📆 Short Date: {now.strftime('%m/%d/%Y')}\n"
            output += f"📆 ISO Format: {now.strftime('%Y-%m-%d')}\n"
            output += f"📊 Day of Year: Day {day_of_year} of {days_in_year}\n"
            output += f"📊 Days Remaining: {days_remaining} days left in {now.year}\n"
            output += f"📊 Week Number: Week {week_number} of {now.year}\n"
            output += f"🗓️  Month: {now.strftime('%B')} (Month {now.month} of 12)\n"
            output += f"🗓️  Quarter: Q{(now.month-1)//3 + 1}\n"
        else:
            output += f"📆 Date: {now.strftime('%A, %B %d, %Y')}\n"
        
        output += f"{'='*50}\n"
        
        return output
    
    def get_date_and_time(self):
        """Get both date and time together"""
        now = datetime.now()
        
        output = f"\n{'='*50}\n"
        output += f"🕐 CURRENT DATE & TIME\n"
        output += f"{'='*50}\n\n"
        output += f"📅 Date: {now.strftime('%A, %B %d, %Y')}\n"
        output += f"⏰ Time: {now.strftime('%I:%M:%S %p')}\n"
        output += f"🌍 Timezone: {now.astimezone().tzname()}\n"
        output += f"📊 Timestamp: {int(now.timestamp())}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def get_day_info(self):
        """Get information about current day"""
        now = datetime.now()
        day_name = now.strftime('%A')
        
        # Fun facts about days
        day_facts = {
            'Monday': '💼 Start of the work week!',
            'Tuesday': '🔥 Keep the momentum going!',
            'Wednesday': '📈 Hump day - halfway there!',
            'Thursday': '🎯 Almost to the weekend!',
            'Friday': '🎉 TGIF - Weekend is near!',
            'Saturday': '🌟 Enjoy your weekend!',
            'Sunday': '☀️ Rest and recharge!'
        }
        
        output = f"\n{'='*50}\n"
        output += f"📅 TODAY'S INFO\n"
        output += f"{'='*50}\n\n"
        output += f"📆 Day: {day_name}\n"
        output += f"💭 {day_facts.get(day_name, 'Have a great day!')}\n"
        output += f"📅 Date: {now.strftime('%B %d, %Y')}\n"
        output += f"⏰ Time: {now.strftime('%I:%M %p')}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def get_week_info(self):
        """Get information about current week"""
        now = datetime.now()
        week_number = now.isocalendar()[1]
        day_name = now.strftime('%A')
        
        # Calculate week progress
        weekday = now.weekday()  # Monday = 0, Sunday = 6
        week_progress = ((weekday + 1) / 7) * 100
        
        output = f"\n{'='*50}\n"
        output += f"📊 WEEK INFORMATION\n"
        output += f"{'='*50}\n\n"
        output += f"📅 Week Number: Week {week_number} of {now.year}\n"
        output += f"📆 Current Day: {day_name}\n"
        output += f"📈 Week Progress: {week_progress:.0f}% complete\n"
        output += f"🗓️  Days into week: {weekday + 1} of 7\n"
        output += f"{'='*50}\n"
        
        return output
    
    def get_month_info(self):
        """Get information about current month"""
        now = datetime.now()
        month_name = now.strftime('%B')
        year = now.year
        
        # Get month details
        days_in_month = calendar.monthrange(year, now.month)[1]
        current_day = now.day
        days_remaining = days_in_month - current_day
        month_progress = (current_day / days_in_month) * 100
        
        output = f"\n{'='*50}\n"
        output += f"📅 MONTH INFORMATION\n"
        output += f"{'='*50}\n\n"
        output += f"🗓️  Month: {month_name} {year}\n"
        output += f"📊 Month Number: {now.month} of 12\n"
        output += f"📆 Current Day: Day {current_day} of {days_in_month}\n"
        output += f"📊 Days Remaining: {days_remaining} days left\n"
        output += f"📈 Month Progress: {month_progress:.1f}% complete\n"
        output += f"🗓️  Quarter: Q{(now.month-1)//3 + 1}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def get_year_info(self):
        """Get information about current year"""
        now = datetime.now()
        year = now.year
        
        # Calculate year progress
        day_of_year = now.timetuple().tm_yday
        is_leap = calendar.isleap(year)
        days_in_year = 366 if is_leap else 365
        days_remaining = days_in_year - day_of_year
        year_progress = (day_of_year / days_in_year) * 100
        
        output = f"\n{'='*50}\n"
        output += f"📅 YEAR INFORMATION\n"
        output += f"{'='*50}\n\n"
        output += f"🗓️  Year: {year} {'(Leap Year 🐸)' if is_leap else ''}\n"
        output += f"📊 Day of Year: Day {day_of_year} of {days_in_year}\n"
        output += f"📊 Days Remaining: {days_remaining} days left in {year}\n"
        output += f"📈 Year Progress: {year_progress:.1f}% complete\n"
        output += f"🗓️  Current Month: {now.strftime('%B')} (Month {now.month})\n"
        output += f"📅 Current Date: {now.strftime('%B %d, %Y')}\n"
        output += f"{'='*50}\n"
        
        return output


def create_quick_info():
    """Factory function to create QuickInfo instance"""
    return QuickInfo()
