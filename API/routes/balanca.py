from flask import Blueprint, request, jsonify
from models.db_models import db, Produto, Prateleira, PrateleiraProduto, HistoricoMovimentacao, Alertas
from routes.alertas import verificar_alerta


balanca_bp = Blueprint('balanca', __name__)

@balanca_bp.route("/balanca/adicionar_produto", methods=["POST"])
def adicionar_produto():
    try:
        data = request.json
        produto_id = data.get('produto_id')
        prateleira_id = data.get('prateleira_id')
        quantidade_adicionada = data.get('quantidade')
        
        if not produto_id or not prateleira_id or not quantidade_adicionada:
            return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400
        
        produto = Produto.query.get(produto_id)
        prateleira_produto = PrateleiraProduto.query.filter_by(produto_id=produto_id, prateleira_id=prateleira_id).first()
        
        if not produto:
            return jsonify({'success': False, 'message': 'Produto não encontrado.'}), 404
        if not prateleira_produto:
            return jsonify({'success': False, 'message': 'Produto não está registrado nesta prateleira.'}), 404
        
        peso_por_unidade = produto.peso  
        peso_atual_adicionado = peso_por_unidade * quantidade_adicionada

        preco_total = produto.preco_unidade * quantidade_adicionada

        prateleira_produto.quantidade += quantidade_adicionada
        prateleira_produto.peso_atual += peso_atual_adicionado
        prateleira_produto.preco_total += preco_total  

        historico = HistoricoMovimentacao(
            produto_id=produto_id,
            prateleira_id=prateleira_id,
            tipo_movimentacao='entrada',
            quantidade=quantidade_adicionada,
            preco_total=preco_total
        )


        db.session.add(historico)
        db.session.commit()
        
        verificar_alerta(produto_id, prateleira_id, 'entrada')

        return jsonify({'success': True, 'message': 'Produto adicionado com sucesso.', 'peso_atual': prateleira_produto.peso_atual})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no servidor: {str(e)}'}), 500
    
@balanca_bp.route("/balanca/retirar_produto", methods=["POST"])
def retirar_produto():
    try:
        data = request.json
        produto_id = data.get('produto_id')
        prateleira_id = data.get('prateleira_id')
        quantidade_retirada = data.get('quantidade')
        
        if not produto_id or not prateleira_id or not quantidade_retirada:
            return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400
        
        produto = Produto.query.get(produto_id)
        prateleira_produto = PrateleiraProduto.query.filter_by(produto_id=produto_id, prateleira_id=prateleira_id).first()

        if not produto:
            return jsonify({'success': False, 'message': 'Produto não encontrado.'}), 404
        if not prateleira_produto:
            return jsonify({'success': False, 'message': 'Produto não está registrado nesta prateleira.'}), 404
        
        if prateleira_produto.quantidade == 0:
            return jsonify({'success': False, 'message': 'Não é possível retirar essa quantidade de produtos.'}), 400

        peso_por_unidade = produto.peso  
        peso_atual_retirado = peso_por_unidade * quantidade_retirada

        preco_total = produto.preco_unidade * quantidade_retirada

        prateleira_produto.quantidade -= quantidade_retirada
        prateleira_produto.peso_atual -= peso_atual_retirado
        prateleira_produto.preco_total -= preco_total

        historico = HistoricoMovimentacao(
            produto_id=produto_id,
            prateleira_id=prateleira_id,
            tipo_movimentacao='saida',
            quantidade=quantidade_retirada,
            preco_total=preco_total
        )

        db.session.add(historico)
        db.session.commit()

        verificar_alerta(produto_id, prateleira_id, 'saida')
        
        return jsonify({'success': True, 'message': 'Produto retirado com sucesso.', 'peso_atual': prateleira_produto.peso_atual})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no servidor: {str(e)}'}), 500