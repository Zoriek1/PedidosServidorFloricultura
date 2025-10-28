# -*- coding: utf-8 -*-
"""
Rotas da API REST
Mantém compatibilidade 100% com PDFgen.py existente
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models import Pedido
from datetime import datetime
import re

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    """
    Cria novo pedido via API (usado pelo cliente desktop PDFgen.py)
    COMPATIBILIDADE TOTAL: Aceita formato antigo e novo
    """
    try:
        data = request.get_json()
        
        # Verificação inicial de dados
        if not data:
            return jsonify({'error': 'Nenhum dado fornecido'}), 400
        
        # Extração de dados do JSON (suporta múltiplos formatos)
        cliente = data.get('cliente', '').strip()
        produto = data.get('produto', '').strip()
        quantidade_raw = data.get('quantidade', 1)
        
        # Suporte para múltiplos nomes de campo (compatibilidade)
        horario = data.get('horario', data.get('hora_entrega', '')).strip()
        dia_entrega_str = data.get('dia_entrega', data.get('data_entrega', '')).strip()
        
        destinatario = data.get('destinatario', '').strip()
        mensagem = data.get('mensagem', '').strip()
        
        # Campos novos (opcionais)
        telefone_cliente = data.get('telefone_cliente', data.get('telefone', '')).strip()
        tipo_pedido = data.get('tipo_pedido', 'Entrega')
        endereco = data.get('endereco', '').strip()
        observacoes = data.get('observacoes', '').strip()
        
        # Validação de campos obrigatórios
        campos_obrigatorios = {
            'cliente': cliente,
            'produto': produto,
            'horario': horario,
            'dia_entrega': dia_entrega_str,
            'destinatario': destinatario
        }
        
        campos_faltantes = [campo for campo, valor in campos_obrigatorios.items() if not valor]
        if campos_faltantes:
            return jsonify({
                'error': f'Campos obrigatórios ausentes: {", ".join(campos_faltantes)}',
                'campos_enviados': list(data.keys())
            }), 400
        
        # Conversão de quantidade para inteiro
        try:
            if isinstance(quantidade_raw, str):
                quantidade_raw = quantidade_raw.strip()
            quantidade = int(quantidade_raw) if quantidade_raw and str(quantidade_raw).strip() else 1
            if quantidade < 0:
                quantidade = 1
        except (ValueError, TypeError):
            quantidade = 1
        
        # Validação de formato de horário (HH:MM)
        if not re.match(r'^([01]?\d|2[0-3]):[0-5]\d$', horario):
            return jsonify({
                'error': 'Formato de horário inválido',
                'horario_recebido': horario,
                'formato_esperado': 'HH:MM (ex: 14:30)'
            }), 400
        
        # Conversão de data de entrega
        try:
            dia_entrega = datetime.strptime(dia_entrega_str, '%Y-%m-%d').date()
        except ValueError as e:
            return jsonify({
                'error': 'Formato de data inválido',
                'data_recebida': dia_entrega_str,
                'formato_esperado': 'YYYY-MM-DD (ex: 2024-12-25)',
                'detalhes': str(e)
            }), 400
        
        # Criar instância do pedido
        pedido = Pedido(
            cliente=cliente,
            produto=produto,
            quantidade=quantidade,
            horario=horario,
            dia_entrega=dia_entrega,
            destinatario=destinatario,
            mensagem=mensagem if mensagem else None,
            telefone_cliente=telefone_cliente if telefone_cliente else None,
            tipo_pedido=tipo_pedido,
            endereco=endereco if endereco else None,
            observacoes=observacoes if observacoes else None,
            status='agendado'
        )
        
        # Inserir no banco de dados
        db.session.add(pedido)
        db.session.commit()
        
        # Resposta de sucesso (formato compatível)
        return jsonify({
            'success': True,
            'pedido_id': pedido.id,
            'message': 'Pedido recebido e armazenado com sucesso',
            'dados_armazenados': {
                'id': pedido.id,
                'cliente': pedido.cliente,
                'produto': pedido.produto,
                'quantidade': pedido.quantidade,
                'destinatario': pedido.destinatario,
                'dia_entrega': pedido.dia_entrega.strftime('%Y-%m-%d'),
                'horario': pedido.horario,
                'status': pedido.status
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Erro interno do servidor',
            'detalhes': str(e)
        }), 500


@api_bp.route('/pedidos', methods=['GET'])
def listar_pedidos():
    """Lista todos os pedidos com filtros opcionais"""
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
        return jsonify({
            'error': 'Erro interno do servidor',
            'detalhes': str(e)
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
        return jsonify({
            'error': 'Pedido não encontrado',
            'detalhes': str(e)
        }), 404


@api_bp.route('/pedidos/<int:pedido_id>/status', methods=['PUT', 'POST'])
def atualizar_status(pedido_id):
    """Atualiza status do pedido"""
    try:
        data = request.get_json() or {}
        novo_status = data.get('status') or request.form.get('status')
        
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
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Status atualizado para {novo_status}',
            'pedido': pedido.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Erro ao atualizar status',
            'detalhes': str(e)
        }), 500


@api_bp.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
def deletar_pedido(pedido_id):
    """Deleta pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        
        db.session.delete(pedido)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido deletado com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Erro ao deletar pedido',
            'detalhes': str(e)
        }), 500


@api_bp.route('/stats', methods=['GET'])
def obter_estatisticas():
    """Retorna estatísticas dos pedidos"""
    try:
        stats = Pedido.get_statistics()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'error': 'Erro ao obter estatísticas',
            'detalhes': str(e)
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
        return jsonify({
            'error': 'Erro ao obter pedidos atrasados',
            'detalhes': str(e)
        }), 500


@api_bp.route('/cleanup', methods=['POST'])
def limpar_pedidos_antigos():
    """Remove pedidos antigos automaticamente"""
    try:
        days = request.json.get('days', 1) if request.json else 1
        count = Pedido.cleanup_old_pedidos(days=days)
        
        return jsonify({
            'success': True,
            'message': f'{count} pedidos antigos removidos',
            'count': count
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao limpar pedidos antigos',
            'detalhes': str(e)
        }), 500

