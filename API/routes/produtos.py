from flask import Blueprint, request, jsonify
from models.db_models import db, Produto
from models.db_models import PrateleiraProduto 

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

        produto.marca = marca
        produto.nome = nome
        produto.descricao = descricao
        produto.peso = peso
        produto.preco_unidade = preco_unidade

        prateleira_produtos = PrateleiraProduto.query.filter_by(produto_id=produto_id).all()
        for prateleira_produto in prateleira_produtos:
            prateleira_produto.preco_total = prateleira_produto.quantidade * preco_unidade
            prateleira_produto.peso_atual = prateleira_produto.quantidade * peso

        db.session.commit()

        return jsonify({'success': True, 'message': 'Produto atualizado com sucesso.'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no servidor: {str(e)}'}), 500


@produtos_bp.route('/produtos', methods=['GET'])
def listar():
    try:
        produtos = Produto.query.all()

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
def deletar(produto_id):
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            return jsonify({'success': False, 'message': 'Produto não encontrado.'}), 404

        PrateleiraProduto.query.filter_by(produto_id=produto_id).delete()

        db.session.delete(produto)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Produto deletado com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao deletar produto: {str(e)}'}), 500
