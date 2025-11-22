@echo off
REM ========================================
REM File Operations Batch Script
REM Handles creating, deleting, and editing files
REM ========================================

setlocal enabledelayedexpansion

REM Get the operation type
set "OPERATION=%~1"

if "%OPERATION%"=="" (
    echo Error: No operation specified
    echo Usage: file_operations.bat [create^|delete^|edit^|append] [filepath] [content]
    exit /b 1
)

if "%OPERATION%"=="create" goto CREATE_FILE
if "%OPERATION%"=="delete" goto DELETE_FILE
if "%OPERATION%"=="edit" goto EDIT_FILE
if "%OPERATION%"=="append" goto APPEND_FILE
if "%OPERATION%"=="read" goto READ_FILE

echo Error: Unknown operation: %OPERATION%
exit /b 1

:CREATE_FILE
REM Create a new file with optional content
set "FILEPATH=%~2"
set "CONTENT=%~3"

if "%FILEPATH%"=="" (
    echo Error: No file path specified
    exit /b 1
)

REM Create parent directory if it doesn't exist
for %%F in ("%FILEPATH%") do set "PARENTDIR=%%~dpF"
if not exist "%PARENTDIR%" (
    mkdir "%PARENTDIR%" 2>nul
)

REM Create the file
if "%CONTENT%"=="" (
    REM Create empty file
    type nul > "%FILEPATH%"
    if exist "%FILEPATH%" (
        echo SUCCESS: File created: %FILEPATH%
        exit /b 0
    ) else (
        echo ERROR: Failed to create file
        exit /b 1
    )
) else (
    REM Create file with content
    echo %CONTENT%> "%FILEPATH%"
    if exist "%FILEPATH%" (
        echo SUCCESS: File created with content: %FILEPATH%
        exit /b 0
    ) else (
        echo ERROR: Failed to create file
        exit /b 1
    )
)

:DELETE_FILE
REM Delete a file
set "FILEPATH=%~2"

if "%FILEPATH%"=="" (
    echo Error: No file path specified
    exit /b 1
)

if not exist "%FILEPATH%" (
    echo ERROR: File does not exist: %FILEPATH%
    exit /b 1
)

del "%FILEPATH%" 2>nul
if not exist "%FILEPATH%" (
    echo SUCCESS: File deleted: %FILEPATH%
    exit /b 0
) else (
    echo ERROR: Failed to delete file
    exit /b 1
)

:EDIT_FILE
REM Edit/overwrite file content
set "FILEPATH=%~2"
set "CONTENT=%~3"

if "%FILEPATH%"=="" (
    echo Error: No file path specified
    exit /b 1
)

if "%CONTENT%"=="" (
    echo Error: No content specified
    exit /b 1
)

REM Create parent directory if it doesn't exist
for %%F in ("%FILEPATH%") do set "PARENTDIR=%%~dpF"
if not exist "%PARENTDIR%" (
    mkdir "%PARENTDIR%" 2>nul
)

REM Overwrite file with new content
echo %CONTENT%> "%FILEPATH%"
if exist "%FILEPATH%" (
    echo SUCCESS: File edited: %FILEPATH%
    exit /b 0
) else (
    echo ERROR: Failed to edit file
    exit /b 1
)

:APPEND_FILE
REM Append content to existing file
set "FILEPATH=%~2"
set "CONTENT=%~3"

if "%FILEPATH%"=="" (
    echo Error: No file path specified
    exit /b 1
)

if "%CONTENT%"=="" (
    echo Error: No content specified
    exit /b 1
)

REM Create file if it doesn't exist
if not exist "%FILEPATH%" (
    for %%F in ("%FILEPATH%") do set "PARENTDIR=%%~dpF"
    if not exist "!PARENTDIR!" (
        mkdir "!PARENTDIR!" 2>nul
    )
    type nul > "%FILEPATH%"
)

REM Append content
echo %CONTENT%>> "%FILEPATH%"
echo SUCCESS: Content appended to: %FILEPATH%
exit /b 0

:READ_FILE
REM Read and display file content
set "FILEPATH=%~2"

if "%FILEPATH%"=="" (
    echo Error: No file path specified
    exit /b 1
)

if not exist "%FILEPATH%" (
    echo ERROR: File does not exist: %FILEPATH%
    exit /b 1
)

echo SUCCESS: File content:
type "%FILEPATH%"
exit /b 0

endlocal
