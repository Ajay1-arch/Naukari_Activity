@echo off
REM Naukri Automation - Single Run
REM Run this manually or schedule it with Windows Task Scheduler

setlocal enabledelayedexpansion

REM Change to script directory
cd /d "%~dp0"

REM Run the main script
python src\naukri_main.py

pause
