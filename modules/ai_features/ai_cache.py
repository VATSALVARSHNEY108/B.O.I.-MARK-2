"""
AI Response Cache System
Provides fast caching for AI responses to reduce latency and API calls
"""
import json
import hashlib
from typing import Optional, Any
from datetime import datetime, timedelta


class AIResponseCache:
    """Intelligent caching system for AI responses"""
    
    def __init__(self, max_size: int = 200, ttl_hours: int = 24):
        self._cache = {}
        self._max_size = max_size
        self._ttl = timedelta(hours=ttl_hours)
        self._hit_count = 0
        self._miss_count = 0
    
    def _generate_key(self, prompt: str, model: str = "gemini-2.0-flash") -> str:
        """Generate cache key from prompt and model"""
        combined = f"{model}:{prompt.lower().strip()}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get(self, prompt: str, model: str = "gemini-2.0-flash") -> Optional[str]:
        """Get cached response if available and not expired"""
        key = self._generate_key(prompt, model)
        
        if key in self._cache:
            cached_data = self._cache[key]
            
            # Check if expired
            if datetime.now() - cached_data['timestamp'] < self._ttl:
                self._hit_count += 1
                return cached_data['response']
            else:
                # Remove expired entry
                del self._cache[key]
        
        self._miss_count += 1
        return None
    
    def set(self, prompt: str, response: str, model: str = "gemini-2.0-flash"):
        """Cache a response"""
        # Enforce max size - remove oldest entry if needed
        if len(self._cache) >= self._max_size:
            oldest_key = min(self._cache.keys(), 
                           key=lambda k: self._cache[k]['timestamp'])
            del self._cache[oldest_key]
        
        key = self._generate_key(prompt, model)
        self._cache[key] = {
            'response': response,
            'timestamp': datetime.now(),
            'prompt': prompt[:100]  # Store truncated prompt for debugging
        }
    
    def clear(self):
        """Clear all cached responses"""
        self._cache.clear()
        self._hit_count = 0
        self._miss_count = 0
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total_requests = self._hit_count + self._miss_count
        hit_rate = (self._hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_size": len(self._cache),
            "max_size": self._max_size,
            "hit_count": self._hit_count,
            "miss_count": self._miss_count,
            "hit_rate_percent": round(hit_rate, 2),
            "total_requests": total_requests
        }


# Global cache instance
global_ai_cache = AIResponseCache()
