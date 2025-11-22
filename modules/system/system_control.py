"""
System Control Module
Handles system-level automation: brightness, audio, sleep/wake, disk cleanup
"""

import platform
import subprocess
import os
import shutil
import time
from datetime import datetime, timedelta
import json
import psutil
import threading

class SystemController:
    def __init__(self):
        self.os = platform.system()
        self.config_file = "system_config.json"
        self.shutdown_process = None
        self.batch_files_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "scripts", "windows_controls")
        self.load_config()
    
    def load_config(self):
        """Load system configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "sleep_schedule": {"enabled": False, "time": "23:00"},
                "wake_schedule": {"enabled": False, "time": "07:00"},
                "auto_cleanup": {"enabled": False, "disk_limit": 90},
                "brightness_schedule": {"enabled": False, "day_brightness": 80, "night_brightness": 30}
            }
            self.save_config()
    
    def save_config(self):
        """Save system configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def mute_microphone(self):
        """Mute system microphone"""
        try:
            if self.os == "Windows":
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                
                devices = AudioUtilities.GetMicrophone()
                if devices:
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = interface.QueryInterface(IAudioEndpointVolume)
                    volume.SetMute(True, None)
                    return "✅ Microphone muted"
                else:
                    return "⚠️ No microphone device found"
            elif self.os == "Darwin":
                subprocess.run(["osascript", "-e", "set volume input volume 0"], check=False)
                return "✅ Microphone muted"
            elif self.os == "Linux":
                subprocess.run(["amixer", "set", "Capture", "nocap"], check=False)
                return "✅ Microphone muted"
        except Exception as e:
            return f"❌ Failed to mute microphone: {str(e)}"
    
    def unmute_microphone(self):
        """Unmute system microphone"""
        try:
            if self.os == "Windows":
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                
                devices = AudioUtilities.GetMicrophone()
                if devices:
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = interface.QueryInterface(IAudioEndpointVolume)
                    volume.SetMute(False, None)
                    return "✅ Microphone unmuted"
                else:
                    return "⚠️ No microphone device found"
            elif self.os == "Darwin":
                subprocess.run(["osascript", "-e", "set volume input volume 50"], check=False)
                return "✅ Microphone unmuted"
            elif self.os == "Linux":
                subprocess.run(["amixer", "set", "Capture", "cap"], check=False)
                return "✅ Microphone unmuted"
        except Exception as e:
            return f"❌ Failed to unmute microphone: {str(e)}"
    
    def set_brightness(self, level):
        """Set screen brightness (0-100)"""
        try:
            level = max(0, min(100, int(level)))
            
            if self.os == "Windows":
                subprocess.run(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})", shell=True, check=False)
                return f"✅ Brightness set to {level}%"
            elif self.os == "Darwin":
                subprocess.run(f"brightness {level/100}", shell=True, check=False)
                return f"✅ Brightness set to {level}%"
            elif self.os == "Linux":
                subprocess.run(f"xrandr --output $(xrandr | grep ' connected' | awk '{{print $1}}') --brightness {level/100}", shell=True, check=False)
                return f"✅ Brightness set to {level}%"
        except Exception as e:
            return f"❌ Failed to set brightness: {str(e)}"
    
    def increase_brightness(self, amount=10):
        """Increase brightness by specified amount"""
        try:
            current = self.get_brightness()
            if current is not None:
                new_level = min(100, current + amount)
                return self.set_brightness(new_level)
            else:
                # If can't get current, just increase by amount
                return self.set_brightness(50 + amount)
        except Exception as e:
            return f"❌ Failed to increase brightness: {str(e)}"
    
    def decrease_brightness(self, amount=10):
        """Decrease brightness by specified amount"""
        try:
            current = self.get_brightness()
            if current is not None:
                new_level = max(0, current - amount)
                return self.set_brightness(new_level)
            else:
                # If can't get current, just decrease
                return self.set_brightness(max(0, 50 - amount))
        except Exception as e:
            return f"❌ Failed to decrease brightness: {str(e)}"
    
    def get_brightness(self):
        """Get current brightness level (0-100)"""
        try:
            if self.os == "Windows":
                result = subprocess.run(
                    "powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness",
                    shell=True, capture_output=True, text=True, check=False
                )
                if result.returncode == 0 and result.stdout.strip():
                    return int(result.stdout.strip())
            elif self.os == "Darwin":
                result = subprocess.run("brightness -l", shell=True, capture_output=True, text=True, check=False)
                if result.returncode == 0 and result.stdout.strip():
                    return int(float(result.stdout.strip()) * 100)
            elif self.os == "Linux":
                result = subprocess.run(
                    "xrandr --verbose | grep -i brightness | head -n 1 | awk '{print $2}'",
                    shell=True, capture_output=True, text=True, check=False
                )
                if result.returncode == 0 and result.stdout.strip():
                    return int(float(result.stdout.strip()) * 100)
            return None
        except:
            return None
    
    def auto_brightness(self):
        """Auto-adjust brightness based on time of day"""
        try:
            current_hour = datetime.now().hour
            
            if 6 <= current_hour < 18:
                brightness = self.config["brightness_schedule"]["day_brightness"]
            else:
                brightness = self.config["brightness_schedule"]["night_brightness"]
            
            return self.set_brightness(brightness)
        except Exception as e:
            return f"❌ Auto-brightness failed: {str(e)}"
    
    # ==================== VOLUME CONTROL ====================
    
    def set_volume(self, level):
        """Set system volume (0-100)"""
        try:
            level = max(0, min(100, int(level)))
            
            if self.os == "Windows":
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                from ctypes import cast, POINTER
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = interface.QueryInterface(IAudioEndpointVolume)
                volume.SetMasterVolumeLevelScalar(level / 100.0, None)
                return f"🔊 Volume set to {level}%"
            elif self.os == "Darwin":
                subprocess.run(f"osascript -e 'set volume output volume {level}'", shell=True, check=False)
                return f"🔊 Volume set to {level}%"
            elif self.os == "Linux":
                # Use pactl for PulseAudio (most common)
                subprocess.run(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%", shell=True, check=False)
                return f"🔊 Volume set to {level}%"
        except Exception as e:
            return f"❌ Failed to set volume: {str(e)}"
    
    def increase_volume(self, amount=10):
        """Increase volume by specified amount"""
        try:
            current = self.get_volume()
            if current is not None:
                new_level = min(100, current + amount)
                return self.set_volume(new_level)
            else:
                # If can't get current, use fallback methods
                if self.os == "Darwin":
                    subprocess.run(f"osascript -e 'set volume output volume (output volume of (get volume settings) + {amount})'", shell=True, check=False)
                    return f"🔊 Volume increased by {amount}%"
                elif self.os == "Linux":
                    subprocess.run(f"pactl set-sink-volume @DEFAULT_SINK@ +{amount}%", shell=True, check=False)
                    return f"🔊 Volume increased by {amount}%"
                else:
                    return f"⚠️ Unable to get current volume. Try setting absolute volume instead."
        except Exception as e:
            return f"❌ Failed to increase volume: {str(e)}"
    
    def decrease_volume(self, amount=10):
        """Decrease volume by specified amount"""
        try:
            current = self.get_volume()
            if current is not None:
                new_level = max(0, current - amount)
                return self.set_volume(new_level)
            else:
                # If can't get current, use fallback methods
                if self.os == "Darwin":
                    subprocess.run(f"osascript -e 'set volume output volume (output volume of (get volume settings) - {amount})'", shell=True, check=False)
                    return f"🔉 Volume decreased by {amount}%"
                elif self.os == "Linux":
                    subprocess.run(f"pactl set-sink-volume @DEFAULT_SINK@ -{amount}%", shell=True, check=False)
                    return f"🔉 Volume decreased by {amount}%"
                else:
                    return f"⚠️ Unable to get current volume. Try setting absolute volume instead."
        except Exception as e:
            return f"❌ Failed to decrease volume: {str(e)}"
    
    def get_volume(self):
        """Get current volume level (0-100)"""
        try:
            if self.os == "Windows":
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = interface.QueryInterface(IAudioEndpointVolume)
                current_volume = volume.GetMasterVolumeLevelScalar()
                return int(current_volume * 100)
            elif self.os == "Darwin":
                result = subprocess.run(
                    "osascript -e 'output volume of (get volume settings)'",
                    shell=True, capture_output=True, text=True, check=False
                )
                if result.returncode == 0 and result.stdout.strip():
                    return int(result.stdout.strip())
            elif self.os == "Linux":
                result = subprocess.run(
                    "pactl get-sink-volume @DEFAULT_SINK@ | grep -Po '[0-9]+(?=%)' | head -1",
                    shell=True, capture_output=True, text=True, check=False
                )
                if result.returncode == 0 and result.stdout.strip():
                    return int(result.stdout.strip())
            return None
        except:
            return None
    
    def mute_volume(self):
        """Mute system volume"""
        try:
            if self.os == "Windows":
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = interface.QueryInterface(IAudioEndpointVolume)
                volume.SetMute(True, None)
                return "🔇 Volume muted"
            elif self.os == "Darwin":
                subprocess.run("osascript -e 'set volume output muted true'", shell=True, check=False)
                return "🔇 Volume muted"
            elif self.os == "Linux":
                subprocess.run("pactl set-sink-mute @DEFAULT_SINK@ 1", shell=True, check=False)
                return "🔇 Volume muted"
        except Exception as e:
            return f"❌ Failed to mute volume: {str(e)}"
    
    def unmute_volume(self):
        """Unmute system volume"""
        try:
            if self.os == "Windows":
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = interface.QueryInterface(IAudioEndpointVolume)
                volume.SetMute(False, None)
                return "🔊 Volume unmuted"
            elif self.os == "Darwin":
                subprocess.run("osascript -e 'set volume output muted false'", shell=True, check=False)
                return "🔊 Volume unmuted"
            elif self.os == "Linux":
                subprocess.run("pactl set-sink-mute @DEFAULT_SINK@ 0", shell=True, check=False)
                return "🔊 Volume unmuted"
        except Exception as e:
            return f"❌ Failed to unmute volume: {str(e)}"
    
    def toggle_mute(self):
        """Toggle mute/unmute"""
        try:
            if self.os == "Windows":
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = interface.QueryInterface(IAudioEndpointVolume)
                current_mute = volume.GetMute()
                volume.SetMute(not current_mute, None)
                return "🔇 Volume muted" if not current_mute else "🔊 Volume unmuted"
            elif self.os == "Darwin":
                result = subprocess.run(
                    "osascript -e 'output muted of (get volume settings)'",
                    shell=True, capture_output=True, text=True, check=False
                )
                is_muted = result.stdout.strip() == "true"
                if is_muted:
                    return self.unmute_volume()
                else:
                    return self.mute_volume()
            elif self.os == "Linux":
                subprocess.run("pactl set-sink-mute @DEFAULT_SINK@ toggle", shell=True, check=False)
                return "🔊 Volume toggled"
        except Exception as e:
            return f"❌ Failed to toggle mute: {str(e)}"
    
    def get_volume_info(self):
        """Get detailed volume information"""
        try:
            level = self.get_volume()
            if level is not None:
                return f"🔊 Current Volume: {level}%"
            else:
                return "ℹ️ Unable to retrieve volume level"
        except Exception as e:
            return f"❌ Failed to get volume info: {str(e)}"
    
    def schedule_sleep(self, time_str="23:00"):
        """
        Schedule PC to enter sleep mode at specific time (NOT shutdown)
        
        LIMITATIONS:
        - Cannot be cancelled once scheduled
        - Avoid scheduling multiple sleep times
        - For critical scheduling, use OS task scheduler instead
        - Basic timer-based sleep for convenience
        """
        try:
            hours, minutes = map(int, time_str.split(':'))
            now = datetime.now()
            sleep_time = now.replace(hour=hours, minute=minutes, second=0)
            
            if sleep_time < now:
                sleep_time += timedelta(days=1)
            
            seconds_until_sleep = (sleep_time - now).total_seconds()
            
            def execute_sleep():
                """Execute sleep mode after delay"""
                try:
                    time.sleep(seconds_until_sleep)
                    result = self.sleep_mode()
                    self._show_notification(
                        "💤 BOI Sleep Mode",
                        f"Entering sleep mode as scheduled at {time_str}"
                    )
                    print(f"[SCHEDULED SLEEP] {result}")
                except Exception as e:
                    error_msg = f"Scheduled sleep failed: {str(e)}"
                    self._show_notification("❌ Sleep Error", error_msg)
                    print(f"[ERROR] {error_msg}")
            
            threading.Thread(target=execute_sleep, daemon=True).start()
            return f"😴 Sleep mode scheduled for {time_str} ({sleep_time.strftime('%Y-%m-%d %H:%M')})\n⚠️  System will SLEEP (not shutdown) at scheduled time\nℹ️  Cannot be cancelled once set"
        except Exception as e:
            return f"❌ Failed to schedule sleep: {str(e)}"
    
    def cancel_sleep(self):
        """
        Cancel scheduled sleep
        
        Note: This only works for shutdown-based scheduling.
        Timer-based sleep schedules cannot be cancelled once started.
        """
        try:
            if self.os == "Windows":
                subprocess.run("shutdown /a", shell=True, check=False)
                return "✅ Shutdown/restart cancelled (if any were scheduled)\nℹ️  Note: Timer-based sleep schedules cannot be cancelled"
            elif self.os in ["Darwin", "Linux"]:
                subprocess.run("sudo shutdown -c", shell=True, check=False)
                return "✅ Shutdown/restart cancelled (if any were scheduled)\nℹ️  Note: Timer-based sleep schedules cannot be cancelled"
        except Exception as e:
            return f"❌ Failed to cancel: {str(e)}"
    
    def schedule_wake(self, time_str="07:00"):
        """Schedule PC to wake at specific time (Windows only)"""
        try:
            if self.os == "Windows":
                hours, minutes = map(int, time_str.split(':'))
                subprocess.run(f'powershell "powercfg /waketimers /create /type wakeup /time {hours}:{minutes}"', shell=True, check=False)
                return f"✅ Wake scheduled for {time_str}"
            else:
                return "ℹ️ Wake scheduling is only supported on Windows"
        except Exception as e:
            return f"❌ Failed to schedule wake: {str(e)}"
    
    def clear_temp_files(self):
        """Clear temporary files and cache"""
        try:
            cleared_size = 0
            cleared_files = 0
            
            temp_dirs = []
            if self.os == "Windows":
                user_profile = os.environ.get('USERPROFILE')
                temp_dirs = [
                    os.environ.get('TEMP'),
                    os.environ.get('TMP'),
                ]
                if user_profile:
                    temp_dirs.append(os.path.join(user_profile, 'AppData', 'Local', 'Temp'))
            elif self.os in ["Darwin", "Linux"]:
                temp_dirs = ['/tmp', os.path.expanduser('~/.cache')]
            
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        try:
                            if os.path.isfile(item_path):
                                size = os.path.getsize(item_path)
                                os.remove(item_path)
                                cleared_size += size
                                cleared_files += 1
                            elif os.path.isdir(item_path):
                                size = sum(os.path.getsize(os.path.join(dirpath, filename))
                                          for dirpath, _, filenames in os.walk(item_path)
                                          for filename in filenames)
                                shutil.rmtree(item_path)
                                cleared_size += size
                                cleared_files += 1
                        except:
                            continue
            
            cleared_mb = cleared_size / (1024 * 1024)
            return f"✅ Cleared {cleared_files} items ({cleared_mb:.2f} MB)"
        except Exception as e:
            return f"❌ Failed to clear temp files: {str(e)}"
    
    def empty_recycle_bin(self):
        """Empty recycle bin"""
        try:
            if self.os == "Windows":
                try:
                    import winshell
                    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                    return "✅ Recycle bin emptied"
                except (ImportError, Exception):
                    subprocess.run("rd /s /q %temp%", shell=True, check=False)
                    return "✅ Temp cleaned (winshell not available)"
            elif self.os == "Darwin":
                subprocess.run("rm -rf ~/.Trash/*", shell=True, check=False)
                return "✅ Trash emptied"
            elif self.os == "Linux":
                subprocess.run("rm -rf ~/.local/share/Trash/*", shell=True, check=False)
                return "✅ Trash emptied"
        except Exception as e:
            return f"❌ Failed to empty recycle bin: {str(e)}"
    
    def check_disk_space(self):
        """Check disk space and auto-cleanup if needed"""
        try:
            usage = shutil.disk_usage("/")
            percent_used = (usage.used / usage.total) * 100
            
            result = f"💾 Disk Usage: {percent_used:.1f}% ({usage.used//(1024**3)}GB / {usage.total//(1024**3)}GB)\n"
            
            if self.config["auto_cleanup"]["enabled"] and percent_used > self.config["auto_cleanup"]["disk_limit"]:
                result += "\n⚠️ Disk space limit exceeded. Running auto-cleanup...\n"
                cleanup_msg = self.clear_temp_files()
                if cleanup_msg:
                    result += cleanup_msg + "\n"
                bin_msg = self.empty_recycle_bin()
                if bin_msg:
                    result += bin_msg
            
            return result
        except Exception as e:
            return f"❌ Failed to check disk space: {str(e)}"
    
    def auto_cleanup_on_limit(self, limit_percent=90):
        """Configure auto-cleanup when disk hits limit"""
        self.config["auto_cleanup"]["enabled"] = True
        self.config["auto_cleanup"]["disk_limit"] = limit_percent
        self.save_config()
        return f"✅ Auto-cleanup enabled at {limit_percent}% disk usage"
    
    def lock_screen(self):
        """Lock the computer screen"""
        try:
            print("🔒 Attempting to lock screen...")
            
            if self.os == "Windows":
                result = subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True, check=False, capture_output=True, text=True)
                print(f"Lock command executed (Windows): return code {result.returncode}")
                return "🔒 Screen locked successfully"
                
            elif self.os == "Darwin":
                result = subprocess.run(
                    ["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"], 
                    check=False, capture_output=True, text=True
                )
                print(f"Lock command executed (macOS): return code {result.returncode}")
                return "🔒 Screen locked successfully"
                
            elif self.os == "Linux":
                # Try multiple methods in order of preference
                lock_methods = [
                    (["loginctl", "lock-session"], "loginctl"),
                    (["xdg-screensaver", "lock"], "xdg-screensaver"),
                    (["gnome-screensaver-command", "--lock"], "gnome-screensaver"),
                    (["dm-tool", "lock"], "dm-tool"),
                    (["xscreensaver-command", "-lock"], "xscreensaver"),
                ]
                
                for cmd, method_name in lock_methods:
                    try:
                        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=5)
                        print(f"Lock command executed (Linux - {method_name}): return code {result.returncode}")
                        return f"🔒 Screen locked successfully (using {method_name})"
                    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                        continue
                
                # If all methods failed
                print("⚠️ All lock methods failed on Linux")
                return "❌ Failed to lock screen. No compatible screen locker found. Please install xdg-screensaver, gnome-screensaver, or configure loginctl."
            else:
                return f"❌ Unsupported operating system: {self.os}"
                
        except Exception as e:
            print(f"❌ Exception in lock_screen: {str(e)}")
            return f"❌ Failed to lock screen: {str(e)}"
    
    def shutdown_system(self, delay_seconds=10):
        """Shutdown the computer with optional delay"""
        try:
            print(f"⚠️ Attempting to shutdown system (delay: {delay_seconds}s)...")
            
            # Cancel any existing shutdown/restart process
            if self.os in ["Darwin", "Linux"]:
                if self.shutdown_process and self.shutdown_process.poll() is None:
                    self.shutdown_process.terminate()
                    self.shutdown_process = None
                    print("Cancelled previous shutdown process")
            
            if self.os == "Windows":
                # Cancel any existing shutdown first
                subprocess.run("shutdown /a", shell=True, check=False, capture_output=True)
                
                # Schedule new shutdown
                result = subprocess.run(f'shutdown /s /t {delay_seconds}', shell=True, capture_output=True, text=True)
                print(f"Shutdown command executed (Windows): return code {result.returncode}")
                
                if result.returncode != 0:
                    error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                    print(f"Shutdown command failed: {error_msg}")
                    return f"❌ Failed to shutdown: {error_msg}\n💡 Make sure you have administrator privileges."
                
                if delay_seconds > 0:
                    return f"⚠️ Computer will shutdown in {delay_seconds} seconds.\n💡 Run 'cancel shutdown' command to abort."
                else:
                    return "⚠️ Shutting down computer now..."
                    
            elif self.os == "Darwin":
                if delay_seconds > 0:
                    self.shutdown_process = subprocess.Popen(
                        f'sleep {delay_seconds} && sudo shutdown -h now',
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    print(f"Shutdown scheduled (macOS): PID {self.shutdown_process.pid}")
                    return f"⚠️ Computer will shutdown in {delay_seconds} seconds.\n💡 Click 'Cancel Shutdown' or run 'cancel shutdown' to abort."
                else:
                    subprocess.Popen(['sudo', 'shutdown', '-h', 'now'])
                    print("Immediate shutdown initiated (macOS)")
                    return "⚠️ Shutting down computer now..."
                    
            elif self.os == "Linux":
                if delay_seconds > 0:
                    # Use systemctl with delay
                    minutes = max(1, delay_seconds // 60)
                    try:
                        # Try systemctl first
                        result = subprocess.run(
                            f'sudo systemctl poweroff --message="Shutdown scheduled via BOI" --no-wall',
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=2
                        )
                        print(f"Shutdown command executed (Linux systemctl): return code {result.returncode}")
                        return f"⚠️ Computer will shutdown in {delay_seconds} seconds.\n💡 Run 'cancel shutdown' to abort."
                    except:
                        # Fallback to sleep + poweroff
                        self.shutdown_process = subprocess.Popen(
                            f'sleep {delay_seconds} && sudo systemctl poweroff',
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        print(f"Shutdown scheduled (Linux fallback): PID {self.shutdown_process.pid}")
                        return f"⚠️ Computer will shutdown in {delay_seconds} seconds.\n💡 Run 'cancel shutdown' to abort."
                else:
                    subprocess.Popen(['sudo', 'systemctl', 'poweroff'])
                    print("Immediate shutdown initiated (Linux)")
                    return "⚠️ Shutting down computer now..."
            else:
                return f"❌ Unsupported operating system: {self.os}"
                
        except Exception as e:
            print(f"❌ Exception in shutdown_system: {str(e)}")
            return f"❌ Failed to shutdown: {str(e)}"
    
    def restart_system(self, delay_seconds=10):
        """Restart the computer with optional delay"""
        try:
            print(f"🔄 Attempting to restart system (delay: {delay_seconds}s)...")
            
            if self.os in ["Darwin", "Linux"]:
                if self.shutdown_process and self.shutdown_process.poll() is None:
                    self.shutdown_process.terminate()
                    self.shutdown_process = None
            
            if self.os == "Windows":
                # Cancel any existing shutdown first
                subprocess.run("shutdown /a", shell=True, check=False, capture_output=True)
                
                # Schedule restart with proper error handling
                result = subprocess.run(f'shutdown /r /t {delay_seconds}', shell=True, capture_output=True, text=True)
                print(f"Restart command executed (Windows): return code {result.returncode}")
                
                if result.returncode != 0:
                    error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                    print(f"Restart command failed: {error_msg}")
                    return f"❌ Failed to restart: {error_msg}\n💡 Make sure you have administrator privileges."
                
                if delay_seconds > 0:
                    return f"🔄 Computer will restart in {delay_seconds} seconds.\n💡 Run 'cancel shutdown' to abort."
                else:
                    return "🔄 Restarting computer now..."
            elif self.os == "Darwin":
                if delay_seconds > 0:
                    self.shutdown_process = subprocess.Popen(
                        f'sleep {delay_seconds} && sudo shutdown -r now',
                        shell=True
                    )
                    return f"🔄 Computer will restart in {delay_seconds} seconds. Run 'cancel shutdown' to abort."
                else:
                    subprocess.Popen(['sudo', 'shutdown', '-r', 'now'])
                    return "🔄 Restarting computer now..."
            elif self.os == "Linux":
                if delay_seconds > 0:
                    self.shutdown_process = subprocess.Popen(
                        f'sleep {delay_seconds} && sudo systemctl reboot',
                        shell=True
                    )
                    return f"🔄 Computer will restart in {delay_seconds} seconds. Run 'cancel shutdown' to abort."
                else:
                    subprocess.Popen(['sudo', 'systemctl', 'reboot'])
                    return "🔄 Restarting computer now..."
        except Exception as e:
            return f"❌ Failed to restart: {str(e)}"
    
    def cancel_shutdown_restart(self):
        """Cancel scheduled shutdown or restart"""
        try:
            if self.os == "Windows":
                subprocess.run("shutdown /a", shell=True, check=False)
                return "✅ Shutdown/restart cancelled"
            elif self.os in ["Darwin", "Linux"]:
                if self.shutdown_process and self.shutdown_process.poll() is None:
                    self.shutdown_process.terminate()
                    self.shutdown_process = None
                    return "✅ Shutdown/restart cancelled"
                else:
                    subprocess.run("sudo killall sleep", shell=True, check=False)
                    return "✅ Attempted to cancel shutdown/restart"
        except Exception as e:
            return f"❌ Failed to cancel: {str(e)}"
    
    # ==================== BATCH FILE INTEGRATION ====================
    
    def use_batch_volume_control(self, command, value=None):
        """
        Use Windows batch file for volume control (alternative method)
        Args:
            command: 'set', 'up', 'down', 'mute', or 'get'
            value: Volume level or amount (optional for some commands)
        """
        if self.os != "Windows":
            return "ℹ️ Batch file control is only available on Windows"
        
        try:
            batch_file = os.path.join(self.batch_files_dir, "quick_volume_control.bat")
            
            if not os.path.exists(batch_file):
                return f"❌ Batch file not found: {batch_file}\nPlease ensure scripts/windows_controls/ folder exists."
            
            if command == "get":
                result = subprocess.run(
                    [batch_file, command],
                    capture_output=True,
                    text=True,
                    check=False
                )
                return result.stdout.strip() if result.stdout else "ℹ️ Unable to get volume"
            
            elif command in ["set", "up", "down"]:
                if value is None:
                    value = 10 if command in ["up", "down"] else 50
                subprocess.run([batch_file, command, str(value)], check=False)
                return f"🔊 Volume {command} to {value}%" if command == "set" else f"🔊 Volume {command} by {value}%"
            
            elif command == "mute":
                subprocess.run([batch_file, command], check=False)
                return "🔇 Volume toggled"
            
            else:
                return f"❌ Unknown command: {command}"
                
        except Exception as e:
            return f"❌ Batch file error: {str(e)}"
    
    def use_batch_brightness_control(self, level):
        """
        Use Windows batch file for brightness control (alternative method)
        Args:
            level: Brightness level (0-100)
        """
        if self.os != "Windows":
            return "ℹ️ Batch file control is only available on Windows"
        
        try:
            batch_file = os.path.join(self.batch_files_dir, "quick_brightness_control.bat")
            
            if not os.path.exists(batch_file):
                return f"❌ Batch file not found: {batch_file}\nPlease ensure scripts/windows_controls/ folder exists."
            
            level = max(0, min(100, int(level)))
            subprocess.run([batch_file, str(level)], check=False)
            return f"🔆 Brightness set to {level}% (via batch file)"
            
        except Exception as e:
            return f"❌ Batch file error: {str(e)}"
    
    def open_volume_brightness_menu(self):
        """
        Open the interactive Windows volume & brightness control menu
        """
        if self.os != "Windows":
            return "ℹ️ Interactive menu is only available on Windows"
        
        try:
            batch_file = os.path.join(self.batch_files_dir, "windows_volume_brightness_control.bat")
            
            if not os.path.exists(batch_file):
                return f"❌ Batch file not found: {batch_file}\nPlease ensure scripts/windows_controls/ folder exists."
            
            subprocess.Popen([batch_file], shell=True)
            return "🎛️ Opening Windows Volume & Brightness Control Menu..."
            
        except Exception as e:
            return f"❌ Failed to open menu: {str(e)}"
    
    # ==================== SYSTEM INFORMATION ====================
    
    def get_cpu_usage(self):
        """Get current CPU usage percentage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            return f"💻 CPU Usage: {cpu_percent}%\n📊 CPU Cores: {cpu_count}"
        except Exception as e:
            return f"❌ Failed to get CPU usage: {str(e)}"
    
    def get_ram_usage(self):
        """Get current RAM usage"""
        try:
            ram = psutil.virtual_memory()
            total_gb = ram.total / (1024**3)
            used_gb = ram.used / (1024**3)
            available_gb = ram.available / (1024**3)
            percent = ram.percent
            
            return f"🧠 RAM Usage: {percent}%\n📊 Used: {used_gb:.2f} GB / {total_gb:.2f} GB\n✅ Available: {available_gb:.2f} GB"
        except Exception as e:
            return f"❌ Failed to get RAM usage: {str(e)}"
    
    def get_battery_status(self):
        """Get battery status and percentage"""
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return "🔌 No battery detected (Desktop PC or battery info unavailable)"
            
            percent = battery.percent
            plugged = battery.power_plugged
            time_left = battery.secsleft
            
            status = "🔌 Charging" if plugged else "🔋 On Battery"
            
            if time_left == -1:
                time_str = "Calculating..."
            elif time_left == -2:
                time_str = "Unlimited (Plugged in)"
            else:
                hours = time_left // 3600
                minutes = (time_left % 3600) // 60
                time_str = f"{hours}h {minutes}m remaining"
            
            return f"{status}\n🔋 Battery: {percent}%\n⏱️ {time_str}"
        except Exception as e:
            return f"❌ Failed to get battery status: {str(e)}"
    
    def get_system_uptime(self):
        """Get system uptime"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            days = uptime.days
            hours = uptime.seconds // 3600
            minutes = (uptime.seconds % 3600) // 60
            
            return f"⏱️ System Uptime: {days} days, {hours} hours, {minutes} minutes\n🔄 Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}"
        except Exception as e:
            return f"❌ Failed to get uptime: {str(e)}"
    
    def get_network_status(self):
        """Get network connection status and IP address"""
        try:
            import socket
            
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            net_info = psutil.net_if_stats()
            active_connections = []
            
            for interface, stats in net_info.items():
                if stats.isup:
                    active_connections.append(interface)
            
            return f"🌐 Hostname: {hostname}\n📡 Local IP: {local_ip}\n✅ Active Interfaces: {', '.join(active_connections[:3])}"
        except Exception as e:
            return f"❌ Failed to get network status: {str(e)}"
    
    def get_disk_usage(self):
        """Get disk usage for all drives"""
        try:
            partitions = psutil.disk_partitions()
            result = "💾 Disk Usage:\n"
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    total_gb = usage.total / (1024**3)
                    used_gb = usage.used / (1024**3)
                    free_gb = usage.free / (1024**3)
                    percent = usage.percent
                    
                    result += f"\n📁 {partition.device} ({partition.mountpoint})\n"
                    result += f"   Used: {used_gb:.1f} GB / {total_gb:.1f} GB ({percent}%)\n"
                    result += f"   Free: {free_gb:.1f} GB\n"
                except:
                    continue
            
            return result
        except Exception as e:
            return f"❌ Failed to get disk usage: {str(e)}"
    
    def get_system_info(self):
        """Get comprehensive system information"""
        try:
            system = platform.system()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()
            
            info = f"🖥️ System Information\n"
            info += f"━━━━━━━━━━━━━━━━━━━━━━\n"
            info += f"OS: {system} {release}\n"
            info += f"Version: {version}\n"
            info += f"Architecture: {machine}\n"
            info += f"Processor: {processor}\n"
            info += f"\n{self.get_cpu_usage()}\n"
            info += f"\n{self.get_ram_usage()}\n"
            
            return info
        except Exception as e:
            return f"❌ Failed to get system info: {str(e)}"
    
    # ==================== CLIPBOARD MANAGEMENT ====================
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            import pyperclip
            pyperclip.copy(text)
            return f"✅ Copied to clipboard: {text[:50]}..." if len(text) > 50 else f"✅ Copied to clipboard: {text}"
        except Exception as e:
            return f"❌ Failed to copy to clipboard: {str(e)}"
    
    def get_clipboard(self):
        """Get current clipboard content"""
        try:
            import pyperclip
            content = pyperclip.paste()
            if not content:
                return "📋 Clipboard is empty"
            return f"📋 Clipboard content:\n{content}"
        except Exception as e:
            return f"❌ Failed to get clipboard: {str(e)}"
    
    def clear_clipboard(self):
        """Clear clipboard content"""
        try:
            import pyperclip
            pyperclip.copy('')
            return "✅ Clipboard cleared"
        except Exception as e:
            return f"❌ Failed to clear clipboard: {str(e)}"
    
    # ==================== POWER MANAGEMENT ====================
    
    def sleep_mode(self):
        """Put system to sleep"""
        try:
            if self.os == "Windows":
                subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True, check=False)
                return "😴 Putting system to sleep..."
            elif self.os == "Darwin":
                subprocess.run(["pmset", "sleepnow"], check=False)
                return "😴 Putting system to sleep..."
            elif self.os == "Linux":
                subprocess.run(["systemctl", "suspend"], check=False)
                return "😴 Putting system to sleep..."
        except Exception as e:
            return f"❌ Failed to sleep: {str(e)}"
    
    def hibernate(self):
        """Hibernate the system"""
        try:
            if self.os == "Windows":
                subprocess.run("shutdown /h", shell=True, check=False)
                return "💤 Hibernating system..."
            elif self.os == "Darwin":
                subprocess.run(["pmset", "hibernatemode", "25"], check=False)
                subprocess.run(["pmset", "sleepnow"], check=False)
                return "💤 Hibernating system..."
            elif self.os == "Linux":
                subprocess.run(["systemctl", "hibernate"], check=False)
                return "💤 Hibernating system..."
        except Exception as e:
            return f"❌ Failed to hibernate: {str(e)}"
    
    # ==================== WINDOW MANAGEMENT ====================
    
    def minimize_all_windows(self):
        """Minimize all windows (show desktop)"""
        try:
            if self.os == "Windows":
                import pyautogui
                pyautogui.hotkey('win', 'd')
                return "🪟 All windows minimized (Desktop shown)"
            elif self.os == "Darwin":
                subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 103 using {command down}'], check=False)
                return "🪟 All windows minimized"
            elif self.os == "Linux":
                subprocess.run(["wmctrl", "-k", "on"], check=False)
                return "🪟 All windows minimized"
        except Exception as e:
            return f"❌ Failed to minimize windows: {str(e)}"
    
    def show_desktop(self):
        """Show desktop"""
        return self.minimize_all_windows()
    
    def close_all_windows(self):
        """Close all open windows and tabs (browsers, applications)"""
        try:
            if self.os == "Windows":
                # Use batch file for comprehensive window closing
                batch_file = os.path.join(self.batch_files_dir, "close_all_windows.bat")
                
                if os.path.exists(batch_file):
                    print("Using batch file to close all windows...")
                    result = subprocess.run(
                        [batch_file],
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        return "✅ All windows and tabs closed successfully"
                    else:
                        print(f"Batch file warning: {result.stderr}")
                
                # Fallback method using PowerShell
                print("Using PowerShell fallback to close windows...")
                
                # Close browsers first
                browsers = ['chrome', 'firefox', 'msedge', 'opera', 'brave']
                for browser in browsers:
                    subprocess.run(f'taskkill /F /IM {browser}.exe', shell=True, check=False, capture_output=True)
                
                # Close other common applications
                apps = ['notepad', 'Code', 'Discord', 'Spotify', 'Telegram', 'WhatsApp']
                for app in apps:
                    subprocess.run(f'taskkill /F /IM {app}.exe', shell=True, check=False, capture_output=True)
                
                # Close remaining windows gracefully using PowerShell
                powershell_cmd = """Get-Process | Where-Object {$_.MainWindowTitle -ne ''} | Where-Object {$_.ProcessName -notin @('explorer','taskmgr','SystemSettings','cmd','powershell','python','pythonw')} | Stop-Process -Force -ErrorAction SilentlyContinue"""
                subprocess.run(['powershell', '-Command', powershell_cmd], check=False, capture_output=True)
                
                return "✅ All windows and tabs closed successfully"
                
            elif self.os == "Darwin":
                # macOS: Close all applications except Finder and System apps
                script = '''
                tell application "System Events"
                    set allApps to name of every process whose background only is false
                    repeat with appName in allApps
                        if appName is not in {"Finder", "System Preferences", "Terminal"} then
                            try
                                tell application appName to quit
                            end try
                        end if
                    end repeat
                end tell
                '''
                subprocess.run(['osascript', '-e', script], check=False)
                return "✅ All applications closed (macOS)"
                
            elif self.os == "Linux":
                # Linux: Close all non-system windows
                try:
                    # Close browsers
                    subprocess.run("killall chrome firefox opera brave", shell=True, check=False)
                    
                    # Close other windows using wmctrl if available
                    subprocess.run("wmctrl -l | awk '{print $1}' | xargs -I {} wmctrl -ic {}", shell=True, check=False)
                    return "✅ All windows closed (Linux)"
                except:
                    return "⚠️ Partial close - some windows may remain open"
            
        except Exception as e:
            return f"❌ Failed to close all windows: {str(e)}"
    
    def close_all_tabs(self):
        """Quick close all browser tabs (alias for close_all_windows)"""
        return self.close_all_windows()
    
    def list_open_windows(self):
        """List all open windows"""
        try:
            if self.os == "Windows":
                import win32gui
                windows = []
                
                def callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            windows.append(title)
                
                win32gui.EnumWindows(callback, windows)
                
                if windows:
                    return "🪟 Open Windows:\n" + "\n".join([f"  • {w}" for w in windows[:15]])
                else:
                    return "ℹ️ No visible windows found"
            else:
                return "ℹ️ Window listing only available on Windows"
        except Exception as e:
            return f"❌ Failed to list windows: {str(e)}"
    
    # ==================== PROCESS MANAGEMENT ====================
    
    def list_running_processes(self, limit=10):
        """List top running processes by CPU usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except:
                    pass
            
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            result = f"⚙️ Top {limit} Processes (by CPU usage):\n"
            for i, proc in enumerate(processes[:limit], 1):
                result += f"{i}. {proc['name']} (PID: {proc['pid']})\n"
                result += f"   CPU: {proc['cpu_percent']}% | RAM: {proc['memory_percent']:.1f}%\n"
            
            return result
        except Exception as e:
            return f"❌ Failed to list processes: {str(e)}"
    
    def kill_process(self, process_name):
        """
        Kill a process by name
        
        WARNING: This forcefully terminates processes. Be careful with system processes!
        Killing critical system processes can cause system instability.
        
        Safe to kill: chrome, firefox, notepad, calculator, etc.
        DO NOT kill: explorer, System, csrss, winlogon, services, etc.
        """
        try:
            critical_processes = [
                'system', 'csrss', 'winlogon', 'services', 'lsass', 'smss',
                'explorer', 'svchost', 'dwm', 'systemd', 'init', 'kernel'
            ]
            
            if process_name.lower() in critical_processes:
                return f"🚫 Cannot kill '{process_name}' - This is a critical system process!\nKilling it may crash your system."
            
            killed = []
            for proc in psutil.process_iter(['pid', 'name']):
                if process_name.lower() in proc.info['name'].lower():
                    try:
                        proc.terminate()  # Try graceful termination first
                        proc.wait(timeout=3)
                        killed.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
                    except psutil.TimeoutExpired:
                        proc.kill()  # Force kill if graceful fails
                        killed.append(f"{proc.info['name']} (PID: {proc.info['pid']}) - Force killed")
                    except psutil.AccessDenied:
                        return f"🚫 Access denied: '{proc.info['name']}' requires administrator privileges"
            
            if killed:
                return f"✅ Terminated processes:\n" + "\n".join([f"  • {p}" for p in killed])
            else:
                return f"⚠️ No process found matching '{process_name}'"
        except Exception as e:
            return f"❌ Failed to terminate process: {str(e)}"
    
    # ==================== QUICK APP LAUNCHERS ====================
    
    def open_calculator(self):
        """Open calculator application"""
        try:
            if self.os == "Windows":
                subprocess.Popen("calc.exe")
                return "🧮 Opening Calculator..."
            elif self.os == "Darwin":
                subprocess.Popen(["open", "-a", "Calculator"])
                return "🧮 Opening Calculator..."
            elif self.os == "Linux":
                subprocess.Popen(["gnome-calculator"])
                return "🧮 Opening Calculator..."
        except Exception as e:
            return f"❌ Failed to open calculator: {str(e)}"
    
    def open_notepad(self):
        """Open notepad/text editor"""
        try:
            if self.os == "Windows":
                subprocess.Popen("notepad.exe")
                return "📝 Opening Notepad..."
            elif self.os == "Darwin":
                subprocess.Popen(["open", "-a", "TextEdit"])
                return "📝 Opening TextEdit..."
            elif self.os == "Linux":
                subprocess.Popen(["gedit"])
                return "📝 Opening Text Editor..."
        except Exception as e:
            return f"❌ Failed to open notepad: {str(e)}"
    
    def open_task_manager(self):
        """Open task manager"""
        try:
            if self.os == "Windows":
                subprocess.Popen("taskmgr.exe")
                return "📊 Opening Task Manager..."
            elif self.os == "Darwin":
                subprocess.Popen(["open", "-a", "Activity Monitor"])
                return "📊 Opening Activity Monitor..."
            elif self.os == "Linux":
                subprocess.Popen(["gnome-system-monitor"])
                return "📊 Opening System Monitor..."
        except Exception as e:
            return f"❌ Failed to open task manager: {str(e)}"
    
    def open_file_explorer(self, path=None):
        """Open file explorer at specified path"""
        try:
            if self.os == "Windows":
                if path:
                    subprocess.Popen('explorer "' + path + '"')
                else:
                    subprocess.Popen("explorer")
                return f"📂 Opening File Explorer{' at ' + path if path else ''}..."
            elif self.os == "Darwin":
                if path:
                    subprocess.Popen(["open", path])
                else:
                    subprocess.Popen(["open", "."])
                return f"📂 Opening Finder{' at ' + path if path else ''}..."
            elif self.os == "Linux":
                if path:
                    subprocess.Popen(["xdg-open", path])
                else:
                    subprocess.Popen(["xdg-open", "."])
                return f"📂 Opening File Manager{' at ' + path if path else ''}..."
        except Exception as e:
            return f"❌ Failed to open file explorer: {str(e)}"
    
    def open_command_prompt(self):
        """Open command prompt/terminal"""
        try:
            if self.os == "Windows":
                subprocess.Popen("cmd.exe")
                return "💻 Opening Command Prompt..."
            elif self.os == "Darwin":
                subprocess.Popen(["open", "-a", "Terminal"])
                return "💻 Opening Terminal..."
            elif self.os == "Linux":
                subprocess.Popen(["gnome-terminal"])
                return "💻 Opening Terminal..."
        except Exception as e:
            return f"❌ Failed to open command prompt: {str(e)}"
    
    # ==================== TIMER AND ALARM ====================
    
    def set_timer(self, seconds, message="Timer finished!"):
        """Set a countdown timer"""
        try:
            def timer_thread():
                time.sleep(seconds)
                self._show_notification("⏰ Timer Alert", message)
            
            threading.Thread(target=timer_thread, daemon=True).start()
            
            minutes = seconds // 60
            secs = seconds % 60
            return f"⏱️ Timer set for {minutes}m {secs}s"
        except Exception as e:
            return f"❌ Failed to set timer: {str(e)}"
    
    def set_alarm(self, time_str, message="Alarm!"):
        """Set an alarm for specific time (format: HH:MM)"""
        try:
            target_time = datetime.strptime(time_str, "%H:%M").time()
            now = datetime.now()
            target_datetime = datetime.combine(now.date(), target_time)
            
            if target_datetime < now:
                target_datetime += timedelta(days=1)
            
            wait_seconds = (target_datetime - now).total_seconds()
            
            def alarm_thread():
                time.sleep(wait_seconds)
                self._show_notification("⏰ Alarm Alert", message)
            
            threading.Thread(target=alarm_thread, daemon=True).start()
            
            return f"⏰ Alarm set for {time_str} ({target_datetime.strftime('%Y-%m-%d %H:%M')})"
        except Exception as e:
            return f"❌ Failed to set alarm: {str(e)}"
    
    def _show_notification(self, title, message):
        """Show system notification with multiple fallback methods"""
        notification_sent = False
        
        try:
            if self.os == "Windows":
                try:
                    from plyer import notification as plyer_notify
                    plyer_notify.notify(
                        title=title,
                        message=message,
                        app_name="BOI",
                        timeout=10
                    )
                    notification_sent = True
                except:
                    try:
                        import win32api
                        import win32con
                        win32api.MessageBox(0, message, title, win32con.MB_ICONINFORMATION)
                        notification_sent = True
                    except:
                        pass
                        
            elif self.os == "Darwin":
                try:
                    subprocess.run([
                        "osascript", "-e",
                        f'display notification "{message}" with title "{title}"'
                    ], check=True)
                    notification_sent = True
                except:
                    pass
                    
            elif self.os == "Linux":
                try:
                    subprocess.run(["notify-send", title, message], check=True)
                    notification_sent = True
                except:
                    pass
        except Exception as e:
            pass
        
        if not notification_sent:
            print(f"\n{'='*60}")
            print(f"🔔 {title}")
            print(f"{'='*60}")
            print(f"   {message}")
            print(f"{'='*60}\n")
            
            try:
                import logging
                logging.warning(f"BOI ALERT - {title}: {message}")
            except:
                pass

if __name__ == "__main__":
    controller = SystemController()
    print("System Control Module - Testing")
    print(controller.check_disk_space())
    print(controller.get_volume_info())
    print(controller.get_brightness())
