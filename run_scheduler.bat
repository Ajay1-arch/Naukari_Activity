@echo off
REM Naukri Automation - Scheduler (runs continuously)
REM This will run the script at scheduled intervals (hourly or random times)

setlocal enabledelayedexpansion

REM Change to script directory
cd /d "%~dp0"

REM Run the scheduler
python src\scheduler.py
