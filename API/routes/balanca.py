from flask import Blueprint, request, jsonify
from models.db_models import db, Produto, Prateleira, PrateleiraProduto, HistoricoMovimentacao, Alertas
from routes.alertas import verificar_alerta

balanca_bp = Blueprint('balanca', __name__)

def emular_sensor(produto_id, quantidade):
    produto = Produto.query.get(produto_id)
    if not produto:
        raise ValueError("Produto não encontrado.")
    peso_prod = produto.peso
    peso_total_balanca = peso_prod * quantidade
    return peso_total_balanca


@balanca_bp.route("/balanca/adicionar_produto", methods=["POST"])
def adicionar_produto():
    try:
        data = request.json
        produto_id = data.get('produto_id')
        prateleira_id = data.get('prateleira_id')
        quantidade_adicionada = data.get('quantidade')
             
        if not produto_id or not prateleira_id or not quantidade_adicionada:
            return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400
        
        peso_total_balanca = emular_sensor(produto_id, quantidade_adicionada)   

        produto = Produto.query.get(produto_id)
        prateleira_produto = PrateleiraProduto.query.filter_by(produto_id=produto_id, prateleira_id=prateleira_id).first()
        
        if not produto:
            return jsonify({'success': False, 'message': 'Produto não encontrado.'}), 404
        if not prateleira_produto:
            return jsonify({'success': False, 'message': 'Produto não está registrado nesta prateleira.'}), 404
        
        quantidade_calculada = round(peso_total_balanca / produto.peso)

        prateleira_produto.quantidade += quantidade_calculada
        prateleira_produto.peso_atual += peso_total_balanca
        prateleira_produto.preco_total += produto.preco_unidade * quantidade_calculada

        historico = HistoricoMovimentacao(
            produto_id=produto_id,
            prateleira_id=prateleira_id,
            tipo_movimentacao='entrada',
            quantidade=quantidade_calculada,
            preco_total=produto.preco_unidade * quantidade_calculada
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
        
        peso_total_balanca = emular_sensor(produto_id, quantidade_retirada)

        produto = Produto.query.get(produto_id)
        prateleira_produto = PrateleiraProduto.query.filter_by(produto_id=produto_id, prateleira_id=prateleira_id).first()

        if not produto:
            return jsonify({'success': False, 'message': 'Produto não encontrado.'}), 404
        if not prateleira_produto:
            return jsonify({'success': False, 'message': 'Produto não está registrado nesta prateleira.'}), 404
        
        if prateleira_produto.quantidade == 0:
            return jsonify({'success': False, 'message': 'Não há produtos para retirar.'}), 400

        peso_para_quantidade = peso_total_balanca / produto.peso

        if prateleira_produto.quantidade < peso_para_quantidade:
            return jsonify({'success': False, 'message': 'Quantidade insuficiente para retirada.'}), 400

        peso_por_unidade = produto.peso  
        peso_atual_retirado = peso_por_unidade * peso_para_quantidade
        preco_total = produto.preco_unidade * peso_para_quantidade

        prateleira_produto.quantidade -= peso_para_quantidade
        prateleira_produto.peso_atual -= peso_atual_retirado
        prateleira_produto.preco_total -= preco_total

        historico = HistoricoMovimentacao(
            produto_id=produto_id,
            prateleira_id=prateleira_id,
            tipo_movimentacao='saida',
            quantidade=peso_para_quantidade,
            preco_total=preco_total
        )

        db.session.add(historico)
        db.session.commit()

        verificar_alerta(produto_id, prateleira_id, 'saida')
        
        return jsonify({'success': True, 'message': 'Produto retirado com sucesso.', 'peso_atual': prateleira_produto.peso_atual})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no servidor: {str(e)}'}), 500
