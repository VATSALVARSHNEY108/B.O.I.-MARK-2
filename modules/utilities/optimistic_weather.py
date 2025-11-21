"""
Optimistic Weather System for BOI (Barely Obeys Instructions)
Presents weather information in a positive, upbeat, and motivating way
"""

import random
import requests
from datetime import datetime


class OptimisticWeatherPresenter:
    """Presents weather data with optimistic, positive spin"""
    
    def __init__(self):
        self.positive_phrases = {
            "clear": [
                "🌞 What a beautiful clear day! Perfect for enjoying the sunshine!",
                "☀️ The sky is absolutely gorgeous today! Great time to be outside!",
                "✨ Crystal clear skies await you! Nature's gift to make your day special!",
                "🌟 Stunning clear weather! This is your day to shine!"
            ],
            "sunny": [
                "🌞 Glorious sunshine to brighten your day!",
                "☀️ The sun is out and smiling at you!",
                "✨ Radiant sunshine to energize your adventures!",
                "🌟 Brilliant sunny weather - your perfect day begins now!"
            ],
            "cloudy": [
                "☁️ Lovely clouds creating natural shade - perfect for outdoor activities without harsh sun!",
                "🌥️ Gentle cloud cover making it comfortable - great for a peaceful walk!",
                "☁️ Soft clouds painting the sky beautifully - photography weather!",
                "🌤️ Mild cloud cover keeping things cool and comfortable!"
            ],
            "rain": [
                "🌧️ Refreshing rain bringing life to nature! Cozy weather for indoor comfort!",
                "☔ Nature's shower making everything green and fresh! Great reading weather!",
                "💧 Cleansing rain refreshing the earth - tomorrow will smell amazing!",
                "🌧️ Perfect weather for hot coffee and good vibes! The earth is happy!"
            ],
            "storm": [
                "⚡ Nature's spectacular light show! Stay cozy and safe indoors!",
                "🌩️ Dramatic weather creating epic views! Perfect time for indoor productivity!",
                "⛈️ Powerful nature display - stay safe and enjoy from inside!",
                "⚡ Electrifying atmosphere! Great excuse for a relaxing day in!"
            ],
            "snow": [
                "❄️ Magical winter wonderland forming! Nature's blanket of beauty!",
                "⛄ Snow is falling - time for winter fun and hot chocolate!",
                "🌨️ Gorgeous snowflakes creating a fairy tale scene!",
                "❄️ Winter magic happening right now! Bundle up and enjoy!"
            ],
            "fog": [
                "🌫️ Mystical fog creating an enchanting atmosphere!",
                "🌁 Dreamy fog adding mystery to your day! Drive safe and enjoy the mood!",
                "🌫️ Ethereal fog making everything look magical!",
                "🌁 Nature's soft blanket creating a peaceful ambiance!"
            ],
            "wind": [
                "💨 Refreshing breeze energizing the air! Great for flying kites!",
                "🌬️ Invigorating winds of change! Nature's way of keeping things fresh!",
                "💨 Breezy day perfect for feeling alive!",
                "🌬️ Dynamic air movement - energy in the atmosphere!"
            ]
        }
        
        self.temperature_positives = {
            "hot": [
                "🔥 Warm and toasty! Perfect beach/pool weather!",
                "🌡️ Delightfully warm - great for summer activities!",
                "☀️ Gloriously hot - ice cream weather!",
                "🏖️ Prime sunshine and warmth - summer vibes!"
            ],
            "warm": [
                "🌤️ Pleasantly warm - ideal outdoor temperature!",
                "☀️ Comfortable warmth making everything perfect!",
                "🌻 Just right warmth for any activity!",
                "✨ Beautiful mild temperature - couldn't be better!"
            ],
            "mild": [
                "🌸 Perfectly mild - nature's comfort zone!",
                "☁️ Ideal temperature for absolutely anything!",
                "🍃 Goldilocks weather - not too hot, not too cold!",
                "🌿 Comfortable climate making your day easy!"
            ],
            "cool": [
                "🍂 Refreshingly cool - sweater weather perfection!",
                "❄️ Crisp and invigorating - energizing freshness!",
                "🌬️ Pleasantly cool - great for staying active!",
                "🍁 Lovely cool air - autumn magic!"
            ],
            "cold": [
                "❄️ Beautifully crisp - cozy season in full effect!",
                "☃️ Wonderfully cold - perfect for hot drinks and warmth!",
                "🧣 Refreshingly chilly - brings out the best coziness!",
                "🔥 Cold outside, warm inside - the best contrast!"
            ]
        }
        
        self.motivational_additions = [
            "Make the most of this beautiful day!",
            "Every weather brings its own magic!",
            "Nature is spectacular in all its forms!",
            "Today is going to be amazing!",
            "Embrace the weather and have a wonderful day!",
            "You've got this - weather is just part of the adventure!",
            "Perfect day to make great memories!",
            "Weather can't stop your positive energy!",
            "Turn this weather into your opportunity!",
            "Every day is a gift - enjoy it!"
        ]
    
    def get_weather_emoji(self, condition: str) -> str:
        """Get appropriate emoji for weather condition"""
        condition_lower = condition.lower()
        
        emoji_map = {
            "clear": "☀️",
            "sunny": "🌞",
            "cloudy": "☁️",
            "partly": "⛅",
            "rain": "🌧️",
            "drizzle": "🌦️",
            "storm": "⛈️",
            "thunder": "⚡",
            "snow": "❄️",
            "fog": "🌫️",
            "mist": "🌁",
            "wind": "💨"
        }
        
        for key, emoji in emoji_map.items():
            if key in condition_lower:
                return emoji
        
        return "🌤️"
    
    def get_positive_message(self, condition: str) -> str:
        """Get optimistic message for weather condition"""
        condition_lower = condition.lower()
        
        for key in self.positive_phrases:
            if key in condition_lower:
                return random.choice(self.positive_phrases[key])
        
        return random.choice(self.positive_phrases["clear"])
    
    def get_temperature_message(self, temp_c: float) -> str:
        """Get optimistic message for temperature"""
        if temp_c >= 30:
            category = "hot"
        elif temp_c >= 20:
            category = "warm"
        elif temp_c >= 10:
            category = "mild"
        elif temp_c >= 0:
            category = "cool"
        else:
            category = "cold"
        
        return random.choice(self.temperature_positives[category])
    
    def format_optimistic_weather(self, city: str, temp_c: float, temp_f: float, 
                                  condition: str, humidity: int = None, 
                                  wind_speed: float = None) -> str:
        """Format weather data with optimistic presentation"""
        
        emoji = self.get_weather_emoji(condition)
        positive_msg = self.get_positive_message(condition)
        temp_msg = self.get_temperature_message(temp_c)
        motivation = random.choice(self.motivational_additions)
        
        output = f"🌍 **Weather Update for {city}** 🌍\n\n"
        output += f"{positive_msg}\n\n"
        output += f"{emoji} **Condition:** {condition}\n"
        output += f"{temp_msg}\n"
        output += f"🌡️ **Temperature:** {temp_c}°C ({temp_f}°F)\n"
        
        if humidity:
            if humidity > 70:
                output += f"💧 **Humidity:** {humidity}% - Extra fresh air!\n"
            elif humidity < 30:
                output += f"💧 **Humidity:** {humidity}% - Crisp and clear!\n"
            else:
                output += f"💧 **Humidity:** {humidity}% - Just right!\n"
        
        if wind_speed:
            if wind_speed > 20:
                output += f"💨 **Wind:** {wind_speed} km/h - Breezy and dynamic!\n"
            elif wind_speed < 5:
                output += f"🍃 **Wind:** {wind_speed} km/h - Calm and peaceful!\n"
            else:
                output += f"🌬️ **Wind:** {wind_speed} km/h - Gentle breeze!\n"
        
        output += f"\n✨ **{motivation}** ✨"
        
        return output
    
    def get_optimistic_weather_from_api(self, city: str = "New York") -> str:
        """Fetch weather from wttr.in API and present optimistically"""
        try:
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                current = data.get("current_condition", [{}])[0]
                
                temp_c = float(current.get("temp_C", 20))
                temp_f = float(current.get("temp_F", 68))
                condition = current.get("weatherDesc", [{}])[0].get("value", "Clear")
                humidity = int(current.get("humidity", 50))
                wind_speed = float(current.get("windspeedKmph", 10))
                
                return self.format_optimistic_weather(
                    city, temp_c, temp_f, condition, humidity, wind_speed
                )
            else:
                return self._get_fallback_optimistic_message(city)
                
        except Exception as e:
            return self._get_fallback_optimistic_message(city, str(e))
    
    def _get_fallback_optimistic_message(self, city: str, error: str = None) -> str:
        """Provide optimistic message when API fails"""
        messages = [
            f"🌤️ Hey! I couldn't fetch the live weather for {city} right now, but that's okay!\n\n"
            f"✨ Remember: Every day is an opportunity, regardless of the weather!\n\n"
            f"💪 You're going to have an amazing day! Stay positive and make it count!",
            
            f"🌟 Weather data is taking a break for {city}, but YOU don't have to!\n\n"
            f"☀️ Whatever the weather, you've got the power to make today incredible!\n\n"
            f"🎯 Go out there and shine!",
            
            f"🌈 The weather in {city} is being mysterious today, but that's part of the adventure!\n\n"
            f"🚀 Don't let anything stop your positive vibes!\n\n"
            f"💖 You're going to rock this day!"
        ]
        
        return random.choice(messages)
    
    def get_forecast_optimistic(self, city: str = "New York", days: int = 3) -> str:
        """Get optimistic weather forecast"""
        try:
            try:
                days = int(days)
                days = max(1, min(days, 7))
            except (ValueError, TypeError):
                days = 3
            
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                forecast = data.get("weather", [])[:days]
                
                output = f"🌟 **{days}-Day Optimistic Forecast for {city}** 🌟\n\n"
                
                for day_data in forecast:
                    date = day_data.get("date", "Unknown")
                    max_temp_c = day_data.get("maxtempC", "20")
                    min_temp_c = day_data.get("mintempC", "15")
                    condition = day_data.get("hourly", [{}])[0].get("weatherDesc", [{}])[0].get("value", "Clear")
                    
                    emoji = self.get_weather_emoji(condition)
                    positive = self.get_positive_message(condition)
                    
                    output += f"📅 **{date}**\n"
                    output += f"{emoji} {condition}\n"
                    output += f"🌡️ {min_temp_c}°C - {max_temp_c}°C\n"
                    output += f"💭 {positive}\n\n"
                
                output += f"✨ **Great days ahead! Plan something wonderful!** ✨"
                return output
            else:
                return f"🌤️ Forecast temporarily unavailable for {city}, but every day is full of possibilities! Stay optimistic! 🌟"
                
        except Exception as e:
            return f"🌈 Weather forecast is shy today, but your future is bright regardless! Keep that positive energy! 💪"


# Create global instance
optimistic_weather = OptimisticWeatherPresenter()


if __name__ == "__main__":
    print("Testing Optimistic Weather System...\n")
    print(optimistic_weather.get_optimistic_weather_from_api("London"))
    print("\n" + "="*60 + "\n")
    print(optimistic_weather.get_forecast_optimistic("Paris", 3))
