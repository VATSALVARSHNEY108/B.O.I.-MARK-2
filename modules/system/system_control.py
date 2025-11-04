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
                subprocess.run(["nircmd.exe", "mutesysvolume", "1", "microphone"], check=False)
                return "✅ Microphone muted"
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
                subprocess.run(["nircmd.exe", "mutesysvolume", "0", "microphone"], check=False)
                return "✅ Microphone unmuted"
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
                # Try pycaw library first (best method)
                try:
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    from comtypes import CLSCTX_ALL
                    from ctypes import cast, POINTER
                    
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMasterVolumeLevelScalar(level / 100, None)
                    return f"🔊 Volume set to {level}%"
                except ImportError:
                    # pycaw not installed, try nircmd
                    result = subprocess.run(
                        f"nircmd.exe setsysvolume {int(level * 655.35)}", 
                        shell=True, 
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    if result.returncode == 0:
                        return f"🔊 Volume set to {level}%"
                    else:
                        return f"⚠️ Volume control unavailable. Please install 'pycaw' (pip install pycaw) or download nircmd.exe"
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
                # If can't get current, just increase
                if self.os == "Windows":
                    subprocess.run(f"nircmd.exe changesysvolume {int(amount * 655.35)}", shell=True, check=False)
                    return f"🔊 Volume increased by {amount}%"
                elif self.os == "Darwin":
                    subprocess.run(f"osascript -e 'set volume output volume (output volume of (get volume settings) + {amount})'", shell=True, check=False)
                    return f"🔊 Volume increased by {amount}%"
                elif self.os == "Linux":
                    subprocess.run(f"pactl set-sink-volume @DEFAULT_SINK@ +{amount}%", shell=True, check=False)
                    return f"🔊 Volume increased by {amount}%"
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
                # If can't get current, just decrease
                if self.os == "Windows":
                    subprocess.run(f"nircmd.exe changesysvolume -{int(amount * 655.35)}", shell=True, check=False)
                    return f"🔉 Volume decreased by {amount}%"
                elif self.os == "Darwin":
                    subprocess.run(f"osascript -e 'set volume output volume (output volume of (get volume settings) - {amount})'", shell=True, check=False)
                    return f"🔉 Volume decreased by {amount}%"
                elif self.os == "Linux":
                    subprocess.run(f"pactl set-sink-volume @DEFAULT_SINK@ -{amount}%", shell=True, check=False)
                    return f"🔉 Volume decreased by {amount}%"
        except Exception as e:
            return f"❌ Failed to decrease volume: {str(e)}"
    
    def get_volume(self):
        """Get current volume level (0-100)"""
        try:
            if self.os == "Windows":
                result = subprocess.run(
                    "nircmd.exe getsysvolume",
                    shell=True, capture_output=True, text=True, check=False
                )
                if result.returncode == 0 and result.stdout.strip():
                    return int(int(result.stdout.strip()) / 655.35)
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
                subprocess.run("nircmd.exe mutesysvolume 1", shell=True, check=False)
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
                subprocess.run("nircmd.exe mutesysvolume 0", shell=True, check=False)
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
                subprocess.run("nircmd.exe mutesysvolume 2", shell=True, check=False)
                return "🔊 Volume toggled"
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
        """Schedule PC to sleep at specific time"""
        try:
            hours, minutes = map(int, time_str.split(':'))
            now = datetime.now()
            sleep_time = now.replace(hour=hours, minute=minutes, second=0)
            
            if sleep_time < now:
                sleep_time += timedelta(days=1)
            
            seconds_until_sleep = (sleep_time - now).total_seconds()
            
            if self.os == "Windows":
                subprocess.Popen(f'shutdown /s /t {int(seconds_until_sleep)}', shell=True)
                return f"✅ Sleep scheduled for {time_str}"
            elif self.os == "Darwin":
                subprocess.Popen(f'sudo shutdown -s +{int(seconds_until_sleep/60)}', shell=True)
                return f"✅ Sleep scheduled for {time_str}"
            elif self.os == "Linux":
                subprocess.Popen(f'sudo shutdown -h +{int(seconds_until_sleep/60)}', shell=True)
                return f"✅ Sleep scheduled for {time_str}"
        except Exception as e:
            return f"❌ Failed to schedule sleep: {str(e)}"
    
    def cancel_sleep(self):
        """Cancel scheduled sleep"""
        try:
            if self.os == "Windows":
                subprocess.run("shutdown /a", shell=True, check=False)
                return "✅ Sleep cancelled"
            elif self.os in ["Darwin", "Linux"]:
                subprocess.run("sudo shutdown -c", shell=True, check=False)
                return "✅ Sleep cancelled"
        except Exception as e:
            return f"❌ Failed to cancel sleep: {str(e)}"
    
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
                            f'sudo systemctl poweroff --message="Shutdown scheduled via VATSAL" --no-wall',
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
            if self.os in ["Darwin", "Linux"]:
                if self.shutdown_process and self.shutdown_process.poll() is None:
                    self.shutdown_process.terminate()
                    self.shutdown_process = None
            
            if self.os == "Windows":
                subprocess.run("shutdown /a", shell=True, check=False)
                subprocess.Popen(f'shutdown /r /t {delay_seconds}', shell=True)
                if delay_seconds > 0:
                    return f"🔄 Computer will restart in {delay_seconds} seconds. Run 'cancel shutdown' to abort."
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

if __name__ == "__main__":
    controller = SystemController()
    print("System Control Module - Testing")
    print(controller.check_disk_space())
