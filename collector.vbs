Dim objShell,objFSO,objFile

'
' This wrapper exists soley to make powershell run
' from the task scheduler without a window popping up.
' Tweaked from a blog post by Jeffrey Hicks.
' Call using wscript.exe
'

Set objShell=CreateObject("WScript.Shell")
Set objFSO=CreateObject("Scripting.FileSystemObject")

'enter the path for your PowerShell Script
strPath="C:\Users\James\projects\HearthstoneDebugLog\collector.ps1"

'verify file exists
If objFSO.FileExists(strPath) Then
'return short path name
    set objFile=objFSO.GetFile(strPath)
    strCMD="powershell -nologo -command " & Chr(34) & "&{" &_
     objFile.ShortPath & "}" & Chr(34) 
    'Uncomment next line for debugging
    'WScript.Echo strCMD
    
    'use 0 to hide window
    objShell.Run strCMD,0

Else

'Display error message
    WScript.Echo "Failed to find " & strPath
    WScript.Quit
    
End If