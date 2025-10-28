# -*- coding: utf-8 -*-
"""
Rotas da API REST
"""
from flask import Blueprint, request, jsonify, current_app
from app.models.pedido import Pedido
from app.utils.auth import require_api_auth, block_web_creation
from app.utils.logger import setup_logger
from datetime import datetime
import re

api_bp = Blueprint('api', __name__)
logger = setup_logger(__name__)

@api_bp.route('/pedidos', methods=['POST'])
@require_api_auth
def criar_pedido():
    """Cria novo pedido via API (apenas para cliente desktop)"""
    try:
        data = request.get_json()
        
        # Verificação inicial de dados
        if not data:
            return jsonify({'error': 'Nenhum dado fornecido'}), 400
        
        # Extrair e validar dados
        pedido_data = _validate_pedido_data(data)
        if 'error' in pedido_data:
            return jsonify(pedido_data), 400
        
        # Criar pedido
        pedido = Pedido(
            cliente=pedido_data['cliente'],
            produto=pedido_data['produto'],
            quantidade=pedido_data['quantidade'],
            horario=pedido_data['horario'],
            dia_entrega=pedido_data['dia_entrega'],
            destinatario=pedido_data['destinatario'],
            mensagem=pedido_data.get('mensagem'),
            telefone_cliente=pedido_data.get('telefone_cliente'),
            tipo_pedido=pedido_data.get('tipo_pedido', 'Entrega'),
            endereco=pedido_data.get('endereco'),
            observacoes=pedido_data.get('observacoes')
        )
        
        # Salvar no banco
        from app import db
        db.session.add(pedido)
        db.session.commit()
        
        logger.info(f"Pedido {pedido.id} criado via API")
        
        return jsonify({
            'success': True,
            'pedido_id': pedido.id,
            'message': 'Pedido criado com sucesso',
            'data': pedido.to_dict()
        }), 201
        
    except Exception as e:
        from app import db
        db.session.rollback()
        logger.error(f"Erro ao criar pedido via API: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@api_bp.route('/pedidos', methods=['GET'])
def listar_pedidos():
    """Lista todos os pedidos"""
    try:
        # Parâmetros de filtro
        status = request.args.get('status')
        limit = request.args.get('limit', type=int)
        
        # Query base
        query = Pedido.query
        
        # Aplicar filtros
        if status:
            query = query.filter(Pedido.status == status)
        
        # Ordenar por data de entrega e horário
        query = query.order_by(Pedido.dia_entrega.asc(), Pedido.horario.asc())
        
        # Aplicar limite
        if limit:
            query = query.limit(limit)
        
        pedidos = query.all()
        
        return jsonify({
            'success': True,
            'count': len(pedidos),
            'pedidos': [p.to_dict() for p in pedidos]
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar pedidos: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@api_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
def obter_pedido(pedido_id):
    """Obtém pedido específico"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        return jsonify({
            'success': True,
            'pedido': pedido.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter pedido {pedido_id}: {e}")
        return jsonify({
            'error': 'Pedido não encontrado',
            'details': str(e)
        }), 404

@api_bp.route('/pedidos/<int:pedido_id>/status', methods=['PUT'])
def atualizar_status(pedido_id):
    """Atualiza status do pedido"""
    try:
        data = request.get_json()
        novo_status = data.get('status')
        
        if not novo_status:
            return jsonify({'error': 'Status não fornecido'}), 400
        
        # Validar status
        status_validos = ['agendado', 'em_producao', 'pronto_entrega', 'em_rota', 'pronto_retirada', 'concluido']
        if novo_status not in status_validos:
            return jsonify({
                'error': 'Status inválido',
                'valid_statuses': status_validos
            }), 400
        
        # Atualizar pedido
        pedido = Pedido.query.get_or_404(pedido_id)
        pedido.status = novo_status
        pedido.updated_at = datetime.utcnow()
        
        from app import db
        db.session.commit()
        
        logger.info(f"Status do pedido {pedido_id} atualizado para {novo_status}")
        
        return jsonify({
            'success': True,
            'message': f'Status atualizado para {novo_status}',
            'pedido': pedido.to_dict()
        })
        
    except Exception as e:
        from app import db
        db.session.rollback()
        logger.error(f"Erro ao atualizar status do pedido {pedido_id}: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@api_bp.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
def deletar_pedido(pedido_id):
    """Deleta pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        
        from app import db
        db.session.delete(pedido)
        db.session.commit()
        
        logger.info(f"Pedido {pedido_id} deletado")
        
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

@api_bp.route('/pedidos/overdue', methods=['GET'])
def pedidos_atrasados():
    """Retorna pedidos atrasados"""
    try:
        overdue_pedidos = Pedido.get_overdue_pedidos()
        
        return jsonify({
            'success': True,
            'count': len(overdue_pedidos),
            'pedidos': [p.to_dict() for p in overdue_pedidos]
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter pedidos atrasados: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@api_bp.route('/cleanup', methods=['POST'])
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

def _validate_pedido_data(data):
    """Valida dados do pedido"""
    # Campos obrigatórios
    required_fields = ['cliente', 'produto', 'horario', 'dia_entrega', 'destinatario']
    
    for field in required_fields:
        if not data.get(field):
            return {'error': f'Campo obrigatório ausente: {field}'}
    
    # Validar horário
    horario = data.get('horario', '').strip()
    if not re.match(r'^([01]?\d|2[0-3]):[0-5]\d$', horario):
        return {'error': 'Formato de horário inválido. Use HH:MM'}
    
    # Validar data
    try:
        dia_entrega = datetime.strptime(data.get('dia_entrega'), '%Y-%m-%d').date()
    except ValueError:
        return {'error': 'Formato de data inválido. Use YYYY-MM-DD'}
    
    # Validar quantidade
    quantidade = data.get('quantidade', 1)
    try:
        quantidade = int(quantidade)
        if quantidade < 0:
            quantidade = 0
    except (ValueError, TypeError):
        quantidade = 1
    
    return {
        'cliente': data.get('cliente', '').strip(),
        'produto': data.get('produto', '').strip(),
        'quantidade': quantidade,
        'horario': horario,
        'dia_entrega': dia_entrega,
        'destinatario': data.get('destinatario', '').strip(),
        'mensagem': data.get('mensagem', '').strip() or None,
        'telefone_cliente': data.get('telefone_cliente', '').strip() or None,
        'tipo_pedido': data.get('tipo_pedido', 'Entrega'),
        'endereco': data.get('endereco', '').strip() or None,
        'observacoes': data.get('observacoes', '').strip() or None
    }