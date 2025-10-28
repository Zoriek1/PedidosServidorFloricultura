# -*- coding: utf-8 -*-
"""
Gerador de PDFs otimizado
"""
import os
from pathlib import Path
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from app.utils.fonts import font_manager
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class PDFGenerator:
    """Gerador de PDFs otimizado com cache de fontes"""
    
    def __init__(self):
        self.font_manager = font_manager
    
    def create_pdf(self, file_path: str, data: Dict, pedido_num: int = None) -> bool:
        """Cria PDF do pedido"""
        try:
            # Carregar fontes apenas quando necessário
            self.font_manager.load_fonts()
            
            fonte_regular = self.font_manager.get_font('regular')
            fonte_bold = self.font_manager.get_font('bold')
            
            # Criar canvas
            cnv = canvas.Canvas(file_path, pagesize=A4)
            largura, altura = A4
            
            # Header
            y_pos = self._draw_header(cnv, largura, altura, fonte_bold, pedido_num)
            
            # Conteúdo
            y_pos = self._draw_content(cnv, largura, altura, data, fonte_regular, fonte_bold, y_pos)
            
            # Rodapé
            self._draw_footer(cnv, largura, altura, data, fonte_regular, fonte_bold, y_pos)
            
            # Salvar
            cnv.save()
            logger.info(f"PDF gerado com sucesso: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            return False
    
    def _draw_header(self, cnv, largura, altura, fonte_bold, pedido_num):
        """Desenha cabeçalho do PDF"""
        cnv.setFont(fonte_bold, 18)
        cnv.drawCentredString(largura / 2, altura - 2*cm, "PLANTE UMA FLOR FLORICULTURA")
        cnv.setLineWidth(0.7)
        cnv.line(2*cm, altura - 2.5*cm, largura - 2*cm, altura - 2.5*cm)
        
        y_pos = altura - 3.5*cm
        
        if pedido_num:
            cnv.setFont(fonte_bold, 14)
            cnv.drawString(3*cm, y_pos, "Pedido:")
            cnv.setFont("Helvetica", 12)
            cnv.drawRightString(largura - 3*cm, y_pos + 0.1*cm, f"Nº {int(pedido_num)}")
            y_pos -= 1*cm
        
        return y_pos
    
    def _draw_content(self, cnv, largura, altura, data, fonte_regular, fonte_bold, y_pos):
        """Desenha conteúdo do PDF"""
        espacamento = 0.6 * cm
        left_label_x = 3*cm
        resposta_center_x = (largura / 2) + (largura / 4) - 1*cm
        bottom_margin = 2*cm
        
        def check_new_page_if_needed(y_current, linhas_necessarias=1):
            est_min = bottom_margin + 4*cm
            if y_current - (linhas_necessarias * espacamento) < est_min:
                cnv.showPage()
                return self._draw_header(cnv, largura, altura, fonte_bold, None)
            return y_current
        
        def desenhar_campo(label, valor, y, negrito=False):
            valor = "" if valor is None else str(valor)
            linhas = [l.rstrip() for l in valor.splitlines()] if valor.strip() != "" else []
            linhas = linhas if linhas else [""]
            linhas_necessarias = max(1, len(linhas))
            y = check_new_page_if_needed(y, linhas_necessarias + 1)
            
            cnv.setFont(fonte_bold if negrito else fonte_regular, 11)
            cnv.drawString(left_label_x, y, f"{label}:")
            cnv.setFont(fonte_regular, 10)
            y_text = y
            for linha in linhas:
                if linha.strip() == "":
                    y_text -= espacamento
                else:
                    cnv.drawCentredString(resposta_center_x, y_text, linha)
                    y_text -= espacamento
            return y_text - 0.2*cm
        
        # Campos do PDF
        y_pos = desenhar_campo("Produto", data.get("produto", ""), y_pos)
        y_pos = desenhar_campo("Para", data.get("destinatario", ""), y_pos, negrito=True)
        y_pos = desenhar_campo("Quem enviou", data.get("cliente", ""), y_pos)
        
        # Campos opcionais
        if data.get("telefone_cliente"):
            y_pos = desenhar_campo("Telefone", data.get("telefone_cliente"), y_pos)
        
        if data.get("tipo_pedido"):
            y_pos = desenhar_campo("Tipo", data.get("tipo_pedido"), y_pos, negrito=True)
        
        if data.get("flores_cor"):
            y_pos = desenhar_campo("Flores e Cor", data.get("flores_cor"), y_pos)
        
        y_pos = desenhar_campo("Carta", data.get("mensagem", ""), y_pos)
        y_pos = desenhar_campo("Dia de Entrega", data.get("data", ""), y_pos, negrito=True)
        y_pos = desenhar_campo("Horário", data.get("horario", ""), y_pos, negrito=True)
        y_pos = desenhar_campo("Endereço", data.get("endereco", ""), y_pos)
        y_pos = desenhar_campo("Como Entregar", data.get("obs_entrega", "") or data.get("obs", ""), y_pos)
        
        return y_pos
    
    def _draw_footer(self, cnv, largura, altura, data, fonte_regular, fonte_bold, y_pos):
        """Desenha rodapé do PDF"""
        bottom_margin = 2*cm
        
        y_pos = max(y_pos, bottom_margin + 4*cm)
        cnv.line(2*cm, y_pos, largura - 2*cm, y_pos)
        y_pos -= 1*cm
        
        cnv.setFont(fonte_bold, 12)
        cnv.drawCentredString(largura / 2, y_pos, "CONTROLE INTERNO")
        y_pos -= 1*cm
        cnv.setFont(fonte_regular, 11)
        
        info_pagamento = f"Valor: {self._format_currency(data.get('valor',''))} | Pagamento: {data.get('pagamento','')}"
        cnv.drawCentredString(largura / 2, y_pos, info_pagamento)
    
    def _format_currency(self, value_str):
        """Formata valor monetário"""
        try:
            v = float(str(value_str).replace(",", "."))
            return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            return str(value_str or "")