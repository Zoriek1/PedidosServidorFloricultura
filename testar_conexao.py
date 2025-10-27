#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a conexão entre PDFgen e Flask
"""
import requests
import json

print("=" * 50)
print("Teste de Conexão - PDFgen ↔️ Flask")
print("=" * 50)
print()

# URL do servidor
url = "http://192.168.1.148:5000/api/pedidos"

# Dados de teste
dados_teste = {
    "cliente": "João Silva",
    "produto": "Buquê 12 rosas vermelhas",
    "quantidade": 1,
    "horario": "14:30",
    "dia_entrega": "2024-12-25",
    "destinatario": "Maria Santos",
    "mensagem": "Feliz Aniversário! Teste de conexão."
}

print(f"🔗 Conectando ao servidor Flask...")
print(f"📍 URL: {url}")
print()

try:
    # Fazer requisição POST
    print("📤 Enviando requisição POST...")
    print(f"📝 Dados: {json.dumps(dados_teste, indent=2, ensure_ascii=False)}")
    print()
    
    response = requests.post(
        url,
        json=dados_teste,
        timeout=5,
        headers={'Content-Type': 'application/json'}
    )
    
    # Verificar status
    if response.status_code == 201:
        print("✅ SUCESSO! Pedido enviado com sucesso!")
        print()
        
        resposta = response.json()
        print(f"📋 ID do Pedido: {resposta.get('pedido_id')}")
        print(f"💬 Mensagem: {resposta.get('message')}")
        print()
        print("📊 Dados armazenados:")
        dados_armazenados = resposta.get('dados_armazenados', {})
        for campo, valor in dados_armazenados.items():
            print(f"   {campo}: {valor}")
    else:
        print(f"❌ ERRO! Status: {response.status_code}")
        print(f"📝 Resposta: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ ERRO DE CONEXÃO!")
    print("⚠️ O servidor Flask não está acessível.")
    print()
    print("📋 Possíveis causas:")
    print("   1. O servidor Flask não está rodando")
    print("   2. IP incorreto (verifique seu IP com: ipconfig)")
    print("   3. Firewall bloqueando a conexão")
    print()
    print("🔧 Solução:")
    print("   1. Abra um terminal")
    print("   2. Execute: cd Servidor")
    print("   3. Execute: .\\iniciar_servidor.ps1")
    print("   4. Aguarde o servidor iniciar")
    print("   5. Execute este teste novamente")

except requests.exceptions.Timeout:
    print("⏱️ TIMEOUT!")
    print("⚠️ O servidor não respondeu em 5 segundos")
    
except Exception as e:
    print(f"❌ ERRO: {e}")

print()
print("=" * 50)

