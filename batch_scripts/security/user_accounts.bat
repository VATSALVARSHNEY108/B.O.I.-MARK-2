@echo off
REM ==========================================
REM USER ACCOUNT MANAGEMENT
REM Manage Windows user accounts
REM ==========================================

color 0C
title User Account Management

:menu
cls
echo ========================================
echo    USER ACCOUNT MANAGEMENT
echo ========================================
echo.
echo 1. List All Users
echo 2. Create New User
echo 3. Delete User
echo 4. Change Password
echo 5. Enable User Account
echo 6. Disable User Account
echo 7. Add User to Administrators
echo 8. View Current User Info
echo 9. Open User Accounts
echo 10. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto listusers
if "%choice%"=="2" goto createuser
if "%choice%"=="3" goto deleteuser
if "%choice%"=="4" goto changepass
if "%choice%"=="5" goto enableuser
if "%choice%"=="6" goto disableuser
if "%choice%"=="7" goto addadmin
if "%choice%"=="8" goto currentuser
if "%choice%"=="9" start netplwiz & goto menu
if "%choice%"=="10" exit /b

goto menu

:listusers
echo.
echo All User Accounts:
net user
echo.
pause
goto menu

:createuser
set /p username="Enter new username: "
set /p password="Enter password: "
net user %username% %password% /add
echo.
echo User %username% created successfully!
pause
goto menu

:deleteuser
echo.
echo WARNING: This will permanently delete the user account!
set /p username="Enter username to delete: "
set /p confirm="Are you sure? (Y/N): "
if /i "%confirm%"=="Y" (
    net user %username% /delete
    echo User deleted!
) else (
    echo Operation cancelled.
)
pause
goto menu

:changepass
set /p username="Enter username: "
set /p password="Enter new password: "
net user %username% %password%
echo.
echo Password changed successfully!
pause
goto menu

:enableuser
set /p username="Enter username to enable: "
net user %username% /active:yes
echo.
echo User account enabled!
pause
goto menu

:disableuser
set /p username="Enter username to disable: "
net user %username% /active:no
echo.
echo User account disabled!
pause
goto menu

:addadmin
set /p username="Enter username: "
net localgroup administrators %username% /add
echo.
echo User added to Administrators group!
pause
goto menu

:currentuser
echo.
echo Current User Information:
echo Username: %USERNAME%
echo Computer Name: %COMPUTERNAME%
echo User Domain: %USERDOMAIN%
echo User Profile: %USERPROFILE%
echo.
whoami /all
echo.
pause
goto menu
