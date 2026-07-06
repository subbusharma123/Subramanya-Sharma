# Creates a Windows Startup shortcut for PAIOS — run this once
$WshShell = New-Object -ComObject WScript.Shell
$StartupFolder = [System.Environment]::GetFolderPath('Startup')
$ShortcutPath = Join-Path $StartupFolder 'PAIOS.lnk'
$VbsPath = 'C:\Users\subra\Documents\GitHub\Subramanya-Sharma\PAIOS\start_paios_silent.vbs'

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = 'wscript.exe'
$Shortcut.Arguments = "`"$VbsPath`""
$Shortcut.WorkingDirectory = 'C:\Users\subra\Documents\GitHub\Subramanya-Sharma\PAIOS'
$Shortcut.Description = 'PAIOS Personal AI Operating System'
$Shortcut.WindowStyle = 7
$Shortcut.Save()

Write-Host "✅ Startup shortcut created at: $ShortcutPath"
Write-Host "🚀 PAIOS will auto-start every time you log into Windows!"
