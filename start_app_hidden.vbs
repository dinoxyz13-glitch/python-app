' AI writing tool launcher without a console window.
' Put a shortcut to this file in the Startup folder (shell:startup) to run it at sign-in.
' If the app is already running, it only opens the browser.
' Server output goes to streamlit.log in this folder. Use stop_app.bat to stop the app.
Option Explicit

Const APP_URL = "http://localhost:8501"
Const WAIT_SECONDS = 60

Dim fso, sh, i
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = fso.GetParentFolderName(WScript.ScriptFullName)

If Not IsRunning() Then
    ' 0 = hidden window. headless=true skips the first-run email prompt, which would wait forever while hidden.
    sh.Run "cmd /c set PYTHONIOENCODING=utf-8&& python -m streamlit run app.py --server.headless true > streamlit.log 2>&1", 0, False
    For i = 1 To WAIT_SECONDS
        WScript.Sleep 1000
        If IsRunning() Then Exit For
    Next
    If Not IsRunning() Then
        MsgBox "AI writing tool did not start within " & WAIT_SECONDS & " seconds." & vbCrLf & _
            "Open streamlit.log in the app folder to see the error, or run start_app.bat to see it on screen.", _
            vbExclamation, "AI writing tool"
        WScript.Quit 1
    End If
End If

sh.Run APP_URL, 1, False

Function IsRunning()
    Dim http
    IsRunning = False
    On Error Resume Next
    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    http.setTimeouts 1000, 1000, 1000, 1000
    http.Open "GET", APP_URL & "/_stcore/health", False
    http.Send
    If Err.Number = 0 Then
        If http.Status = 200 Then IsRunning = True
    End If
    Err.Clear
    On Error GoTo 0
End Function
