# -*- coding: utf-8 -*-
"""
Gerenciamento otimizado de fontes para PDFs
"""
import os
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class FontManager:
    """Gerenciador de fontes com cache para melhor performance"""
    
    def __init__(self):
        self._fonts_loaded = False
        self._font_cache = {}
        self.fonts_dir = Path(__file__).parent.parent.parent / "resources" / "fonts"
    
    def load_fonts(self):
        """Carrega fontes apenas quando necessário (lazy loading)"""
        if self._fonts_loaded:
            return
        
        try:
            # Fontes padrão do sistema
            self._font_cache['regular'] = 'Helvetica'
            self._font_cache['bold'] = 'Helvetica-Bold'
            
            # Tentar carregar fontes customizadas
            font_files = {
                'Raleway': 'Raleway-VariableFont_wght.ttf',
                'Montserrat': 'Montserrat-VariableFont_wght.ttf'
            }
            
            for font_name, filename in font_files.items():
                font_path = self.fonts_dir / filename
                if font_path.exists():
                    try:
                        pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                        self._font_cache['regular'] = font_name
                        logger.info(f"Fonte {font_name} carregada com sucesso")
                    except Exception as e:
                        logger.warning(f"Erro ao carregar fonte {font_name}: {e}")
            
            self._fonts_loaded = True
            logger.info("Fontes carregadas com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao carregar fontes: {e}")
    
    def get_font(self, style='regular'):
        """Retorna fonte do cache"""
        if not self._fonts_loaded:
            self.load_fonts()
        return self._font_cache.get(style, 'Helvetica')
    
    def get_available_fonts(self):
        """Retorna lista de fontes disponíveis"""
        if not self._fonts_loaded:
            self.load_fonts()
        return list(self._font_cache.keys())

# Instância global para reutilização
font_manager = FontManager()