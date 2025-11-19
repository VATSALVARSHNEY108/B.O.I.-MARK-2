@echo off
REM ============================================================
REM WhatsApp Contact Manager
REM Manage contacts for easy messaging by name
REM ============================================================

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."
set "PYTHON_SCRIPT=%PROJECT_ROOT%\scripts\whatsapp_contact_manager.py"
set "DATA_DIR=%PROJECT_ROOT%\data"

REM Color definitions
set "GREEN=[92m"
set "BLUE=[94m"
set "YELLOW=[93m"
set "RED=[91m"
set "CYAN=[96m"
set "RESET=[0m"

:MENU
cls
echo.
echo %BLUE%================================================================%RESET%
echo %GREEN%            📇 WHATSAPP CONTACT MANAGER                       %RESET%
echo %BLUE%================================================================%RESET%
echo.
echo  %CYAN%CONTACT MANAGEMENT:%RESET%
echo  1. Add New Contact
echo  2. Edit Contact
echo  3. Rename Contact
echo  4. Delete Contact
echo  5. List All Contacts
echo  6. Search Contacts
echo.
echo  %CYAN%BATCH OPERATIONS:%RESET%
echo  7. Import Contacts from CSV
echo  8. Export Contacts to CSV
echo  9. Create Batch CSV from Contacts
echo.
echo  %CYAN%QUICK ACTIONS:%RESET%
echo  10. Quick Message by Name
echo  11. Contact Statistics
echo  12. Help / Guide
echo  0. Exit
echo.
echo %BLUE%================================================================%RESET%
echo.

set /p choice="Select option (0-12): "

if "%choice%"=="1" goto ADD_CONTACT
if "%choice%"=="2" goto EDIT_CONTACT
if "%choice%"=="3" goto RENAME_CONTACT
if "%choice%"=="4" goto DELETE_CONTACT
if "%choice%"=="5" goto LIST_CONTACTS
if "%choice%"=="6" goto SEARCH_CONTACTS
if "%choice%"=="7" goto IMPORT_CSV
if "%choice%"=="8" goto EXPORT_CSV
if "%choice%"=="9" goto CREATE_BATCH_CSV
if "%choice%"=="10" goto QUICK_MESSAGE
if "%choice%"=="11" goto STATS
if "%choice%"=="12" goto HELP
if "%choice%"=="0" goto END

echo %RED%Invalid option!%RESET%
timeout /t 2 >nul
goto MENU

:ADD_CONTACT
cls
echo.
echo %GREEN%=== Add New Contact ===%RESET%
echo.
set /p name="Enter contact name: "
echo.
set /p phone="Enter phone number (with country code, e.g., +1234567890): "
echo.
set /p email="Enter email (optional): "
echo.
set /p notes="Enter notes (optional): "
echo.
echo %YELLOW%Adding contact...%RESET%
python "%PYTHON_SCRIPT%" add "%name%" "%phone%" --email "%email%" --notes "%notes%"
echo.
pause
goto MENU

:EDIT_CONTACT
cls
echo.
echo %GREEN%=== Edit Contact ===%RESET%
echo.
set /p name="Enter contact name to edit: "
echo.
echo %YELLOW%Leave blank to skip a field%RESET%
echo.
set /p phone="New phone number: "
set /p email="New email: "
set /p notes="New notes: "
echo.
echo %YELLOW%Updating contact...%RESET%

set "cmd=python "%PYTHON_SCRIPT%" edit "%name%""
if not "%phone%"=="" set "cmd=!cmd! --phone "%phone%""
if not "%email%"=="" set "cmd=!cmd! --email "%email%""
if not "%notes%"=="" set "cmd=!cmd! --notes "%notes%""

%cmd%
echo.
pause
goto MENU

:RENAME_CONTACT
cls
echo.
echo %GREEN%=== Rename Contact ===%RESET%
echo.
set /p old_name="Current contact name: "
echo.
set /p new_name="New contact name: "
echo.
echo %YELLOW%Renaming contact...%RESET%
python "%PYTHON_SCRIPT%" rename "%old_name%" "%new_name%"
echo.
pause
goto MENU

:DELETE_CONTACT
cls
echo.
echo %GREEN%=== Delete Contact ===%RESET%
echo.
set /p name="Enter contact name to delete: "
echo.
echo %RED%WARNING: This will permanently delete the contact!%RESET%
echo.
python "%PYTHON_SCRIPT%" delete "%name%"
echo.
pause
goto MENU

:LIST_CONTACTS
cls
echo.
echo %GREEN%=== All Contacts ===%RESET%
echo.
python "%PYTHON_SCRIPT%" list
echo.
pause
goto MENU

:SEARCH_CONTACTS
cls
echo.
echo %GREEN%=== Search Contacts ===%RESET%
echo.
set /p query="Enter search query (name, phone, or email): "
echo.
python "%PYTHON_SCRIPT%" search "%query%"
echo.
pause
goto MENU

:IMPORT_CSV
cls
echo.
echo %GREEN%=== Import Contacts from CSV ===%RESET%
echo.
echo %YELLOW%CSV should have columns: name, phone, email, notes%RESET%
echo.
set /p csv_file="Enter CSV file path: "
echo.
if not exist "%csv_file%" (
    echo %RED%File not found!%RESET%
    pause
    goto MENU
)
echo %YELLOW%Importing contacts...%RESET%
python "%PYTHON_SCRIPT%" import "%csv_file%"
echo.
pause
goto MENU

:EXPORT_CSV
cls
echo.
echo %GREEN%=== Export Contacts to CSV ===%RESET%
echo.
set /p csv_file="Enter output CSV file path: "
echo.
echo %YELLOW%Exporting contacts...%RESET%
python "%PYTHON_SCRIPT%" export "%csv_file%"
echo.
echo %GREEN%Contacts exported! You can now use this CSV for batch messaging.%RESET%
echo.
pause
goto MENU

:CREATE_BATCH_CSV
cls
echo.
echo %GREEN%=== Create Batch CSV from Contacts ===%RESET%
echo.
echo  1. All Contacts
echo  2. Specific Contacts
echo.
set /p batch_choice="Select option (1-2): "

set /p output_file="Enter output CSV file name: "

REM Add .csv extension if not present
echo %output_file% | find ".csv" >nul
if errorlevel 1 set "output_file=%output_file%.csv"

set "full_path=%DATA_DIR%\%output_file%"

if "%batch_choice%"=="1" (
    echo.
    echo %YELLOW%Creating batch CSV with all contacts...%RESET%
    python "%PYTHON_SCRIPT%" create-batch "%full_path%"
) else if "%batch_choice%"=="2" (
    echo.
    echo %YELLOW%Enter contact names separated by spaces (e.g., John Jane Bob):%RESET%
    set /p names=""
    echo.
    echo %YELLOW%Creating batch CSV with selected contacts...%RESET%
    python "%PYTHON_SCRIPT%" create-batch "%full_path%" --names %names%
) else (
    echo %RED%Invalid option!%RESET%
    timeout /t 2 >nul
    goto CREATE_BATCH_CSV
)

echo.
echo %GREEN%Batch CSV created! Use it with WhatsApp Batch Automation.%RESET%
echo.
pause
goto MENU

:QUICK_MESSAGE
cls
echo.
echo %GREEN%=== Quick Message by Name ===%RESET%
echo.
set /p name="Enter contact name: "
echo.
set /p message="Enter message: "
echo.
echo %YELLOW%Looking up contact and sending message...%RESET%
echo.

REM Use whatsapp_cli to send message (it supports contact names)
python "%PROJECT_ROOT%\scripts\whatsapp_cli.py" send "%name%" "%message%"

echo.
pause
goto MENU

:STATS
cls
echo.
echo %GREEN%=== Contact Statistics ===%RESET%
echo.
python "%PYTHON_SCRIPT%" stats
echo.
pause
goto MENU

:HELP
cls
echo.
echo %BLUE%================================================================%RESET%
echo %GREEN%            WHATSAPP CONTACT MANAGER GUIDE                   %RESET%
echo %BLUE%================================================================%RESET%
echo.
echo %YELLOW%Adding Contacts:%RESET%
echo   - Add contacts with name, phone, email, and notes
echo   - Phone numbers MUST include country code (e.g., +1234567890)
echo   - Names can be anything (e.g., "Mom", "John Smith", "Office")
echo.
echo %YELLOW%Using Contacts:%RESET%
echo   - Message contacts by name instead of phone numbers
echo   - Search contacts by name, phone, or email
echo   - Export contacts to CSV for batch messaging
echo.
echo %YELLOW%Batch Operations:%RESET%
echo   - Import multiple contacts from CSV file
echo   - Export all contacts to CSV
echo   - Create batch CSV from selected contacts
echo.
echo %YELLOW%Quick Messaging:%RESET%
echo   - Option 10: Send quick message by contact name
echo   - No need to remember phone numbers!
echo   - Works with all WhatsApp automation tools
echo.
echo %YELLOW%CSV Format for Import:%RESET%
echo   name,phone,email,notes
echo   John Doe,+1234567890,john@email.com,Friend from school
echo   Jane Smith,+0987654321,jane@email.com,Work colleague
echo.
echo %BLUE%================================================================%RESET%
echo.
pause
goto MENU

:END
echo.
echo %GREEN%Thank you for using WhatsApp Contact Manager!%RESET%
echo.
timeout /t 2 >nul
exit /b 0
