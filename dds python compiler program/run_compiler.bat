@echo off
echo Starting Python Script Compiler by dds...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Run the compiler application
python python_compiler.py

REM If there was an error, pause to show the message
if errorlevel 1 (
    echo.
    echo An error occurred while running the compiler.
    pause
) 