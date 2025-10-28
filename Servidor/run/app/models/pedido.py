# -*- coding: utf-8 -*-
"""
Modelo de dados para Pedidos
"""
from app import db
from datetime import datetime, timedelta

class Pedido(db.Model):
    """Modelo expandido de Pedido com todos os campos necessários"""
    __tablename__ = 'pedidos'
    
    # Campos básicos (compatibilidade com versão anterior)
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
    
    # Campos novos (opcionais para compatibilidade)
    telefone_cliente = db.Column(db.String(20), nullable=True)
    tipo_pedido = db.Column(db.String(20), default='Entrega')  # 'Entrega' ou 'Retirada'
    endereco = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Pedido {self.id} - {self.cliente} - {self.status}>'
    
    def to_dict(self):
        """Converte o pedido para dicionário (para API JSON)"""
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
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else ''
        }
    
    def is_overdue(self):
        """Verifica se o pedido está atrasado"""
        if self.status == 'concluido':
            return False
        
        try:
            # Combinar data e hora de entrega
            delivery_datetime = datetime.combine(
                self.dia_entrega,
                datetime.strptime(self.horario, '%H:%M').time()
            )
            return datetime.now() > delivery_datetime
        except Exception:
            return False
    
    @staticmethod
    def get_statistics():
        """Retorna estatísticas dos pedidos"""
        stats = {
            'total': Pedido.query.count(),
            'agendado': Pedido.query.filter_by(status='agendado').count(),
            'em_producao': Pedido.query.filter_by(status='em_producao').count(),
            'pronto_entrega': Pedido.query.filter_by(status='pronto_entrega').count(),
            'em_rota': Pedido.query.filter_by(status='em_rota').count(),
            'pronto_retirada': Pedido.query.filter_by(status='pronto_retirada').count(),
            'concluido': Pedido.query.filter_by(status='concluido').count()
        }
        return stats
    
    @staticmethod
    def get_overdue_pedidos():
        """Retorna pedidos atrasados"""
        all_pedidos = Pedido.query.filter(Pedido.status != 'concluido').all()
        return [p for p in all_pedidos if p.is_overdue()]
    
    @staticmethod
    def cleanup_old_pedidos(days=1):
        """Remove pedidos concluídos há mais de X dias"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        old_pedidos = Pedido.query.filter(
            Pedido.status == 'concluido',
            Pedido.updated_at < cutoff_date
        ).all()
        
        count = len(old_pedidos)
        for pedido in old_pedidos:
            db.session.delete(pedido)
        
        db.session.commit()
        return count

