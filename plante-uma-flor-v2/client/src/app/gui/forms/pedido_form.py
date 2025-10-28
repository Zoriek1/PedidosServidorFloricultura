# -*- coding: utf-8 -*-
"""
Formulário de pedido otimizado com validações
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Dict, Any, Callable
from app.core.database import DatabaseManager
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class PedidoForm:
    """Formulário de pedido com validações otimizadas"""
    
    def __init__(self, parent, on_created_callback: Callable):
        self.parent = parent
        self.on_created_callback = on_created_callback
        self.current_step = 0
        self.data = {}
        
        # Configurar interface
        self._setup_interface()
        self._create_steps()
        self._show_step(0)
    
    def _setup_interface(self):
        """Configura interface do formulário"""
        # Título da etapa
        self.step_title = ttk.Label(
            self.parent,
            text="",
            font=("Arial", 14, "bold")
        )
        self.step_title.pack(pady=(0, 20))
        
        # Container das etapas
        self.steps_container = ttk.Frame(self.parent)
        self.steps_container.pack(fill=tk.BOTH, expand=True)
        
        # Botões de navegação
        self._create_navigation_buttons()
    
    def _create_steps(self):
        """Cria todas as etapas do formulário"""
        self.steps = [
            self._create_step1(),  # Dados pessoais
            self._create_step2(),  # Dados do produto
            self._create_step3(),  # Logística (condicional)
            self._create_step4()   # Detalhes finais
        ]
    
    def _create_step1(self):
        """Etapa 1: Dados pessoais"""
        frame = ttk.Frame(self.steps_container)
        
        # Cliente
        ttk.Label(frame, text="Cliente (Quem envia):").pack(anchor="w", pady=(0, 5))
        self.entry_cliente = tk.Entry(frame, font=("Arial", 11))
        self.entry_cliente.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder(self.entry_cliente, "Nome do remetente")
        
        # Telefone (obrigatório)
        ttk.Label(frame, text="Telefone do Cliente *:").pack(anchor="w", pady=(0, 5))
        self.entry_telefone = tk.Entry(frame, font=("Arial", 11))
        self.entry_telefone.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder(self.entry_telefone, "Ex.: (62) 99999-9999")
        
        # Destinatário (obrigatório)
        ttk.Label(frame, text="Destinatário (Para quem) *:").pack(anchor="w", pady=(0, 5))
        self.entry_destinatario = tk.Entry(frame, font=("Arial", 11))
        self.entry_destinatario.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder(self.entry_destinatario, "Nome do destinatário")
        
        # Tipo de pedido
        ttk.Label(frame, text="Tipo de Pedido:").pack(anchor="w", pady=(0, 5))
        self.tipo_frame = ttk.Frame(frame)
        self.tipo_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.var_tipo = tk.StringVar(value="Entrega")
        ttk.Radiobutton(self.tipo_frame, text="Entrega", variable=self.var_tipo, value="Entrega").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(self.tipo_frame, text="Retirada", variable=self.var_tipo, value="Retirada").pack(side=tk.LEFT)
        
        return frame
    
    def _create_step2(self):
        """Etapa 2: Dados do produto"""
        frame = ttk.Frame(self.steps_container)
        
        # Produto
        ttk.Label(frame, text="Nome do Produto:").pack(anchor="w", pady=(0, 5))
        self.text_produto = tk.Text(frame, height=3, font=("Arial", 11), wrap=tk.WORD)
        self.text_produto.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder_text(self.text_produto, "Ex.: Buquê 12 rosas vermelhas")
        
        # Flores e cor
        ttk.Label(frame, text="Flores e Cor:").pack(anchor="w", pady=(0, 5))
        self.text_flores = tk.Text(frame, height=3, font=("Arial", 11), wrap=tk.WORD)
        self.text_flores.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder_text(self.text_flores, "Ex.: 12 rosas vermelhas, gipsófilas brancas")
        
        # Valor
        ttk.Label(frame, text="Valor Total (R$):").pack(anchor="w", pady=(0, 5))
        self.entry_valor = tk.Entry(frame, font=("Arial", 11))
        self.entry_valor.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder(self.entry_valor, "Ex.: R$ 120,00")
        self.entry_valor.bind("<KeyRelease>", self._format_currency)
        
        # Data e horário
        datetime_frame = ttk.Frame(frame)
        datetime_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Data
        ttk.Label(datetime_frame, text="Data (DD/MM/YYYY):").pack(anchor="w", pady=(0, 5))
        self.entry_data = tk.Entry(datetime_frame, font=("Arial", 11))
        self.entry_data.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self._add_placeholder(self.entry_data, "Ex.: 15/10/2025")
        self.entry_data.bind("<KeyRelease>", self._format_date)
        
        # Horário
        ttk.Label(datetime_frame, text="Horário (HH:MM):").pack(anchor="w", pady=(0, 5))
        self.entry_horario = tk.Entry(datetime_frame, font=("Arial", 11))
        self.entry_horario.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self._add_placeholder(self.entry_horario, "Ex.: 14:30")
        self.entry_horario.bind("<KeyRelease>", self._format_time)
        
        return frame
    
    def _create_step3(self):
        """Etapa 3: Logística de entrega (condicional)"""
        frame = ttk.Frame(self.steps_container)
        
        # Endereço
        ttk.Label(frame, text="Endereço Completo:").pack(anchor="w", pady=(0, 5))
        self.text_endereco = tk.Text(frame, height=4, font=("Arial", 11), wrap=tk.WORD)
        self.text_endereco.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder_text(self.text_endereco, "Rua, número, complemento, bairro, cidade")
        
        # Observações de entrega
        ttk.Label(frame, text="Observações para Entrega:").pack(anchor="w", pady=(0, 5))
        self.text_obs_entrega = tk.Text(frame, height=3, font=("Arial", 11), wrap=tk.WORD)
        self.text_obs_entrega.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder_text(self.text_obs_entrega, "Ex.: Entregar na portaria / Bater na campainha")
        
        return frame
    
    def _create_step4(self):
        """Etapa 4: Detalhes finais"""
        frame = ttk.Frame(self.steps_container)
        
        # Observações gerais
        ttk.Label(frame, text="Observações Gerais:").pack(anchor="w", pady=(0, 5))
        self.text_obs = tk.Text(frame, height=3, font=("Arial", 11), wrap=tk.WORD)
        self.text_obs.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder_text(self.text_obs, "Observações gerais sobre o pedido")
        
        # Mensagem do cartão
        ttk.Label(frame, text="Mensagem do Cartão:").pack(anchor="w", pady=(0, 5))
        self.text_mensagem = tk.Text(frame, height=4, font=("Arial", 11), wrap=tk.WORD)
        self.text_mensagem.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder_text(self.text_mensagem, "Ex.: Feliz Aniversário! Com carinho, João")
        
        # Forma de pagamento
        ttk.Label(frame, text="Forma de Pagamento:").pack(anchor="w", pady=(0, 5))
        self.entry_pagamento = tk.Entry(frame, font=("Arial", 11))
        self.entry_pagamento.pack(fill=tk.X, pady=(0, 15))
        self._add_placeholder(self.entry_pagamento, "Ex.: Dinheiro / Cartão / PIX")
        
        return frame
    
    def _create_navigation_buttons(self):
        """Cria botões de navegação"""
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botão anterior
        self.btn_previous = ttk.Button(
            button_frame,
            text="← Anterior",
            command=self._previous_step,
            state=tk.DISABLED
        )
        self.btn_previous.pack(side=tk.LEFT)
        
        # Botão próximo/finalizar
        self.btn_next = ttk.Button(
            button_frame,
            text="Próximo →",
            command=self._next_step
        )
        self.btn_next.pack(side=tk.RIGHT)
    
    def _show_step(self, step: int):
        """Mostra etapa específica"""
        # Esconder todas as etapas
        for i, step_frame in enumerate(self.steps):
            if i == step:
                step_frame.pack(fill=tk.BOTH, expand=True)
            else:
                step_frame.pack_forget()
        
        # Atualizar título
        titles = [
            "Passo 1/4 — Dados Pessoais",
            "Passo 2/4 — Dados do Produto", 
            "Passo 3/4 — Logística de Entrega",
            "Passo 4/4 — Detalhes Finais"
        ]
        self.step_title.config(text=titles[step])
        
        # Atualizar botões
        self.btn_previous.config(state=tk.NORMAL if step > 0 else tk.DISABLED)
        
        if step == len(self.steps) - 1:
            self.btn_next.config(text="✓ Finalizar Pedido")
        else:
            self.btn_next.config(text="Próximo →")
        
        # Lógica especial para etapa 3 (logística)
        if step == 2 and hasattr(self, 'var_tipo'):
            tipo = self.var_tipo.get().lower()
            if tipo == "retirada":
                # Pular etapa de logística
                self._next_step()
                return
    
    def _next_step(self):
        """Avança para próxima etapa"""
        if self.current_step < len(self.steps) - 1:
            # Salvar dados da etapa atual
            self._save_current_step_data()
            
            # Avançar
            self.current_step += 1
            
            # Lógica especial para pular etapa 3 se for retirada
            if self.current_step == 2 and hasattr(self, 'var_tipo'):
                tipo = self.var_tipo.get().lower()
                if tipo == "retirada":
                    self.current_step += 1
            
            self._show_step(self.current_step)
        else:
            # Finalizar pedido
            self._finalize_pedido()
    
    def _previous_step(self):
        """Volta para etapa anterior"""
        if self.current_step > 0:
            # Salvar dados da etapa atual
            self._save_current_step_data()
            
            # Voltar
            self.current_step -= 1
            
            # Lógica especial para pular etapa 3 se for retirada
            if self.current_step == 2 and hasattr(self, 'var_tipo'):
                tipo = self.var_tipo.get().lower()
                if tipo == "retirada":
                    self.current_step -= 1
            
            self._show_step(self.current_step)
    
    def _save_current_step_data(self):
        """Salva dados da etapa atual"""
        if self.current_step == 0:  # Dados pessoais
            self.data.update({
                "cliente": self._get_entry_value(self.entry_cliente),
                "telefone_cliente": self._get_entry_value(self.entry_telefone),
                "destinatario": self._get_entry_value(self.entry_destinatario),
                "tipo_pedido": self.var_tipo.get()
            })
        elif self.current_step == 1:  # Dados do produto
            self.data.update({
                "produto": self._get_text_value(self.text_produto),
                "flores_cor": self._get_text_value(self.text_flores),
                "valor": self._get_entry_value(self.entry_valor),
                "data": self._get_entry_value(self.entry_data),
                "horario": self._get_entry_value(self.entry_horario)
            })
        elif self.current_step == 2:  # Logística
            self.data.update({
                "endereco": self._get_text_value(self.text_endereco),
                "obs_entrega": self._get_text_value(self.text_obs_entrega)
            })
        elif self.current_step == 3:  # Detalhes finais
            self.data.update({
                "obs": self._get_text_value(self.text_obs),
                "mensagem": self._get_text_value(self.text_mensagem),
                "pagamento": self._get_entry_value(self.entry_pagamento)
            })
    
    def _finalize_pedido(self):
        """Finaliza criação do pedido"""
        try:
            # Salvar dados da etapa atual
            self._save_current_step_data()
            
            # Validações obrigatórias
            if not self._validate_required_fields():
                return
            
            # Preparar dados finais
            pedido_data = self._prepare_pedido_data()
            
            # Chamar callback
            self.on_created_callback(pedido_data)
            
        except Exception as e:
            logger.error(f"Erro ao finalizar pedido: {e}")
            messagebox.showerror("Erro", f"Erro ao finalizar pedido: {e}")
    
    def _validate_required_fields(self) -> bool:
        """Valida campos obrigatórios"""
        # Telefone obrigatório
        if not self.data.get("telefone_cliente", "").strip():
            messagebox.showerror("Erro", "O campo 'Telefone do Cliente' é obrigatório.")
            self._show_step(0)
            return False
        
        # Destinatário obrigatório
        if not self.data.get("destinatario", "").strip():
            messagebox.showerror("Erro", "O campo 'Destinatário' é obrigatório.")
            self._show_step(0)
            return False
        
        # Data obrigatória
        data = self.data.get("data", "").strip()
        if not data or not self._validate_date(data):
            messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/YYYY.")
            self._show_step(1)
            return False
        
        # Horário obrigatório
        horario = self.data.get("horario", "").strip()
        if not horario or not self._validate_time(horario):
            messagebox.showerror("Erro", "Horário inválido. Use o formato HH:MM.")
            self._show_step(1)
            return False
        
        return True
    
    def _prepare_pedido_data(self) -> Dict[str, Any]:
        """Prepara dados finais do pedido"""
        # Obter próximo número de pedido
        from app.core.database import DatabaseManager
        db = DatabaseManager()
        pedido_num = db.get_next_pedido_num()
        
        # Converter data para formato ISO
        data_iso = self._convert_date_to_iso(self.data.get("data", ""))
        
        # Preparar dados
        pedido_data = {
            "pedido_num": pedido_num,
            "cliente": self.data.get("cliente", ""),
            "telefone_cliente": self.data.get("telefone_cliente", ""),
            "destinatario": self.data.get("destinatario", ""),
            "tipo_pedido": self.data.get("tipo_pedido", "Entrega"),
            "produto": self.data.get("produto", ""),
            "flores_cor": self.data.get("flores_cor", ""),
            "obs_entrega": self.data.get("obs_entrega", ""),
            "mensagem": self.data.get("mensagem", ""),
            "valor_text": self.data.get("valor", ""),
            "pagamento": self.data.get("pagamento", ""),
            "endereco": self.data.get("endereco", ""),
            "data_entrega": data_iso,
            "hora_entrega": self.data.get("horario", ""),
            "obs": self.data.get("obs", ""),
            "status": "pendente",
            "quantidade": 1  # Padrão
        }
        
        return pedido_data
    
    def _get_entry_value(self, entry: tk.Entry) -> str:
        """Obtém valor de Entry limpando placeholder"""
        value = entry.get().strip()
        placeholder = getattr(entry, "placeholder", "")
        return "" if value == placeholder else value
    
    def _get_text_value(self, text: tk.Text) -> str:
        """Obtém valor de Text limpando placeholder"""
        value = text.get("1.0", tk.END).strip()
        placeholder = getattr(text, "placeholder", "")
        return "" if value == placeholder else value
    
    def _add_placeholder(self, entry: tk.Entry, placeholder: str):
        """Adiciona placeholder a Entry"""
        entry.placeholder = placeholder
        entry.insert(0, placeholder)
        entry.config(fg="gray")
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="black")
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg="gray")
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    
    def _add_placeholder_text(self, text: tk.Text, placeholder: str):
        """Adiciona placeholder a Text"""
        text.placeholder = placeholder
        text.insert("1.0", placeholder)
        text.config(fg="gray")
        
        def on_focus_in(event):
            if text.get("1.0", tk.END).strip() == placeholder:
                text.delete("1.0", tk.END)
                text.config(fg="black")
        
        def on_focus_out(event):
            if not text.get("1.0", tk.END).strip():
                text.insert("1.0", placeholder)
                text.config(fg="gray")
        
        text.bind("<FocusIn>", on_focus_in)
        text.bind("<FocusOut>", on_focus_out)
    
    def _format_currency(self, event):
        """Formata valor monetário em tempo real"""
        # Implementação simplificada - pode ser expandida
        pass
    
    def _format_date(self, event):
        """Formata data em tempo real"""
        # Implementação simplificada - pode ser expandida
        pass
    
    def _format_time(self, event):
        """Formata horário em tempo real"""
        # Implementação simplificada - pode ser expandida
        pass
    
    def _validate_date(self, date_str: str) -> bool:
        """Valida formato de data"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    def _validate_time(self, time_str: str) -> bool:
        """Valida formato de horário"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    def _convert_date_to_iso(self, date_str: str) -> str:
        """Converte data DD/MM/YYYY para YYYY-MM-DD"""
        try:
            dt = datetime.strptime(date_str, "%d/%m/%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return ""