@echo off
echo ================================================
echo Socket Error Detection Project - Environment Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the project:
echo   1. Start Server: python server\server.py
echo   2. Start Client 2 (Receiver): python client2\client2.py
echo   3. Start Client 1 (Sender): python client1\client1.py
echo.
pause
