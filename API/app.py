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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
