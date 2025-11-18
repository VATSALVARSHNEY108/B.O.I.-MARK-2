@echo off
REM ==========================================
REM Quick Notes
REM Simple note-taking utility
REM ==========================================

title Quick Notes

set notes_file=%USERPROFILE%\Desktop\QuickNotes.txt

:menu
cls
echo ========================================
echo          QUICK NOTES
echo ========================================
echo.
echo 1. Add New Note
echo 2. View All Notes
echo 3. Clear All Notes
echo 4. Open Notes in Notepad
echo 5. Search Notes
echo 6. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto add
if "%choice%"=="2" goto view
if "%choice%"=="3" goto clear
if "%choice%"=="4" goto open
if "%choice%"=="5" goto search
if "%choice%"=="6" exit
goto menu

:add
cls
echo ========================================
echo Add New Note (Type below, press Enter when done)
echo ========================================
echo.
set /p note="Note: "
echo.
echo [%date% %time%] >> "%notes_file%"
echo %note% >> "%notes_file%"
echo ---------------------------------------- >> "%notes_file%"
echo.
echo Note saved!
timeout /t 2 >nul
goto menu

:view
cls
echo ========================================
echo           ALL NOTES
echo ========================================
echo.
if exist "%notes_file%" (
    type "%notes_file%"
) else (
    echo No notes found.
)
echo.
pause
goto menu

:clear
del "%notes_file%" 2>nul
echo All notes cleared!
timeout /t 2 >nul
goto menu

:open
if not exist "%notes_file%" echo. > "%notes_file%"
start notepad "%notes_file%"
goto menu

:search
cls
set /p keyword="Enter search keyword: "
echo.
echo Search Results:
echo ========================================
findstr /i /c:"%keyword%" "%notes_file%" 2>nul
if errorlevel 1 echo No results found
echo.
pause
goto menu
