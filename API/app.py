import subprocess
from flask import Flask
from flask_cors import CORS  
from config import Config
from routes.produtos import produtos_bp
from routes.prateleiras import prateleiras_bp
from routes.prateleiras_produtos import prateleiras_produtos_bp
from routes.historico_estoque import historico_movimentacoes_bp
from routes.balanca import balanca_bp
from routes.alertas import alertas_bp
from models.db_models import db
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import sys

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "*"}})

db.init_app(app)

app.register_blueprint(produtos_bp)  
app.register_blueprint(prateleiras_bp)  
app.register_blueprint(prateleiras_produtos_bp)  
app.register_blueprint(balanca_bp)  
app.register_blueprint(historico_movimentacoes_bp)  
app.register_blueprint(alertas_bp)  

def excluir_arquivos_tago():
    caminho_arquivo = os.path.join(os.getcwd(), "scripts", "excluir_tago.py")
    try:
        print(f"Executando o arquivo {caminho_arquivo} em {datetime.now()}")
        subprocess.run([sys.executable, caminho_arquivo], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o arquivo: {e}")

def enviar_arquivos_tago():
    caminho_arquivo = os.path.join(os.getcwd(), "scripts", "enviar_tago.py")
    try:
        print(f"Executando o arquivo {caminho_arquivo} em {datetime.now()}")
        subprocess.run([sys.executable, caminho_arquivo], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o arquivo: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(excluir_arquivos_tago, 'interval', minutes=10)  
scheduler.add_job(enviar_arquivos_tago, 'interval', minutes=12)  

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  

    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler.start()

    app.run(debug=True)