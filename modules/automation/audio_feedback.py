"""
Audio Feedback Module for Gesture Recognition
Plays sound signals when listening starts/stops
"""

import os
import threading
from typing import Optional

# Try to use pygame for better sound quality
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

# Fallback to system beep
import sys
import platform


class AudioFeedback:
    """Plays audio signals for gesture recognition events"""
    
    def __init__(self):
        """Initialize audio feedback system"""
        self.enabled = True
        self.volume = 0.7
        
        # Generate simple beep sounds if pygame available
        if PYGAME_AVAILABLE:
            self._generate_beep_sounds()
    
    def _generate_beep_sounds(self):
        """Generate simple beep sounds using pygame"""
        try:
            import numpy as np
            
            # Generate listening start sound (rising tone)
            sample_rate = 22050
            duration = 0.2  # seconds
            
            # Rising beep: 800Hz -> 1200Hz
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency_start = np.linspace(800, 1200, len(t))
            signal_start = np.sin(2 * np.pi * frequency_start * t)
            signal_start = (signal_start * 32767 * self.volume).astype(np.int16)
            
            # Convert to stereo
            stereo_signal_start = np.column_stack((signal_start, signal_start))
            
            self.listening_start_sound = pygame.sndarray.make_sound(stereo_signal_start)
            
            # Falling beep for stop: 1200Hz -> 800Hz
            frequency_stop = np.linspace(1200, 800, len(t))
            signal_stop = np.sin(2 * np.pi * frequency_stop * t)
            signal_stop = (signal_stop * 32767 * self.volume).astype(np.int16)
            stereo_signal_stop = np.column_stack((signal_stop, signal_stop))
            
            self.listening_stop_sound = pygame.sndarray.make_sound(stereo_signal_stop)
            
            # Success beep (high tone)
            frequency_success = 1500
            signal_success = np.sin(2 * np.pi * frequency_success * t)
            signal_success = (signal_success * 32767 * self.volume).astype(np.int16)
            stereo_signal_success = np.column_stack((signal_success, signal_success))
            
            self.success_sound = pygame.sndarray.make_sound(stereo_signal_success)
            
        except Exception as e:
            print(f"⚠️  Could not generate beep sounds: {e}")
            self.listening_start_sound = None
            self.listening_stop_sound = None
            self.success_sound = None
    
    def _system_beep(self, frequency: int = 1000, duration: float = 0.2):
        """Fallback to system beep if pygame not available"""
        try:
            if platform.system() == 'Windows':
                import winsound
                winsound.Beep(frequency, int(duration * 1000))
            elif platform.system() == 'Darwin':  # macOS
                os.system(f'say -v "Boing" ""')
            else:  # Linux
                os.system(f'beep -f {frequency} -l {int(duration * 1000)} 2>/dev/null || printf "\\a"')
        except Exception:
            # Last resort: ASCII bell
            print('\a', end='', flush=True)
    
    def play_listening_start(self):
        """Play sound when listening starts"""
        if not self.enabled:
            return
        
        def _play():
            try:
                if PYGAME_AVAILABLE and hasattr(self, 'listening_start_sound') and self.listening_start_sound:
                    self.listening_start_sound.play()
                else:
                    self._system_beep(frequency=1000, duration=0.15)
            except Exception as e:
                print(f"⚠️  Could not play listening start sound: {e}")
        
        # Play in thread to avoid blocking
        threading.Thread(target=_play, daemon=True).start()
    
    def play_listening_stop(self):
        """Play sound when listening stops"""
        if not self.enabled:
            return
        
        def _play():
            try:
                if PYGAME_AVAILABLE and hasattr(self, 'listening_stop_sound') and self.listening_stop_sound:
                    self.listening_stop_sound.play()
                else:
                    self._system_beep(frequency=800, duration=0.15)
            except Exception as e:
                print(f"⚠️  Could not play listening stop sound: {e}")
        
        threading.Thread(target=_play, daemon=True).start()
    
    def play_success(self):
        """Play sound when command recognized successfully"""
        if not self.enabled:
            return
        
        def _play():
            try:
                if PYGAME_AVAILABLE and hasattr(self, 'success_sound') and self.success_sound:
                    self.success_sound.play()
                else:
                    self._system_beep(frequency=1500, duration=0.1)
            except Exception as e:
                print(f"⚠️  Could not play success sound: {e}")
        
        threading.Thread(target=_play, daemon=True).start()
    
    def set_enabled(self, enabled: bool):
        """Enable or disable audio feedback"""
        self.enabled = enabled
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        
        # Update sound volumes if pygame available
        if PYGAME_AVAILABLE:
            self._generate_beep_sounds()


# Global instance
_audio_feedback: Optional[AudioFeedback] = None


def get_audio_feedback() -> AudioFeedback:
    """Get global audio feedback instance"""
    global _audio_feedback
    if _audio_feedback is None:
        _audio_feedback = AudioFeedback()
    return _audio_feedback


def play_listening_signal():
    """Quick helper to play listening start signal"""
    get_audio_feedback().play_listening_start()


def play_stop_signal():
    """Quick helper to play listening stop signal"""
    get_audio_feedback().play_listening_stop()


def play_success_signal():
    """Quick helper to play success signal"""
    get_audio_feedback().play_success()
