' ===================================================
' PLANTE UMA FLOR - Iniciar Servidor HTTPS Invisível
' Inicia o servidor Flask em HTTPS sem janela visível
' ===================================================

Option Explicit

Dim objShell, scriptDir, backendDir, pythonCmd, strCommand

' Criar objeto Shell
Set objShell = CreateObject("WScript.Shell")

' Obter diretório do script (backend/UtilsScripts)
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Obter diretório do backend (um nível acima)
backendDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(scriptDir)
objShell.CurrentDirectory = backendDir

' Verificar se certificados existem
Dim fso
Set fso = CreateObject("Scripting.FileSystemObject")

If Not fso.FileExists(backendDir & "\ssl\cert.pem") Or Not fso.FileExists(backendDir & "\ssl\key.pem") Then
    MsgBox "Certificados SSL não encontrados!" & vbCrLf & vbCrLf & _
           "Execute primeiro:" & vbCrLf & _
           "1. ssl\INSTALAR_MKCERT.bat" & vbCrLf & _
           "2. ssl\GERAR_CERTIFICADOS.bat", _
           vbCritical, "Plante Uma Flor - Erro"
    WScript.Quit 1
End If

' Tentar encontrar Python
pythonCmd = "python"

' Verificar se python está disponível
Dim result
result = objShell.Run("cmd /c where python > nul 2>&1", 0, True)

If result <> 0 Then
    ' Tentar py launcher
    result = objShell.Run("cmd /c where py > nul 2>&1", 0, True)
    If result = 0 Then
        pythonCmd = "py"
    Else
        MsgBox "Python não encontrado!" & vbCrLf & vbCrLf & _
               "Certifique-se de que o Python está instalado e no PATH.", _
               vbCritical, "Plante Uma Flor - Erro"
        WScript.Quit 1
    End If
End If

' Criar comando para iniciar o servidor com encoding UTF-8 e log
' Definir variáveis de ambiente para UTF-8
Dim logFile
logFile = backendDir & "\servidor_https.log"

' Comando com encoding UTF-8, sem reloader (mais estável) e redirecionamento de saída
strCommand = "cmd /c ""chcp 65001 >nul 2>&1 && cd /d """ & backendDir & """ && " & _
             "set PYTHONIOENCODING=utf-8 && " & _
             "set NO_RELOAD=true && " & _
             pythonCmd & " main.py --https --no-reload > """ & logFile & """ 2>&1"""

' Executar em modo oculto (0 = janela oculta, False = não esperar conclusão)
objShell.Run strCommand, 0, False

' Aguardar 5 segundos para o servidor iniciar completamente
WScript.Sleep 5000

' Verificar se o servidor realmente iniciou (verificando o log)
Dim objFSO2, objFile, strLogContent
Set objFSO2 = CreateObject("Scripting.FileSystemObject")

If objFSO2.FileExists(logFile) Then
    On Error Resume Next
    Set objFile = objFSO2.OpenTextFile(logFile, 1)
    strLogContent = objFile.ReadAll
    objFile.Close
    On Error GoTo 0
    
    ' Verificar se há indicação de erro no log
    If InStr(strLogContent, "Erro") > 0 Or InStr(strLogContent, "Error") > 0 Then
        MsgBox "Servidor iniciado mas pode haver problemas!" & vbCrLf & vbCrLf & _
               "Verifique o log para detalhes:" & vbCrLf & _
               "backend\servidor_https.log", _
               vbExclamation, "Plante Uma Flor - Aviso"
    Else
        ' Mostrar notificação de sucesso
        On Error Resume Next
        Dim objNotify
        Set objNotify = CreateObject("WScript.Shell")
        objNotify.Popup "Servidor HTTPS iniciado com sucesso!" & vbCrLf & vbCrLf & _
                        "Acesse: https://localhost:5000" & vbCrLf & _
                        "ou https://Gestor-pedidos.local:5000" & vbCrLf & vbCrLf & _
                        "Log: backend\servidor_https.log", _
                        6, "Plante Uma Flor", vbInformation
        On Error GoTo 0
    End If
Else
    MsgBox "Servidor iniciado mas log nao encontrado!" & vbCrLf & vbCrLf & _
           "Verifique se o servidor esta funcionando:" & vbCrLf & _
           "https://localhost:5000", _
           vbExclamation, "Plante Uma Flor - Aviso"
End If

' Limpar objetos
Set objShell = Nothing
Set fso = Nothing

WScript.Quit 0


