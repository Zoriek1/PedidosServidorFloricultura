# -*- coding: utf-8 -*-
"""
Modelo de dados para pedidos
"""
from datetime import datetime, timedelta
from app import db
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class Pedido(db.Model):
    """Modelo de dados para pedidos da floricultura"""
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    produto = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(30), default='agendado')
    horario = db.Column(db.String(10), nullable=False)  # HH:MM
    dia_entrega = db.Column(db.Date, nullable=False)
    destinatario = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Campos adicionais para compatibilidade
    telefone_cliente = db.Column(db.String(20), nullable=True)
    tipo_pedido = db.Column(db.String(20), default='Entrega')
    endereco = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Pedido {self.id} - {self.cliente}>'
    
    def to_dict(self):
        """Converte o pedido para dicionário"""
        return {
            'id': self.id,
            'cliente': self.cliente,
            'produto': self.produto,
            'quantidade': self.quantidade,
            'status': self.status,
            'horario': self.horario,
            'dia_entrega': self.dia_entrega.strftime('%Y-%m-%d'),
            'destinatario': self.destinatario,
            'mensagem': self.mensagem or '',
            'telefone_cliente': self.telefone_cliente or '',
            'tipo_pedido': self.tipo_pedido or 'Entrega',
            'endereco': self.endereco or '',
            'observacoes': self.observacoes or '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def is_overdue(self):
        """Verifica se o pedido está atrasado"""
        if not self.dia_entrega or not self.horario:
            return False
        
        try:
            # Combinar data e horário
            delivery_datetime = datetime.combine(
                self.dia_entrega,
                datetime.strptime(self.horario, '%H:%M').time()
            )
            
            # Verificar se está atrasado
            return delivery_datetime < datetime.now()
        except Exception as e:
            logger.error(f"Erro ao verificar atraso do pedido {self.id}: {e}")
            return False
    
    def is_ready_for_cleanup(self):
        """Verifica se o pedido pode ser removido (concluído há mais de 24h)"""
        if self.status != 'concluido':
            return False
        
        # Verificar se foi concluído há mais de 24 horas
        cleanup_time = self.updated_at + timedelta(hours=24)
        return datetime.utcnow() > cleanup_time
    
    @staticmethod
    def get_overdue_pedidos():
        """Retorna pedidos atrasados"""
        pedidos = Pedido.query.filter(
            Pedido.status.in_(['agendado', 'em_producao', 'pronto_entrega', 'em_rota'])
        ).all()
        
        return [p for p in pedidos if p.is_overdue()]
    
    @staticmethod
    def get_pedidos_ready_for_cleanup():
        """Retorna pedidos prontos para limpeza"""
        return Pedido.query.filter(
            Pedido.status == 'concluido',
            Pedido.updated_at < datetime.utcnow() - timedelta(hours=24)
        ).all()
    
    @staticmethod
    def cleanup_old_pedidos():
        """Remove pedidos antigos automaticamente"""
        try:
            old_pedidos = Pedido.get_pedidos_ready_for_cleanup()
            count = len(old_pedidos)
            
            if count > 0:
                for pedido in old_pedidos:
                    db.session.delete(pedido)
                
                db.session.commit()
                logger.info(f"Removidos {count} pedidos antigos automaticamente")
                return count
            
            return 0
        except Exception as e:
            logger.error(f"Erro ao limpar pedidos antigos: {e}")
            db.session.rollback()
            return 0