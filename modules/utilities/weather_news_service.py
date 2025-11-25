"""
Weather & News Service Module
Provides real-time weather information and news headlines
"""

import requests
import json
from datetime import datetime
import time

class WeatherNewsService:
    def __init__(self):
        self.weather_cache = {}
        self.news_cache = {}
        
    def get_weather(self, city="New York"):
        """Get current weather for a city using free API with retry logic"""
        for attempt in range(3):
            try:
                url = f"https://wttr.in/{city}?format=j1"
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    current = data['current_condition'][0]
                    
                    weather_info = {
                        'city': city,
                        'temperature': f"{current['temp_C']}°C / {current['temp_F']}°F",
                        'condition': current['weatherDesc'][0]['value'],
                        'humidity': f"{current['humidity']}%",
                        'wind': f"{current['windspeedKmph']} km/h",
                        'feels_like': f"{current['FeelsLikeC']}°C / {current['FeelsLikeF']}°F",
                        'uv_index': current.get('uvIndex', 'N/A')
                    }
                    
                    return self._format_weather(weather_info)
                else:
                    return f"Could not fetch weather for {city}. Please check the city name."
                    
            except requests.exceptions.Timeout:
                if attempt < 2:
                    time.sleep(1)
                    continue
                return self._format_weather_error(city, "The weather service is taking too long to respond. Please try again in a moment.")
            except requests.exceptions.ConnectionError:
                if attempt < 2:
                    time.sleep(1)
                    continue
                return self._format_weather_error(city, "Unable to connect to the weather service. Please check your internet connection.")
            except Exception as e:
                if attempt < 2:
                    time.sleep(1)
                    continue
                return self._format_weather_error(city, f"Weather service error: {str(e)}")
        
        return self._format_weather_error(city, "Weather service is currently unavailable after multiple attempts.")
    
    def get_forecast(self, city="New York", days=3):
        """Get weather forecast for upcoming days with retry logic"""
        for attempt in range(3):
            try:
                url = f"https://wttr.in/{city}?format=j1"
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    forecast_data = data['weather'][:days]
                    
                    forecast = f"📅 {days}-Day Forecast for {city}:\n\n"
                    
                    for day in forecast_data:
                        date = day['date']
                        max_temp = day['maxtempC']
                        min_temp = day['mintempC']
                        condition = day['hourly'][0]['weatherDesc'][0]['value']
                        
                        forecast += f"📆 {date}:\n"
                        forecast += f"   🌡️ High: {max_temp}°C, Low: {min_temp}°C\n"
                        forecast += f"   ☁️ {condition}\n\n"
                    
                    return forecast
                else:
                    return f"Could not fetch forecast for {city}."
                    
            except requests.exceptions.Timeout:
                if attempt < 2:
                    time.sleep(1)
                    continue
                return f"⚠️ Forecast service timeout. Please try again later."
            except requests.exceptions.ConnectionError:
                if attempt < 2:
                    time.sleep(1)
                    continue
                return f"⚠️ Unable to connect to forecast service. Please check your internet connection."
            except Exception as e:
                if attempt < 2:
                    time.sleep(1)
                    continue
                return f"⚠️ Forecast service error: {str(e)}"
        
        return f"⚠️ Forecast service is currently unavailable for {city}."
    
    def get_news_headlines(self, category="general", count=5):
        """Get latest news headlines - requires NEWS_API_KEY environment variable"""
        try:
            import os
            api_key = os.environ.get('NEWS_API_KEY')
            
            if not api_key:
                return self._format_general_news(category, count)
            
            categories_map = {
                'general': 'general',
                'business': 'business',
                'technology': 'technology',
                'tech': 'technology',
                'sports': 'sports',
                'entertainment': 'entertainment',
                'health': 'health',
                'science': 'science'
            }
            
            cat = categories_map.get(category.lower(), 'general')
            
            url = f"https://newsapi.org/v2/top-headlines?category={cat}&pageSize={count}&apiKey={api_key}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                if articles:
                    return self._format_news(articles, category)
            
            return self._format_general_news(category, count)
                
        except Exception as e:
            return self._format_general_news(category, count)
    
    def _format_weather(self, weather):
        """Format weather information beautifully"""
        output = f"\n{'='*50}\n"
        output += f"🌤️  WEATHER FOR {weather['city'].upper()}\n"
        output += f"{'='*50}\n\n"
        output += f"🌡️  Temperature: {weather['temperature']}\n"
        output += f"🌡️  Feels Like: {weather['feels_like']}\n"
        output += f"☁️  Condition: {weather['condition']}\n"
        output += f"💧 Humidity: {weather['humidity']}\n"
        output += f"💨 Wind Speed: {weather['wind']}\n"
        output += f"☀️  UV Index: {weather['uv_index']}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def _format_weather_error(self, city, error_message):
        """Format weather error message"""
        output = f"\n{'='*50}\n"
        output += f"⚠️  WEATHER SERVICE ERROR\n"
        output += f"{'='*50}\n\n"
        output += f"📍 City: {city}\n"
        output += f"❌ Error: {error_message}\n\n"
        output += f"💡 Tips:\n"
        output += f"   • Check your internet connection\n"
        output += f"   • Try again in a few moments\n"
        output += f"   • Verify the city name spelling\n"
        output += f"{'='*50}\n"
        
        return output
    
    def _format_news(self, articles, category):
        """Format news articles beautifully"""
        output = f"\n{'='*50}\n"
        output += f"📰 TOP {category.upper()} NEWS HEADLINES\n"
        output += f"{'='*50}\n\n"
        
        for i, article in enumerate(articles[:5], 1):
            title = article.get('title', 'No title')
            source = article.get('source', {}).get('name', 'Unknown')
            
            output += f"{i}. {title}\n"
            output += f"   📌 Source: {source}\n\n"
        
        output += f"{'='*50}\n"
        return output
    
    def _format_general_news(self, category, count):
        """Format general news when API unavailable"""
        output = f"\n{'='*50}\n"
        output += f"📰 {category.upper()} NEWS\n"
        output += f"{'='*50}\n\n"
        output += "ℹ️  News service requires an API key.\n"
        output += "To get real news headlines:\n"
        output += "1. Get free API key from newsapi.org\n"
        output += "2. Set NEWS_API_KEY environment variable\n"
        output += f"{'='*50}\n"
        
        return output
    
    def get_weather_alert(self, city="New York"):
        """Check for weather alerts and warnings"""
        return f"Weather alerts feature - Coming soon for {city}!"

if __name__ == "__main__":
    service = WeatherNewsService()
    
    print("Testing Weather Service...")
    print(service.get_weather("London"))
    
    print("\nTesting Forecast...")
    print(service.get_forecast("Paris", days=3))
    
    print("\nTesting News Service...")
    print(service.get_news_headlines("technology", count=5))
