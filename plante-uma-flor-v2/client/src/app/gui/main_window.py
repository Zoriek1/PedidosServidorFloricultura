# -*- coding: utf-8 -*-
"""
Janela principal otimizada com carregamento lazy
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from app.core.database import DatabaseManager
from app.core.api_client import APIClient
from app.core.pdf_generator import PDFGenerator
from app.gui.forms.pedido_form import PedidoForm
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class MainWindow:
    """Janela principal otimizada"""
    
    def __init__(self, db_manager: DatabaseManager, api_client: APIClient):
        self.db_manager = db_manager
        self.api_client = api_client
        self.pdf_generator = PDFGenerator()
        
        # Configurar janela principal
        self.root = tk.Tk()
        self._setup_window()
        self._setup_styles()
        
        # Criar interface
        self._create_interface()
        
        # Testar conexão com servidor em background
        self._test_server_connection()
    
    def _setup_window(self):
        """Configura janela principal"""
        self.root.title("Plante Uma Flor v2.0 - Gerador de Pedidos")
        self.root.geometry("800x700")
        self.root.minsize(640, 520)
        self.root.configure(bg="#F7F9FB")
        
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")
    
    def _setup_styles(self):
        """Configura estilos da interface"""
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        
        # Configurar estilos customizados
        self.style.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        self.style.configure("TLabel", background="#F7F9FB", foreground="#222222")
        self.style.configure("Title.TLabel", background="#F7F9FB", foreground="#0b5fa5")
        self.style.configure("TButton", padding=8)
    
    def _create_interface(self):
        """Cria interface principal"""
        # Container principal
        self.container = ttk.Frame(self.root, padding=20)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.header = ttk.Label(
            self.container, 
            text="🌺 Plante Uma Flor v2.0",
            style="Title.TLabel",
            font=("Arial", 18, "bold")
        )
        self.header.pack(pady=(0, 20))
        
        # Card principal
        self.card = ttk.Frame(self.container, style="Card.TFrame", padding=20)
        self.card.pack(fill=tk.BOTH, expand=True)
        
        # Status de conexão
        self.status_frame = ttk.Frame(self.card)
        self.status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="🔄 Verificando conexão com servidor...",
            font=("Arial", 10)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Formulário de pedido
        self.pedido_form = PedidoForm(self.card, self._on_pedido_created)
        self.pedido_form.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        self._create_action_buttons()
    
    def _create_action_buttons(self):
        """Cria botões de ação"""
        button_frame = ttk.Frame(self.card)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botão para abrir pasta de saída
        self.btn_open_folder = ttk.Button(
            button_frame,
            text="📁 Abrir Pasta de Saída",
            command=self._open_output_folder
        )
        self.btn_open_folder.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão para exportar CSV
        self.btn_export_csv = ttk.Button(
            button_frame,
            text="📊 Exportar CSV",
            command=self._export_csv
        )
        self.btn_export_csv.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão para testar conexão
        self.btn_test_connection = ttk.Button(
            button_frame,
            text="🔗 Testar Conexão",
            command=self._test_server_connection
        )
        self.btn_test_connection.pack(side=tk.RIGHT)
    
    def _test_server_connection(self):
        """Testa conexão com servidor em background"""
        def test_connection():
            try:
                if self.api_client.test_connection():
                    self.status_label.config(
                        text="✅ Conectado ao servidor",
                        foreground="green"
                    )
                else:
                    self.status_label.config(
                        text="⚠️ Servidor offline - modo local",
                        foreground="orange"
                    )
            except Exception as e:
                self.status_label.config(
                    text="❌ Erro de conexão - modo local",
                    foreground="red"
                )
                logger.warning(f"Erro ao testar conexão: {e}")
        
        # Executar em thread separada para não bloquear UI
        self.root.after(100, test_connection)
    
    def _on_pedido_created(self, pedido_data: Dict[str, Any]):
        """Callback quando pedido é criado"""
        try:
            # Gerar PDF
            pdf_path = self._generate_pdf(pedido_data)
            if not pdf_path:
                return
            
            # Salvar no banco local
            pedido_data['caminho_pdf'] = pdf_path
            pedido_id = self.db_manager.save_pedido(pedido_data)
            
            # Enviar para servidor
            self._send_to_server(pedido_data)
            
            # Mostrar sucesso
            messagebox.showinfo(
                "Sucesso!",
                f"Pedido #{pedido_data.get('pedido_num')} criado com sucesso!\n\n"
                f"PDF: {pdf_path}\n"
                f"ID Local: {pedido_id}"
            )
            
            # Abrir pasta de saída
            self._open_output_folder()
            
            # Fechar aplicação
            self.root.quit()
            
        except Exception as e:
            logger.error(f"Erro ao processar pedido: {e}")
            messagebox.showerror("Erro", f"Erro ao processar pedido: {e}")
    
    def _generate_pdf(self, pedido_data: Dict[str, Any]) -> str:
        """Gera PDF do pedido"""
        try:
            # Criar nome do arquivo
            pedido_num = pedido_data.get('pedido_num', 1)
            data_hoje = datetime.now().strftime('%Y-%m-%d')
            destinatario = pedido_data.get('destinatario', 'Cliente')
            nome_seguro = self._sanitize_filename(destinatario)
            
            nome_arquivo = f"Pedido_{pedido_num:03d}_{data_hoje}_{nome_seguro}.pdf"
            
            # Pasta de saída
            output_dir = Path.home() / "Documents" / "Pedidos-Floricultura"
            output_dir.mkdir(exist_ok=True)
            
            pdf_path = output_dir / nome_arquivo
            
            # Gerar PDF
            if self.pdf_generator.create_pdf(str(pdf_path), pedido_data, pedido_num):
                return str(pdf_path)
            else:
                raise Exception("Falha ao gerar PDF")
                
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")
            return None
    
    def _send_to_server(self, pedido_data: Dict[str, Any]):
        """Envia pedido para servidor"""
        try:
            result = self.api_client.send_pedido(pedido_data)
            if result:
                logger.info(f"Pedido enviado para servidor: {result.get('pedido_id')}")
            else:
                logger.warning("Pedido salvo apenas localmente")
        except Exception as e:
            logger.error(f"Erro ao enviar para servidor: {e}")
    
    def _open_output_folder(self):
        """Abre pasta de saída"""
        try:
            import subprocess
            import platform
            
            output_dir = Path.home() / "Documents" / "Pedidos-Floricultura"
            output_dir.mkdir(exist_ok=True)
            
            if platform.system() == "Windows":
                os.startfile(str(output_dir))
            elif platform.system() == "Darwin":
                subprocess.call(["open", str(output_dir)])
            else:
                subprocess.call(["xdg-open", str(output_dir)])
                
        except Exception as e:
            logger.error(f"Erro ao abrir pasta: {e}")
            messagebox.showwarning("Aviso", f"Não foi possível abrir a pasta automaticamente.\n\nLocal: {output_dir}")
    
    def _export_csv(self):
        """Exporta dados para CSV"""
        try:
            from tkinter import filedialog
            
            output_dir = Path.home() / "Documents" / "Pedidos-Floricultura"
            output_dir.mkdir(exist_ok=True)
            
            csv_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialdir=str(output_dir),
                title="Salvar CSV de pedidos"
            )
            
            if csv_path:
                self.db_manager.export_to_csv(csv_path)
                messagebox.showinfo("Sucesso", f"CSV exportado para:\n{csv_path}")
                
        except Exception as e:
            logger.error(f"Erro ao exportar CSV: {e}")
            messagebox.showerror("Erro", f"Erro ao exportar CSV: {e}")
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitiza nome do arquivo"""
        import re
        safe = re.sub(r"[^A-Za-z0-9 _-]", "", str(filename))
        return safe.replace(" ", "_")[:60]
    
    def run(self):
        """Executa aplicação"""
        try:
            logger.info("Iniciando interface gráfica")
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Erro na interface gráfica: {e}")
            raise
        finally:
            # Limpar recursos
            self.api_client.close()
            logger.info("Aplicação finalizada")