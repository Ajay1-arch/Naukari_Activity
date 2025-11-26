@echo off
REM Naukri Automation - Scheduler (runs continuously)
REM Frequency: 1.5 hours with ±15 minutes random variance
REM Progress tracked in logs/progress.json

setlocal enabledelayedexpansion

REM Change to script directory
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════╗
echo ║  NAUKRI AUTOMATION SCHEDULER STARTED   ║
echo ║  Frequency: 1.5 hours (with variance)  ║
echo ║  Progress: logs/progress.json          ║
echo ║  Logs: logs/naukri.log                 ║
echo ╚════════════════════════════════════════╝
echo.
echo Tip: To view progress, run: view_progress.bat
echo Tip: Press Ctrl+C to stop the scheduler
echo.

REM Run the scheduler
python src\scheduler.py

