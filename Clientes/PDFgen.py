# -*- coding: utf-8 -*-
"""
Gerador de Pedidos — Plante Uma Flor
Versão com integração SQLite: salva cada pedido em 'pedidos.db' na pasta de saída.
"""
__version__ = "1.0.0"

import tkinter as tk
from tkinter import ttk, messagebox, Text, filedialog
from tkinter import font as tkFont
import os
import platform
import subprocess
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re
import traceback
import sqlite3
import csv
import requests

# ---------------- Helpers ----------------

def try_register_font(name, filename):
    try:
        pdfmetrics.registerFont(TTFont(name, filename))
        return name
    except Exception:
        return None

def safe_currency_format(value_str):
    try:
        v = float(str(value_str).replace(",", "."))
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(value_str or "")

def format_brl_from_digits(digits: str) -> str:
    if digits is None:
        digits = ""
    digits = re.sub(r"\D", "", digits)
    if digits == "":
        return ""
    if len(digits) == 1:
        reais = "0"
        centavos = f"0{digits}"
    elif len(digits) == 2:
        reais = "0"
        centavos = digits
    else:
        reais = digits[:-2]
        centavos = digits[-2:]
    reais_int = int(reais) if reais != "" else 0
    reais_fmt = f"{reais_int:,}".replace(",", ".")
    return f"R$ {reais_fmt},{centavos}"

def sanitize_filename_component(s, max_len=60):
    s = str(s or "")
    s = s.strip()
    safe = re.sub(r"[^A-Za-z0-9 _-]", "", s)
    safe = safe.replace(" ", "_")
    return safe[:max_len]

def open_file_platform(path):
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])
    except Exception as e:
        messagebox.showwarning("Aviso", f"Não foi possível abrir o caminho automaticamente.\n\nLocal: {path}\nErro: {e}")

# ---------------- PDF generation ----------------

def criar_pdf(caminho_arquivo, dados, pedido_num=None):
    try:
        fonte_regular = "Helvetica"
        fonte_bold = "Helvetica-Bold"
        if try_register_font("Verdana", "Verdana.ttf"):
            fonte_regular = "Verdana"
            if try_register_font("Verdana-Bold", "verdanab.ttf") or try_register_font("Verdana-Bold", "Verdana Bold.ttf"):
                fonte_bold = "Verdana-Bold"

        cnv = canvas.Canvas(caminho_arquivo, pagesize=A4)
        largura, altura = A4

        def novo_header_y():
            cnv.setFont(fonte_bold, 18)
            cnv.drawCentredString(largura / 2, altura - 2*cm, "PLANTE UMA FLOR FLORICULTURA")
            cnv.setLineWidth(0.7)
            cnv.line(2*cm, altura - 2.5*cm, largura - 2*cm, altura - 2.5*cm)
            return altura - 3.5*cm

        y_pos = novo_header_y()

        if pedido_num is not None:
            cnv.setFont(fonte_bold, 14)
            cnv.drawString(3*cm, y_pos, "Pedido:")
            cnv.setFont(fonte_regular, 12)
            cnv.drawRightString(largura - 3*cm, y_pos + 0.1*cm, f"Nº {int(pedido_num)}")
            y_pos -= 1*cm

        espacamento = 0.6 * cm
        left_label_x = 3*cm
        resposta_center_x = (largura / 2) + (largura / 4) - 1*cm
        bottom_margin = 2*cm

        def check_new_page_if_needed(y_current, linhas_necessarias=1):
            est_min = bottom_margin + 4*cm
            if y_current - (linhas_necessarias * espacamento) < est_min:
                cnv.showPage()
                return novo_header_y()
            return y_current

        def desenhar_campo(label, valor, y, negrito=False):
            nonlocal cnv
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

        # Campos no PDF - ordem do PDF antigo, adaptado para novos campos
        y_pos = desenhar_campo("Produto", dados.get("produto", ""), y_pos)
        y_pos = desenhar_campo("Para", dados.get("destinatario", ""), y_pos, negrito=True)
        y_pos = desenhar_campo("Quem enviou", dados.get("cliente", ""), y_pos)
        
        # Campos novos se existirem
        telefone = dados.get("telefone_cliente", "")
        if telefone:
            y_pos = desenhar_campo("Telefone", telefone, y_pos)
        
        tipo_pedido = dados.get("tipo_pedido", "")
        if tipo_pedido:
            y_pos = desenhar_campo("Tipo", tipo_pedido, y_pos, negrito=True)
        
        flores = dados.get("flores_cor", "")
        if flores:
            y_pos = desenhar_campo("Flores e Cor", flores, y_pos)
        
        y_pos = desenhar_campo("Carta", dados.get("mensagem", ""), y_pos)
        y_pos = desenhar_campo("Dia de Entrega", dados.get("data", ""), y_pos, negrito=True)
        y_pos = desenhar_campo("Horário", dados.get("horario", ""), y_pos, negrito=True)
        y_pos = desenhar_campo("Endereço", dados.get("endereco", ""), y_pos)
        y_pos = desenhar_campo("Como Entregar", dados.get("obs_entrega", "") or dados.get("obs", ""), y_pos)

        # Rodapé
        y_pos = check_new_page_if_needed(y_pos, 4)
        cnv.line(2*cm, y_pos, largura - 2*cm, y_pos)
        y_pos -= 1*cm
        cnv.setFont(fonte_bold, 12)
        cnv.drawCentredString(largura / 2, y_pos, "CONTROLE INTERNO")
        y_pos -= 1*cm
        cnv.setFont(fonte_regular, 11)

        info_pagamento = f"Valor: {safe_currency_format(dados.get('valor',''))} | Pagamento: {dados.get('pagamento','')}"
        cnv.drawCentredString(largura / 2, y_pos, info_pagamento)
        
        cnv.save()
        return True
    except Exception:
        traceback.print_exc()
        return False

# ---------------- SQLite integration ----------------

def init_db(path_db):
    conn = sqlite3.connect(path_db, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      pedido_num INTEGER NOT NULL,
      cliente TEXT,
      telefone_cliente TEXT,
      destinatario TEXT NOT NULL,
      tipo_pedido TEXT,
      produto TEXT,
      flores_cor TEXT,
      obs_entrega TEXT,
      mensagem TEXT,
      valor_cents INTEGER,
      valor_text TEXT,
      pagamento TEXT,
      endereco TEXT,
      data_entrega DATE,
      hora_entrega TIME,
      obs TEXT,
      caminho_pdf TEXT,
      status TEXT DEFAULT 'pendente',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(pedido_num)
    )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_data ON pedidos(data_entrega)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_dest ON pedidos(destinatario)")
    conn.commit()
    return conn

def save_pedido_db(conn, pedido: dict):
    cur = conn.cursor()
    try:
        cur.execute("""
          INSERT INTO pedidos (pedido_num, cliente, telefone_cliente, destinatario, tipo_pedido, 
                               produto, flores_cor, obs_entrega, mensagem, valor_cents, valor_text, pagamento, 
                               endereco, data_entrega, hora_entrega, obs, caminho_pdf, status)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
          pedido.get('pedido_num'),
          pedido.get('cliente'),
          pedido.get('telefone_cliente'),
          pedido.get('destinatario'),
          pedido.get('tipo_pedido'),
          pedido.get('produto'),
          pedido.get('flores_cor'),
          pedido.get('obs_entrega'),
          pedido.get('mensagem'),
          pedido.get('valor_cents'),
          pedido.get('valor_text'),
          pedido.get('pagamento'),
          pedido.get('endereco'),
          pedido.get('data_entrega'),
          pedido.get('hora_entrega'),
          pedido.get('obs'),
          pedido.get('caminho_pdf'),
          pedido.get('status','pendente')
        ))
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise ValueError(f"Erro ao salvar pedido: pedido Nº {pedido.get('pedido_num')} já existe no banco de dados") from e
    except Exception as e:
        conn.rollback()
        raise

def export_db_to_csv(conn, csv_path):
    cur = conn.cursor()
    cur.execute("SELECT * FROM pedidos ORDER BY created_at DESC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)

# ---------------- Placeholder helpers ----------------

def add_placeholder_entry(entry: tk.Entry, placeholder: str):
    entry.placeholder = placeholder # type: ignore
    try:
        default_fg = entry.cget("fg")
    except Exception:
        default_fg = "black"
    placeholder_color = "#9a9a9a"

    def on_focus_in(event):
        if entry.get() == placeholder and entry.cget("fg") == placeholder_color:
            entry.delete(0, tk.END)
            entry.config(fg=default_fg)

    def on_focus_out(event):
        if entry.get().strip() == "":
            entry.delete(0, tk.END)
            entry.insert(0, placeholder)
            entry.config(fg=placeholder_color)

    entry.delete(0, tk.END)
    entry.insert(0, placeholder)
    entry.config(fg=placeholder_color)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def add_placeholder_text(text_widget: Text, placeholder: str):
    text_widget.placeholder = placeholder # type: ignore # tipy : ignore
    placeholder_color = "#9a9a9a"
    try:
        normal_color = text_widget.cget("fg")
    except Exception:
        normal_color = "black"

    def set_placeholder():
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", placeholder)
        text_widget.tag_add("ph", "1.0", "end")
        text_widget.tag_configure("ph", foreground=placeholder_color)

    def focus_in(event):
        current = text_widget.get("1.0", "end").strip()
        if current == placeholder:
            text_widget.delete("1.0", "end")
            text_widget.config(fg=normal_color)

    def focus_out(event):
        if text_widget.get("1.0", "end").strip() == "":
            set_placeholder()

    def on_enter(event):
        text_widget.insert("insert", "\n")
        return "break"

    set_placeholder()
    text_widget.bind("<FocusIn>", focus_in)
    text_widget.bind("<FocusOut>", focus_out)
    text_widget.bind("<Return>", on_enter)

# ---------------- Main App ----------------

class App:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Gerador de Pedidos — Plante Uma Flor (v{__version__})")
        self.root.geometry("760x680")
        self.root.minsize(640, 520)
        self.root.configure(bg="#F7F9FB")

        # Fonts
        try:
            self.title_font = tkFont.Font(family="Raleway", size=18, weight="bold")
            self.label_font = tkFont.Font(family="Raleway", size=11)
            self.input_font = tkFont.Font(family="Montserrat", size=10)
        except Exception:
            self.title_font = tkFont.Font(size=18, weight="bold")
            self.label_font = tkFont.Font(size=11)
            self.input_font = tkFont.Font(size=10)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        style.configure("TLabel", background="#F7F9FB", foreground="#222222", font=self.label_font)
        style.configure("Title.TLabel", background="#F7F9FB", foreground="#0b5fa5", font=self.title_font)
        style.configure("TButton", padding=8, font=("Raleway", 11, "bold"))

        self.dados = {}
        self.passo_atual = 0
        self.output_folder = os.path.join(os.path.expanduser("~"), "Documents", "Pedidos-Floricultura")
        os.makedirs(self.output_folder, exist_ok=True)

        # DB connection (initialized lazily)
        self._db_conn = None
        self._db_path = os.path.join(self.output_folder, "pedidos.db")

        # buffer e flag para formatação de valor em centavos
        self._valor_cents = ""

        # Container principal
        self.container = ttk.Frame(root, padding=14)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.header = ttk.Label(self.container, text="Gerador de Pedidos — Plante Uma Flor", style="Title.TLabel")
        self.header.pack(pady=(4,12), anchor="n")

        # Card (frame branco) que contém etapas
        self.card = ttk.Frame(self.container, style="Card.TFrame", padding=(12,12,12,12))
        self.card.pack(fill=tk.BOTH, expand=True)

        self.titulo_etapa = ttk.Label(self.card, text="", font=self.title_font, background="#FFFFFF")
        self.titulo_etapa.pack(pady=(4,10))

        # Frames das etapas (agora são 4: Dados Pessoais, Dados Produto, Logística Condicional, Detalhes Finais)
        self.frames = [self.criar_frame1(), self.criar_frame2(), self.criar_frame3(), self.criar_frame4()]
        self.mostrar_etapa(0)

    def mostrar_etapa(self, numero_etapa):
        for f in self.frames:
            f.pack_forget()
        self.passo_atual = numero_etapa
        titulos = ["Dados Pessoais", "Dados do Produto", "Logística de Entrega", "Detalhes Finais"]
        self.titulo_etapa.config(text=f"Passo {self.passo_atual + 1}/4 — {titulos[self.passo_atual]}")
        self.frames[self.passo_atual].pack(fill=tk.BOTH, expand=True)

    def proxima_etapa(self):
        self.salvar_dados_etapa(self.passo_atual)
        
        # Lógica para pular etapa 3 (logística) se for retirada
        proximo = self.passo_atual + 1
        if proximo == 2 and hasattr(self, 'var_tipo'):
            tipo = self.var_tipo.get().lower()
            if tipo == "retirada":
                proximo = 3  # Pula a etapa de logística
        
        if self.passo_atual < len(self.frames) - 1:
            if proximo < len(self.frames):
                self.mostrar_etapa(proximo)
            else:
                self.mostrar_etapa(self.passo_atual + 1)

    def etapa_anterior(self):
        self.salvar_dados_etapa(self.passo_atual)
        
        # Lógica para pular etapa 3 (logística) se voltando e for retirada
        anterior = self.passo_atual - 1
        if anterior == 2 and hasattr(self, 'var_tipo'):
            tipo = self.var_tipo.get().lower()
            if tipo == "retirada":
                anterior = 1  # Vai direto para etapa 1
        
        if self.passo_atual > 0:
            self.mostrar_etapa(anterior)

    def criar_frame_botoes(self, parent, row, anterior=False, proximo=False, finalizar=False):
        botoes_frame = ttk.Frame(parent)
        botoes_frame.grid(row=row, column=0, sticky="ew", pady=18)
        botoes_frame.columnconfigure(0, weight=1)
        botoes_frame.columnconfigure(1, weight=1)
        botoes_frame.columnconfigure(2, weight=1)

        if anterior:
            btn_ant = ttk.Button(botoes_frame, text="← Anterior", command=self.etapa_anterior)
            btn_ant.grid(row=0, column=0, sticky="w", padx=8)
        
        if finalizar:
            btn_gerar = ttk.Button(botoes_frame, text="✔ Gerar PDF do Pedido", command=self.finalizar_e_gerar_pdf)
            btn_gerar.grid(row=0, column=2, sticky="e", padx=8)
        elif proximo:
            btn_prox = ttk.Button(botoes_frame, text="Próximo →", command=self.proxima_etapa)
            btn_prox.grid(row=0, column=2, sticky="e", padx=8)

    def criar_campo(self, parent, label_text, row):
        lbl = ttk.Label(parent, text=label_text)
        lbl.grid(row=row, column=0, sticky="ew", padx=8, pady=(6,2))
        entry = tk.Entry(parent, font=self.input_font, justify="center", relief="solid", bd=1)
        entry.grid(row=row+1, column=0, sticky="ew", padx=8, pady=(0,8))
        parent.columnconfigure(0, weight=1)
        return entry

    def criar_campo_multilinha(self, parent, label_text, row, height=3):
        lbl = ttk.Label(parent, text=label_text)
        lbl.grid(row=row, column=0, sticky="ew", padx=8, pady=(6,2))
        frame_txt = tk.Frame(parent, bg="#e9eef5", bd=1, relief="solid")
        frame_txt.grid(row=row+1, column=0, sticky="nsew", padx=8, pady=(0,8))
        text = Text(frame_txt, height=height, wrap="word", font=self.input_font, bd=0, padx=6, pady=6)
        text.pack(fill="both", expand=True)
        text.bind("<Return>", lambda e: (text.insert("insert", "\n"), "break"))
        text.frame_parent = frame_txt  # type: ignore # Guarda referência ao frame pai
        parent.rowconfigure(row+1, weight=1)
        parent.columnconfigure(0, weight=1)
        return text

    # ---------- FRAME 1 ----------
    def criar_frame1(self):
        frame = ttk.Frame(self.card, style="Card.TFrame", padding=(6,6,6,6))
        frame.columnconfigure(0, weight=1)

        self.entry_cliente = self.criar_campo(frame, "Quem enviou (Cliente):", 0)
        add_placeholder_entry(self.entry_cliente, "Nome do remetente")

        self.entry_telefone = self.criar_campo(frame, "Telefone do Cliente (Obrigatório):", 2)
        add_placeholder_entry(self.entry_telefone, "Ex.: (62) 99999-9999")

        self.entry_destinatario = self.criar_campo(frame, "Para (Destinatário) - Obrigatório:", 4)
        add_placeholder_entry(self.entry_destinatario, "Nome do destinatário")

        # Tipo de pedido: Entrega ou Retirada
        lbl_tipo = ttk.Label(frame, text="Tipo de Pedido:")
        lbl_tipo.grid(row=6, column=0, sticky="ew", padx=8, pady=(6,2))
        self.var_tipo = tk.StringVar(value="Entrega")
        frame_tipo = ttk.Frame(frame)
        frame_tipo.grid(row=7, column=0, sticky="ew", padx=8, pady=(0,8))
        r1 = ttk.Radiobutton(frame_tipo, text="Entrega", variable=self.var_tipo, value="Entrega")
        r1.pack(side=tk.LEFT, padx=10)
        r2 = ttk.Radiobutton(frame_tipo, text="Retirada", variable=self.var_tipo, value="Retirada")
        r2.pack(side=tk.LEFT, padx=10)

        self.criar_frame_botoes(frame, row=8, proximo=True)
        return frame

    # ---------- FRAME 2 ----------
    def criar_frame2(self):
        frame = ttk.Frame(self.card, style="Card.TFrame", padding=(6,6,6,6))
        frame.columnconfigure(0, weight=1)

        # Nome do Produto
        self.text_produto = self.criar_campo_multilinha(frame, "Nome do Produto:", 0, height=3)
        add_placeholder_text(self.text_produto, "Ex.: Buquê 12 rosas vermelhas")

        # Flores e Cor
        self.text_flores = self.criar_campo_multilinha(frame, "Flores que vão e Cor:", 2, height=3)
        add_placeholder_text(self.text_flores, "Ex.: 12 rosas vermelhas, gipsófilas brancas")

        # Valor (Entry com buffer de centavos)
        lbl_valor = ttk.Label(frame, text="Valor Total (R$):")
        lbl_valor.grid(row=4, column=0, sticky="ew", padx=8, pady=(6,2))
        self.var_valor = tk.StringVar()
        self.entry_valor = tk.Entry(frame, font=self.input_font, justify="center", relief="solid", bd=1, textvariable=self.var_valor)
        self.entry_valor.grid(row=5, column=0, sticky="ew", padx=8, pady=(0,8))
        add_placeholder_entry(self.entry_valor, "Ex.: R$ 120,00")
        self.entry_valor.bind("<KeyPress>", self._valor_keypress)
        self.entry_valor.bind("<FocusOut>", lambda e: self._valor_normalize_on_focusout())

        # Data e Horário (sempre visíveis no Frame 2)
        self.lbl_data = ttk.Label(frame, text="Data (DD/MM/YYYY):")
        self.lbl_data.grid(row=6, column=0, sticky="ew", padx=8, pady=(6,2))
        self.entry_data = tk.Entry(frame, font=self.input_font, justify="center", relief="solid", bd=1)
        self.entry_data.grid(row=7, column=0, sticky="ew", padx=8, pady=(0,8))
        add_placeholder_entry(self.entry_data, "Ex.: 15/10/2025")
        self.entry_data.bind("<KeyRelease>", lambda e: self._mask_data(self.entry_data))

        self.lbl_horario = ttk.Label(frame, text="Horário (ex.: 14:30):")
        self.lbl_horario.grid(row=8, column=0, sticky="ew", padx=8, pady=(6,2))
        self.entry_horario = tk.Entry(frame, font=self.input_font, justify="center", relief="solid", bd=1)
        self.entry_horario.grid(row=9, column=0, sticky="ew", padx=8, pady=(0,8))
        add_placeholder_entry(self.entry_horario, "Ex.: 14:30")
        self.entry_horario.bind("<KeyRelease>", lambda e: self._mask_horario(self.entry_horario))

        folder_frame = ttk.Frame(frame)
        folder_frame.grid(row=10, column=0, sticky="ew", padx=8, pady=(8,0))
        folder_frame.columnconfigure(0, weight=1)
        self.folder_label = ttk.Label(folder_frame, text=f"Pasta de saída: {self.output_folder}")
        self.folder_label.grid(row=0, column=0, sticky="w")
        btn_choose = ttk.Button(folder_frame, text="Alterar pasta...", command=self.escolher_pasta_saida)
        btn_choose.grid(row=0, column=1, sticky="e", padx=6)

        tools_frame = ttk.Frame(frame)
        tools_frame.grid(row=11, column=0, sticky="ew", padx=8, pady=(8,0))
        tools_frame.columnconfigure(0, weight=1)
        tools_frame.columnconfigure(1, weight=1)
        btn_open_db = ttk.Button(tools_frame, text="Abrir pasta (contém DB)", command=lambda: open_file_platform(self.output_folder))
        btn_open_db.grid(row=0, column=0, sticky="w")
        btn_export = ttk.Button(tools_frame, text="Exportar pedidos (CSV)", command=self._export_csv_prompt)
        btn_export.grid(row=0, column=1, sticky="e")

        self.criar_frame_botoes(frame, row=12, anterior=True, proximo=True)
        return frame

    # ---------- FRAME 3 (Logística de Entrega) ----------
    def criar_frame3(self):
        frame = ttk.Frame(self.card, style="Card.TFrame", padding=(6,6,6,6))
        frame.columnconfigure(0, weight=1)

        # Endereço completo
        self.lbl_endereco = ttk.Label(frame, text="Endereço Completo:")
        self.lbl_endereco.grid(row=0, column=0, sticky="ew", padx=8, pady=(6,2))
        frame_endereco = tk.Frame(frame, bg="#e9eef5", bd=1, relief="solid")
        frame_endereco.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.text_endereco = Text(frame_endereco, height=4, wrap="word", font=self.input_font, bd=0, padx=6, pady=6)
        self.text_endereco.pack(fill="both", expand=True)
        self.text_endereco.frame_parent = frame_endereco  # type: ignore
        add_placeholder_text(self.text_endereco, "Rua, número, complemento, bairro, cidade")

        # Observações de entrega
        self.text_obs_entrega = self.criar_campo_multilinha(frame, "Observações para Entrega:", 2, height=3)
        add_placeholder_text(self.text_obs_entrega, "Ex.: Entregar na portaria / Bater na campainha")

        self.criar_frame_botoes(frame, row=8, anterior=True, proximo=True)
        return frame

    # ---------- FRAME 4 (Detalhes Finais) ----------
    def criar_frame4(self):
        frame = ttk.Frame(self.card, style="Card.TFrame", padding=(6,6,6,6))
        frame.columnconfigure(0, weight=1)

        self.entry_obs = self.criar_campo_multilinha(frame, "Observações Gerais:", 0, height=3)
        add_placeholder_text(self.entry_obs, "Observações gerais sobre o pedido")

        self.text_mensagem = self.criar_campo_multilinha(frame, "Mensagem do Cartão:", 2, height=4)
        add_placeholder_text(self.text_mensagem, "Ex.: Feliz Aniversário! Com carinho, João")

        self.entry_pagamento = self.criar_campo(frame, "Forma de Pagamento:", 4)
        add_placeholder_entry(self.entry_pagamento, "Ex.: Dinheiro / Cartão / PIX")

        self.criar_frame_botoes(frame, row=8, anterior=True, finalizar=True)
        return frame

    def escolher_pasta_saida(self):
        pasta = filedialog.askdirectory(initialdir=self.output_folder, title="Escolha a pasta para salvar PDFs")
        if pasta:
            self.output_folder = pasta
            self.folder_label.config(text=f"Pasta de saída: {self.output_folder}")
            # atualizar caminho DB também
            self._db_path = os.path.join(self.output_folder, "pedidos.db")
            # se já tivesse conexão aberta, feche para reabrir no novo local quando salvar
            if self._db_conn:
                try:
                    self._db_conn.close()
                except Exception:
                    pass
                self._db_conn = None

    def salvar_dados_etapa(self, numero_etapa):
        def clean_entry(entry_widget):
            try:
                val = entry_widget.get().strip()
            except Exception:
                return ""
            ph = getattr(entry_widget, "placeholder", None)
            if ph is not None and val == ph:
                return ""
            return val

        def clean_text(text_widget):
            try:
                val = text_widget.get("1.0", "end").strip()
            except Exception:
                return ""
            ph = getattr(text_widget, "placeholder", None)
            if ph is not None and val == ph:
                return ""
            return val

        mappings = [
            # Frame 0: Dados Pessoais
            lambda: {
                "cliente": clean_entry(self.entry_cliente),
                "telefone_cliente": clean_entry(self.entry_telefone),
                "destinatario": clean_entry(self.entry_destinatario),
                "tipo_pedido": self.var_tipo.get() if hasattr(self, 'var_tipo') else "Entrega"
            },
            # Frame 1: Dados do Produto
            lambda: {
                "produto": clean_text(self.text_produto),
                "flores_cor": clean_text(self.text_flores),
                "valor": clean_entry(self.entry_valor),
                "data": clean_entry(self.entry_data),
                "horario": clean_entry(self.entry_horario)
            },
            # Frame 2: Logística de Entrega
            lambda: {
                "endereco": clean_text(self.text_endereco),
                "obs_entrega": clean_text(self.text_obs_entrega)
            },
            # Frame 3: Detalhes Finais
            lambda: {
                "obs": clean_text(self.entry_obs),
                "mensagem": clean_text(self.text_mensagem),
                "pagamento": clean_entry(self.entry_pagamento)
            }
        ]

        try:
            self.dados.update(mappings[numero_etapa]())
            # normalizar valor salvo para ser sempre "R$ X.XXX,XX"
            raw_val = self.dados.get("valor", "")
            digits = re.sub(r"\D", "", raw_val or "")
            if digits:
                self.dados["valor"] = self._format_brl_from_cents(digits)
            else:
                self.dados["valor"] = ""
        except Exception:
            pass

    def validar_data(self, data_str):
        if not data_str:
            return True
        try:
            datetime.strptime(data_str, "%d/%m/%Y")
            return True
        except Exception:
            return False

    def validar_horario(self, hstr):
        if not hstr:
            return True
        if re.match(r"^([01]?\d|2[0-3]):[0-5]\d$", hstr):
            return True
        return False

    def contar_pedidos_existentes(self):
        try:
            arquivos = [f for f in os.listdir(self.output_folder) if f.startswith("Pedido_") and f.lower().endswith(".pdf")]
            return len(arquivos)
        except Exception:
            return 0

    def finalizar_e_gerar_pdf(self):
        # salva o estado atual
        self.salvar_dados_etapa(self.passo_atual if self.passo_atual < 4 else 3)
        
        # Validação de telefone (obrigatório)
        telefone = (self.dados.get("telefone_cliente") or "").strip()
        if not telefone:
            messagebox.showerror("Erro", 'O campo "Telefone do Cliente" é obrigatório.')
            self.mostrar_etapa(0)
            return
        
        # Validação de destinatário (obrigatório)
        destinatario = (self.dados.get("destinatario") or "").strip()
        if not destinatario:
            messagebox.showerror("Erro", 'O campo "Destinatário" é obrigatório.')
            self.mostrar_etapa(0)
            return

        # Validação de data e horário (obrigatórios para todos os pedidos)
        data = (self.dados.get("data") or "").strip()
        if not self.validar_data(data):
            messagebox.showerror("Erro", 'Formato de data inválido. Use DD/MM/YYYY (ex.: 15/10/2025).')
            self.mostrar_etapa(1)
            return

        horario = (self.dados.get("horario") or "").strip()
        if not self.validar_horario(horario):
            messagebox.showerror("Erro", 'Formato de horário inválido. Use HH:MM (ex.: 14:30) ou deixe vazio.')
            self.mostrar_etapa(1)
            return

        pedido_num = self.contar_pedidos_existentes() + 1
        data_hoje_str = datetime.now().strftime('%Y-%m-%d')
        nome_seguro = sanitize_filename_component(destinatario)
        nome_arquivo = f"Pedido_{pedido_num:03d}_{data_hoje_str}_{nome_seguro}.pdf"
        caminho_completo_arquivo = os.path.join(self.output_folder, nome_arquivo)

        if os.path.exists(caminho_completo_arquivo):
            resp = messagebox.askyesno("Arquivo existe", f"O arquivo {nome_arquivo} já existe. Deseja sobrescrever?")
            if not resp:
                i = 1
                base, ext = os.path.splitext(nome_arquivo)
                while os.path.exists(os.path.join(self.output_folder, f"{base}_{i}{ext}")) and i < 2000:
                    i += 1
                nome_arquivo = f"{base}_{i}{ext}"
                caminho_completo_arquivo = os.path.join(self.output_folder, nome_arquivo)

        # Gera o PDF
        sucesso = criar_pdf(caminho_completo_arquivo, self.dados, pedido_num=pedido_num)
        if not sucesso:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o PDF.\n\nCaminho: {caminho_completo_arquivo}\n\nVerifique o console para detalhes.")
            return

        # Prepara dados para salvar no DB
        # valor_cents: preferir buffer interno se existir, senão extrair do valor formatado
        valor_cents = None
        if self._valor_cents:
            try:
                valor_cents = int(self._valor_cents.lstrip("0") or "0")
            except Exception:
                valor_cents = None
        else:
            # extrair de self.dados['valor']
            vraw = self.dados.get("valor", "") or ""
            digits = re.sub(r"\D", "", vraw)
            if digits:
                try:
                    valor_cents = int(digits)
                except Exception:
                    valor_cents = None

        # converter data para YYYY-MM-DD
        data_entrega_iso = None
        d = (self.dados.get("data") or "").strip()
        if d:
            try:
                data_entrega_iso = datetime.strptime(d, "%d/%m/%Y").strftime("%Y-%m-%d")
            except Exception:
                data_entrega_iso = None

        pedido_record = {
            'pedido_num': pedido_num,
            'cliente': self.dados.get('cliente', ''),
            'telefone_cliente': self.dados.get('telefone_cliente', ''),
            'destinatario': self.dados.get('destinatario', ''),
            'tipo_pedido': self.dados.get('tipo_pedido', ''),
            'produto': self.dados.get('produto', ''),
            'quantidade': 1,  # Padrão: 1 unidade (campo não existe no formulário atual)
            'flores_cor': self.dados.get('flores_cor', ''),
            'obs_entrega': self.dados.get('obs_entrega', ''),
            'mensagem': self.dados.get('mensagem', ''),
            'valor_cents': valor_cents,
            'valor_text': self.dados.get('valor', ''),
            'pagamento': self.dados.get('pagamento', ''),
            'endereco': self.dados.get('endereco', ''),
            'data_entrega': data_entrega_iso,
            'hora_entrega': self.dados.get('horario', ''),
            'obs': self.dados.get('obs', ''),
            'caminho_pdf': caminho_completo_arquivo,
            'status': 'pendente'
        }

        # Tenta salvar no DB (inicializa conexão se necessário)
        try:
            if not self._db_conn:
                self._db_conn = init_db(self._db_path)
            save_pedido_db(self._db_conn, pedido_record)
        except ValueError as e:
            # Pedido duplicado ou erro de integridade
            messagebox.showwarning("Aviso", f"PDF gerado com sucesso!\n\nAviso: {str(e)}")
        except Exception as e:
            # não bloqueia a geração do PDF; apenas informa
            messagebox.showwarning("Aviso (DB)", f"PDF gerado, mas houve erro ao salvar no banco: {e}\n\nVerifique permissões ou caminho: {self._db_path}")

        # Sucesso total
        self.enviar_pedido_para_painel(pedido_record)
        messagebox.showinfo("Sucesso", f"PDF gerado com sucesso!\n\nLocal: {caminho_completo_arquivo}\nPedido Nº: {pedido_num}")
        try:
            open_file_platform(caminho_completo_arquivo)
        except Exception:
            pass
        self.root.destroy()


    # ---------- Máscaras / valor buffer ----------
    def _format_brl_from_cents(self, cents_digits: str) -> str:
        if not cents_digits:
            return ""
        cents_digits = cents_digits.lstrip("0")
        if cents_digits == "":
            cents_digits = "0"
        total_cents = int(cents_digits)
        reais = total_cents // 100
        centavos = total_cents % 100
        reais_fmt = f"{reais:,}".replace(",", ".")
        return f"R$ {reais_fmt},{centavos:02d}"

    def _valor_keypress(self, event):
        allow_keysym = {"Tab", "ISO_Left_Tab", "Left", "Right", "Up", "Down", "Home", "End", "Return", "KP_Enter", "Escape"}
        ks = event.keysym
        if ks in allow_keysym:
            return None
        if ks == "BackSpace":
            if self._valor_cents:
                self._valor_cents = self._valor_cents[:-1]
            formatted = self._format_brl_from_cents(self._valor_cents)
            if formatted == "":
                self.var_valor.set("")
            else:
                self.var_valor.set(formatted)
            return "break"
        if not event.char:
            return "break"
        # allow paste via Ctrl+V (do not intercept)
        if (event.state & 0x4) and (ks.lower() == "v"):
            return None
        if event.char.isdigit():
            ph = getattr(self.entry_valor, "placeholder", None)
            if ph is not None and self.var_valor.get() == ph:
                self._valor_cents = ""
            max_digits = 15
            if len(self._valor_cents) < max_digits:
                self._valor_cents += event.char
            self.var_valor.set(self._format_brl_from_cents(self._valor_cents))
            return "break"
        return "break"

    def _valor_normalize_on_focusout(self):
        txt = self.var_valor.get()
        digits = re.sub(r"\D", "", txt)
        digits = digits.lstrip("0")
        if digits == "":
            self._valor_cents = ""
            self.var_valor.set("")
            return
        self._valor_cents = digits
        self.var_valor.set(self._format_brl_from_cents(self._valor_cents))

    def _mask_data(self, entry_widget):
        s = entry_widget.get()
        ph = getattr(entry_widget, "placeholder", None)
        if ph is not None and s == ph:
            return
        digits = re.sub(r"\D", "", s)[:8]
        parts = []
        if len(digits) >= 2:
            parts.append(digits[:2])
            if len(digits) >= 4:
                parts.append(digits[2:4])
                if len(digits) > 4:
                    parts.append(digits[4:])
            else:
                parts.append(digits[2:])
        else:
            parts.append(digits)
        masked = "/".join([p for p in parts if p != ""])
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, masked)

    def _mask_horario(self, entry_widget):
        s = entry_widget.get()
        ph = getattr(entry_widget, "placeholder", None)
        if ph is not None and s == ph:
            return
        digits = re.sub(r"\D", "", s)[:4]
        if len(digits) <= 2:
            masked = digits
        else:
            masked = digits[:2] + ":" + digits[2:]
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, masked)

    # ---------- CSV export ----------
    def _export_csv_prompt(self):
        # inicializar DB se necessário
        try:
            if not self._db_conn:
                self._db_conn = init_db(self._db_path)
        except Exception as e:
            messagebox.showerror("Erro (DB)", f"Não foi possível abrir/criar DB em: {self._db_path}\nErro: {e}")
            return
        destino = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialdir=self.output_folder, title="Salvar CSV de pedidos")
        if not destino:
            return
        try:
            export_db_to_csv(self._db_conn, destino)
            messagebox.showinfo("Exportado", f"Pedidos exportados para CSV:\n{destino}")
            open_file_platform(destino)
        except Exception as e:
            messagebox.showerror("Erro exportar CSV", f"Falha ao exportar: {e}")

    def enviar_pedido_para_painel(self, pedido: dict):
        """Envia pedido para o servidor Flask via POST"""
        try:
            import requests
            
            # Montar dados para envio conforme especificação da API
            dados_envio = {
                "cliente": pedido.get("cliente", ""),
                "produto": pedido.get("produto", ""),
                "quantidade": pedido.get("quantidade", 1),  # Valor padrão: 1
                "horario": pedido.get("hora_entrega", ""),
                "dia_entrega": pedido.get("data_entrega", ""),
                "destinatario": pedido.get("destinatario", ""),
                "mensagem": pedido.get("mensagem", "")
            }
            
            # Enviar requisição POST para o servidor
            response = requests.post(
                "http://192.168.1.148:5000/api/pedidos",
                json=dados_envio,
                timeout=5,
                headers={'Content-Type': 'application/json'}
            )
            
            # Verificar status da resposta
            response.raise_for_status()
            
            # Log de sucesso
            resposta_json = response.json()
            pedido_id = resposta_json.get('pedido_id', 'N/A')
            print(f"✅ Pedido #{pedido_id} enviado ao painel com sucesso!")
            
        except ImportError:
            print("⚠️ Módulo 'requests' não está disponível. Instale com: pip install requests")
        except requests.exceptions.ConnectionError:
            print("⚠️ Erro de conexão: Servidor Flask não está acessível em http://192.168.0.10:5000")
        except requests.exceptions.Timeout:
            print("⚠️ Timeout: O servidor não respondeu a tempo")
        except requests.exceptions.HTTPError as e:
            print(f"⚠️ Erro HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            print(f"⚠️ Erro ao enviar pedido ao painel: {e}")

# ---------------- App start ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
