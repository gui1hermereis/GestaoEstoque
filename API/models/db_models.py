from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import pytz

db = SQLAlchemy()

tz = pytz.timezone('America/Sao_Paulo')

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)  
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)  
    peso = db.Column(db.Float, nullable=False)  
    preco_unidade = db.Column(db.Float, nullable=False)  
    ativo = db.Column(db.Boolean, default=True)

    prateleiras = db.relationship('PrateleiraProduto', back_populates='produto')

    def __repr__(self):
        return f'<Produto {self.nome}>'


class Prateleira(db.Model):
    __tablename__ = 'prateleiras' 

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    setor = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    produtos = db.relationship('PrateleiraProduto', back_populates='prateleira')

    def __repr__(self):
        return f'<Prateleira {self.nome}>'


class PrateleiraProduto(db.Model):
    __tablename__ = 'prateleira_produto'

    id = db.Column(db.Integer, primary_key=True)  
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    prateleira_id = db.Column(db.Integer, db.ForeignKey('prateleiras.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    quantidade_min = db.Column(db.Integer, nullable=False)
    peso_atual = db.Column(db.Float, nullable=False)
    preco_total = db.Column(db.Float, nullable=False)

    produto = db.relationship('Produto', back_populates='prateleiras')
    prateleira = db.relationship('Prateleira', back_populates='produtos')

    def __repr__(self):
        return f'<PrateleiraProduto Produto={self.produto_id} Prateleira={self.prateleira_id}>'
    
class HistoricoMovimentacao(db.Model):
    __tablename__ = 'historico_movimentacoes'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    prateleira_id = db.Column(db.Integer, db.ForeignKey('prateleiras.id'), nullable=True) 
    tipo_movimentacao = db.Column(db.String(10), nullable=False) 
    quantidade = db.Column(db.Integer, nullable=False)
    preco_total = db.Column(db.Float, nullable=False)
    data_hora = db.Column(db.DateTime, default=lambda: datetime.now(tz))

    produto = db.relationship('Produto', backref=db.backref('historicos', lazy=True))
    prateleira = db.relationship('Prateleira', backref=db.backref('historicos', lazy=True))

    def __repr__(self):
        return f'<Movimentacao {self.tipo_movimentacao} de {self.quantidade} unidades do Produto ID {self.produto_id}>'
    
class Alertas(db.Model):
    __tablename__ = 'alertas'

    id = db.Column(db.Integer, primary_key=True)
    tipo_alerta = db.Column(db.String(100), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    prateleira_id = db.Column(db.Integer, db.ForeignKey('prateleiras.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, default=lambda: datetime.now(tz))
    ativo = db.Column(db.Boolean, default=True)

    produto = db.relationship('Produto', backref=db.backref('alertas', lazy=True))
    prateleira = db.relationship('Prateleira', backref=db.backref('alertas', lazy=True))

    def __repr__(self):
        return f'<Alerta {self.tipo_alerta} Produto={self.produto_id}>'

