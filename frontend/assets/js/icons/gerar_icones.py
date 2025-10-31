#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar ícones PNG para o PWA

Agora tenta converter automaticamente o arquivo de logo "Buques.ico"
em PNGs nos tamanhos necessários. Caso o .ico não seja encontrado,
gera ícones genéricos como fallback.
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    print("✅ Pillow instalado")
except ImportError:
    print("❌ Pillow não instalado. Instalando...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont

def criar_icone_de_imagem_or_fallback(caminho_ico, tamanho, nome_arquivo):
    """Gera PNG no tamanho especificado a partir de um .ico; se falhar, gera fallback genérico."""
    try:
        base = Image.open(caminho_ico).convert('RGBA')
        # Redimensionar preservando proporção
        base.thumbnail((tamanho, tamanho), Image.LANCZOS)
        # Colocar centralizado em canvas quadrado
        canvas = Image.new('RGBA', (tamanho, tamanho), (0, 0, 0, 0))
        x = (tamanho - base.width) // 2
        y = (tamanho - base.height) // 2
        canvas.paste(base, (x, y), mask=base)
        canvas.save(nome_arquivo, 'PNG')
        print(f"✅ Criado (Buques): {nome_arquivo} ({tamanho}x{tamanho})")
    except Exception as e:
        # Fallback genérico
        img = Image.new('RGB', (tamanho, tamanho), color='#9333ea')
        draw = ImageDraw.Draw(img)
        margem = tamanho // 4
        draw.ellipse([margem, margem, tamanho - margem, tamanho - margem], fill='white', outline='white')
        try:
            fonte_tamanho = tamanho // 3
            fonte = ImageFont.truetype('arial.ttf', fonte_tamanho)
        except Exception:
            fonte = ImageFont.load_default()
        texto = '🌺'
        bbox = draw.textbbox((0, 0), texto, font=fonte)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        tx = (tamanho - text_width) // 2
        ty = (tamanho - text_height) // 2 - bbox[1]
        draw.text((tx, ty), texto, fill='#9333ea', font=fonte)
        img.save(nome_arquivo, 'PNG')
        print(f"⚠️ Fallback (genérico): {nome_arquivo} ({tamanho}x{tamanho}) - erro: {e}")

if __name__ == '__main__':
    import os
    
    # Garantir que estamos no diretório correto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🎨 Gerando ícones PWA...")
    print()
    
    # Tamanhos necessários
    tamanhos = [72, 96, 128, 144, 152, 192, 384, 512]
    
    caminho_ico = os.path.abspath(os.path.join(script_dir, '../../images/Buques.ico'))
    if os.path.exists(caminho_ico):
        print(f"🔎 Usando fonte: {caminho_ico}")
    else:
        print("❌ Buques.ico não encontrado; gerando ícones genéricos de fallback.")

    for tamanho in tamanhos:
        criar_icone_de_imagem_or_fallback(caminho_ico, tamanho, f'icon-{tamanho}x{tamanho}.png')
    
    print()
    print("🎉 Todos os ícones foram criados com sucesso!")
    print("Recarregue a página (Ctrl+F5) para ver o botão de instalação!")


