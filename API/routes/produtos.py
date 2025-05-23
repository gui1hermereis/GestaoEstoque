from flask import Blueprint, request, jsonify
from models.db_models import db, Produto, PrateleiraProduto, Alertas

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route("/produtos", methods=["POST"])
def cadastrar():
    try:
        data = request.json
        marca = data.get('marca')
        nome = data.get('nome')
        descricao = data.get('descricao')
        peso = data.get('peso')
        preco_unidade = data.get('preco_unidade')

        if not marca or not nome or not descricao or not peso or not preco_unidade:
            return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400
        
        produto_existente = Produto.query.filter_by(marca=marca, nome=nome).first()
        if produto_existente:
            return jsonify({'success': False, 'message': 'Produto já cadastrado com essa combinação de nome e marca.'}), 400
        
        new_prod = Produto(
            marca=marca, 
            nome=nome, 
            descricao=descricao, 
            peso=peso,
            preco_unidade=preco_unidade
        )
        
        db.session.add(new_prod)
        db.session.commit()
    
        return jsonify({'success': True, 'message': 'Produto registrado com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no servidor: {str(e)}'}), 500

@produtos_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
def editar(produto_id):
    try:
        data = request.json
        marca = data.get('marca')
        nome = data.get('nome')
        descricao = data.get('descricao')
        peso = data.get('peso')
        preco_unidade = data.get('preco_unidade')

        if not marca or not nome or not descricao or not peso or not preco_unidade:
            return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400

        produto = Produto.query.get(produto_id)
        if not produto:
            return jsonify({'success': False, 'message': 'Produto não encontrado.'}), 404
        
        if produto.nome != nome or produto.marca != marca:
            produto_existente = Produto.query.filter_by(marca=marca, nome=nome).filter(Produto.id != produto_id).first()
            if produto_existente:
                return jsonify({'success': False, 'message': 'Produto já cadastrado com essa combinação de nome e marca.'}), 400

        produto.marca = marca
        produto.nome = nome
        produto.descricao = descricao
        produto.peso = peso
        produto.preco_unidade = preco_unidade

        prateleira_produto = PrateleiraProduto.query.filter_by(produto_id=produto_id).first()

        if prateleira_produto:
            prateleira_produto.preco_total = prateleira_produto.quantidade * int(preco_unidade)
            prateleira_produto.peso_atual = prateleira_produto.quantidade * int(peso)

            print(prateleira_produto.preco_total)
            print(prateleira_produto.peso_atual)

        db.session.commit()

        return jsonify({'success': True, 'message': 'Produto atualizado com sucesso.'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no servidor: {str(e)}'}), 500


@produtos_bp.route('/produtos', methods=['GET'])
def listar():
    try:
        produtos = Produto.query.filter_by(ativo=True).order_by(Produto.id.desc()).all()

        produtos_lista = [{
            'id': produto.id,
            'marca': produto.marca,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'peso': produto.peso,
            'preco_unidade': produto.preco_unidade
        } for produto in produtos]

        return jsonify({'success': True, 'produtos': produtos_lista})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao buscar produtos: {str(e)}'}), 500
    

@produtos_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
def desativar_produto(produto_id):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            return jsonify({'success': False, 'message': 'Produto não encontrado.'}), 404

        produto.ativo = False  
        PrateleiraProduto.query.filter_by(produto_id=produto_id).delete()

        db.session.commit()

        return jsonify({'success': True, 'message': 'Produto desativado com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao desativar produto: {str(e)}'}), 500
