from flask import Blueprint, request, jsonify
from models.db_models import db, Prateleira
from models.db_models import PrateleiraProduto 

prateleiras_bp = Blueprint('prateleiras', __name__)

@prateleiras_bp.route("/prateleiras", methods=["POST"])
def cadastrar():
    try:
        data = request.json
        nome = data.get('nome')
        setor = data.get('setor')

        if not nome or not setor:
            return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400
        
        prateleira_nome_existente = Prateleira.query.filter_by(nome=nome).first()
        if prateleira_nome_existente:
            return jsonify({'success': False, 'message': 'Já existe uma prateleira com esse nome.'}), 400
        
        prateleira_existente = Prateleira.query.filter_by(nome=nome, setor=setor).first()
        if prateleira_existente:
            return jsonify({'success': False, 'message': 'Já existe uma prateleira com esse nome e setor.'}), 400
        
        new_prat = Prateleira(
            nome=nome, 
            setor=setor
        )

        db.session.add(new_prat)
        db.session.commit()
    
        return jsonify({'success': True, 'message': 'Prateleria registrada com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no servidor: {str(e)}'}), 500

@prateleiras_bp.route("/prateleiras/<int:prateleira_id>", methods=["PUT"])
def editar(prateleira_id):
    try:
        data = request.json
        nome = data.get('nome')
        setor = data.get('setor')

        if not nome or not setor:
            return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400

        prateleira = Prateleira.query.get(prateleira_id)
        if not prateleira:
            return jsonify({'success': False, 'message': 'Prateleira não encontrada.'}), 404

        prateleira_nome_existente = Prateleira.query.filter_by(nome=nome).filter(Prateleira.id != prateleira_id).first()
        if prateleira_nome_existente:
            return jsonify({'success': False, 'message': 'Já existe uma prateleira com esse nome.'}), 400
        
        prateleira_existente = Prateleira.query.filter_by(nome=nome, setor=setor).filter(Prateleira.id != prateleira_id).first()
        if prateleira_existente:
            return jsonify({'success': False, 'message': 'Já existe uma prateleira com esse nome e setor.'}), 400

        prateleira.nome = nome
        prateleira.setor = setor

        db.session.commit()

        return jsonify({'success': True, 'message': 'Prateleira atualizada com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no servidor: {str(e)}'}), 500


@prateleiras_bp.route('/prateleiras', methods=['GET'])
def listar():
    try:
        prateleiras = Prateleira.query.filter_by(ativo=True).order_by(Prateleira.id.desc()).all()

        prateleiras_lista = [{
            'id': prateleira.id,
            'nome': prateleira.nome,
            'setor': prateleira.setor,
        } for prateleira in prateleiras]

        return jsonify({'success': True, 'Prateleiras': prateleiras_lista})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao buscar prateleiras: {str(e)}'}), 500
    
@prateleiras_bp.route('/prateleiras/<int:prateleira_id>', methods=['DELETE'])
def desativar_prateleira(prateleira_id):
    try:
        prateleira = Prateleira.query.get(prateleira_id)
        if not prateleira:
            return jsonify({'success': False, 'message': 'Produto não encontrado.'}), 404

        prateleira.ativo = False  
        PrateleiraProduto.query.filter_by(prateleira_id=prateleira_id).delete()

        db.session.commit()

        return jsonify({'success': True, 'message': 'Prateleira desativada com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao desativar prateleira: {str(e)}'}), 500
