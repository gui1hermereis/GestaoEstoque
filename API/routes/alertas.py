from flask import Blueprint, request, jsonify
from models.db_models import db, Produto, Prateleira, PrateleiraProduto, Alertas
from datetime import datetime

alertas_bp = Blueprint('alertas', __name__)

def verificar_alerta(produto_id, prateleira_id, tipo_movimentacao):
    prateleira_produto = PrateleiraProduto.query.filter_by(
        produto_id=produto_id, 
        prateleira_id=prateleira_id
    ).first()

    if not prateleira_produto:
        return None  

    quantidade_atual = prateleira_produto.quantidade
    alerta_existente = Alertas.query.filter_by(
        produto_id=produto_id, 
        prateleira_id=prateleira_id
    ).order_by(Alertas.id.desc()).first()

    tipo_alerta = None
    if quantidade_atual == 0:
        tipo_alerta = "Sem estoque para o produto"
    elif quantidade_atual < prateleira_produto.quantidade_min:
        tipo_alerta = "Quantidade Crítica"
    elif quantidade_atual == prateleira_produto.quantidade_min:
        tipo_alerta = "Quantidade no mínimo permitido"
    elif quantidade_atual > prateleira_produto.quantidade_min:
        tipo_alerta = "Estoque regualarizado"

    if tipo_movimentacao == 'saida':
        if tipo_alerta:
            if alerta_existente and alerta_existente.ativo:
                alerta_existente.tipo_alerta = tipo_alerta
                alerta_existente.quantidade = quantidade_atual
                db.session.commit()
            else:
                novo_alerta = Alertas(
                    tipo_alerta=tipo_alerta,
                    produto_id=produto_id,
                    prateleira_id=prateleira_id,
                    quantidade=quantidade_atual,
                    ativo=True
                )
                db.session.add(novo_alerta)
                db.session.commit()
                return novo_alerta

    elif tipo_movimentacao == 'entrada':
        if alerta_existente:
            if quantidade_atual > prateleira_produto.quantidade_min:
                alerta_existente.tipo_alerta = "Estoque regularizado"
                alerta_existente.quantidade = quantidade_atual
                alerta_existente.ativo = False
                db.session.commit()
            else:
                alerta_existente.tipo_alerta = tipo_alerta
                alerta_existente.quantidade = quantidade_atual
                db.session.commit()

    return None
    
@alertas_bp.route("/alertas/contagem_total", methods=["GET"])
def total_alertas():
    try:
        agora = datetime.now()
        primeiro_dia_mes = datetime(agora.year, agora.month, 1)

        resultado = db.session.query(
            db.func.count(Alertas.id)
        ).filter(
            Alertas.data_hora >= primeiro_dia_mes
        ).scalar() or 0

        dado = {
            "total_alertas": int(resultado),
            "mes": agora.strftime("%m/%Y")
        }

        return jsonify({"success": True, "data": [dado]})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500
    
@alertas_bp.route("/alertas/todos", methods=["GET"])
def listar():
    try:
        resultados = db.session.query(
            Alertas.tipo_alerta.label("tipo_alerta"),
            Produto.nome.label("nome_produto"),
            Prateleira.nome.label("nome_prateleira"),
            Alertas.quantidade.label("quantidade"),
            Alertas.data_hora.label("data_hora"),
            Alertas.ativo.label("ativo")
        ).join(Produto, Alertas.produto_id == Produto.id
        ).join(Prateleira, Alertas.prateleira_id == Prateleira.id
        ).all()

        dados = []
        for r in resultados:
            data_hora_formatada = r.data_hora.strftime("%d/%m/%y %H:%M") if r.data_hora else None
            status = "Ativo" if r.ativo else "Inativo"
            dados.append({
                "tipo_alerta": r.tipo_alerta,
                "nome_produto": r.nome_produto,
                "nome_prateleira": r.nome_prateleira,
                "quantidade": r.quantidade,
                "data_hora": data_hora_formatada,
                "ativo": status,
            })

        return jsonify({"success": True, "data": dados})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500

    
@alertas_bp.route("/alertas/contagem_nao_resolvidos", methods=["GET"])
def total_alertas_nao_resolvidos():
    try:
        resultado = db.session.query(
            db.func.count(Alertas.id)
        ).filter(
            Alertas.ativo == True
        ).scalar() or 0

        dado = {
            "total_nao_resolvidos": int(resultado),
        }

        return jsonify({"success": True, "data": [dado]})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500


@alertas_bp.route("/alertas/nao_resolvidos", methods=["GET"])
def listar_nao_resolvidos():
    try:
        resultados = db.session.query(
            Alertas.tipo_alerta.label("tipo_alerta"),
            Produto.nome.label("nome_produto"),
            Prateleira.nome.label("nome_prateleira"),
            Alertas.quantidade.label("quantidade"),
            Alertas.data_hora.label("data_hora"),
            Alertas.ativo.label("ativo")
        ).join(Produto, Alertas.produto_id == Produto.id
        ).join(Prateleira, Alertas.prateleira_id == Prateleira.id
        ).filter(
            Alertas.ativo == True
        ).all()

        dados = []
        for r in resultados:
            data_hora_formatada = r.data_hora.strftime("%d/%m/%y %H:%M") if r.data_hora else None
            status = "Ativo" if r.ativo else "Inativo"
            dados.append({
                "tipo_alerta": r.tipo_alerta,
                "nome_produto": r.nome_produto,
                "nome_prateleira": r.nome_prateleira,
                "quantidade": r.quantidade,
                "data_hora": data_hora_formatada,
                "ativo": status,
            })

        return jsonify({"success": True, "data": dados})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500
    
@alertas_bp.route("/alertas/contagem_resolvidos", methods=["GET"])
def total_alertas_resolvidos():
    try:
        resultado = db.session.query(
            db.func.count(Alertas.id)
        ).filter(
            Alertas.ativo == False
        ).scalar() or 0

        dado = {
            "total_resolvidos": int(resultado),
        }

        return jsonify({"success": True, "data": [dado]})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500