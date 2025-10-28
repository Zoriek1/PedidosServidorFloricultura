# -*- coding: utf-8 -*-
"""
Sistema de Gerenciamento de Comandas - Plante Uma Flor
Servidor Flask para gerenciamento de pedidos
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# Configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'plante-uma-flor-secret-key-2024'

db = SQLAlchemy(app)


# Modelo de Pedido
class Pedido(db.Model):
    """Modelo de dados para pedidos da floricultura"""
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    produto = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), default='agendado')
    horario = db.Column(db.String(10), nullable=False)  # HH:MM
    dia_entrega = db.Column(db.Date, nullable=False)
    destinatario = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


# Inicializa o banco de dados
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Página principal com listagem de pedidos"""
    try:
        pedidos = Pedido.query.order_by(Pedido.created_at.desc()).all()
        return render_template('painel_ifood.html', pedidos=pedidos)
    except Exception as e:
        print(f"Erro ao buscar pedidos: {e}")
        return render_template('painel_ifood.html', pedidos=[])


@app.route('/criar-pedido', methods=['GET', 'POST'])
def criar_pedido():
    """Rota para criar novo pedido via formulário"""
    
    if request.method == 'GET':
        return render_template('criar_pedido.html')
    
    # POST - Processar formulário
    try:
        # Captura dos dados do formulário
        cliente = request.form.get('cliente', '').strip()
        produto = request.form.get('produto', '').strip()
        quantidade_str = request.form.get('quantidade', '0').strip()
        horario = request.form.get('horario', '').strip()
        dia_entrega_str = request.form.get('dia_entrega', '').strip()
        destinatario = request.form.get('destinatario', '').strip()
        mensagem = request.form.get('mensagem', '').strip()
        
        # Validação de campos obrigatórios
        if not cliente or not produto or not horario or not dia_entrega_str or not destinatario:
            flash('Todos os campos obrigatórios devem ser preenchidos!', 'error')
            return render_template('criar_pedido.html', 
                                 cliente=cliente, produto=produto, 
                                 destinatario=destinatario, mensagem=mensagem)
        
        # Conversão de quantidade
        try:
            quantidade = int(quantidade_str) if quantidade_str else 0
            if quantidade < 0:
                quantidade = 0
        except ValueError:
            quantidade = 0
        
        # Conversão de mensagem (None se vazia)
        mensagem = mensagem if mensagem else None
        
        # Conversão de data
        try:
            dia_entrega = datetime.strptime(dia_entrega_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido. Use YYYY-MM-DD', 'error')
            return render_template('criar_pedido.html', 
                                 cliente=cliente, produto=produto, 
                                 destinatario=destinatario, mensagem=mensagem)
        
        # Validação de horário (formato HH:MM)
        import re
        if not re.match(r'^([01]?\d|2[0-3]):[0-5]\d$', horario):
            flash('Formato de horário inválido. Use HH:MM (ex: 14:30)', 'error')
            return render_template('criar_pedido.html', 
                                 cliente=cliente, produto=produto, 
                                 destinatario=destinatario, mensagem=mensagem)
        
        # Criar instância do pedido
        pedido = Pedido(
            cliente=cliente,
            produto=produto,
            quantidade=quantidade,
            horario=horario,
            dia_entrega=dia_entrega,
            destinatario=destinatario,
            mensagem=mensagem,
            status='agendado'
        )
        
        # Adicionar ao banco de dados
        db.session.add(pedido)
        db.session.commit()
        
        flash(f'Pedido #{pedido.id} criado com sucesso!', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar pedido: {e}")
        flash(f'Erro ao criar pedido: {str(e)}', 'error')
        return render_template('criar_pedido.html')


@app.route('/api/pedidos', methods=['POST'])
def api_criar_pedido():
    """API para criação de pedidos via JSON (usada pelo cliente desktop PDFgen)"""
    try:
        data = request.get_json()
        
        # Verificação inicial de dados
        if not data:
            return jsonify({'error': 'Nenhum dado fornecido'}), 400
        
        # Extração de dados do JSON
        cliente = data.get('cliente', '').strip()
        produto = data.get('produto', '').strip()
        quantidade_raw = data.get('quantidade', 0)
        horario = data.get('horario', data.get('hora_entrega', '')).strip()
        dia_entrega_str = data.get('dia_entrega', data.get('data_entrega', '')).strip()
        destinatario = data.get('destinatario', '').strip()
        mensagem = data.get('mensagem', '').strip()
        
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
            quantidade = int(quantidade_raw) if quantidade_raw and str(quantidade_raw).strip() else 0
            if quantidade < 0:
                quantidade = 0
        except (ValueError, TypeError) as e:
            return jsonify({
                'error': f'Quantidade inválida: {quantidade_raw}',
                'detalhes': str(e)
            }), 400
        
        # Conversão de mensagem (None se vazia)
        mensagem = mensagem if mensagem else None
        
        # Validação de formato de horário (HH:MM)
        import re
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
        try:
            pedido = Pedido(
                cliente=cliente,
                produto=produto,
                quantidade=quantidade,
                horario=horario,
                dia_entrega=dia_entrega,
                destinatario=destinatario,
                mensagem=mensagem,
                status='agendado'
            )
            
            # Inserir no banco de dados
            db.session.add(pedido)
            db.session.commit()
            
            # Resposta de sucesso
            return jsonify({
                'success': True,
                'pedido_id': pedido.id,
                'message': 'Pedido recebido e armazenado com sucesso',
                'dados_armazenados': {
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
                'error': 'Erro ao inserir pedido no banco de dados',
                'detalhes': str(e)
            }), 500
        
    except Exception as e:
        # Erro geral não previsto
        return jsonify({
            'error': 'Erro interno do servidor',
            'detalhes': str(e)
        }), 500


@app.route('/pedido/<int:pedido_id>/atualizar-status', methods=['POST'])
def atualizar_status(pedido_id):
    """Atualiza o status de um pedido"""
    try:
        novo_status = request.form.get('status', 'agendado')
        pedido = Pedido.query.get_or_404(pedido_id)
        pedido.status = novo_status
        db.session.commit()
        flash(f'Status do pedido #{pedido_id} atualizado para: {novo_status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar status: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/pedido/<int:pedido_id>/deletar', methods=['POST'])
def deletar_pedido(pedido_id):
    """Deleta um pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        db.session.delete(pedido)
        db.session.commit()
        flash(f'Pedido #{pedido_id} deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar pedido: {str(e)}', 'error')
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

