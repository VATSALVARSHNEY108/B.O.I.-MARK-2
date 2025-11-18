@echo off
REM ==========================================
REM Organize Downloads Folder
REM Sorts files by type into folders
REM ==========================================

title Organize Downloads

set downloads=%USERPROFILE%\Downloads

echo ========================================
echo     ORGANIZE DOWNLOADS FOLDER
echo ========================================
echo.
echo This will organize files in: %downloads%
echo.
pause

cd /d "%downloads%"

REM Create folders
if not exist "Documents" mkdir "Documents"
if not exist "Images" mkdir "Images"
if not exist "Videos" mkdir "Videos"
if not exist "Music" mkdir "Music"
if not exist "Archives" mkdir "Archives"
if not exist "Programs" mkdir "Programs"
if not exist "Others" mkdir "Others"

echo Moving files...

REM Move Documents
move *.pdf Documents\ >nul 2>&1
move *.doc Documents\ >nul 2>&1
move *.docx Documents\ >nul 2>&1
move *.txt Documents\ >nul 2>&1
move *.xlsx Documents\ >nul 2>&1
move *.pptx Documents\ >nul 2>&1

REM Move Images
move *.jpg Images\ >nul 2>&1
move *.jpeg Images\ >nul 2>&1
move *.png Images\ >nul 2>&1
move *.gif Images\ >nul 2>&1
move *.bmp Images\ >nul 2>&1
move *.svg Images\ >nul 2>&1

REM Move Videos
move *.mp4 Videos\ >nul 2>&1
move *.avi Videos\ >nul 2>&1
move *.mkv Videos\ >nul 2>&1
move *.mov Videos\ >nul 2>&1
move *.wmv Videos\ >nul 2>&1

REM Move Music
move *.mp3 Music\ >nul 2>&1
move *.wav Music\ >nul 2>&1
move *.flac Music\ >nul 2>&1
move *.m4a Music\ >nul 2>&1

REM Move Archives
move *.zip Archives\ >nul 2>&1
move *.rar Archives\ >nul 2>&1
move *.7z Archives\ >nul 2>&1
move *.tar Archives\ >nul 2>&1
move *.gz Archives\ >nul 2>&1

REM Move Programs
move *.exe Programs\ >nul 2>&1
move *.msi Programs\ >nul 2>&1

echo.
echo ========================================
echo Downloads folder organized!
echo ========================================
pause
