@echo off
REM SmartView MCP Server Installation Script (Windows)

echo Installing Equinix SmartView MCP Server v2.0
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.10 or higher.
    exit /b 1
)

echo Python detected
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Add your OAuth credentials to .env
echo 3. Configure Claude Desktop
echo.
echo To activate the virtual environment:
echo   venv\Scripts\activate.bat
echo.
pause
