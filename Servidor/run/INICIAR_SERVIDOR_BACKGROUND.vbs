' ============================================
' Plante Uma Flor v2.0 - Iniciar em Background
' ============================================
' Este script inicia o servidor Flask em segundo plano
' sem mostrar nenhuma janela do CMD
' ============================================

Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Obter o diretório onde este script está localizado
ScriptDir = FSO.GetParentFolderName(WScript.ScriptFullName)

' Comando para executar: navega até o diretório e executa main.py
Command = "cmd /c cd /d """ & ScriptDir & """ && python main.py"

' Executar o comando:
' - Primeiro parâmetro: comando a executar
' - Segundo parâmetro: 0 = janela oculta
' - Terceiro parâmetro: False = não esperar conclusão
WshShell.Run Command, 0, False

' Mostrar mensagem de confirmação
MsgBox "Servidor iniciado em segundo plano!" & vbCrLf & vbCrLf & _
       "Para acessar o painel:" & vbCrLf & _
       "http://localhost:5000" & vbCrLf & vbCrLf & _
       "Para parar o servidor, execute:" & vbCrLf & _
       "PARAR_SERVIDOR.bat", vbInformation, "Plante Uma Flor v2.0"


