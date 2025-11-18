"""
Batch Utilities Module
Python implementations of all batch file functionalities
Integrates system control, file management, network tools, and maintenance utilities
"""

import os
import sys
import platform
import subprocess
import psutil
import shutil
from datetime import datetime
from pathlib import Path
import socket
import time


class BatchUtilities:
    """Comprehensive batch utilities class"""

    def __init__(self):
        self.home = Path.home()
        self.downloads = self.home / "Downloads"
        self.desktop = self.home / "Desktop"
        self.pictures = self.home / "Pictures"
        self.is_windows = platform.system() == "Windows"

    # ==================== SYSTEM CONTROL ====================

    def get_system_info(self):
        """Get comprehensive system information"""
        try:
            info = {
                "Computer Name": platform.node(),
                "Username": os.getenv("USERNAME") or os.getenv("USER"),
                "OS": f"{platform.system()} {platform.release()}",
                "Version": platform.version(),
                "Architecture": platform.machine(),
                "Processor": platform.processor(),
                "Python Version": sys.version,
            }

            # Memory info
            mem = psutil.virtual_memory()
            info["Total Memory"] = f"{mem.total / (1024**3):.2f} GB"
            info["Available Memory"] = f"{mem.available / (1024**3):.2f} GB"
            info["Memory Usage"] = f"{mem.percent}%"

            # Disk info
            disk = psutil.disk_usage("/")
            info["Disk Total"] = f"{disk.total / (1024**3):.2f} GB"
            info["Disk Used"] = f"{disk.used / (1024**3):.2f} GB"
            info["Disk Free"] = f"{disk.free / (1024**3):.2f} GB"
            info["Disk Usage"] = f"{disk.percent}%"

            # CPU info
            info["CPU Cores"] = psutil.cpu_count(logical=False)
            info["CPU Threads"] = psutil.cpu_count(logical=True)
            info["CPU Usage"] = f"{psutil.cpu_percent(interval=1)}%"

            # Network info
            try:
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                info["IP Address"] = ip_address
            except:
                info["IP Address"] = "Unable to determine"

            return {"success": True, "info": info}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_battery_info(self):
        """Get battery status and information"""
        try:
            if not hasattr(psutil, "sensors_battery"):
                return {"success": False, "error": "Battery info not available on this system"}

            battery = psutil.sensors_battery()
            if battery is None:
                return {"success": False, "error": "No battery detected"}

            info = {
                "Battery Percent": f"{battery.percent}%",
                "Power Plugged": "Yes" if battery.power_plugged else "No",
                "Time Remaining": str(battery.secsleft // 60) + " minutes" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Charging/Unknown"
            }

            return {"success": True, "info": info}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def volume_control(self, action, value=None):
        """Control system volume"""
        try:
            # macOS volume control
            if sys.platform == "darwin":
                try:
                    if action == "up":
                        subprocess.run(["osascript", "-e", "set volume output volume ((output volume of (get volume settings)) + 10)"], check=True)
                        return {"success": True, "message": "Volume increased"}
                    elif action == "down":
                        subprocess.run(["osascript", "-e", "set volume output volume ((output volume of (get volume settings)) - 10)"], check=True)
                        return {"success": True, "message": "Volume decreased"}
                    elif action == "mute":
                        subprocess.run(["osascript", "-e", "set volume output muted (not (output muted of (get volume settings)))"], check=True)
                        return {"success": True, "message": "Volume muted/unmuted"}
                    elif action == "set" and value is not None:
                        subprocess.run(["osascript", "-e", f"set volume output volume {value}"], check=True)
                        return {"success": True, "message": f"Volume set to {value}%"}
                    return {"success": False, "error": "Invalid volume action"}
                except subprocess.CalledProcessError as e:
                    return {"success": False, "error": f"Volume control failed: {str(e)}"}
            
            # Linux volume control
            elif sys.platform.startswith("linux"):
                try:
                    if action == "up":
                        subprocess.run(["amixer", "set", "Master", "5%+"], check=True)
                        return {"success": True, "message": "Volume increased"}
                    elif action == "down":
                        subprocess.run(["amixer", "set", "Master", "5%-"], check=True)
                        return {"success": True, "message": "Volume decreased"}
                    elif action == "mute":
                        subprocess.run(["amixer", "set", "Master", "toggle"], check=True)
                        return {"success": True, "message": "Volume muted/unmuted"}
                    elif action == "set" and value is not None:
                        subprocess.run(["amixer", "set", "Master", f"{value}%"], check=True)
                        return {"success": True, "message": f"Volume set to {value}%"}
                    return {"success": False, "error": "Invalid volume action"}
                except subprocess.CalledProcessError as e:
                    return {"success": False, "error": f"Volume control failed: {str(e)}"}
                except FileNotFoundError:
                    return {"success": False, "error": "amixer not found. Please install alsa-utils"}
            
            # Windows volume control
            elif self.is_windows:
                try:
                    # Try using pycaw library for proper Windows volume control
                    from ctypes import cast, POINTER
                    from comtypes import CLSCTX_ALL
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    
                    if action == "mute":
                        current_mute = volume.GetMute()
                        volume.SetMute(not current_mute, None)
                        return {"success": True, "message": "Volume muted" if not current_mute else "Volume unmuted"}
                    elif action == "up":
                        current_vol = volume.GetMasterVolumeLevelScalar()
                        new_vol = min(1.0, current_vol + 0.1)
                        volume.SetMasterVolumeLevelScalar(new_vol, None)
                        return {"success": True, "message": f"Volume increased to {int(new_vol*100)}%"}
                    elif action == "down":
                        current_vol = volume.GetMasterVolumeLevelScalar()
                        new_vol = max(0.0, current_vol - 0.1)
                        volume.SetMasterVolumeLevelScalar(new_vol, None)
                        return {"success": True, "message": f"Volume decreased to {int(new_vol*100)}%"}
                    elif action == "set" and value is not None:
                        volume.SetMasterVolumeLevelScalar(value / 100, None)
                        return {"success": True, "message": f"Volume set to {value}%"}
                    else:
                        return {"success": False, "error": "Invalid volume action"}
                        
                except ImportError:
                    return {"success": False, "error": "Volume control requires pycaw library. Install with: pip install pycaw comtypes"}
                except Exception as e:
                    return {"success": False, "error": f"Volume control failed: {str(e)}"}
            else:
                return {"success": False, "error": "Volume control not supported on this platform"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def power_options(self, option):
        """Control power options"""
        try:
            if not self.is_windows:
                # Unix-like systems
                try:
                    if option == "shutdown":
                        result = subprocess.run(["shutdown", "-h", "now"], capture_output=True)
                        if result.returncode != 0:
                            return {"success": False, "error": f"Shutdown failed: {result.stderr.decode()}"}
                    elif option == "restart":
                        result = subprocess.run(["shutdown", "-r", "now"], capture_output=True)
                        if result.returncode != 0:
                            return {"success": False, "error": f"Restart failed: {result.stderr.decode()}"}
                    elif option == "sleep":
                        if sys.platform == "darwin":  # macOS
                            result = subprocess.run(["pmset", "sleepnow"], capture_output=True)
                        else:  # Linux
                            result = subprocess.run(["systemctl", "suspend"], capture_output=True)
                        if result.returncode != 0:
                            return {"success": False, "error": f"Sleep failed: {result.stderr.decode()}"}
                    elif option == "lock":
                        if sys.platform == "darwin":
                            result = subprocess.run(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"], capture_output=True)
                        else:
                            result = subprocess.run(["loginctl", "lock-session"], capture_output=True)
                        if result.returncode != 0:
                            return {"success": False, "error": f"Lock failed: {result.stderr.decode()}"}
                    else:
                        return {"success": False, "error": "Invalid power option for this platform"}
                    return {"success": True, "message": f"Power option '{option}' executed successfully"}
                except FileNotFoundError:
                    return {"success": False, "error": "Power control command not found on this system"}
                except subprocess.CalledProcessError as e:
                    return {"success": False, "error": f"Power command failed: {str(e)}"}
            else:
                # Windows
                try:
                    if option == "shutdown":
                        result = subprocess.run(["shutdown", "/s", "/t", "5"], capture_output=True)
                        if result.returncode != 0:
                            return {"success": False, "error": "Shutdown command failed"}
                        return {"success": True, "message": "Shutting down in 5 seconds..."}
                    elif option == "restart":
                        result = subprocess.run(["shutdown", "/r", "/t", "5"], capture_output=True)
                        if result.returncode != 0:
                            return {"success": False, "error": "Restart command failed"}
                        return {"success": True, "message": "Restarting in 5 seconds..."}
                    elif option == "sleep":
                        result = subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], capture_output=True)
                        if result.returncode != 0:
                            return {"success": False, "error": "Sleep command failed"}
                        return {"success": True, "message": "Entering sleep mode..."}
                    elif option == "hibernate":
                        result = subprocess.run(["shutdown", "/h"], capture_output=True)
                        if result.returncode != 0:
                            return {"success": False, "error": "Hibernate command failed"}
                        return {"success": True, "message": "Hibernating..."}
                    elif option == "lock":
                        result = subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], capture_output=True)
                        if result.returncode != 0:
                            return {"success": False, "error": "Lock command failed"}
                        return {"success": True, "message": "Locking computer..."}
                    elif option == "logoff":
                        result = subprocess.run(["shutdown", "/l"], capture_output=True)
                        if result.returncode != 0:
                            return {"success": False, "error": "Logoff command failed"}
                        return {"success": True, "message": "Logging off..."}
                    else:
                        return {"success": False, "error": "Invalid power option"}
                except Exception as e:
                    return {"success": False, "error": f"Power command failed: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def take_screenshot(self, delay=0, filename=None):
        """Take a screenshot"""
        try:
            import pyautogui

            if delay > 0:
                time.sleep(delay)

            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = self.pictures / f"Screenshot_{timestamp}.png"
            else:
                filename = Path(filename)

            # Ensure directory exists
            filename.parent.mkdir(parents=True, exist_ok=True)

            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filename))

            return {"success": True, "message": f"Screenshot saved to {filename}", "path": str(filename)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_process_list(self):
        """Get list of running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        "PID": proc.info['pid'],
                        "Name": proc.info['name'],
                        "CPU": f"{proc.info['cpu_percent']:.1f}%",
                        "Memory": f"{proc.info['memory_percent']:.1f}%"
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Sort by CPU usage
            processes.sort(key=lambda x: float(x["CPU"].rstrip('%')), reverse=True)
            return {"success": True, "processes": processes[:50]}  # Top 50
        except Exception as e:
            return {"success": False, "error": str(e)}

    def kill_process(self, pid_or_name):
        """Kill a process by PID or name"""
        try:
            killed = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if str(proc.info['pid']) == str(pid_or_name) or proc.info['name'].lower() == pid_or_name.lower():
                        proc.kill()
                        killed.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            if killed:
                return {"success": True, "message": f"Killed: {', '.join(killed)}"}
            else:
                return {"success": False, "error": "Process not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ==================== FILE MANAGEMENT ====================

    def organize_downloads(self):
        """Organize downloads folder by file type"""
        try:
            if not self.downloads.exists():
                return {"success": False, "error": "Downloads folder not found"}

            # Create category folders
            categories = {
                "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".odt", ".rtf"],
                "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp"],
                "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
                "Music": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"],
                "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
                "Programs": [".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"],
                "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h"],
                "Others": []
            }

            moved_files = []

            for category, extensions in categories.items():
                category_path = self.downloads / category
                category_path.mkdir(exist_ok=True)

            # Move files
            for file_path in self.downloads.iterdir():
                if file_path.is_file():
                    ext = file_path.suffix.lower()
                    moved = False

                    for category, extensions in categories.items():
                        if ext in extensions:
                            dest = self.downloads / category / file_path.name
                            try:
                                shutil.move(str(file_path), str(dest))
                                moved_files.append(f"{file_path.name} → {category}")
                                moved = True
                                break
                            except Exception as e:
                                print(f"Error moving {file_path.name}: {e}")

                    if not moved and ext:  # Unknown extension
                        dest = self.downloads / "Others" / file_path.name
                        try:
                            shutil.move(str(file_path), str(dest))
                            moved_files.append(f"{file_path.name} → Others")
                        except Exception as e:
                            print(f"Error moving {file_path.name}: {e}")

            return {
                "success": True,
                "message": f"Organized {len(moved_files)} files",
                "files": moved_files
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def search_files(self, pattern, directory=None, max_results=100):
        """Search for files by pattern"""
        try:
            if directory is None:
                directory = self.home

            directory = Path(directory)
            if not directory.exists():
                return {"success": False, "error": "Directory not found"}

            results = []
            for file_path in directory.rglob(f"*{pattern}*"):
                if len(results) >= max_results:
                    break
                try:
                    results.append({
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size if file_path.is_file() else 0,
                        "type": "File" if file_path.is_file() else "Directory"
                    })
                except:
                    pass

            return {
                "success": True,
                "count": len(results),
                "results": results
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def find_duplicates(self, directory=None):
        """Find duplicate files in a directory"""
        try:
            import hashlib

            if directory is None:
                directory = self.downloads

            directory = Path(directory)
            if not directory.exists():
                return {"success": False, "error": "Directory not found"}

            hashes = {}
            duplicates = []

            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    try:
                        # Calculate file hash
                        hasher = hashlib.md5()
                        with open(file_path, 'rb') as f:
                            buf = f.read(65536)
                            while len(buf) > 0:
                                hasher.update(buf)
                                buf = f.read(65536)

                        file_hash = hasher.hexdigest()

                        if file_hash in hashes:
                            duplicates.append({
                                "original": hashes[file_hash],
                                "duplicate": str(file_path),
                                "size": file_path.stat().st_size
                            })
                        else:
                            hashes[file_hash] = str(file_path)
                    except:
                        pass

            return {
                "success": True,
                "count": len(duplicates),
                "duplicates": duplicates
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_backup(self, source, destination=None):
        """Create a backup of files/folders"""
        try:
            source = Path(source)
            if not source.exists():
                return {"success": False, "error": "Source not found"}

            if destination is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                destination = self.desktop / f"Backup_{source.name}_{timestamp}"

            destination = Path(destination)

            if source.is_file():
                shutil.copy2(str(source), str(destination))
            else:
                shutil.copytree(str(source), str(destination))

            return {
                "success": True,
                "message": f"Backup created at {destination}",
                "path": str(destination)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ==================== NETWORK ====================

    def get_network_info(self):
        """Get network information"""
        try:
            info = {}

            # Hostname and IP
            info["Hostname"] = socket.gethostname()
            try:
                info["Local IP"] = socket.gethostbyname(info["Hostname"])
            except:
                info["Local IP"] = "Unable to determine"

            # Network interfaces
            interfaces = psutil.net_if_addrs()
            info["Interfaces"] = {}
            for interface, addrs in interfaces.items():
                info["Interfaces"][interface] = []
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        info["Interfaces"][interface].append(f"IPv4: {addr.address}")
                    elif addr.family == socket.AF_INET6:
                        info["Interfaces"][interface].append(f"IPv6: {addr.address}")

            # Network stats
            net_io = psutil.net_io_counters()
            info["Bytes Sent"] = f"{net_io.bytes_sent / (1024**2):.2f} MB"
            info["Bytes Received"] = f"{net_io.bytes_recv / (1024**2):.2f} MB"
            info["Packets Sent"] = net_io.packets_sent
            info["Packets Received"] = net_io.packets_recv

            return {"success": True, "info": info}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_active_connections(self):
        """Get active network connections"""
        try:
            connections = []
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        "Local": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "Remote": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        "Status": conn.status,
                        "PID": conn.pid
                    })

            return {"success": True, "connections": connections}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def test_network_speed(self):
        """Test network speed (simple ping test)"""
        try:
            import subprocess

            # Ping Google DNS
            if self.is_windows:
                result = subprocess.run(["ping", "-n", "4", "8.8.8.8"], capture_output=True, text=True)
            else:
                result = subprocess.run(["ping", "-c", "4", "8.8.8.8"], capture_output=True, text=True)

            return {
                "success": True,
                "result": result.stdout
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ==================== MAINTENANCE ====================

    def disk_cleanup(self):
        """Clean temporary files"""
        try:
            cleaned = []
            total_freed = 0

            # Clean temp folders
            temp_dirs = []
            if self.is_windows:
                temp_dirs = [
                    Path(os.environ.get("TEMP", "")),
                    Path(os.environ.get("TMP", "")),
                ]
            else:
                temp_dirs = [Path("/tmp")]

            for temp_dir in temp_dirs:
                if temp_dir.exists():
                    for item in temp_dir.iterdir():
                        try:
                            if item.is_file():
                                size = item.stat().st_size
                                item.unlink()
                                total_freed += size
                                cleaned.append(str(item))
                            elif item.is_dir():
                                size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                                shutil.rmtree(item)
                                total_freed += size
                                cleaned.append(str(item))
                        except:
                            pass

            return {
                "success": True,
                "message": f"Cleaned {len(cleaned)} items, freed {total_freed / (1024**2):.2f} MB",
                "items_cleaned": len(cleaned),
                "space_freed_mb": total_freed / (1024**2)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_startup_programs(self):
        """Get list of startup programs"""
        try:
            startup_items = []

            if self.is_windows:
                import winreg
                paths = [
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
                ]

                for path in paths:
                    try:
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                startup_items.append({"name": name, "path": value, "location": path})
                                i += 1
                            except WindowsError:
                                break
                        winreg.CloseKey(key)
                    except:
                        pass
            else:
                # Linux/Mac startup locations
                startup_dirs = [
                    Path.home() / ".config" / "autostart",
                    Path("/etc/xdg/autostart") if platform.system() == "Linux" else None
                ]

                for startup_dir in startup_dirs:
                    if startup_dir and startup_dir.exists():
                        for item in startup_dir.iterdir():
                            if item.is_file():
                                startup_items.append({"name": item.name, "path": str(item)})

            return {"success": True, "items": startup_items}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def browser_cleanup(self):
        """Clean browser cache and temporary files"""
        try:
            cleaned = []

            # Common browser cache locations
            if self.is_windows:
                browser_paths = [
                    self.home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
                    self.home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache",
                    self.home / "AppData" / "Local" / "Mozilla" / "Firefox" / "Profiles",
                ]
            else:
                browser_paths = [
                    self.home / ".cache" / "google-chrome",
                    self.home / ".cache" / "mozilla" / "firefox",
                    self.home / "Library" / "Caches" / "Google" / "Chrome" if platform.system() == "Darwin" else None,
                ]

            total_freed = 0
            for browser_path in browser_paths:
                if browser_path and browser_path.exists():
                    try:
                        for item in browser_path.rglob("*"):
                            if item.is_file():
                                try:
                                    size = item.stat().st_size
                                    item.unlink()
                                    total_freed += size
                                    cleaned.append(str(item))
                                except:
                                    pass
                    except:
                        pass

            return {
                "success": True,
                "message": f"Cleaned {len(cleaned)} browser cache files, freed {total_freed / (1024**2):.2f} MB",
                "files_cleaned": len(cleaned)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


# Create singleton instance
_batch_utilities_instance = None


def get_batch_utilities():
    """Get the singleton batch utilities instance"""
    global _batch_utilities_instance
    if _batch_utilities_instance is None:
        _batch_utilities_instance = BatchUtilities()
    return _batch_utilities_instance
