# -*- coding: utf-8 -*-
"""
Rotas da interface web (BLOQUEADAS para criação)
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models.pedido import Pedido
from app.utils.auth import block_web_creation
from app.utils.logger import setup_logger
from datetime import datetime, timedelta

web_bp = Blueprint('web', __name__)
logger = setup_logger(__name__)

@web_bp.route('/')
def painel():
    """Painel principal de gestão de pedidos"""
    try:
        # Obter todos os pedidos ordenados por data/hora
        pedidos = Pedido.query.order_by(
            Pedido.dia_entrega.asc(),
            Pedido.horario.asc()
        ).all()
        
        # Separar pedidos por status
        pedidos_por_status = {
            'agendado': [],
            'em_producao': [],
            'pronto_entrega': [],
            'em_rota': [],
            'pronto_retirada': [],
            'concluido': []
        }
        
        for pedido in pedidos:
            status = pedido.status or 'agendado'
            if status in pedidos_por_status:
                pedidos_por_status[status].append(pedido)
        
        # Identificar pedidos atrasados
        pedidos_atrasados = Pedido.get_overdue_pedidos()
        
        # Estatísticas
        stats = {
            'total': len(pedidos),
            'agendado': len(pedidos_por_status['agendado']),
            'em_producao': len(pedidos_por_status['em_producao']),
            'pronto_entrega': len(pedidos_por_status['pronto_entrega']),
            'em_rota': len(pedidos_por_status['em_rota']),
            'pronto_retirada': len(pedidos_por_status['pronto_retirada']),
            'concluido': len(pedidos_por_status['concluido']),
            'atrasados': len(pedidos_atrasados)
        }
        
        return render_template('painel.html',
                             pedidos=pedidos,
                             pedidos_por_status=pedidos_por_status,
                             pedidos_atrasados=pedidos_atrasados,
                             stats=stats)
        
    except Exception as e:
        logger.error(f"Erro ao carregar painel: {e}")
        return render_template('painel.html',
                             pedidos=[],
                             pedidos_por_status={},
                             pedidos_atrasados=[],
                             stats={},
                             error=str(e))

@web_bp.route('/criar-pedido', methods=['GET', 'POST'])
@block_web_creation
def criar_pedido():
    """Criação de pedidos BLOQUEADA via interface web"""
    # Esta rota sempre retorna erro 403
    # O decorator @block_web_creation garante isso
    pass

@web_bp.route('/pedido/<int:pedido_id>/atualizar-status', methods=['POST'])
def atualizar_status(pedido_id):
    """Atualiza status do pedido"""
    try:
        novo_status = request.form.get('status')
        
        if not novo_status:
            return jsonify({'error': 'Status não fornecido'}), 400
        
        # Validar status
        status_validos = ['agendado', 'em_producao', 'pronto_entrega', 'em_rota', 'pronto_retirada', 'concluido']
        if novo_status not in status_validos:
            return jsonify({'error': 'Status inválido'}), 400
        
        # Atualizar pedido
        pedido = Pedido.query.get_or_404(pedido_id)
        pedido.status = novo_status
        pedido.updated_at = datetime.utcnow()
        
        from app import db
        db.session.commit()
        
        logger.info(f"Status do pedido {pedido_id} atualizado para {novo_status}")
        
        return jsonify({
            'success': True,
            'message': f'Status atualizado para {novo_status}'
        })
        
    except Exception as e:
        from app import db
        db.session.rollback()
        logger.error(f"Erro ao atualizar status do pedido {pedido_id}: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@web_bp.route('/pedido/<int:pedido_id>/deletar', methods=['POST'])
def deletar_pedido(pedido_id):
    """Deleta pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        
        from app import db
        db.session.delete(pedido)
        db.session.commit()
        
        logger.info(f"Pedido {pedido_id} deletado via interface web")
        
        return jsonify({
            'success': True,
            'message': 'Pedido deletado com sucesso'
        })
        
    except Exception as e:
        from app import db
        db.session.rollback()
        logger.error(f"Erro ao deletar pedido {pedido_id}: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@web_bp.route('/pedidos/atrasados')
def pedidos_atrasados():
    """Página de pedidos atrasados"""
    try:
        pedidos_atrasados = Pedido.get_overdue_pedidos()
        
        return render_template('pedidos_atrasados.html',
                             pedidos_atrasados=pedidos_atrasados)
        
    except Exception as e:
        logger.error(f"Erro ao carregar pedidos atrasados: {e}")
        return render_template('pedidos_atrasados.html',
                             pedidos_atrasados=[],
                             error=str(e))

@web_bp.route('/limpar-antigos', methods=['POST'])
def limpar_pedidos_antigos():
    """Remove pedidos antigos automaticamente"""
    try:
        count = Pedido.cleanup_old_pedidos()
        
        return jsonify({
            'success': True,
            'message': f'{count} pedidos antigos removidos',
            'count': count
        })
        
    except Exception as e:
        logger.error(f"Erro ao limpar pedidos antigos: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@web_bp.route('/api/pedidos', methods=['POST'])
@block_web_creation
def api_criar_pedido():
    """Endpoint API para criação - BLOQUEADO via web"""
    # Esta rota sempre retorna erro 403
    # O decorator @block_web_creation garante isso
    pass