#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar SECRET_KEY segura para produção
"""
import secrets
import string

def generate_secret_key(length=32):
    """Gera uma chave secreta segura"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == '__main__':
    print("🔐 Gerando SECRET_KEY para produção...")
    print()
    
    # Gerar chave
    secret_key = generate_secret_key(32)
    
    print("✅ SECRET_KEY gerada:")
    print(f"SECRET_KEY={secret_key}")
    print()
    print("📋 Copie esta chave e configure na plataforma de hospedagem:")
    print("   - Vercel: Settings > Environment Variables")
    print("   - Railway: Variables tab")
    print("   - Heroku: Settings > Config Vars")
    print()
    print("⚠️  IMPORTANTE: Mantenha esta chave segura e não compartilhe!")