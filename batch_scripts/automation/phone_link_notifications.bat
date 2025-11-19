@echo off
REM ============================================================
REM Phone Link Notification Monitor
REM Access Phone Link notifications from command line
REM ============================================================

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."
set "PYTHON_SCRIPT=%PROJECT_ROOT%\scripts\phone_link_notifications_cli.py"

echo.
echo ============================================================
echo 📱 PHONE LINK NOTIFICATION MONITOR
echo ============================================================
echo.

REM Check if Python script exists
if not exist "%PYTHON_SCRIPT%" (
    echo ❌ Error: Python script not found at:
    echo    %PYTHON_SCRIPT%
    echo.
    echo Creating script...
    call :CREATE_PYTHON_SCRIPT
)

REM Parse command line arguments
set "ACTION=%~1"

if "%ACTION%"=="" (
    set "ACTION=check"
)

REM Execute Python script
python "%PYTHON_SCRIPT%" %ACTION%

goto :END

:CREATE_PYTHON_SCRIPT
REM Create the Python CLI script if it doesn't exist
mkdir "%PROJECT_ROOT%\scripts" 2>nul
(
echo import sys
echo import os
echo.
echo # Add project root to path
echo project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__^)^)^)
echo sys.path.insert(0, project_root^)
echo.
echo from modules.communication.phone_link_monitor import PhoneLinkMonitor
echo.
echo def main(^):
echo     action = sys.argv[1] if len(sys.argv^) ^> 1 else "check"
echo     
echo     monitor = PhoneLinkMonitor(^)
echo     
echo     if action == "check":
echo         print("🔍 Checking for new notifications..."^)
echo         new_notifs = monitor.check_new_notifications(^)
echo         
echo         if new_notifs:
echo             print(f"✅ Found {len(new_notifs^)} new notification(s^):"^)
echo             for notif in new_notifs:
echo                 print(f"\n📱 {notif['type'].upper(^)}"^)
echo                 print(f"   Title: {notif['title']}"^)
echo                 print(f"   Message: {notif['message']}"^)
echo                 print(f"   Sender: {notif['sender']}"^)
echo         else:
echo             print("ℹ️ No new notifications"^)
echo     
echo     elif action == "recent":
echo         recent = monitor.get_recent_notifications(10^)
echo         print(f"📋 Recent notifications ({len(recent^)}^):"^)
echo         for i, notif in enumerate(recent, 1^):
echo             print(f"\n{i}. {notif['type'].upper(^)} - {notif.get('timestamp', 'N/A'^)}"^)
echo             print(f"   {notif['title']}"^)
echo             print(f"   {notif['message']}"^)
echo     
echo     elif action == "monitor":
echo         print("📱 Starting continuous monitoring... (Press Ctrl+C to stop^)"^)
echo         monitor.start_monitoring(5^)
echo         try:
echo             import time
echo             while True:
echo                 time.sleep(1^)
echo         except KeyboardInterrupt:
echo             monitor.stop_monitoring(^)
echo             print("\n✅ Monitoring stopped"^)
echo     
echo     elif action == "clear":
echo         monitor.clear_notifications(^)
echo         print("✅ Notifications cleared"^)
echo     
echo     elif action == "count":
echo         counts = monitor.get_unread_count(^)
echo         print(f"📊 Total notifications: {counts['total']}"^)
echo         print("By type:"^)
echo         for notif_type, count in counts['by_type'].items(^):
echo             print(f"  • {notif_type}: {count}"^)
echo     
echo     else:
echo         print(f"❌ Unknown action: {action}"^)
echo         print("\nAvailable actions:"^)
echo         print("  check   - Check for new notifications"^)
echo         print("  recent  - Show recent notifications"^)
echo         print("  monitor - Start continuous monitoring"^)
echo         print("  count   - Show notification counts"^)
echo         print("  clear   - Clear stored notifications"^)
echo.
echo if __name__ == "__main__":
echo     main(^)
) > "%PYTHON_SCRIPT%"

echo ✅ Python script created
goto :eof

:END
echo.
echo ============================================================
echo.
echo 💡 Usage:
echo    %~nx0 [action]
echo.
echo Actions:
echo    check   - Check for new notifications (default)
echo    recent  - Show recent notifications  
echo    monitor - Start continuous monitoring
echo    count   - Show notification counts
echo    clear   - Clear stored notifications
echo.
echo ============================================================
pause
