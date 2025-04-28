from flask import Blueprint, request, jsonify
from models.db_models import db, Produto, Prateleira, PrateleiraProduto

prateleiras_produtos_bp = Blueprint('prateleiras_produtos', __name__)

@prateleiras_produtos_bp.route("/prateleiras_produtos", methods=["POST"])
def cadastrar():
    try:
        data = request.json
        produto_id = data.get('produto_id')
        prateleira_id = data.get('prateleira_id')
        quantidade = data.get('quantidade')
        quantidade_min = data.get('quantidade_min')

        if not produto_id or not prateleira_id or not quantidade or not quantidade_min:
            return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400

        produto = Produto.query.get(produto_id)
        prateleira = Prateleira.query.get(prateleira_id)

        if not produto:
            return jsonify({'success': False, 'message': 'Produto não encontrado.'}), 404
        if not prateleira:
            return jsonify({'success': False, 'message': 'Prateleira não encontrada.'}), 404

        estoque_existente = PrateleiraProduto.query.filter_by(produto_id=produto_id).first()
        if estoque_existente:
            return jsonify({'success': False, 'message': 'Produto já está registrado em outra prateleira.'}), 400
        
        prateleira_produto_existente = PrateleiraProduto.query.filter_by(prateleira_id=prateleira_id).first()
        if prateleira_produto_existente:
            return jsonify({'success': False, 'message': 'Prateleira já contém um produto. Não é possível adicionar outro.'}), 400

        if quantidade_min > quantidade:
            return jsonify({'success': False, 'message': 'Quantidade mínima não pode ser maior que a quantidade atual.'}), 400

        peso_atual = produto.peso * quantidade
        preco_total = produto.preco_unidade * quantidade

        new_estoq = PrateleiraProduto(
            produto_id=produto_id, 
            prateleira_id=prateleira_id, 
            quantidade=quantidade, 
            quantidade_min=quantidade_min, 
            peso_atual=peso_atual,
            preco_total=preco_total
        )

        db.session.add(new_estoq)
        db.session.commit()
    
        return jsonify({'success': True, 'message':'Estoque atualizado com sucesso.', 'id': new_estoq.id})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no servidor: {str(e)}'}), 500

@prateleiras_produtos_bp.route("/prateleiras_produtos/<int:id>", methods=["PUT"])
def editar(id):
    try:
        data = request.json
        produto_id = data.get('produto_id')
        prateleira_id = data.get('prateleira_id')
        quantidade_min = data.get('quantidade_min')
        quantidade = data.get('quantidade')

        if not produto_id or not prateleira_id or not quantidade_min or not quantidade:
            return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400
        
        produto = Produto.query.get(produto_id)
        prateleira = Prateleira.query.get(prateleira_id)

        if not produto:
            return jsonify({'success': False, 'message': 'Produto não encontrado.'}), 404
        if not prateleira:
            return jsonify({'success': False, 'message': 'Prateleira não encontrada.'}), 404

        estoque = PrateleiraProduto.query.get(id)
        if not estoque:
            return jsonify({'success': False, 'message': 'Estoque não encontrado.'}), 404

        if estoque.produto_id != produto_id:
            estoque_existente = PrateleiraProduto.query.filter_by(produto_id=produto_id).first()
            if estoque_existente:
                return jsonify({'success': False, 'message': 'Produto já está registrado em outra prateleira.'}), 400

        if estoque.prateleira_id != prateleira_id:
            prateleira_produto_existente = PrateleiraProduto.query.filter_by(prateleira_id=prateleira_id).first()
            if prateleira_produto_existente:
                return jsonify({'success': False, 'message': 'Prateleira já contém um produto. Não é possível adicionar outro.'}), 400

        # Atualizar os dados do estoque
        estoque.produto_id = produto_id
        estoque.prateleira_id = prateleira_id
        estoque.quantidade = quantidade
        estoque.quantidade_min = quantidade_min

        peso_unitario = produto.peso
        preco_unitario = produto.preco_unidade
        estoque.peso_atual = peso_unitario * quantidade
        estoque.preco_total = preco_unitario * quantidade

        db.session.commit()

        return jsonify({'success': True, 'message': 'Produto atualizado com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no servidor: {str(e)}'}), 500

@prateleiras_produtos_bp.route('/prateleiras_produtos/<int:id>', methods=['DELETE'])
def deletar(id):
    try:
        estoque = PrateleiraProduto.query.get(id)
        if not estoque:
            return jsonify({'success': False, 'message': 'Estoque não encontrado.'}), 404

        PrateleiraProduto.query.filter_by(id=id).delete()

        db.session.delete(estoque)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Estoque deletada com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao deletar estoque: {str(e)}'}), 500


@prateleiras_produtos_bp.route("/prateleiras_produtos", methods=["GET"])
def listar():
    try:
        resultados = db.session.query(
            PrateleiraProduto.id.label("id"),
            PrateleiraProduto.produto_id.label("produto_id"),
            PrateleiraProduto.prateleira_id.label("prateleira_id"),
            Produto.nome.label("nome_produto"),
            Produto.marca.label("marca"),
            Prateleira.nome.label("nome_prateleira"),
            Prateleira.setor.label("setor"),
            PrateleiraProduto.quantidade.label("quantidade"),
            PrateleiraProduto.quantidade_min.label("quantidade_min"),
            PrateleiraProduto.peso_atual.label("peso_atual"),
            PrateleiraProduto.preco_total.label("preco_total")
        ).join(PrateleiraProduto, Produto.id == PrateleiraProduto.produto_id
        ).join(Prateleira, Prateleira.id == PrateleiraProduto.prateleira_id
        ).order_by(PrateleiraProduto.id.desc()
        ).all()

        dados = []
        for r in resultados:
            dados.append({
                "id": r.id,
                "produto_id": r.produto_id,
                "nome_produto": r.nome_produto,
                "marca": r.marca,
                "prateleira_id": r.prateleira_id,
                "nome_prateleira": r.nome_prateleira,
                "setor": r.setor,
                "quantidade": r.quantidade,
                "quantidade_min": r.quantidade_min,
                "peso_atual": r.peso_atual,
                "preco_total": r.preco_total
            })

        return jsonify({"success": True, "data": dados})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500
    

@prateleiras_produtos_bp.route("/prateleiras_produtos/total", methods=["GET"])
def total_produtos_nas_prateleiras():
    try:
        resultado = db.session.query(
            db.func.count(PrateleiraProduto.id)
        ).filter(
            PrateleiraProduto.quantidade > 0
        ).scalar() or 0

        dado = {
            "total_produtos": int(resultado),
        }

        return jsonify({"success": True, "data": [dado]})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500

@prateleiras_produtos_bp.route("/prateleiras_produtos/total_estoque_baixo", methods=["GET"])
def total_produtos_com_estoque_baixo():
    try:
        resultado = db.session.query(
            db.func.count(PrateleiraProduto.id)
        ).filter(
            PrateleiraProduto.quantidade <= PrateleiraProduto.quantidade_min
        ).scalar() or 0

        dado = {
            "total_estoque_baixo": int(resultado),
        }

        return jsonify({"success": True, "data": [dado]})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500
    
@prateleiras_produtos_bp.route("/prateleiras_produtos/lista_estoque_baixo", methods=["GET"])
def listar_estoque_baixo():
    try:
        resultados = db.session.query(
            Produto.nome.label("nome_produto"),
            Prateleira.nome.label("nome_prateleira"),
            PrateleiraProduto.quantidade.label("quantidade"),
            PrateleiraProduto.quantidade_min.label("quantidade_min"),
        ).join(PrateleiraProduto, Produto.id == PrateleiraProduto.produto_id
        ).join(Prateleira, Prateleira.id == PrateleiraProduto.prateleira_id
        ).filter(
            PrateleiraProduto.quantidade <= PrateleiraProduto.quantidade_min
        ).all()

        dados = []
        for r in resultados:
            dados.append({
                "nome_produto": r.nome_produto,
                "nome_prateleira": r.nome_prateleira,
                "quantidade": r.quantidade,
                "quantidade_min": r.quantidade_min
            })

        return jsonify({"success": True, "data": dados})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500
    