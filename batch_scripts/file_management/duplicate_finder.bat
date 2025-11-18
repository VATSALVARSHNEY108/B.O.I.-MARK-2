@echo off
REM ==========================================
REM Duplicate File Finder
REM Find duplicate files by name or size
REM ==========================================

title Duplicate File Finder

:menu
cls
echo ========================================
echo      DUPLICATE FILE FINDER
echo ========================================
echo.
echo 1. Find Duplicate Files (by name)
echo 2. Find Large Duplicate Files (by size)
echo 3. Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto findname
if "%choice%"=="2" goto findsize
if "%choice%"=="3" exit
goto menu

:findname
cls
set /p search_dir="Enter directory to search (or press Enter for Downloads): "
if "%search_dir%"=="" set search_dir=%USERPROFILE%\Downloads

echo.
echo Searching for duplicate files in: %search_dir%
echo This may take a while...
echo.

set output_file=%TEMP%\duplicates_%random%.txt
dir /s /b "%search_dir%" > "%output_file%"

echo Duplicate Files Found:
echo ========================================
for /f "delims=" %%a in ('type "%output_file%" ^| findstr /i /c:".*"') do (
    for /f "delims=" %%b in ('type "%output_file%" ^| findstr /i /c:"%%~nxa"') do (
        if not "%%a"=="%%b" (
            echo %%~nxa
        )
    )
)
echo ========================================
del "%output_file%"
echo.
pause
goto menu

:findsize
cls
set /p search_dir="Enter directory to search: "
set /p min_size="Enter minimum file size in MB: "

echo.
echo Searching for large files over %min_size%MB...
echo.

powershell -Command "Get-ChildItem -Path '%search_dir%' -Recurse -File | Where-Object {$_.Length -gt %min_size%MB} | Group-Object -Property Length | Where-Object {$_.Count -gt 1} | ForEach-Object {$_.Group | Select-Object Name, FullName, @{Name='SizeMB';Expression={[math]::Round($_.Length/1MB,2)}}}"

echo.
pause
goto menu
