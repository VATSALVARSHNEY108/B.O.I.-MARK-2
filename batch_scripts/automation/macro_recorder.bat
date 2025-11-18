@echo off
REM ==========================================
REM SIMPLE MACRO RECORDER
REM Record and play simple command macros
REM ==========================================

color 0F
title Macro Recorder

:menu
cls
echo ========================================
echo       MACRO RECORDER
echo ========================================
echo.
echo 1. Create New Macro
echo 2. Run Existing Macro
echo 3. List Saved Macros
echo 4. Delete Macro
echo 5. Edit Macro
echo 6. Back to Main Menu
echo.
echo ========================================
set /p choice="Select option: "

if "%choice%"=="1" goto create
if "%choice%"=="2" goto run
if "%choice%"=="3" goto list
if "%choice%"=="4" goto delete
if "%choice%"=="5" goto edit
if "%choice%"=="6" exit /b

goto menu

:create
set /p macroname="Enter macro name: "
set macrofile=%~dp0macros\%macroname%.bat

if not exist "%~dp0macros" mkdir "%~dp0macros"

echo.
echo Enter commands (one per line, type 'END' to finish):
echo @echo off > "%macrofile%"
echo REM Macro: %macroname% >> "%macrofile%"
echo. >> "%macrofile%"

:inputcommands
set /p cmd="Command: "
if /i "%cmd%"=="END" goto createdone
echo %cmd% >> "%macrofile%"
goto inputcommands

:createdone
echo pause >> "%macrofile%"
echo.
echo Macro '%macroname%' created!
pause
goto menu

:run
call :list
set /p macroname="Enter macro name to run: "
if exist "%~dp0macros\%macroname%.bat" (
    call "%~dp0macros\%macroname%.bat"
) else (
    echo Macro not found!
    pause
)
goto menu

:list
echo.
echo Saved Macros:
if exist "%~dp0macros" (
    dir /b "%~dp0macros\*.bat"
) else (
    echo No macros found.
)
echo.
pause
goto menu

:delete
call :list
set /p macroname="Enter macro name to delete: "
if exist "%~dp0macros\%macroname%.bat" (
    del "%~dp0macros\%macroname%.bat"
    echo Macro deleted!
) else (
    echo Macro not found!
)
pause
goto menu

:edit
call :list
set /p macroname="Enter macro name to edit: "
if exist "%~dp0macros\%macroname%.bat" (
    notepad "%~dp0macros\%macroname%.bat"
) else (
    echo Macro not found!
    pause
)
goto menu
