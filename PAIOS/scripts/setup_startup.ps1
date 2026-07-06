# PAIOS Windows Startup Setup Script
# Run this once as Administrator to register PAIOS as a startup task.
# Usage: .\scripts\setup_startup.ps1

$ProjectDir = "C:\Users\subra\Documents\GitHub\Subramanya-Sharma\PAIOS"
$VenvPython = "$ProjectDir\venv\Scripts\python.exe"
$StartupScript = "$ProjectDir\main.py"
$DashboardScript = "$ProjectDir\dashboard\app.py"
$LogFile = "$ProjectDir\logs\startup.log"

Write-Host "🧠 Setting up PAIOS Windows Startup Tasks..." -ForegroundColor Cyan

# Create logs directory
New-Item -ItemType Directory -Force -Path "$ProjectDir\logs" | Out-Null

# Task 1: Start PAIOS background agents on boot
$BackendAction = New-ScheduledTaskAction `
    -Execute $VenvPython `
    -Argument $StartupScript `
    -WorkingDirectory $ProjectDir

$Trigger = New-ScheduledTaskTrigger -AtLogon
$Settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopOnIdleEnd `
    -ExecutionTimeLimit (New-TimeSpan -Hours 24)

Register-ScheduledTask `
    -TaskName "PAIOS_Backend" `
    -Action $BackendAction `
    -Trigger $Trigger `
    -Settings $Settings `
    -RunLevel Highest `
    -Force

Write-Host "✅ Backend task registered: PAIOS_Backend" -ForegroundColor Green

# Task 2: Launch Dashboard 60 seconds after login
$DashboardAction = New-ScheduledTaskAction `
    -Execute $VenvPython `
    -Argument "-m streamlit run `"$DashboardScript`" --server.port 8501 --server.headless true" `
    -WorkingDirectory $ProjectDir

$DashboardTrigger = New-ScheduledTaskTrigger -AtLogon
# 60 second delay via trigger settings
$DashboardSettings = New-ScheduledTaskSettingsSet -StartWhenAvailable
$DashboardTrigger.Delay = "PT60S"

Register-ScheduledTask `
    -TaskName "PAIOS_Dashboard" `
    -Action $DashboardAction `
    -Trigger $DashboardTrigger `
    -Settings $DashboardSettings `
    -RunLevel Highest `
    -Force

Write-Host "✅ Dashboard task registered: PAIOS_Dashboard" -ForegroundColor Green

# Open dashboard in browser after startup
$BrowserAction = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c timeout 90 && start http://localhost:8501"

$BrowserTrigger = New-ScheduledTaskTrigger -AtLogon
$BrowserTrigger.Delay = "PT90S"

Register-ScheduledTask `
    -TaskName "PAIOS_OpenBrowser" `
    -Action $BrowserAction `
    -Trigger $BrowserTrigger `
    -RunLevel Limited `
    -Force

Write-Host "✅ Browser auto-open task registered" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 PAIOS will auto-start on next login!" -ForegroundColor Cyan
Write-Host "   Dashboard: http://localhost:8501" -ForegroundColor Yellow
