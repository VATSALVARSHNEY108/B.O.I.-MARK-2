# AI Phone Link Controller Launcher (PowerShell)
# Alternative launcher for PowerShell users

Write-Host ""
Write-Host "========================================"  -ForegroundColor Green
Write-Host " AI PHONE LINK CONTROLLER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Starting AI-powered phone control..." -ForegroundColor Yellow
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "  Please install Python from python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Run the AI Phone Link Controller
python ai_phone_link_controller.py

# Check exit code
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "✗ ERROR: The program encountered an error" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
