# Naukri Automation - Windows Setup Script
# Run this script to automatically set up the project

param(
    [switch]$SkipSetup,
    [switch]$SkipScheduler,
    [switch]$TestOnly
)

Write-Host "=" * 70
Write-Host "NAUKRI AUTOMATION - WINDOWS SETUP" -ForegroundColor Cyan
Write-Host "=" * 70

# Get project root
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Step 1: Verify structure
Write-Host "`n[1/5] Verifying project structure..." -ForegroundColor Yellow
try {
    python "$projectRoot\verify_setup.py"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Project structure incomplete" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Python not found or verify_setup.py failed" -ForegroundColor Red
    exit 1
}

# Step 2: Install requirements
Write-Host "`n[2/5] Installing dependencies..." -ForegroundColor Yellow
pip install -r "$projectRoot\requirements.txt"
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Step 3: Setup secrets
if (-not $SkipSetup) {
    Write-Host "`n[3/5] Setting up credentials..." -ForegroundColor Yellow
    python "$projectRoot\setup.py"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Setup failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Setup complete" -ForegroundColor Green
} else {
    Write-Host "`n[3/5] Skipping setup (--SkipSetup)" -ForegroundColor Yellow
}

# Step 4: Test run
if ($TestOnly) {
    Write-Host "`n[4/5] Testing script (test mode)..." -ForegroundColor Yellow
    python "$projectRoot\src\naukri_main.py"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Test run successful" -ForegroundColor Green
    } else {
        Write-Host "✗ Test run failed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "`n[4/5] Skipping test run (use --TestOnly to test)" -ForegroundColor Yellow
}

# Step 5: Schedule task
if (-not $SkipScheduler) {
    Write-Host "`n[5/5] Setting up Windows Task Scheduler..." -ForegroundColor Yellow
    
    $taskName = "Naukri Automation Hourly"
    $pythonPath = (python -c "import sys; print(sys.executable)")
    $scriptPath = Join-Path $projectRoot "src\naukri_main.py"
    $taskExists = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    
    if ($taskExists) {
        Write-Host "Task '$taskName' already exists. Skipping..."
    } else {
        try {
            # Create trigger (every hour)
            $trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 1) -At (Get-Date) -Once
            
            # Create action
            $action = New-ScheduledTaskAction `
                -Execute $pythonPath `
                -Argument $scriptPath `
                -WorkingDirectory $projectRoot
            
            # Register task
            Register-ScheduledTask `
                -TaskName $taskName `
                -Trigger $trigger `
                -Action $action `
                -RunLevel Highest `
                -Force | Out-Null
            
            Write-Host "✓ Task scheduled: $taskName (runs every hour)" -ForegroundColor Green
        } catch {
            Write-Host "✗ Failed to schedule task: $_" -ForegroundColor Red
            Write-Host "  You can manually create a task in Task Scheduler" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "`n[5/5] Skipping scheduler setup (--SkipScheduler)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n" + "=" * 70 -ForegroundColor Cyan
Write-Host "✓ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=" * 70

Write-Host "`nYour Naukri automation is ready!" -ForegroundColor Green
Write-Host "`nQuick commands:"
Write-Host "  Run once:      python src\naukri_main.py"
Write-Host "  Run scheduler: python src\scheduler.py"
Write-Host "  Check logs:    Get-Content logs\naukri.log -Tail 20"
Write-Host "  View config:   notepad config\config.ini"
Write-Host "`nScheduled task: 'Naukri Automation Hourly' (Task Scheduler)" -ForegroundColor Cyan

Write-Host "`nNext steps:"
Write-Host "1. Monitor first run in Task Scheduler"
Write-Host "2. Check logs/naukri.log for results"
Write-Host "3. Customize headlines in src/naukri_main.py"
Write-Host "4. Push to GitHub when ready"

Write-Host "`n" + "=" * 70
