#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Automação do Servidor Flask
- Inicia automaticamente às 08:00
- Encerra automaticamente às 18:30
- Reinicia o servidor se ele cair
- Compatível com Windows e Linux
"""

import subprocess
import time
import os
import sys
from datetime import datetime, time as dt_time
import signal

# Configurações
HORA_INICIO = dt_time(8, 0)   # 08:00
HORA_FIM = dt_time(18, 30)    # 18:30
CHECK_INTERVAL = 60            # Verificar a cada 60 segundos
FLASK_SCRIPT = "app.py"        # Nome do arquivo Flask
DIRETORIO = "static"           # Diretório onde está o app.py

# Variável global para controlar o processo do servidor Flask
servidor_processo = None

def log(mensagem):
    """Imprime log com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mensagem}")

def aguardar_horario(hora_alvo):
    """
    Aguarda até que o horário atual seja igual ou posterior à hora_alvo
    Retorna True imediatamente se já passou da hora
    """
    agora = datetime.now().time()
    
    if agora >= hora_alvo:
        log(f"✓ Horário já é {agora.strftime('%H:%M')} - servidor pode iniciar")
        return True
    
    log(f"⏳ Aguardando até {hora_alvo.strftime('%H:%M')}...")
    log(f"   Horário atual: {agora.strftime('%H:%M')}")
    
    while True:
        agora = datetime.now().time()
        
        if agora >= hora_alvo:
            log(f"✓ Horário {agora.strftime('%H:%M')} alcançado!")
            return True
        
        # Aguardar um pouco antes de verificar novamente
        time.sleep(CHECK_INTERVAL)

def servidor_deve_rodar():
    """
    Verifica se o servidor Flask deve estar rodando baseado no horário
    Retorna True se está entre HORA_INICIO e HORA_FIM
    """
    agora = datetime.now().time()
    
    if HORA_INICIO <= HORA_FIM:
        # Horário normal: 08:00 - 18:30 (mesmo dia)
        deve_rodar = HORA_INICIO <= agora <= HORA_FIM
    else:
        # Horário que cruza meia-noite (ex: 22:00 - 06:00)
        deve_rodar = (agora >= HORA_INICIO) or (agora <= HORA_FIM)
    
    return deve_rodar

def iniciar_servidor():
    """Inicia o servidor Flask em um processo separado"""
    global servidor_processo
    
    # Se já existe um processo rodando, não inicia outro
    if servidor_processo is not None:
        if servidor_processo.poll() is None:
            log("⚠️ Servidor Flask já está em execução")
            return False
    
    log("🚀 Iniciando servidor Flask...")
    
    try:
        # Determinar o comando Python correto
        python_cmd = sys.executable
        
        # Montar o caminho completo
        caminho_script = os.path.join(DIRETORIO, FLASK_SCRIPT)
        
        # Iniciar o servidor Flask em background
        if os.name == 'nt':  # Windows
            # No Windows, usar CREATE_NEW_PROCESS_GROUP para evitar que Ctrl+C feche o Flask
            servidor_processo = subprocess.Popen(
                [python_cmd, caminho_script],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:  # Linux/Mac
            servidor_processo = subprocess.Popen(
                [python_cmd, caminho_script],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
        
        log("✅ Servidor Flask iniciado com sucesso!")
        log(f"   PID: {servidor_processo.pid}")
        
        # Aguardar um momento para verificar se iniciou corretamente
        time.sleep(3)
        
        if servidor_processo.poll() is not None:
            log("❌ Servidor Flask encerrou imediatamente após iniciar!")
            log("   Verifique os logs e dependências")
            return False
        
        return True
        
    except FileNotFoundError:
        log("❌ Erro: Arquivo app.py não encontrado")
        log(f"   Procurando em: {os.path.abspath(DIRETORIO)}")
        return False
    except Exception as e:
        log(f"❌ Erro ao iniciar servidor: {e}")
        return False

def parar_servidor():
    """Para o servidor Flask"""
    global servidor_processo
    
    if servidor_processo is None:
        return
    
    log("🛑 Parando servidor Flask...")
    
    try:
        # Enviar sinal de término para o processo
        if os.name == 'nt':  # Windows
            servidor_processo.terminate()
        else:  # Linux/Mac
            servidor_processo.send_signal(signal.SIGTERM)
        
        # Aguardar até 10 segundos para encerramento graceful
        try:
            servidor_processo.wait(timeout=10)
        except subprocess.TimeoutExpired:
            log("⚠️ Servidor não encerrou a tempo, forçando encerramento...")
            servidor_processo.kill()
        
        log("✅ Servidor Flask encerrado")
        servidor_processo = None
        
    except Exception as e:
        log(f"❌ Erro ao parar servidor: {e}")

def verificar_servidor():
    """
    Verifica se o servidor Flask está rodando
    Retorna True se está rodando, False caso contrário
    """
    global servidor_processo
    
    if servidor_processo is None:
        return False
    
    # poll() retorna None se o processo ainda está rodando
    if servidor_processo.poll() is None:
        return True
    else:
        # Processo encerrou
        log(f"⚠️ Servidor Flask encerrou (exit code: {servidor_processo.returncode})")
        servidor_processo = None
        return False

def aguardar_proximo_check():
    """Aguarda o intervalo configurado para o próximo check"""
    log(f"⏰ Próxima verificação em {CHECK_INTERVAL} segundos...")
    time.sleep(CHECK_INTERVAL)

def main():
    """Função principal do script"""
    global servidor_processo
    
    log("=" * 60)
    log("🌺 Automação do Servidor Flask - Plante Uma Flor")
    log("=" * 60)
    log("")
    log(f"📅 Início automático: {HORA_INICIO.strftime('%H:%M')}")
    log(f"📅 Encerramento automático: {HORA_FIM.strftime('%H:%M')}")
    log(f"🔄 Intervalo de verificação: {CHECK_INTERVAL} segundos")
    log("")
    
    # Verificar se já passou da hora de início
    agora = datetime.now().time()
    if agora < HORA_INICIO:
        log(f"⏰ Aguardando até {HORA_INICIO.strftime('%H:%M')} para iniciar...")
        while True:
            if aguardar_horario(HORA_INICIO):
                break
    
    # Iniciar servidor imediatamente se estiver dentro do horário
    if servidor_deve_rodar():
        iniciar_servidor()
    
    # Loop principal de monitoramento
    log("🔄 Iniciando loop de monitoramento...")
    log("   Pressione Ctrl+C para parar o script e o servidor")
    log("")
    
    try:
        while True:
            # Verificar se o servidor deve estar rodando
            deve_rodar = servidor_deve_rodar()
            servidor_rodando = verificar_servidor()
            
            if deve_rodar:
                if not servidor_rodando:
                    log("🔄 Servidor não está rodando, reiniciando...")
                    iniciar_servidor()
                # Servidor está rodando, tudo OK
            else:
                if servidor_rodando:
                    log("⏰ Horário de encerramento alcançado, parando servidor...")
                    parar_servidor()
                # Fora do horário de funcionamento
            
            # Aguardar antes do próximo check
            aguardar_proximo_check()
            
    except KeyboardInterrupt:
        log("")
        log("⚠️ Interrupção recebida (Ctrl+C)")
        log("🛑 Encerrando servidor Flask...")
        parar_servidor()
        log("✅ Script encerrado")
    except Exception as e:
        log(f"❌ Erro inesperado: {e}")
        parar_servidor()
        sys.exit(1)

if __name__ == "__main__":
    main()

