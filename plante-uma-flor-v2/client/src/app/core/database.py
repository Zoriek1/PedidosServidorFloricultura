# -*- coding: utf-8 -*-
"""
Gerenciador de banco de dados otimizado
"""
import sqlite3
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class DatabaseManager:
    """Gerenciador de banco de dados com conexões otimizadas"""
    
    def __init__(self):
        self.db_path = self._get_db_path()
        self._connection = None
        self._init_database()
    
    def _get_db_path(self) -> Path:
        """Retorna caminho do banco de dados"""
        # Usar Documents/Pedidos-Floricultura por padrão
        docs_path = Path.home() / "Documents" / "Pedidos-Floricultura"
        docs_path.mkdir(parents=True, exist_ok=True)
        return docs_path / "pedidos.db"
    
    def _init_database(self):
        """Inicializa banco de dados se não existir"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
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
                
                # Índices para performance
                conn.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_data ON pedidos(data_entrega)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_dest ON pedidos(destinatario)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_status ON pedidos(status)")
                
                conn.commit()
                logger.info("Banco de dados inicializado com sucesso")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar banco de dados: {e}")
            raise
    
    def get_connection(self):
        """Retorna conexão com o banco (context manager)"""
        return sqlite3.connect(
            str(self.db_path),
            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
        )
    
    def save_pedido(self, pedido_data: Dict) -> int:
        """Salva pedido no banco de dados"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO pedidos (
                        pedido_num, cliente, telefone_cliente, destinatario, tipo_pedido,
                        produto, flores_cor, obs_entrega, mensagem, valor_cents, valor_text,
                        pagamento, endereco, data_entrega, hora_entrega, obs, caminho_pdf, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pedido_data.get('pedido_num'),
                    pedido_data.get('cliente'),
                    pedido_data.get('telefone_cliente'),
                    pedido_data.get('destinatario'),
                    pedido_data.get('tipo_pedido'),
                    pedido_data.get('produto'),
                    pedido_data.get('flores_cor'),
                    pedido_data.get('obs_entrega'),
                    pedido_data.get('mensagem'),
                    pedido_data.get('valor_cents'),
                    pedido_data.get('valor_text'),
                    pedido_data.get('pagamento'),
                    pedido_data.get('endereco'),
                    pedido_data.get('data_entrega'),
                    pedido_data.get('hora_entrega'),
                    pedido_data.get('obs'),
                    pedido_data.get('caminho_pdf'),
                    pedido_data.get('status', 'pendente')
                ))
                
                conn.commit()
                pedido_id = cursor.lastrowid
                logger.info(f"Pedido {pedido_data.get('pedido_num')} salvo com ID {pedido_id}")
                return pedido_id
                
        except sqlite3.IntegrityError as e:
            logger.error(f"Erro de integridade ao salvar pedido: {e}")
            raise ValueError(f"Pedido Nº {pedido_data.get('pedido_num')} já existe no banco de dados")
        except Exception as e:
            logger.error(f"Erro ao salvar pedido: {e}")
            raise
    
    def get_next_pedido_num(self) -> int:
        """Retorna próximo número de pedido"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(pedido_num) FROM pedidos")
                result = cursor.fetchone()
                return (result[0] or 0) + 1
        except Exception as e:
            logger.error(f"Erro ao obter próximo número de pedido: {e}")
            return 1
    
    def export_to_csv(self, csv_path: str):
        """Exporta dados para CSV"""
        try:
            import csv
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pedidos ORDER BY created_at DESC")
                rows = cursor.fetchall()
                cols = [d[0] for d in cursor.description]
                
                with open(csv_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(cols)
                    writer.writerows(rows)
                
                logger.info(f"Dados exportados para {csv_path}")
                
        except Exception as e:
            logger.error(f"Erro ao exportar CSV: {e}")
            raise