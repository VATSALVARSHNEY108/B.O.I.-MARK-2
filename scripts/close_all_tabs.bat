@echo off
REM Quick Close All Windows - No confirmation
taskkill /F /IM chrome.exe 2>nul
taskkill /F /IM firefox.exe 2>nul
taskkill /F /IM msedge.exe 2>nul
powershell -Command "Get-Process | Where-Object {$_.MainWindowTitle -ne ''} | Where-Object {$_.ProcessName -notin @('explorer','taskmgr','SystemSettings','cmd','powershell')} | Stop-Process -Force -ErrorAction SilentlyContinue"
echo All windows closed!
