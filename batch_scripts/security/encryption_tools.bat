@echo off
REM ==========================================
REM ENCRYPTION TOOLS
REM BitLocker and EFS management
REM ==========================================

color 0C
title Encryption Tools

:menu
cls
echo ========================================
echo       ENCRYPTION TOOLS
echo ========================================
echo.
echo === BITLOCKER ===
echo 1. Check BitLocker Status
echo 2. Enable BitLocker on Drive
echo 3. Disable BitLocker on Drive
echo 4. Unlock BitLocker Drive
echo 5. Open BitLocker Management
echo.
echo === FILE ENCRYPTION ===
echo 6. Encrypt File/Folder (EFS)
echo 7. Decrypt File/Folder (EFS)
echo 8. View Certificate Manager
echo.
echo 9. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto blstatus
if "%choice%"=="2" goto blenable
if "%choice%"=="3" goto bldisable
if "%choice%"=="4" goto blunlock
if "%choice%"=="5" start control /name Microsoft.BitLockerDriveEncryption & goto menu
if "%choice%"=="6" goto encrypt
if "%choice%"=="7" goto decrypt
if "%choice%"=="8" start certmgr.msc & goto menu
if "%choice%"=="9" exit /b

goto menu

:blstatus
echo.
echo BitLocker Status:
manage-bde -status
echo.
pause
goto menu

:blenable
set /p drive="Enter drive letter (e.g., C:): "
echo.
echo Enabling BitLocker on %drive%...
manage-bde -on %drive%
echo.
echo BitLocker encryption started. This may take some time.
pause
goto menu

:bldisable
set /p drive="Enter drive letter (e.g., C:): "
echo.
echo Disabling BitLocker on %drive%...
manage-bde -off %drive%
echo.
echo BitLocker disabled on %drive%
pause
goto menu

:blunlock
set /p drive="Enter drive letter (e.g., D:): "
set /p password="Enter recovery password: "
manage-bde -unlock %drive% -RecoveryPassword %password%
echo.
echo Drive unlocked!
pause
goto menu

:encrypt
set /p path="Enter file or folder path: "
echo.
echo Encrypting %path%...
cipher /e "%path%"
echo.
echo Encryption complete!
pause
goto menu

:decrypt
set /p path="Enter file or folder path: "
echo.
echo Decrypting %path%...
cipher /d "%path%"
echo.
echo Decryption complete!
pause
goto menu
