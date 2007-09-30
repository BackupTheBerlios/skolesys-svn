Set WshShell = WScript.CreateObject("WScript.Shell")
user_shell_folders = "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\"
WshShell.RegWrite user_shell_folders & "Personal" , "P:\Dokumenter", "REG_EXPAND_SZ"

' How to read from registry
' Dim WSHShell, RegKey, ScreenSaver
' Set WSHShell = CreateObject("WScript.Shell")
' desktop = WSHShell.RegRead(user_shell_folders & "Desktop")

' Get Desktop folder
strDesktop = WshShell.SpecialFolders("Desktop")

Set oWS = WScript.CreateObject("WScript.Shell")

sLinkFile = strDesktop & "\Dokumenter.LNK"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "P:\Dokumenter"
oLink.Description = "Dokumenter"
'    oLink.Arguments = ""
'    oLink.HotKey = "ALT+CTRL+F"
oLink.IconLocation = "\\mainserver\netlogon\folder_blue.ico, 0"
'    oLink.WindowStyle = "1"
'    oLink.WorkingDirectory = "C:\temp"
oLink.Save


sLinkFile = strDesktop & "\Grupper.LNK"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "P:\Grupper"
oLink.Description = "Grupper"
'    oLink.Arguments = ""
'    oLink.HotKey = "ALT+CTRL+F"
oLink.IconLocation = "\\mainserver\netlogon\folder_green.ico, 0"
'    oLink.WindowStyle = "1"
'    oLink.WorkingDirectory = "C:\temp"
oLink.Save

Set WshShell = Nothing
