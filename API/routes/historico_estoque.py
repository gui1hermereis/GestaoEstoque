from flask import Blueprint, request, jsonify
from models.db_models import db, Produto, Prateleira, HistoricoMovimentacao
from datetime import datetime, timedelta

historico_movimentacoes_bp = Blueprint('historico', __name__)

@historico_movimentacoes_bp.route("/historico", methods=["GET"])
def listar():
    try:
        resultados = db.session.query(
            Produto.nome.label("nome_produto"),
            Produto.marca.label("marca"),
            Prateleira.nome.label("nome_prateleira"),
            Prateleira.setor.label("setor"),
            HistoricoMovimentacao.tipo_movimentacao.label("tipo_movimentacao"),
            HistoricoMovimentacao.quantidade.label("quantidade"),
            HistoricoMovimentacao.preco_total.label("preco_total"),
            HistoricoMovimentacao.data_hora.label("data_hora")
        ).join(HistoricoMovimentacao, Produto.id == HistoricoMovimentacao.produto_id
        ).join(Prateleira, Prateleira.id == HistoricoMovimentacao.prateleira_id
        ).all()

        dados = []
        for r in resultados:
            data_hora_formatada = r.data_hora.strftime("%d/%m/%y %H:%M") if r.data_hora else None
            dados.append({
                "nome_produto": r.nome_produto,
                "marca": r.marca,
                "nome_prateleira": r.nome_prateleira,
                "setor": r.setor,
                "tipo_movimentacao": r.tipo_movimentacao,
                "quantidade": r.quantidade,
                "preco_total": r.preco_total,
                "data_hora":data_hora_formatada
            })

        return jsonify({"success": True, "data": dados})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500
    
@historico_movimentacoes_bp.route("/historico/vendas", methods=["GET"])
def listar_vendas():
    try:
        resultados = db.session.query(
            Produto.nome.label("nome_produto"),
            db.func.sum(HistoricoMovimentacao.quantidade).label("quantidade_vendida"),
        ).join(
            HistoricoMovimentacao, Produto.id == HistoricoMovimentacao.produto_id
        ).join(
            Prateleira, Prateleira.id == HistoricoMovimentacao.prateleira_id
        ).filter(
            HistoricoMovimentacao.tipo_movimentacao == 'saida'
        ).group_by(
            Produto.id 
        ).order_by(
            db.func.sum(HistoricoMovimentacao.quantidade).desc() 
        ).all()
       
        dados = []
        for r in resultados:
            dados.append({
                "nome_produto": r.nome_produto,
                "quantidade_vendida": r.quantidade_vendida,
            })

        return jsonify({"success": True, "data": dados})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500
    
@historico_movimentacoes_bp.route("/historico/faturamento", methods=["GET"])
def total_faturamento():
    try:
        agora = datetime.now()
        primeiro_dia_mes = datetime(agora.year, agora.month, 1)

        resultado = db.session.query(
            db.func.sum(HistoricoMovimentacao.preco_total)
        ).filter(
            HistoricoMovimentacao.tipo_movimentacao == 'saida',
            HistoricoMovimentacao.data_hora >= primeiro_dia_mes
        ).scalar() or 0  

        dado = {
            "faturamento_total": float(resultado),
            "mes": agora.strftime("%m/%Y")
        }

        return jsonify({"success": True, "data": [dado]})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500

@historico_movimentacoes_bp.route("/historico/menos_vendido", methods=["GET"])
def listar_menos_vendido():
    try:
        resultado = db.session.query(
            Produto.nome.label("nome_produto"),
            db.func.sum(HistoricoMovimentacao.quantidade).label("quantidade_vendida")
        ).join(
            HistoricoMovimentacao, Produto.id == HistoricoMovimentacao.produto_id
        ).filter(
            HistoricoMovimentacao.tipo_movimentacao == 'saida'
        ).group_by(
            Produto.id
        ).order_by(
            db.func.sum(HistoricoMovimentacao.quantidade).asc()
        ).first()

        if resultado:
            dado = {
                "nome_produto": resultado.nome_produto,
                "quantidade_vendida": resultado.quantidade_vendida
            }
            return jsonify({"success": True, "data": [dado]})
        else:
            return jsonify({"success": True, "data": None, "message": "Nenhum produto vendido encontrado."})

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500

@historico_movimentacoes_bp.route("/historico/mais_vendido", methods=["GET"])
def listar_mais_vendido():
    try:
        resultado = db.session.query(
            Produto.nome.label("nome_produto"),
            db.func.sum(HistoricoMovimentacao.quantidade).label("quantidade_vendida")
        ).join(
            HistoricoMovimentacao, Produto.id == HistoricoMovimentacao.produto_id
        ).filter(
            HistoricoMovimentacao.tipo_movimentacao == 'saida'
        ).group_by(
            Produto.id
        ).order_by(
            db.func.sum(HistoricoMovimentacao.quantidade).desc()
        ).first()

        if resultado:
            dado = {
                "nome_produto": resultado.nome_produto,
                "quantidade_vendida": resultado.quantidade_vendida
            }
            return jsonify({"success": True, "data": [dado]})
        else:
            return jsonify({"success": True, "data": None, "message": "Nenhum produto vendido encontrado."})

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500

@historico_movimentacoes_bp.route("/historico/total_vendas_ultimos_30_dias", methods=["GET"])
def total_vendas_ultimos_30_dias():
    try:
        agora = datetime.now()
        data_inicio = agora - timedelta(days=30)  

        resultado = db.session.query(
            db.func.count(HistoricoMovimentacao.id)
        ).filter(
            HistoricoMovimentacao.tipo_movimentacao == 'saida',
            HistoricoMovimentacao.data_hora >= data_inicio
        ).scalar() or 0

        dado = {
            "total_vendas": int(resultado),
            "periodo": f"{data_inicio.strftime('%d/%m/%Y')} a {agora.strftime('%d/%m/%Y')}"
        }

        return jsonify({"success": True, "data": [dado]})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500

@historico_movimentacoes_bp.route("/historico/unidades_vendidas_ultimos_30_dias", methods=["GET"])
def unidades_vendidas_ultimos_30_dias():
    try:
        agora = datetime.now()
        data_inicio = agora - timedelta(days=30)  

        resultado = db.session.query(
            db.func.sum(HistoricoMovimentacao.quantidade) 
        ).filter(
            HistoricoMovimentacao.tipo_movimentacao == 'saida',
            HistoricoMovimentacao.data_hora >= data_inicio
        ).scalar() or 0

        dado = {
            "unidades_vendidas": int(resultado),
            "periodo": f"{data_inicio.strftime('%d/%m/%Y')} a {agora.strftime('%d/%m/%Y')}"
        }

        return jsonify({"success": True, "data": [dado]})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro no servidor: {str(e)}"}), 500