@echo off
REM ============================================================
REM WhatsApp Batch Automation System
REM Send WhatsApp messages to multiple contacts from CSV files
REM ============================================================

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."
set "PYTHON_SCRIPT=%PROJECT_ROOT%\scripts\whatsapp_batch.py"
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
echo %GREEN%            📱 WHATSAPP BATCH AUTOMATION SYSTEM              %RESET%
echo %BLUE%================================================================%RESET%
echo.
echo  %CYAN%BATCH OPERATIONS:%RESET%
echo  1. Send Batch Messages from CSV
echo  2. Send Batch Messages with Template
echo  3. Send Batch Images
echo  4. Create CSV Template
echo.
echo  %CYAN%MANAGEMENT:%RESET%
echo  5. View Batch Logs
echo  6. View Available Templates
echo  7. Open Data Folder
echo.
echo  %CYAN%HELP:%RESET%
echo  8. Quick Start Guide
echo  9. View Example Templates
echo  0. Exit
echo.
echo %BLUE%================================================================%RESET%
echo.

set /p choice="Select option (0-9): "

if "%choice%"=="1" goto BATCH_SEND
if "%choice%"=="2" goto BATCH_SEND_TEMPLATE
if "%choice%"=="3" goto BATCH_IMAGES
if "%choice%"=="4" goto CREATE_TEMPLATE
if "%choice%"=="5" goto VIEW_LOGS
if "%choice%"=="6" goto VIEW_TEMPLATES
if "%choice%"=="7" goto OPEN_DATA_FOLDER
if "%choice%"=="8" goto QUICK_START
if "%choice%"=="9" goto VIEW_EXAMPLES
if "%choice%"=="0" goto END

echo %RED%Invalid option!%RESET%
timeout /t 2 >nul
goto MENU

:BATCH_SEND
cls
echo.
echo %GREEN%=== Send Batch Messages from CSV ===%RESET%
echo.
echo %YELLOW%Your CSV should have columns: phone, name, message%RESET%
echo %YELLOW%Example: +1234567890,John Doe,Hello John!%RESET%
echo.
set /p csv_file="Enter CSV file path (or press Enter for sample): "

if "%csv_file%"=="" (
    set "csv_file=%DATA_DIR%\whatsapp_batch_template_basic.csv"
    echo %CYAN%Using sample file: %csv_file%%RESET%
)

if not exist "%csv_file%" (
    echo %RED%Error: CSV file not found!%RESET%
    echo %YELLOW%Tip: Use option 4 to create a template first%RESET%
    pause
    goto MENU
)

echo.
set /p delay="Enter delay between messages in seconds (default: 20): "
if "%delay%"=="" set delay=20

echo.
echo %YELLOW%Starting batch send...%RESET%
echo %YELLOW%This may take a while depending on the number of contacts.%RESET%
echo.
python "%PYTHON_SCRIPT%" send "%csv_file%" --delay %delay%
echo.
pause
goto MENU

:BATCH_SEND_TEMPLATE
cls
echo.
echo %GREEN%=== Send Batch Messages with Template ===%RESET%
echo.
echo %YELLOW%Your CSV should have columns matching template placeholders%RESET%
echo %YELLOW%Example CSV: phone,name,order_id,amount%RESET%
echo %YELLOW%Example Template: Hi {name}, your order {order_id} for {amount} is ready!%RESET%
echo.
set /p csv_file="Enter CSV file path (or press Enter for sample): "

if "%csv_file%"=="" (
    set "csv_file=%DATA_DIR%\whatsapp_batch_template_personalized.csv"
    echo %CYAN%Using sample file: %csv_file%%RESET%
)

if not exist "%csv_file%" (
    echo %RED%Error: CSV file not found!%RESET%
    pause
    goto MENU
)

echo.
echo %YELLOW%Enter your message template (use {placeholder} for CSV columns):%RESET%
echo %CYAN%Example: Hi {name}, your {product} plan for {amount} is active!%RESET%
echo.
set /p template="Template: "

if "%template%"=="" (
    echo %RED%Template cannot be empty!%RESET%
    pause
    goto MENU
)

echo.
set /p delay="Enter delay between messages in seconds (default: 20): "
if "%delay%"=="" set delay=20

echo.
echo %YELLOW%Starting batch send with template...%RESET%
echo.
python "%PYTHON_SCRIPT%" send "%csv_file%" --template "%template%" --delay %delay%
echo.
pause
goto MENU

:BATCH_IMAGES
cls
echo.
echo %GREEN%=== Send Batch Images ===%RESET%
echo.
echo %YELLOW%Your CSV should have columns: phone, name, caption (optional)%RESET%
echo.
set /p csv_file="Enter CSV file path (or press Enter for sample): "

if "%csv_file%"=="" (
    set "csv_file=%DATA_DIR%\whatsapp_batch_template_image.csv"
    echo %CYAN%Using sample file: %csv_file%%RESET%
)

if not exist "%csv_file%" (
    echo %RED%Error: CSV file not found!%RESET%
    pause
    goto MENU
)

echo.
set /p image_path="Enter image file path (JPG only): "

if "%image_path%"=="" (
    echo %RED%Image path cannot be empty!%RESET%
    pause
    goto MENU
)

if not exist "%image_path%" (
    echo %RED%Error: Image file not found!%RESET%
    pause
    goto MENU
)

echo.
echo %YELLOW%Enter caption template (optional, use {placeholder} for CSV columns):%RESET%
echo %CYAN%Example: Hi {name}! Check this out!%RESET%
echo %YELLOW%Or press Enter to skip%RESET%
echo.
set /p caption=""

echo.
set /p delay="Enter delay between messages in seconds (default: 25): "
if "%delay%"=="" set delay=25

echo.
echo %YELLOW%Starting batch image send...%RESET%
echo.
if "%caption%"=="" (
    python "%PYTHON_SCRIPT%" image "%csv_file%" "%image_path%" --delay %delay%
) else (
    python "%PYTHON_SCRIPT%" image "%csv_file%" "%image_path%" --caption "%caption%" --delay %delay%
)
echo.
pause
goto MENU

:CREATE_TEMPLATE
cls
echo.
echo %GREEN%=== Create CSV Template ===%RESET%
echo.
echo  1. Basic Template (phone, name, message)
echo  2. Personalized Template (phone, name, company, product, amount)
echo  3. Image Template (phone, name, caption)
echo.
set /p template_type="Select template type (1-3): "

if "%template_type%"=="1" set type_name=basic
if "%template_type%"=="2" set type_name=personalized
if "%template_type%"=="3" set type_name=image

if "%type_name%"=="" (
    echo %RED%Invalid template type!%RESET%
    pause
    goto MENU
)

echo.
set /p output_file="Enter output file name (e.g., my_contacts.csv): "

if "%output_file%"=="" (
    echo %RED%Filename cannot be empty!%RESET%
    pause
    goto MENU
)

REM Add .csv extension if not present
echo %output_file% | find ".csv" >nul
if errorlevel 1 set "output_file=%output_file%.csv"

set "full_path=%DATA_DIR%\%output_file%"

echo.
echo %YELLOW%Creating template...%RESET%
python "%PYTHON_SCRIPT%" create-template "%full_path%" --type %type_name%
echo.
echo %GREEN%Template created at: %full_path%%RESET%
echo %YELLOW%You can now edit this file with your contacts and messages.%RESET%
echo.
pause
goto MENU

:VIEW_LOGS
cls
echo.
echo %GREEN%=== Batch Messaging Logs ===%RESET%
echo.
set /p limit="Enter number of recent logs to show (default: 20): "
if "%limit%"=="" set limit=20

echo.
python "%PYTHON_SCRIPT%" logs --limit %limit%
echo.
pause
goto MENU

:VIEW_TEMPLATES
cls
echo.
echo %GREEN%=== Available Message Templates ===%RESET%
echo.

set "templates_file=%DATA_DIR%\whatsapp_message_templates.txt"
if exist "%templates_file%" (
    type "%templates_file%"
) else (
    echo %YELLOW%No templates file found.%RESET%
    echo %CYAN%Template file should be at: %templates_file%%RESET%
)

echo.
pause
goto MENU

:OPEN_DATA_FOLDER
cls
echo.
echo %GREEN%Opening data folder...%RESET%
echo %CYAN%%DATA_DIR%%RESET%
echo.
start "" "%DATA_DIR%"
timeout /t 2 >nul
goto MENU

:QUICK_START
cls
echo.
echo %BLUE%================================================================%RESET%
echo %GREEN%            QUICK START GUIDE                                %RESET%
echo %BLUE%================================================================%RESET%
echo.
echo %YELLOW%Step 1: Create a CSV Template%RESET%
echo   Use option 4 to create a template CSV file
echo   This will create a sample file with the correct format
echo.
echo %YELLOW%Step 2: Edit the CSV File%RESET%
echo   Open the CSV file in Excel or any text editor
echo   Add your contacts' phone numbers (with country code)
echo   Add names and messages
echo.
echo %YELLOW%Step 3: Send Batch Messages%RESET%
echo   Use option 1 for basic sending (CSV has messages)
echo   Use option 2 for template-based sending (dynamic messages)
echo   Use option 3 for sending images
echo.
echo %YELLOW%Important Notes:%RESET%
echo   - Phone numbers MUST include country code: +1234567890
echo   - Recommended delay: 20-25 seconds between messages
echo   - WhatsApp Web must be logged in on your browser
echo   - Don't send too many messages per day (max ~250)
echo.
echo %YELLOW%Template Placeholders:%RESET%
echo   Use {placeholder} in templates that match CSV column names
echo   Example CSV: phone,name,order_id
echo   Example Template: Hi {name}, order {order_id} is ready!
echo.
echo %BLUE%================================================================%RESET%
echo.
pause
goto MENU

:VIEW_EXAMPLES
cls
echo.
echo %BLUE%================================================================%RESET%
echo %GREEN%            EXAMPLE TEMPLATES                                %RESET%
echo %BLUE%================================================================%RESET%
echo.
echo %YELLOW%Example 1: Order Confirmation%RESET%
echo CSV columns: phone,name,order_id,delivery_date
echo Template: Hi {name}, order #{order_id} confirmed! Delivery: {delivery_date}
echo.
echo %YELLOW%Example 2: Appointment Reminder%RESET%
echo CSV columns: phone,name,date,time,location
echo Template: Hello {name}, reminder for {date} at {time}. Location: {location}
echo.
echo %YELLOW%Example 3: Discount Offer%RESET%
echo CSV columns: phone,name,product,discount,code
echo Template: Hi {name}! {discount}%% off on {product}. Code: {code}
echo.
echo %YELLOW%Example 4: Birthday Wishes%RESET%
echo CSV columns: phone,name
echo Template: Happy Birthday {name}! Wishing you an amazing year ahead!
echo.
echo %YELLOW%Example 5: Payment Reminder%RESET%
echo CSV columns: phone,name,amount,due_date,service
echo Template: Dear {name}, payment of {amount} for {service} due on {due_date}
echo.
echo %BLUE%================================================================%RESET%
echo.
pause
goto MENU

:END
echo.
echo %GREEN%Thank you for using WhatsApp Batch Automation System!%RESET%
echo.
timeout /t 2 >nul
exit /b 0
