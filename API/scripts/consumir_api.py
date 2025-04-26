import requests
import json
import uuid
from datetime import datetime, timezone

# Configurações
DEVICE_TOKEN = "4cd684a4-5f3d-498b-9076-cca5086d3a6a"
HEADERS = {
    "Content-Type": "application/json",
    "Device-Token": DEVICE_TOKEN
}
API_URL = "https://c1a3-2804-7f0-9580-f204-70c8-c365-33f1-f2f3.ngrok-free.app"

# ------------------ PRODUTOS ------------------
def buscar_produtos():
    try:
        res = requests.get(f"{API_URL}/produtos")
        res.raise_for_status()
        return res.json().get("produtos", [])
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return []

def preparar_payload_produtos(produtos):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for produto in produtos:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "produto_marca", "value": produto.get("marca", ""), "serie": serie_id, "time": time_str},
            {"variable": "produto_nome", "value": produto.get("nome", ""), "serie": serie_id, "time": time_str},
            {"variable": "produto_descricao", "value": produto.get("descricao", ""), "serie": serie_id, "time": time_str},
            {"variable": "produto_peso", "value": float(produto.get("peso", 0)), "serie": serie_id, "time": time_str},
            {"variable": "produto_preco_unidade", "value": float(produto.get("preco_unidade", 0)), "serie": serie_id, "time": time_str}
        ])
    return payload

# ------------------ PRATELEIRAS ------------------
def buscar_prateleiras():
    try:
        res = requests.get(f"{API_URL}/prateleiras")
        res.raise_for_status()
        return res.json().get("Prateleiras", [])
    except Exception as e:
        print(f"Erro ao buscar prateleiras: {e}")
        return []

def preparar_payload_prateleiras(prateleiras):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for prateleira in prateleiras:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "prateleira_nome", "value": prateleira.get("nome", ""), "serie": serie_id, "time": time_str},
            {"variable": "prateleira_setor", "value": prateleira.get("setor", ""), "serie": serie_id, "time": time_str}
        ])
    return payload

# ------------------ ESTOQUE ATUAL ------------------
def buscar_prateleiras_produtos():
    try:
        res = requests.get(f"{API_URL}/prateleiras_produtos")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar prateleiras e produtos: {e}")
        return []

def preparar_payload_estoque(prateleiras_produtos):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in prateleiras_produtos:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "estoque_produto_marca", "value": item.get("marca", ""), "serie": serie_id, "time": time_str},
            {"variable": "estoque_produto_nome", "value": item.get("nome_produto", ""), "serie": serie_id, "time": time_str},
            {"variable": "estoque_prateleira_nome", "value": item.get("nome_prateleira", ""), "serie": serie_id, "time": time_str},
            {"variable": "estoque_prateleira_setor", "value": item.get("setor", ""), "serie": serie_id, "time": time_str},
            {"variable": "estoque_quantidade", "value": item.get("quantidade", ""), "serie": serie_id, "time": time_str},
            {"variable": "estoque_quantidade_min", "value": item.get("quantidade_min", ""), "serie": serie_id, "time": time_str},
            {"variable": "estoque_peso_atual", "value": item.get("peso_atual", ""), "serie": serie_id, "time": time_str},
            {"variable": "estoque_preco_total", "value": item.get("preco_total", ""), "serie": serie_id, "time": time_str}
        ])
    return payload

# ------------------ TOTAL DE PRODUTOS COM ESTOQUE BAIXO ------------------

def contar_estoque_baixo():
    try:
        res = requests.get(f"{API_URL}/prateleiras_produtos/total_estoque_baixo")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar historico com total de vendas: {e}")
        return []

def preparar_payload_contar_estoque_baixo(produtos_estoque_baixo):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in produtos_estoque_baixo:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "contagem_prods_estoque_baixo", "value": item.get("total_estoque_baixo", ""), "serie": serie_id, "time": time_str},
        ])
    return payload

# ------------------ LISTA PRODUTOS COM ESTOQUE BAIXO ------------------

def buscar_todos_produtos_estoque_baixo():
    try:
        res = requests.get(f"{API_URL}/prateleiras_produtos/lista_estoque_baixo")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar prateleiras e produtos: {e}")
        return []

def preparar_payload_buscar_estoque_baixo(prateleiras_produtos):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in prateleiras_produtos:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "nome_prod_estoque_baixo", "value": item.get("nome_produto", ""), "serie": serie_id, "time": time_str},
            {"variable": "prateleira_estoque_baixo", "value": item.get("nome_prateleira", ""), "serie": serie_id, "time": time_str},
            {"variable": "quantidade_estoque_baixo", "value": item.get("quantidade", ""), "serie": serie_id, "time": time_str},
            {"variable": "quantidade_min_estoque_baixo", "value": item.get("quantidade_min", ""), "serie": serie_id, "time": time_str},
        ])
    return payload

# ------------------ HISTÓRICO DE MOVIMENTAÇÕES ------------------
def buscar_historico():
    try:
        res = requests.get(f"{API_URL}/historico")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar historico: {e}")
        return []

def preparar_payload_historico(historico_estoque):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in historico_estoque:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "historico_produto_marca", "value": item.get("marca", ""), "serie": serie_id, "time": time_str},
            {"variable": "historico_produto_nome", "value": item.get("nome_produto", ""), "serie": serie_id, "time": time_str},
            {"variable": "historico_prateleira_nome", "value": item.get("nome_prateleira", ""), "serie": serie_id, "time": time_str},
            {"variable": "historico_prateleira_setor", "value": item.get("setor", ""), "serie": serie_id, "time": time_str},
            {"variable": "historico_tipo_movimentacao", "value": item.get("tipo_movimentacao", ""), "serie": serie_id, "time": time_str},
            {"variable": "historico_quantidade", "value": item.get("quantidade", ""), "serie": serie_id, "time": time_str},
            {"variable": "historico_preco_total", "value": item.get("preco_total", ""), "serie": serie_id, "time": time_str},
            {"variable": "historico_data", "value": item.get("data_hora", ""), "serie": serie_id, "time": time_str}
        ])
    return payload

# ------------------ HISTÓRICO DE VENDAS ------------------
def buscar_historico_vendas():
    try:
        res = requests.get(f"{API_URL}/historico/vendas")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar historico de vendas: {e}")
        return []

def preparar_payload_historico_vendas(historico_vendas):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in historico_vendas:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "historico_vendas_produto_nome", "value": item.get("nome_produto", ""), "serie": serie_id, "time": time_str},
            {"variable": "historico_vendas_quantidade", "value": item.get("quantidade_vendida", ""), "serie": serie_id, "time": time_str},
        ])
    return payload

# ------------------ HISTÓRICO DE FATURAMENTO ------------------
def buscar_historico_faturamento():
    try:
        res = requests.get(f"{API_URL}/historico/faturamento")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar historico de faturamento: {e}")
        return []

def preparar_payload_historico_faturamento(historico_faturamento):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in historico_faturamento:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "historico_faturamento_total", "value": item.get("faturamento_total", ""), "serie": serie_id, "time": time_str},
        ])
    return payload


# ------------------ HISTÓRICO DE MENOS VENDIDO ------------------
def buscar_historico_menos_vendido():
    try:
        res = requests.get(f"{API_URL}/historico/menos_vendido")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar historico menos vendido: {e}")
        return []

def preparar_payload_historico_menos_vendido (historico_menos_vendido):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in historico_menos_vendido:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "historico_nome_menos_vendido", "value": item.get("nome_produto", ""), "serie": serie_id, "time": time_str},
            {"variable": "historico_quantidade_menos_vendido", "value": item.get("quantidade_vendida", ""), "serie": serie_id, "time": time_str},
        ])
    return payload

# ------------------ HISTÓRICO DE MAIS VENDIDO ------------------
def buscar_historico_mais_vendido():
    try:
        res = requests.get(f"{API_URL}/historico/mais_vendido")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar historico de produto mais vendido: {e}")
        return []

def preparar_payload_mais_vendido(historico_mais_vendido):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in historico_mais_vendido:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "historico_nome_mais_vendido", "value": item.get("nome_produto", ""), "serie": serie_id, "time": time_str},
            {"variable": "historico_quantidade_mais_vendido", "value": item.get("quantidade_vendida", ""), "serie": serie_id, "time": time_str},
        ])
    return payload

# ------------------ HISTÓRICO DE TOTAL DE VENDAS ------------------
def buscar_total_vendas_ultimos_30_dias():
    try:
        res = requests.get(f"{API_URL}/historico/total_vendas_ultimos_30_dias")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar historico com total de vendas: {e}")
        return []

def preparar_payload_total_vendas_ultimos_30_dias(historico_total_vendas_mes):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in historico_total_vendas_mes:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "total_vendas_30_dias", "value": item.get("total_vendas", ""), "serie": serie_id, "time": time_str},
        ])
    return payload

# ------------------ HISTÓRICO DE TOTAL DE UNIDADES VENDIDAS NO MES ------------------
def buscar_unidades_vendidas_ultimos_30_dias():
    try:
        res = requests.get(f"{API_URL}/historico/unidades_vendidas_ultimos_30_dias")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar historico com total de unidades vendidas: {e}")
        return []

def preparar_payload_unidades_vendidas_ultimos_30_dias(unidades_vendidas_ultimos_30):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in unidades_vendidas_ultimos_30:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "unidades_vendidas_30_dias", "value": item.get("unidades_vendidas", ""), "serie": serie_id, "time": time_str},
        ])
    return payload

# ------------------ Contar todos alertas ------------------
def contar_todos_alertas():
    try:
        res = requests.get(f"{API_URL}/alertas/contagem_total")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao contar alertas: {e}")
        return []

def preparar_payload_contar_todos_alertas(contar_alertas):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in contar_alertas:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "contagem_todos_alertas", "value": item.get("total_alertas", ""), "serie": serie_id, "time": time_str},
        ])
    return payload

# ------------------ Listar todos alertas ------------------
def buscar_todos_alertas():
    try:
        res = requests.get(f"{API_URL}/alertas/todos")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar historico: {e}")
        return []

def preparar_payload_buscar_todos_alertas(buscar_alertas):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in buscar_alertas:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "alerta_todos_tipo", "value": item.get("tipo_alerta", ""), "serie": serie_id, "time": time_str},
            {"variable": "alerta_todos_produto_nome", "value": item.get("nome_produto", ""), "serie": serie_id, "time": time_str},
            {"variable": "alerta_todos_prateleira_nome", "value": item.get("nome_prateleira", ""), "serie": serie_id, "time": time_str},
            {"variable": "alerta_todos_quantidade", "value": item.get("quantidade", ""), "serie": serie_id, "time": time_str},
            {"variable": "alerta_todos_data", "value": item.get("data_hora", ""), "serie": serie_id, "time": time_str},
            {"variable": "alerta_todos_ativo", "value": item.get("ativo", ""), "serie": serie_id, "time": time_str}
        ])
    return payload

# ------------------ Contar alertas não resolvidos ------------------
def contar_alertas_nao_resolvidos():
    try:
        res = requests.get(f"{API_URL}/alertas/contagem_nao_resolvidos")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao contar alertas nao resolvidos: {e}")
        return []

def preparar_payload_contar_alertas_nao_resolvidoss(contar_nao_resolvidos):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in contar_nao_resolvidos:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "contagem_alertas_nao_resolvidos", "value": item.get("total_nao_resolvidos", ""), "serie": serie_id, "time": time_str},
        ])
    return payload

# ------------------ Listar todos alertas não resolvidos------------------
def buscar_alertas_nao_resolvidos():
    try:
        res = requests.get(f"{API_URL}/alertas/nao_resolvidos")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao buscar historico: {e}")
        return []

def preparar_payload_buscar_alertas_nao_resolvidos(buscar_nao_resolvidos):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in buscar_nao_resolvidos:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "alerta_nao_resolvidos_tipo", "value": item.get("tipo_alerta", ""), "serie": serie_id, "time": time_str},
            {"variable": "alerta_nao_resolvidos_produto_nome", "value": item.get("nome_produto", ""), "serie": serie_id, "time": time_str},
            {"variable": "alerta_nao_resolvidos_prateleira_nome", "value": item.get("nome_prateleira", ""), "serie": serie_id, "time": time_str},
            {"variable": "alerta_nao_resolvidos_quantidade", "value": item.get("quantidade", ""), "serie": serie_id, "time": time_str},
            {"variable": "alerta_nao_resolvidos_data", "value": item.get("data_hora", ""), "serie": serie_id, "time": time_str},
            {"variable": "alerta_nao_resolvidos_ativo", "value": item.get("ativo", ""), "serie": serie_id, "time": time_str}
        ])
    return payload

# ------------------ Contar alertas  resolvidos ------------------
def contar_alertas_resolvidos():
    try:
        res = requests.get(f"{API_URL}/alertas/contagem_resolvidos")
        res.raise_for_status()
        return res.json().get("data", [])
    except Exception as e:
        print(f"Erro ao contar alertas resolvidos: {e}")
        return []

def preparar_payload_contar_alertas_resolvidoss(contar_resolvidos):
    payload = []
    time_str = datetime.now(timezone.utc).isoformat()
    for item in contar_resolvidos:
        serie_id = str(uuid.uuid4())
        payload.extend([
            {"variable": "contagem_alertas_resolvidos", "value": item.get("total_resolvidos", ""), "serie": serie_id, "time": time_str},
        ])
    return payload

# ------------------ ENVIO ------------------
def enviar_para_tago(payload):
    try:
        res = requests.post("https://api.tago.io/data", headers=HEADERS, data=json.dumps(payload))
        res.raise_for_status() 
        print("Resposta do TagoIO:", res.json())
    except Exception as e:
        print(f"Erro ao enviar dados para o TagoIO: {e}")

# ------------------ MAIN ------------------
def main():
    # Produtos
    produtos = buscar_produtos()
    if produtos:
        payload = preparar_payload_produtos(produtos)
        enviar_para_tago(payload)

    # Prateleiras
    prateleiras = buscar_prateleiras()
    if prateleiras:
        payload = preparar_payload_prateleiras(prateleiras)
        enviar_para_tago(payload)

    # Estoque atual
    estoque = buscar_prateleiras_produtos()
    if estoque:
        payload = preparar_payload_estoque(estoque)
        enviar_para_tago(payload)

    # Contar Produtos estoque baixo
    contagem_estoque_baixo = contar_estoque_baixo()
    if contagem_estoque_baixo:
        payload = preparar_payload_contar_estoque_baixo(contagem_estoque_baixo)
        enviar_para_tago(payload)

    # Listar produtos estoque baixo
    estoque_baixo = buscar_todos_produtos_estoque_baixo()
    if estoque_baixo:
        payload = preparar_payload_buscar_estoque_baixo(estoque_baixo)
        enviar_para_tago(payload)
    # Histórico de movimentações
    historico = buscar_historico()
    if historico:
        payload = preparar_payload_historico(historico)
        enviar_para_tago(payload)

    # Histórico de vendas
    historico_vendas = buscar_historico_vendas()
    if historico_vendas:
        payload = preparar_payload_historico_vendas(historico_vendas)
        enviar_para_tago(payload)

    # Histórico de faturamento
    historico_faturamento = buscar_historico_faturamento()
    if historico_faturamento:
        payload = preparar_payload_historico_faturamento(historico_faturamento)
        enviar_para_tago(payload)

    # Histórico de produto menos vendido
    historico_menos_vendido = buscar_historico_menos_vendido()
    if historico_menos_vendido:
        payload = preparar_payload_historico_menos_vendido(historico_menos_vendido)
        enviar_para_tago(payload)

    # Histórico de produto mais vendido
    historico_mais_vendido = buscar_historico_mais_vendido()
    if historico_mais_vendido:
        payload = preparar_payload_mais_vendido(historico_mais_vendido)
        enviar_para_tago(payload)

    # Histórico total de vendas do mês
    total_vendas = buscar_total_vendas_ultimos_30_dias()
    if total_vendas:
        payload = preparar_payload_total_vendas_ultimos_30_dias(total_vendas)
        enviar_para_tago(payload)

    # Histórico unidades vendidas ultimos 30 dias
    unidades_vendidas = buscar_unidades_vendidas_ultimos_30_dias()
    if unidades_vendidas:
        payload = preparar_payload_unidades_vendidas_ultimos_30_dias(unidades_vendidas)
        enviar_para_tago(payload)

    # conta todos alertas
    contagem_todos_alertas = contar_todos_alertas()
    if contagem_todos_alertas:
        payload = preparar_payload_contar_todos_alertas(contagem_todos_alertas)
        enviar_para_tago(payload)

    # Lista todos alertas
    listar_todos_alertas = buscar_todos_alertas()
    if listar_todos_alertas:
        payload = preparar_payload_buscar_todos_alertas(listar_todos_alertas)
        enviar_para_tago(payload)

    # conta todos alertas nao resolvidos
    contagem_alertas_nao_resolvidos = contar_alertas_nao_resolvidos()
    if contagem_alertas_nao_resolvidos:
        payload = preparar_payload_contar_alertas_nao_resolvidoss(contagem_alertas_nao_resolvidos)
        enviar_para_tago(payload)

    # lista todos alertas nao resolvidos
    listar_alertas_nao_resolvidos = buscar_alertas_nao_resolvidos()
    if listar_alertas_nao_resolvidos:
        payload = preparar_payload_buscar_alertas_nao_resolvidos(listar_alertas_nao_resolvidos)
        enviar_para_tago(payload)

    # conta todos alertas resolvidos
    contagem_alertas_resolvidos = contar_alertas_resolvidos()
    if contagem_alertas_resolvidos:
        payload = preparar_payload_contar_alertas_resolvidoss(contagem_alertas_resolvidos)
        enviar_para_tago(payload)

if __name__ == "__main__":
    main()