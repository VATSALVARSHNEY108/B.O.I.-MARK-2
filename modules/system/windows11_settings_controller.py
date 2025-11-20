"""
Windows 11 Settings Controller
Comprehensive control for ALL Windows 11 settings via PowerShell, Registry, and Windows APIs
Covers Display, Sound, Network, Bluetooth, Privacy, Personalization, System, Accessibility, Updates, and more
"""

import subprocess
import platform
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import winreg
    WINREG_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    winreg = None
    WINREG_AVAILABLE = False


class Windows11SettingsController:
    """Complete Windows 11 settings control"""
    
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        if not self.is_windows:
            raise RuntimeError("This controller only works on Windows 11")
        
        self.settings_cache = {}
        self.registry_paths = {
            "personalization": r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            "desktop": r"Control Panel\Desktop",
            "explorer": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "system": r"System\CurrentControlSet\Control",
        }
    
    # ==================== DISPLAY SETTINGS ====================
    
    def get_display_info(self) -> Dict[str, Any]:
        """Get comprehensive display information"""
        try:
            cmd = """
            Add-Type -AssemblyName System.Windows.Forms
            $screens = [System.Windows.Forms.Screen]::AllScreens
            foreach ($screen in $screens) {
                Write-Output "Name: $($screen.DeviceName)"
                Write-Output "Primary: $($screen.Primary)"
                Write-Output "Resolution: $($screen.Bounds.Width)x$($screen.Bounds.Height)"
                Write-Output "WorkingArea: $($screen.WorkingArea.Width)x$($screen.WorkingArea.Height)"
                Write-Output "BitsPerPixel: $($screen.BitsPerPixel)"
                Write-Output "---"
            }
            """
            result = self._run_powershell(cmd)
            return {"success": True, "info": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_display_resolution(self, width: int, height: int, display_num: int = 1) -> Dict[str, str]:
        """Set display resolution"""
        try:
            cmd = f"""
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class Display {{
                [DllImport("user32.dll")]
                public static extern int ChangeDisplaySettings(ref DEVMODE devMode, int flags);
                
                [StructLayout(LayoutKind.Sequential)]
                public struct DEVMODE {{
                    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
                    public string dmDeviceName;
                    public short dmSpecVersion;
                    public short dmDriverVersion;
                    public short dmSize;
                    public short dmDriverExtra;
                    public int dmFields;
                    public int dmPositionX;
                    public int dmPositionY;
                    public int dmDisplayOrientation;
                    public int dmDisplayFixedOutput;
                    public short dmColor;
                    public short dmDuplex;
                    public short dmYResolution;
                    public short dmTTOption;
                    public short dmCollate;
                    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
                    public string dmFormName;
                    public short dmLogPixels;
                    public int dmBitsPerPel;
                    public int dmPelsWidth;
                    public int dmPelsHeight;
                    public int dmDisplayFlags;
                    public int dmDisplayFrequency;
                }}
            }}
"@
            $devMode = New-Object Display+DEVMODE
            $devMode.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf($devMode)
            $devMode.dmPelsWidth = {width}
            $devMode.dmPelsHeight = {height}
            $devMode.dmFields = 0x180000
            [Display]::ChangeDisplaySettings([ref]$devMode, 0)
            """
            result = self._run_powershell(cmd)
            return {"success": True, "message": f"Resolution set to {width}x{height}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_display_scaling(self, scale_percent: int) -> Dict[str, str]:
        """Set display scaling (100, 125, 150, 175, 200)"""
        try:
            valid_scales = [100, 125, 150, 175, 200]
            if scale_percent not in valid_scales:
                return {"success": False, "error": f"Invalid scale. Choose from: {valid_scales}"}
            
            cmd = f"""
            $path = "HKCU:\\Control Panel\\Desktop"
            Set-ItemProperty -Path $path -Name "Win8DpiScaling" -Value 1
            Set-ItemProperty -Path $path -Name "LogPixels" -Value {scale_percent}
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Display scaling set to {scale_percent}%", "note": "Restart required"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_night_light(self, enabled: bool, temperature: int = 4800) -> Dict[str, str]:
        """Enable/disable night light with color temperature (1200-6500K)"""
        try:
            cmd = f"""
            $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\DefaultAccount\\Current\\default`$windows.data.bluelightreduction.settings\\windows.data.bluelightreduction.settings"
            if ({str(enabled).lower()}) {{
                Set-ItemProperty -Path $path -Name "Data" -Value ([byte[]](0x02,0x00,0x00,0x00,{temperature % 256},{temperature // 256},0x00,0x00))
            }} else {{
                Set-ItemProperty -Path $path -Name "Data" -Value ([byte[]](0x00,0x00,0x00,0x00))
            }}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Night light {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_display_orientation(self, orientation: str) -> Dict[str, str]:
        """Set display orientation (landscape, portrait, landscape_flipped, portrait_flipped)"""
        try:
            orientations = {
                "landscape": 0,
                "portrait": 1,
                "landscape_flipped": 2,
                "portrait_flipped": 3
            }
            if orientation not in orientations:
                return {"success": False, "error": f"Invalid orientation. Choose from: {list(orientations.keys())}"}
            
            orientation_value = orientations[orientation]
            cmd = f"""
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class DisplayOrientation {{
                [DllImport("user32.dll")]
                public static extern int EnumDisplaySettings(string lpszDeviceName, int iModeNum, ref DEVMODE lpDevMode);
                
                [DllImport("user32.dll")]
                public static extern int ChangeDisplaySettingsEx(string lpszDeviceName, ref DEVMODE lpDevMode, IntPtr hwnd, int dwflags, IntPtr lParam);
                
                [StructLayout(LayoutKind.Sequential)]
                public struct DEVMODE {{
                    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
                    public string dmDeviceName;
                    public short dmSpecVersion;
                    public short dmDriverVersion;
                    public short dmSize;
                    public short dmDriverExtra;
                    public int dmFields;
                    public int dmPositionX;
                    public int dmPositionY;
                    public int dmDisplayOrientation;
                    public int dmDisplayFixedOutput;
                    public short dmColor;
                    public short dmDuplex;
                    public short dmYResolution;
                    public short dmTTOption;
                    public short dmCollate;
                    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
                    public string dmFormName;
                    public short dmLogPixels;
                    public int dmBitsPerPel;
                    public int dmPelsWidth;
                    public int dmPelsHeight;
                    public int dmDisplayFlags;
                    public int dmDisplayFrequency;
                }}
            }}
"@
            $devMode = New-Object DisplayOrientation+DEVMODE
            $devMode.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf($devMode)
            
            # Get current display settings first
            $enumResult = [DisplayOrientation]::EnumDisplaySettings($null, -1, [ref]$devMode)
            if ($enumResult -eq 0) {{
                Write-Output "FAIL:Cannot retrieve current display settings"
                exit 1
            }}
            
            # For portrait rotations (90° or 270°), swap width and height
            $currentOrientation = $devMode.dmDisplayOrientation
            $newOrientation = {orientation_value}
            $needsSwap = (($currentOrientation -eq 0 -or $currentOrientation -eq 2) -and ($newOrientation -eq 1 -or $newOrientation -eq 3)) -or `
                         (($currentOrientation -eq 1 -or $currentOrientation -eq 3) -and ($newOrientation -eq 0 -or $newOrientation -eq 2))
            
            if ($needsSwap) {{
                $temp = $devMode.dmPelsWidth
                $devMode.dmPelsWidth = $devMode.dmPelsHeight
                $devMode.dmPelsHeight = $temp
            }}
            
            # Modify orientation
            $devMode.dmDisplayOrientation = $newOrientation
            $devMode.dmFields = 0x80 -bor 0x180000 -bor 0x40000
            
            # Apply new settings
            $result = [DisplayOrientation]::ChangeDisplaySettingsEx($null, [ref]$devMode, [IntPtr]::Zero, 0, [IntPtr]::Zero)
            Write-Output "RESULT:$result"
            """
            result = self._run_powershell(cmd)
            
            if "RESULT:0" in result:
                return {"success": True, "message": f"Orientation set to {orientation}"}
            elif "FAIL:" in result:
                return {"success": False, "error": result.split("FAIL:")[1].strip()}
            else:
                error_codes = {1: "RESTART_REQUIRED", 2: "BADFLAGS", -1: "BADPARAM", -2: "FAILED", -3: "BADMODE", -4: "NOTUPDATED"}
                result_code = result.split("RESULT:")[1].strip() if "RESULT:" in result else "unknown"
                error_msg = error_codes.get(int(result_code) if result_code.lstrip('-').isdigit() else -99, f"ERROR_CODE_{result_code}")
                return {"success": False, "error": f"Failed to change orientation: {error_msg}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_refresh_rate(self, refresh_rate: int) -> Dict[str, str]:
        """Set display refresh rate (60, 75, 120, 144, etc.)"""
        try:
            cmd = f"""
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class RefreshRate {{
                [DllImport("user32.dll")]
                public static extern int EnumDisplaySettings(string lpszDeviceName, int iModeNum, ref DEVMODE lpDevMode);
                
                [DllImport("user32.dll")]
                public static extern int ChangeDisplaySettingsEx(string lpszDeviceName, ref DEVMODE lpDevMode, IntPtr hwnd, int dwflags, IntPtr lParam);
                
                [StructLayout(LayoutKind.Sequential)]
                public struct DEVMODE {{
                    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
                    public string dmDeviceName;
                    public short dmSpecVersion;
                    public short dmDriverVersion;
                    public short dmSize;
                    public short dmDriverExtra;
                    public int dmFields;
                    public int dmPositionX;
                    public int dmPositionY;
                    public int dmDisplayOrientation;
                    public int dmDisplayFixedOutput;
                    public short dmColor;
                    public short dmDuplex;
                    public short dmYResolution;
                    public short dmTTOption;
                    public short dmCollate;
                    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
                    public string dmFormName;
                    public short dmLogPixels;
                    public int dmBitsPerPel;
                    public int dmPelsWidth;
                    public int dmPelsHeight;
                    public int dmDisplayFlags;
                    public int dmDisplayFrequency;
                }}
            }}
"@
            $devMode = New-Object RefreshRate+DEVMODE
            $devMode.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf($devMode)
            
            # Get current display settings first
            $enumResult = [RefreshRate]::EnumDisplaySettings($null, -1, [ref]$devMode)
            if ($enumResult -eq 0) {{
                Write-Output "FAIL:Cannot retrieve current display settings"
                exit 1
            }}
            
            # Modify only refresh rate, keep other settings
            $devMode.dmDisplayFrequency = {refresh_rate}
            $devMode.dmFields = 0x400000 -bor 0x180000
            
            # Apply new settings
            $result = [RefreshRate]::ChangeDisplaySettingsEx($null, [ref]$devMode, [IntPtr]::Zero, 0, [IntPtr]::Zero)
            Write-Output "RESULT:$result"
            """
            result = self._run_powershell(cmd)
            
            if "RESULT:0" in result:
                return {"success": True, "message": f"Refresh rate set to {refresh_rate}Hz"}
            elif "FAIL:" in result:
                return {"success": False, "error": result.split("FAIL:")[1].strip()}
            else:
                error_codes = {1: "RESTART_REQUIRED", 2: "BADFLAGS", -1: "BADPARAM", -2: "FAILED", -3: "BADMODE", -4: "NOTUPDATED"}
                result_code = result.split("RESULT:")[1].strip() if "RESULT:" in result else "unknown"
                error_msg = error_codes.get(int(result_code) if result_code.lstrip('-').isdigit() else -99, f"ERROR_CODE_{result_code}")
                return {"success": False, "error": f"Failed to change refresh rate: {error_msg}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== SOUND SETTINGS ====================
    
    def list_audio_devices(self, device_type: str = "playback") -> Dict[str, Any]:
        """List audio devices (playback or recording) using native WMI"""
        try:
            if device_type == "playback":
                cmd = """
                Get-CimInstance Win32_SoundDevice | 
                Select-Object Name, DeviceID, Status | 
                Format-List
                """
            else:
                cmd = """
                Get-CimInstance Win32_SoundDevice | 
                Where-Object {$_.Caption -like "*microphone*" -or $_.Caption -like "*input*"} |
                Select-Object Name, DeviceID, Status | 
                Format-List
                """
            result = self._run_powershell(cmd)
            return {"success": True, "devices": result, "note": "Use Windows Settings for detailed audio device configuration"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_default_audio_device(self, device_name: str, device_type: str = "playback") -> Dict[str, str]:
        """Set default audio device using nircmd or native Windows Settings"""
        try:
            return {
                "success": False, 
                "error": "Setting default audio device requires third-party tools or manual configuration",
                "note": "Please use Windows Settings > System > Sound to change default audio device, or install NirCmd utility"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_spatial_sound(self, enabled: bool, format: str = "WindowsSonic") -> Dict[str, str]:
        """Enable/disable spatial sound (WindowsSonic, DolbyAtmos, DTS)"""
        try:
            formats = {"WindowsSonic": 0, "DolbyAtmos": 1, "DTS": 2, "Off": -1}
            if format not in formats:
                return {"success": False, "error": f"Invalid format. Choose from: {list(formats.keys())}"}
            
            cmd = f"""
            $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Audio"
            if ({str(enabled).lower()}) {{
                Set-ItemProperty -Path $path -Name "SpatialAudioEnabled" -Value 1
                Set-ItemProperty -Path $path -Name "SpatialAudioFormat" -Value {formats[format]}
            }} else {{
                Set-ItemProperty -Path $path -Name "SpatialAudioEnabled" -Value 0
            }}
            """
            self._run_powershell(cmd)
            status = f"enabled with {format}" if enabled else "disabled"
            return {"success": True, "message": f"Spatial sound {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== NETWORK SETTINGS ====================
    
    def get_network_adapters(self) -> Dict[str, Any]:
        """Get all network adapters and their status"""
        try:
            cmd = """
            Get-NetAdapter | Select-Object Name, Status, LinkSpeed, MacAddress, InterfaceDescription | 
            ConvertTo-Json
            """
            result = self._run_powershell(cmd)
            return {"success": True, "adapters": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_wifi_state(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable WiFi"""
        try:
            action = "Enable" if enabled else "Disable"
            cmd = f"""
            $adapter = Get-NetAdapter | Where-Object {{$_.Name -like "*Wi-Fi*" -or $_.Name -like "*Wireless*"}}
            if ($adapter) {{
                {action}-NetAdapter -Name $adapter.Name -Confirm:$false
            }}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"WiFi {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_airplane_mode(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable airplane mode"""
        try:
            value = 1 if enabled else 0
            cmd = f"""
            $path = "HKLM:\\SOFTWARE\\Microsoft\\RadioManagement\\SystemRadioState"
            Set-ItemProperty -Path $path -Name "RadioState" -Value {value}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Airplane mode {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_mobile_hotspot(self, enabled: bool, ssid: Optional[str] = None, password: Optional[str] = None) -> Dict[str, str]:
        """Enable/disable mobile hotspot"""
        try:
            if enabled and (ssid or password):
                cmd = f"""
                # Configure mobile hotspot
                $connectionProfile = [Windows.Networking.Connectivity.NetworkInformation,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::GetInternetConnectionProfile()
                $tetheringManager = [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager,Windows.Networking.NetworkOperators,ContentType=WindowsRuntime]::CreateFromConnectionProfile($connectionProfile)
                
                """
                if ssid:
                    cmd += f'$tetheringManager.AccessPointConfiguration.Ssid = "{ssid}"\n'
                if password:
                    cmd += f'$tetheringManager.AccessPointConfiguration.Passphrase = "{password}"\n'
                
                if enabled:
                    cmd += "$tetheringManager.StartTetheringAsync()"
                else:
                    cmd += "$tetheringManager.StopTetheringAsync()"
                
                self._run_powershell(cmd)
            
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Mobile hotspot {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_proxy(self, enabled: bool, server: Optional[str] = None, port: Optional[int] = None) -> Dict[str, str]:
        """Configure proxy settings"""
        try:
            if enabled and server and port:
                cmd = f"""
                Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" -Name ProxyEnable -Value 1
                Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" -Name ProxyServer -Value "{server}:{port}"
                """
            else:
                cmd = """
                Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" -Name ProxyEnable -Value 0
                """
            
            self._run_powershell(cmd)
            status = f"enabled ({server}:{port})" if enabled and server and port else "disabled"
            return {"success": True, "message": f"Proxy {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def flush_dns_cache(self) -> Dict[str, str]:
        """Flush DNS cache"""
        try:
            cmd = "Clear-DnsClientCache"
            self._run_powershell(cmd)
            return {"success": True, "message": "DNS cache flushed"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def reset_network_adapter(self, adapter_name: Optional[str] = None) -> Dict[str, str]:
        """Reset network adapter"""
        try:
            if adapter_name:
                cmd = f"""
                Disable-NetAdapter -Name "{adapter_name}" -Confirm:$false
                Start-Sleep -Seconds 2
                Enable-NetAdapter -Name "{adapter_name}" -Confirm:$false
                """
            else:
                cmd = """
                $adapters = Get-NetAdapter | Where-Object {$_.Status -eq "Up"}
                foreach ($adapter in $adapters) {
                    Disable-NetAdapter -Name $adapter.Name -Confirm:$false
                    Start-Sleep -Seconds 2
                    Enable-NetAdapter -Name $adapter.Name -Confirm:$false
                }
                """
            self._run_powershell(cmd)
            return {"success": True, "message": "Network adapter reset successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== BLUETOOTH SETTINGS ====================
    
    def set_bluetooth_state(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable Bluetooth"""
        try:
            action = "Enable" if enabled else "Disable"
            cmd = f"""
            $bluetooth = Get-PnpDevice | Where-Object {{$_.Class -eq "Bluetooth" -and $_.FriendlyName -like "*Bluetooth*"}}
            if ($bluetooth) {{
                {action}-PnpDevice -InstanceId $bluetooth.InstanceId -Confirm:$false
            }}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Bluetooth {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_bluetooth_devices(self) -> Dict[str, Any]:
        """List paired Bluetooth devices"""
        try:
            cmd = """
            Get-PnpDevice | Where-Object {$_.Class -eq "Bluetooth"} | 
            Select-Object FriendlyName, Status, InstanceId | ConvertTo-Json
            """
            result = self._run_powershell(cmd)
            return {"success": True, "devices": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_bluetooth_discoverable(self, enabled: bool) -> Dict[str, str]:
        """Make Bluetooth discoverable"""
        try:
            value = 1 if enabled else 0
            cmd = f"""
            $path = "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters"
            Set-ItemProperty -Path $path -Name "DeviceDiscoverable" -Value {value}
            """
            self._run_powershell(cmd)
            status = "discoverable" if enabled else "hidden"
            return {"success": True, "message": f"Bluetooth is now {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== PRIVACY & SECURITY SETTINGS ====================
    
    def set_camera_access(self, enabled: bool, app_specific: Optional[str] = None) -> Dict[str, str]:
        """Enable/disable camera access globally or for specific app"""
        try:
            value = "Allow" if enabled else "Deny"
            if app_specific:
                cmd = f"""
                $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam\\{app_specific}"
                Set-ItemProperty -Path $path -Name "Value" -Value "{value}"
                """
            else:
                cmd = f"""
                $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam"
                Set-ItemProperty -Path $path -Name "Value" -Value "{value}"
                """
            
            self._run_powershell(cmd)
            target = f"for {app_specific}" if app_specific else "globally"
            return {"success": True, "message": f"Camera access {value.lower()}ed {target}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_microphone_access(self, enabled: bool, app_specific: Optional[str] = None) -> Dict[str, str]:
        """Enable/disable microphone access globally or for specific app"""
        try:
            value = "Allow" if enabled else "Deny"
            if app_specific:
                cmd = f"""
                $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\microphone\\{app_specific}"
                Set-ItemProperty -Path $path -Name "Value" -Value "{value}"
                """
            else:
                cmd = f"""
                $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\microphone"
                Set-ItemProperty -Path $path -Name "Value" -Value "{value}"
                """
            
            self._run_powershell(cmd)
            target = f"for {app_specific}" if app_specific else "globally"
            return {"success": True, "message": f"Microphone access {value.lower()}ed {target}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_location_access(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable location access"""
        try:
            value = "Allow" if enabled else "Deny"
            cmd = f"""
            $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\location"
            Set-ItemProperty -Path $path -Name "Value" -Value "{value}"
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Location access {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_telemetry_level(self, level: str) -> Dict[str, str]:
        """Set Windows telemetry level (security, basic, enhanced, full)"""
        try:
            levels = {"security": 0, "basic": 1, "enhanced": 2, "full": 3}
            if level not in levels:
                return {"success": False, "error": f"Invalid level. Choose from: {list(levels.keys())}"}
            
            cmd = f"""
            $path = "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection"
            Set-ItemProperty -Path $path -Name "AllowTelemetry" -Value {levels[level]}
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Telemetry level set to {level}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_windows_defender(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable Windows Defender real-time protection"""
        try:
            value = "$true" if enabled else "$false"
            cmd = f"Set-MpPreference -DisableRealtimeMonitoring {value}"
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Windows Defender {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_firewall_state(self, enabled: bool, profile: str = "all") -> Dict[str, str]:
        """Enable/disable Windows Firewall (domain, private, public, all)"""
        try:
            profiles = ["Domain", "Private", "Public"] if profile == "all" else [profile.capitalize()]
            action = "Enable" if enabled else "Disable"
            
            for prof in profiles:
                cmd = f"Set-NetFirewallProfile -{prof}Profile -Enabled {action}"
                self._run_powershell(cmd)
            
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Firewall {status} for {profile} profile(s)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== PERSONALIZATION SETTINGS ====================
    
    def set_dark_mode(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable dark mode"""
        try:
            value = 0 if enabled else 1  # 0 = dark, 1 = light
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" -Name "AppsUseLightTheme" -Value {value}
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" -Name "SystemUsesLightTheme" -Value {value}
            """
            self._run_powershell(cmd)
            mode = "dark" if enabled else "light"
            return {"success": True, "message": f"{mode.capitalize()} mode enabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_wallpaper(self, image_path: str) -> Dict[str, str]:
        """Set desktop wallpaper"""
        try:
            if not os.path.exists(image_path):
                return {"success": False, "error": "Image file not found"}
            
            cmd = f"""
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class Wallpaper {{
                [DllImport("user32.dll", CharSet=CharSet.Auto)]
                public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
            }}
"@
            [Wallpaper]::SystemParametersInfo(0x0014, 0, "{image_path.replace(chr(92), chr(92)+chr(92))}", 0x0001 -bor 0x0002)
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Wallpaper set to {image_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_accent_color(self, color_hex: str) -> Dict[str, str]:
        """Set Windows accent color (hex format: #RRGGBB)"""
        try:
            # Remove '#' if present
            color_hex = color_hex.lstrip('#')
            if len(color_hex) != 6:
                return {"success": False, "error": "Invalid color format. Use #RRGGBB"}
            
            # Convert hex to BGR DWORD
            r, g, b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
            bgr_value = (b << 16) | (g << 8) | r
            
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\DWM" -Name "AccentColor" -Value {bgr_value}
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\DWM" -Name "ColorizationColor" -Value {bgr_value}
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Accent color set to #{color_hex}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_transparency_effects(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable transparency effects"""
        try:
            value = 1 if enabled else 0
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" -Name "EnableTransparency" -Value {value}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Transparency effects {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_taskbar_position(self, position: str) -> Dict[str, str]:
        """Set taskbar position (bottom, top, left, right)"""
        try:
            positions = {"bottom": 3, "top": 1, "left": 0, "right": 2}
            if position not in positions:
                return {"success": False, "error": f"Invalid position. Choose from: {list(positions.keys())}"}
            
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StuckRects3" -Name "Settings" -Value {positions[position]}
            Stop-Process -Name explorer -Force
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Taskbar moved to {position}", "note": "Explorer restarted"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_taskbar_auto_hide(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable taskbar auto-hide"""
        try:
            value = 1 if enabled else 0
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StuckRects3" -Name "Settings[8]" -Value {value}
            Stop-Process -Name explorer -Force
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Taskbar auto-hide {status}", "note": "Explorer restarted"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_start_menu_layout(self, layout: str) -> Dict[str, str]:
        """Set Start menu layout (default, more_pins, more_recommendations)"""
        try:
            layouts = {"default": 0, "more_pins": 1, "more_recommendations": 2}
            if layout not in layouts:
                return {"success": False, "error": f"Invalid layout. Choose from: {list(layouts.keys())}"}
            
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "Start_Layout" -Value {layouts[layout]}
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Start menu layout set to {layout}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== SYSTEM SETTINGS ====================
    
    def set_notifications(self, enabled: bool, app_specific: Optional[str] = None) -> Dict[str, str]:
        """Enable/disable notifications globally or for specific app"""
        try:
            value = 1 if enabled else 0
            if app_specific:
                cmd = f"""
                $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings\\{app_specific}"
                Set-ItemProperty -Path $path -Name "Enabled" -Value {value}
                """
            else:
                cmd = f"""
                Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" -Name "ToastEnabled" -Value {value}
                """
            
            self._run_powershell(cmd)
            target = f"for {app_specific}" if app_specific else "globally"
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Notifications {status} {target}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_focus_assist(self, mode: str) -> Dict[str, str]:
        """Set focus assist mode (off, priority_only, alarms_only)"""
        try:
            modes = {"off": 0, "priority_only": 1, "alarms_only": 2}
            if mode not in modes:
                return {"success": False, "error": f"Invalid mode. Choose from: {list(modes.keys())}"}
            
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\DefaultAccount\\Current\\default`$windows.data.notifications.quiethourssettings\\windows.data.notifications.quiethourssettings" -Name "Value" -Value {modes[mode]}
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Focus assist set to {mode}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_clipboard_history(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable clipboard history"""
        try:
            value = 1 if enabled else 0
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Clipboard" -Name "EnableClipboardHistory" -Value {value}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Clipboard history {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_storage_sense(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable Storage Sense"""
        try:
            value = 1 if enabled else 0
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy" -Name "01" -Value {value}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Storage Sense {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_remote_desktop(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable Remote Desktop"""
        try:
            value = 0 if enabled else 1  # 0 = enabled, 1 = disabled
            cmd = f"""
            Set-ItemProperty -Path "HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server" -Name "fDenyTSConnections" -Value {value}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Remote Desktop {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_storage_usage(self) -> Dict[str, Any]:
        """Get storage usage information"""
        try:
            cmd = """
            Get-Volume | Where-Object {$_.DriveLetter} | 
            Select-Object DriveLetter, FileSystemLabel, FileSystem, 
            @{Name="Size(GB)";Expression={[math]::Round($_.Size/1GB,2)}},
            @{Name="Used(GB)";Expression={[math]::Round(($_.Size - $_.SizeRemaining)/1GB,2)}},
            @{Name="Free(GB)";Expression={[math]::Round($_.SizeRemaining/1GB,2)}},
            @{Name="Usage(%)";Expression={[math]::Round((($_.Size - $_.SizeRemaining)/$_.Size)*100,1)}} |
            ConvertTo-Json
            """
            result = self._run_powershell(cmd)
            return {"success": True, "storage": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== ACCESSIBILITY SETTINGS ====================
    
    def set_narrator(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable Narrator"""
        try:
            if enabled:
                cmd = "Start-Process -FilePath 'C:\\Windows\\System32\\Narrator.exe'"
            else:
                cmd = "Stop-Process -Name 'Narrator' -Force -ErrorAction SilentlyContinue"
            
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Narrator {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_magnifier(self, enabled: bool, zoom_level: int = 200) -> Dict[str, str]:
        """Enable/disable Magnifier with zoom level"""
        try:
            if enabled:
                cmd = f"""
                Start-Process -FilePath 'C:\\Windows\\System32\\Magnify.exe'
                Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\ScreenMagnifier" -Name "Magnification" -Value {zoom_level}
                """
            else:
                cmd = "Stop-Process -Name 'Magnify' -Force -ErrorAction SilentlyContinue"
            
            self._run_powershell(cmd)
            status = f"enabled at {zoom_level}% zoom" if enabled else "disabled"
            return {"success": True, "message": f"Magnifier {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_high_contrast(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable high contrast mode"""
        try:
            value = 1 if enabled else 0
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Control Panel\\Accessibility\\HighContrast" -Name "Flags" -Value {value}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"High contrast mode {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_sticky_keys(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable sticky keys"""
        try:
            flags = "510" if enabled else "506"
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Control Panel\\Accessibility\\StickyKeys" -Name "Flags" -Value "{flags}"
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Sticky keys {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_filter_keys(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable filter keys"""
        try:
            flags = "510" if enabled else "506"
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Control Panel\\Accessibility\\Keyboard Response" -Name "Flags" -Value "{flags}"
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Filter keys {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_mouse_pointer_size(self, size: int) -> Dict[str, str]:
        """Set mouse pointer size (1-15)"""
        try:
            if size < 1 or size > 15:
                return {"success": False, "error": "Size must be between 1 and 15"}
            
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Control Panel\\Cursors" -Name "CursorBaseSize" -Value {size * 32}
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Mouse pointer size set to {size}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== WINDOWS UPDATE SETTINGS ====================
    
    def check_windows_updates(self) -> Dict[str, Any]:
        """Check for Windows updates"""
        try:
            cmd = """
            Install-Module -Name PSWindowsUpdate -Force -SkipPublisherCheck -ErrorAction SilentlyContinue
            Import-Module PSWindowsUpdate
            Get-WindowsUpdate | Select-Object Title, KB, Size | ConvertTo-Json
            """
            result = self._run_powershell(cmd)
            return {"success": True, "updates": result}
        except Exception as e:
            # Fallback without PSWindowsUpdate module
            try:
                cmd = """
                $updateSession = New-Object -ComObject Microsoft.Update.Session
                $updateSearcher = $updateSession.CreateUpdateSearcher()
                $searchResult = $updateSearcher.Search("IsInstalled=0")
                $searchResult.Updates | Select-Object Title | ConvertTo-Json
                """
                result = self._run_powershell(cmd)
                return {"success": True, "updates": result}
            except:
                return {"success": False, "error": str(e)}
    
    def install_windows_updates(self) -> Dict[str, str]:
        """Install all pending Windows updates"""
        try:
            cmd = """
            Install-Module -Name PSWindowsUpdate -Force -SkipPublisherCheck -ErrorAction SilentlyContinue
            Import-Module PSWindowsUpdate
            Get-WindowsUpdate -AcceptAll -Install -AutoReboot
            """
            self._run_powershell(cmd)
            return {"success": True, "message": "Windows updates installation started"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def pause_windows_updates(self, days: int = 7) -> Dict[str, str]:
        """Pause Windows updates for specified days (1-35)"""
        try:
            if days < 1 or days > 35:
                return {"success": False, "error": "Days must be between 1 and 35"}
            
            cmd = f"""
            $date = (Get-Date).AddDays({days}).ToString("yyyy-MM-dd")
            Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\WindowsUpdate\\UX\\Settings" -Name "PauseUpdatesExpiryTime" -Value $date
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Windows updates paused for {days} days"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def resume_windows_updates(self) -> Dict[str, str]:
        """Resume Windows updates"""
        try:
            cmd = """
            Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\WindowsUpdate\\UX\\Settings" -Name "PauseUpdatesExpiryTime" -ErrorAction SilentlyContinue
            """
            self._run_powershell(cmd)
            return {"success": True, "message": "Windows updates resumed"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== APP & STARTUP SETTINGS ====================
    
    def list_startup_apps(self) -> Dict[str, Any]:
        """List all startup applications"""
        try:
            cmd = """
            Get-CimInstance Win32_StartupCommand | 
            Select-Object Name, Command, Location, User | ConvertTo-Json
            """
            result = self._run_powershell(cmd)
            return {"success": True, "apps": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def disable_startup_app(self, app_name: str) -> Dict[str, str]:
        """Disable an app from startup"""
        try:
            cmd = f"""
            Get-CimInstance Win32_StartupCommand | Where-Object {{$_.Name -like "*{app_name}*"}} | 
            Remove-CimInstance
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"{app_name} removed from startup"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_default_browser(self, browser: str) -> Dict[str, str]:
        """Set default web browser (chrome, firefox, edge, opera)"""
        try:
            browsers = {
                "chrome": "ChromeHTML",
                "firefox": "FirefoxHTML",
                "edge": "MSEdgeHTM",
                "opera": "OperaStable"
            }
            
            if browser.lower() not in browsers:
                return {"success": False, "error": f"Unsupported browser. Choose from: {list(browsers.keys())}"}
            
            prog_id = browsers[browser.lower()]
            cmd = f"""
            $regPath = "HKCU:\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice"
            Set-ItemProperty -Path $regPath -Name "ProgId" -Value "{prog_id}"
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Default browser set to {browser}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== TIME & LANGUAGE SETTINGS ====================
    
    def set_time_zone(self, timezone: str) -> Dict[str, str]:
        """Set system timezone (e.g., 'Pacific Standard Time', 'Eastern Standard Time')"""
        try:
            cmd = f'Set-TimeZone -Id "{timezone}"'
            self._run_powershell(cmd)
            return {"success": True, "message": f"Timezone set to {timezone}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_timezones(self) -> Dict[str, Any]:
        """List all available timezones"""
        try:
            cmd = "Get-TimeZone -ListAvailable | Select-Object Id, DisplayName | ConvertTo-Json"
            result = self._run_powershell(cmd)
            return {"success": True, "timezones": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_date_time_format(self, format_type: str, format_string: str) -> Dict[str, str]:
        """Set date/time format (short_date, long_date, short_time, long_time)"""
        try:
            format_keys = {
                "short_date": "sShortDate",
                "long_date": "sLongDate",
                "short_time": "sShortTime",
                "long_time": "sLongTime"
            }
            
            if format_type not in format_keys:
                return {"success": False, "error": f"Invalid format type. Choose from: {list(format_keys.keys())}"}
            
            key = format_keys[format_type]
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Control Panel\\International" -Name "{key}" -Value "{format_string}"
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"{format_type} format set to {format_string}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== GAMING SETTINGS ====================
    
    def set_game_mode(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable Game Mode"""
        try:
            value = 1 if enabled else 0
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\GameBar" -Name "AllowAutoGameMode" -Value {value}
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\GameBar" -Name "AutoGameModeEnabled" -Value {value}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Game Mode {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_game_bar(self, enabled: bool) -> Dict[str, str]:
        """Enable/disable Xbox Game Bar"""
        try:
            value = 1 if enabled else 0
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" -Name "AppCaptureEnabled" -Value {value}
            Set-ItemProperty -Path "HKCU:\\System\\GameConfigStore" -Name "GameDVR_Enabled" -Value {value}
            """
            self._run_powershell(cmd)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Xbox Game Bar {status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== POWER SETTINGS ====================
    
    def set_power_plan(self, plan: str) -> Dict[str, str]:
        """Set power plan (balanced, high_performance, power_saver)"""
        try:
            plans = {
                "balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
                "high_performance": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                "power_saver": "a1841308-3541-4fab-bc81-f71556f20b4a"
            }
            
            if plan not in plans:
                return {"success": False, "error": f"Invalid plan. Choose from: {list(plans.keys())}"}
            
            cmd = f'powercfg /setactive {plans[plan]}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"success": True, "message": f"Power plan set to {plan}"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_sleep_timeout(self, minutes: int, on_battery: bool = False) -> Dict[str, str]:
        """Set sleep timeout in minutes"""
        try:
            power_source = "DC" if on_battery else "AC"
            cmd = f'powercfg /change standby-timeout-{power_source.lower()} {minutes}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                source = "on battery" if on_battery else "plugged in"
                return {"success": True, "message": f"Sleep timeout set to {minutes} minutes when {source}"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_screen_timeout(self, minutes: int, on_battery: bool = False) -> Dict[str, str]:
        """Set screen timeout in minutes"""
        try:
            power_source = "DC" if on_battery else "AC"
            cmd = f'powercfg /change monitor-timeout-{power_source.lower()} {minutes}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                source = "on battery" if on_battery else "plugged in"
                return {"success": True, "message": f"Screen timeout set to {minutes} minutes when {source}"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== ADVANCED SYSTEM SETTINGS ====================
    
    def set_virtual_memory(self, drive: str, initial_mb: int, maximum_mb: int) -> Dict[str, str]:
        """Configure virtual memory (page file)"""
        try:
            cmd = f"""
            $computersys = Get-WmiObject Win32_ComputerSystem -EnableAllPrivileges
            $computersys.AutomaticManagedPagefile = $false
            $computersys.Put()
            
            $pagefileset = Get-WmiObject -Query "SELECT * FROM Win32_PageFileSetting WHERE Name='{drive}:\\pagefile.sys'"
            if ($pagefileset) {{
                $pagefileset.InitialSize = {initial_mb}
                $pagefileset.MaximumSize = {maximum_mb}
                $pagefileset.Put()
            }}
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Virtual memory configured: {initial_mb}-{maximum_mb} MB on {drive}:"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_performance_options(self, option: str) -> Dict[str, str]:
        """Set performance options (best_appearance, best_performance, custom)"""
        try:
            if option == "best_performance":
                value = 2
            elif option == "best_appearance":
                value = 1
            else:
                value = 0
            
            cmd = f"""
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" -Name "VisualFXSetting" -Value {value}
            """
            self._run_powershell(cmd)
            return {"success": True, "message": f"Performance options set to {option}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def optimize_system_performance(self) -> Dict[str, str]:
        """Apply comprehensive performance optimizations"""
        try:
            cmd = """
            # Disable visual effects
            Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" -Name "VisualFXSetting" -Value 2
            
            # Disable Windows Search indexing
            Stop-Service "WSearch" -Force
            Set-Service "WSearch" -StartupType Disabled
            
            # Disable Superfetch/SysMain
            Stop-Service "SysMain" -Force
            Set-Service "SysMain" -StartupType Disabled
            
            # Disable hibernation
            powercfg /hibernate off
            
            # Set high performance power plan
            powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
            """
            self._run_powershell(cmd)
            return {"success": True, "message": "System performance optimizations applied"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== UTILITY METHODS ====================
    
    def _run_powershell(self, command: str) -> str:
        """Execute PowerShell command and return output"""
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0 and result.stderr:
                raise Exception(result.stderr)
            
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise Exception("PowerShell command timed out")
        except Exception as e:
            raise Exception(f"PowerShell execution failed: {str(e)}")
    
    def _read_registry(self, path: str, key: str) -> Any:
        """Read Windows Registry value"""
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            registry_key = winreg.OpenKey(registry, path, 0, winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, key)
            winreg.CloseKey(registry_key)
            return value
        except WindowsError:
            return None
    
    def _write_registry(self, path: str, key: str, value: Any, reg_type: Optional[int] = None) -> bool:
        """Write Windows Registry value"""
        if not WINREG_AVAILABLE or winreg is None:
            return False
        if reg_type is None:
            reg_type = winreg.REG_DWORD
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            registry_key = winreg.OpenKey(registry, path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, key, 0, reg_type, value)
            winreg.CloseKey(registry_key)
            return True
        except WindowsError:
            return False
    
    def get_all_settings_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of all current Windows 11 settings"""
        try:
            summary = {
                "display": self.get_display_info(),
                "network": self.get_network_adapters(),
                "storage": self.get_storage_usage(),
                "bluetooth_devices": self.list_bluetooth_devices(),
                "startup_apps": self.list_startup_apps(),
                "updates": self.check_windows_updates(),
            }
            return {"success": True, "summary": summary}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Singleton instance
_windows11_controller_instance = None

def get_windows11_controller() -> Windows11SettingsController:
    """Get Windows 11 settings controller singleton instance"""
    global _windows11_controller_instance
    if _windows11_controller_instance is None:
        _windows11_controller_instance = Windows11SettingsController()
    return _windows11_controller_instance
