@echo off
REM ==========================================
REM File Search
REM Search for files across drives
REM ==========================================

title File Search

echo ========================================
echo          FILE SEARCH UTILITY
echo ========================================
echo.

set /p filename="Enter filename to search (e.g., *.pdf, document.txt): "
set /p drive="Enter drive letter to search (e.g., C, D) or ALL for all drives: "

echo.
echo Searching for: %filename%
echo.

if /i "%drive%"=="ALL" goto searchall

echo Searching in %drive%:\ ...
dir "%drive%:\%filename%" /s /b
goto end

:searchall
echo Searching all drives...
for %%d in (C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist %%d:\ (
        echo Searching %%d:\
        dir "%%d:\%filename%" /s /b 2>nul
    )
)

:end
echo.
echo ========================================
echo Search complete!
echo ========================================
pause
