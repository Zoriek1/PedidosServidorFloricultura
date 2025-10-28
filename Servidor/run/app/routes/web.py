# -*- coding: utf-8 -*-
"""
Rotas Web (Interface HTML)
"""
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app import db
from app.models import Pedido
from datetime import datetime
import re

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    """Página principal - Painel de gestão moderno"""
    try:
        # Buscar todos os pedidos ordenados
        pedidos = Pedido.query.order_by(
            Pedido.dia_entrega.asc(),
            Pedido.horario.asc()
        ).all()
        
        # Estatísticas
        stats = Pedido.get_statistics()
        
        # Pedidos atrasados
        pedidos_atrasados = Pedido.get_overdue_pedidos()
        
        return render_template(
            'painel.html',
            pedidos=pedidos,
            stats=stats,
            pedidos_atrasados=pedidos_atrasados
        )
    except Exception as e:
        print(f"Erro ao carregar painel: {e}")
        return render_template('painel.html', pedidos=[], stats={}, pedidos_atrasados=[])


@web_bp.route('/criar-pedido', methods=['GET', 'POST'])
def criar_pedido():
    """Página de criação de pedido"""
    
    if request.method == 'GET':
        return render_template('criar_pedido.html')
    
    # POST - Processar formulário
    try:
        # Captura dos dados do formulário
        cliente = request.form.get('cliente', '').strip()
        produto = request.form.get('produto', '').strip()
        quantidade_str = request.form.get('quantidade', '1').strip()
        horario = request.form.get('horario', '').strip()
        dia_entrega_str = request.form.get('dia_entrega', '').strip()
        destinatario = request.form.get('destinatario', '').strip()
        mensagem = request.form.get('mensagem', '').strip()
        telefone_cliente = request.form.get('telefone_cliente', '').strip()
        tipo_pedido = request.form.get('tipo_pedido', 'Entrega')
        endereco = request.form.get('endereco', '').strip()
        observacoes = request.form.get('observacoes', '').strip()
        
        # Validação de campos obrigatórios
        if not cliente or not produto or not horario or not dia_entrega_str or not destinatario:
            flash('Todos os campos obrigatórios devem ser preenchidos!', 'error')
            return render_template('criar_pedido.html')
        
        # Conversão de quantidade
        try:
            quantidade = int(quantidade_str) if quantidade_str else 1
            if quantidade < 0:
                quantidade = 1
        except ValueError:
            quantidade = 1
        
        # Conversão de data
        try:
            dia_entrega = datetime.strptime(dia_entrega_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido. Use YYYY-MM-DD', 'error')
            return render_template('criar_pedido.html')
        
        # Validação de horário (formato HH:MM)
        if not re.match(r'^([01]?\d|2[0-3]):[0-5]\d$', horario):
            flash('Formato de horário inválido. Use HH:MM (ex: 14:30)', 'error')
            return render_template('criar_pedido.html')
        
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
        
        # Adicionar ao banco de dados
        db.session.add(pedido)
        db.session.commit()
        
        flash(f'Pedido #{pedido.id} criado com sucesso!', 'success')
        return redirect(url_for('web.index'))
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar pedido: {e}")
        flash(f'Erro ao criar pedido: {str(e)}', 'error')
        return render_template('criar_pedido.html')


@web_bp.route('/pedido/<int:pedido_id>/atualizar-status', methods=['POST'])
def atualizar_status(pedido_id):
    """Atualiza o status de um pedido (AJAX e form)"""
    try:
        novo_status = request.form.get('status') or request.json.get('status') if request.json else 'agendado'
        pedido = Pedido.query.get_or_404(pedido_id)
        pedido.status = novo_status
        pedido.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Resposta AJAX
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': f'Status atualizado para {novo_status}',
                'pedido': pedido.to_dict()
            })
        
        # Resposta form tradicional
        flash(f'Status do pedido #{pedido_id} atualizado para: {novo_status}', 'success')
        return redirect(url_for('web.index'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
        
        flash(f'Erro ao atualizar status: {str(e)}', 'error')
        return redirect(url_for('web.index'))


@web_bp.route('/pedido/<int:pedido_id>/deletar', methods=['POST'])
def deletar_pedido(pedido_id):
    """Deleta um pedido (AJAX e form)"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        db.session.delete(pedido)
        db.session.commit()
        
        # Resposta AJAX
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'Pedido deletado com sucesso'
            })
        
        # Resposta form tradicional
        flash(f'Pedido #{pedido_id} deletado com sucesso!', 'success')
        return redirect(url_for('web.index'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
        
        flash(f'Erro ao deletar pedido: {str(e)}', 'error')
        return redirect(url_for('web.index'))


@web_bp.route('/limpar-antigos', methods=['POST'])
def limpar_antigos():
    """Remove pedidos concluídos há mais de 24 horas"""
    try:
        count = Pedido.cleanup_old_pedidos(days=1)
        
        # Resposta AJAX
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'count': count,
                'message': f'{count} pedidos antigos removidos'
            })
        
        # Resposta form tradicional
        flash(f'{count} pedidos antigos removidos!', 'success')
        return redirect(url_for('web.index'))
        
    except Exception as e:
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
        
        flash(f'Erro ao limpar pedidos: {str(e)}', 'error')
        return redirect(url_for('web.index'))

