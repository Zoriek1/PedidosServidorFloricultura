#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar ícones PNG para o PWA
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

def criar_icone(tamanho, nome_arquivo):
    """Cria um ícone PNG com o tamanho especificado"""
    # Criar imagem com fundo roxo
    img = Image.new('RGB', (tamanho, tamanho), color='#9333ea')
    draw = ImageDraw.Draw(img)
    
    # Desenhar um círculo branco no centro
    margem = tamanho // 4
    draw.ellipse([margem, margem, tamanho-margem, tamanho-margem], 
                 fill='white', outline='white')
    
    # Desenhar texto "PF" no centro (Plante Flor)
    try:
        fonte_tamanho = tamanho // 3
        fonte = ImageFont.truetype("arial.ttf", fonte_tamanho)
    except:
        fonte = ImageFont.load_default()
    
    texto = "🌺"
    
    # Calcular posição do texto para centralizar
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (tamanho - text_width) // 2
    y = (tamanho - text_height) // 2 - bbox[1]
    
    # Desenhar o texto
    draw.text((x, y), texto, fill='#9333ea', font=fonte)
    
    # Salvar
    img.save(nome_arquivo, 'PNG')
    print(f"✅ Criado: {nome_arquivo} ({tamanho}x{tamanho})")

if __name__ == '__main__':
    import os
    
    # Garantir que estamos no diretório correto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🎨 Gerando ícones PWA...")
    print()
    
    # Tamanhos necessários
    tamanhos = [72, 96, 128, 144, 152, 192, 384, 512]
    
    for tamanho in tamanhos:
        criar_icone(tamanho, f'icon-{tamanho}x{tamanho}.png')
    
    print()
    print("🎉 Todos os ícones foram criados com sucesso!")
    print("Recarregue a página (Ctrl+F5) para ver o botão de instalação!")


