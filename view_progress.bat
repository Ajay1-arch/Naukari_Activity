@echo off
REM View Scheduler Progress Dashboard

echo.
echo Checking if scheduler is running...
tasklist | find /i "python.exe" > nul

if errorlevel 1 (
    echo ⚠️  Scheduler is not currently running
) else (
    echo ✓ Scheduler is running
)

echo.
echo Starting Progress Dashboard...
echo.

python view_progress.py

pause
