# Start Naukri Scheduler with Progress Tracking
# This script starts the scheduler in the background and allows you to view progress

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SchedulerScript = Join-Path $ProjectRoot "src\scheduler.py"
$LogDir = Join-Path $ProjectRoot "logs"
$ProgressFile = Join-Path $LogDir "progress.json"

# Create logs directory if it doesn't exist
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

Write-Host ""
Write-Host "╔════════════════════════════════════════╗"
Write-Host "║  NAUKRI SCHEDULER - 1.5 Hour Frequency║"
Write-Host "║  With Random Timing & Progress Tracking║"
Write-Host "╚════════════════════════════════════════╝"
Write-Host ""

Write-Host "📊 Configuration:"
Write-Host "  • Frequency:   1.5 hours (90 minutes)"
Write-Host "  • Variance:    ±15 minutes (random timing)"
Write-Host "  • Progress:    Tracked in logs/progress.json"
Write-Host "  • Logs:        logs/naukri.log"
Write-Host ""

Write-Host "🔐 Checking credentials..."
$SecretsFile = Join-Path $ProjectRoot ".secrets\secrets.json"
if (-not (Test-Path $SecretsFile)) {
    Write-Host "❌ ERROR: Secrets file not found!"
    Write-Host ""
    Write-Host "Run setup.py first to configure your credentials:"
    Write-Host "  python setup.py"
    Write-Host ""
    pause
    exit 1
}
Write-Host "✓ Credentials found"
Write-Host ""

Write-Host "🚀 Starting scheduler..."
Write-Host ""

# Start the scheduler in a new window
Start-Process -NoNewWindow -FilePath "python" -ArgumentList $SchedulerScript -PassThru

Write-Host "✓ Scheduler started in background"
Write-Host ""
Write-Host "📈 To view progress:"
Write-Host "  • Run: view_progress.bat"
Write-Host "  • Or: python view_progress.py"
Write-Host ""
Write-Host "📝 To view detailed logs:"
Write-Host "  • Open: logs/naukri.log"
Write-Host ""
Write-Host "⏹️  To stop the scheduler:"
Write-Host "  • Press Ctrl+C in the scheduler window"
Write-Host "  • Or run: taskkill /IM python.exe"
Write-Host ""
Write-Host "Press any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
