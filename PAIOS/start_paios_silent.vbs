' PAIOS Silent Launcher
' This VBScript wrapper launches start_paios.bat with NO visible window at all.
' Place the shortcut to THIS file in the Windows Startup folder.

Dim oShell
Set oShell = CreateObject("WScript.Shell")
oShell.Run """C:\Users\subra\Documents\GitHub\Subramanya-Sharma\PAIOS\start_paios.bat""", 0, False
Set oShell = Nothing
