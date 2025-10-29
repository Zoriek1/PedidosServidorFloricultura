' ===================================================
' PLANTE UMA FLOR - Iniciar Servidor HTTPS Invisível
' Inicia o servidor Flask em HTTPS sem janela visível
' ===================================================

Option Explicit

Dim objShell, scriptDir, backendDir, pythonCmd, strCommand

' Criar objeto Shell
Set objShell = CreateObject("WScript.Shell")

' Obter diretório do script
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Mudar para diretório do backend
backendDir = scriptDir
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

' Criar comando para iniciar o servidor
strCommand = "cmd /c cd /d """ & backendDir & """ && " & pythonCmd & " main.py --https"

' Executar em modo oculto (0 = janela oculta, False = não esperar conclusão)
objShell.Run strCommand, 0, False

' Aguardar 3 segundos para o servidor iniciar
WScript.Sleep 3000

' Mostrar notificação de sucesso (se disponível)
On Error Resume Next
Dim objNotify
Set objNotify = CreateObject("WScript.Shell")
objNotify.Popup "Servidor HTTPS iniciado com sucesso!" & vbCrLf & vbCrLf & _
                "Acesse: https://localhost:5000", _
                5, "Plante Uma Flor", vbInformation
On Error GoTo 0

' Limpar objetos
Set objShell = Nothing
Set fso = Nothing

WScript.Quit 0


