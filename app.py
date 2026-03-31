import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import datetime

# 1. Carrega as configurações do arquivo .env
load_dotenv()

# 2. Inicializa o Flask e configura o Banco de Dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///financeiro.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# 3. Inicializa as ferramentas de Banco (SQLAlchemy) e Migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ==========================================
# MODELAGEM DO BANCO DE DADOS (4 Tabelas)
# ==========================================

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    
    # Relacionamentos
    contas = db.relationship('Conta', backref='usuario', lazy=True)
    lancamentos = db.relationship('Lancamento', backref='usuario', lazy=True)

class Conta(db.Model):
    __tablename__ = 'contas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False) # Ex: Nubank, Carteira
    
    # Chave Estrangeira: A qual usuário essa conta pertence?
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    lancamentos = db.relationship('Lancamento', backref='conta', lazy=True)

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False) # Ex: Alimentação, Salário
    descricao = db.Column(db.String(200))
    
    lancamentos = db.relationship('Lancamento', backref='categoria', lazy=True)

class Lancamento(db.Model):
    __tablename__ = 'lancamentos'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(10), nullable=False) # 'entrada' ou 'saida'
    data = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    
    # Chaves Estrangeiras: Amarrando o lançamento ao Usuário, Conta e Categoria
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    conta_id = db.Column(db.Integer, db.ForeignKey('contas.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

# ==========================================
# ROTAS (Vamos criar depois)
# ==========================================
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()

    novo_usuario = Usuario(
        nome=dados.get('nome'),
        email=dados.get('email'),
        senha_hash=dados.get('senha') # Em um projeto real, criptografaríamos a senha aqui
    )
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário criado com sucesso!", "id": novo_usuario.id}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    resultado = [{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios]
    return jsonify(resultado), 200

# ==========================================
# ROTAS DE CONTAS
# ==========================================

@app.route('/contas', methods=['POST'])
def criar_conta():
    dados = request.get_json()

    nova_conta = Conta(
        nome=dados.get('nome'),
        usuario_id=dados.get('usuario_id')
    )
    db.session.add(nova_conta)
    db.session.commit()

    return jsonify({"mensagem": "Conta criada com sucesso!", "id": nova_conta.id}), 201

# ==========================================
# ROTAS DE CATEGORIAS
# ==========================================

@app.route ('/categorias', methods=['POST'])
def criar_categoria():
    dados = request.get_json()

    nova_categoria = Categoria(
        nome=dados.get('nome'),
        descricao=dados.get('descricao')
    )
    db.session.add(nova_categoria)
    db.session.commit()

    return jsonify({"mensagem": "Categoria criada com sucesso!", "id": nova_categoria.id}), 201

# ==========================================
# ROTAS DE LANÇAMENTOS (Regras de Negócio)
# ==========================================
@app.route('/lancamentos', methods=['POST'])
def criar_lancamento():
    dados = request.get_json()

    valor = dados.get('valor')
    tipo = dados.get('tipo')
    categoria_id = dados.get('categoria_id')

    # --- REGRA DE NEGÓCIO 1: Valor deve ser positivo ---
    if valor is None or float(valor) <= 0:
        return jsonify({"erro": "Regra violada: O valor do lançamento deve ser maior que zero."}), 400
    
    # --- REGRA DE NEGÓCIO 2: Tipo deve ser entrada ou saida ---
    if tipo not in ['entrada', 'saida']:
        return jsonify({"erro": "Regra violada: O tipo deve ser exclusivamente 'entrada' ou 'saida'."}), 400
    
    # --- REGRA DE NEGÓCIO 3: Categoria obrigatória ---
    if not categoria_id:
        return jsonify({"erro": "Regra violada: Todo lançamento deve estar associado a uma categoria."}), 400

    # Se passou por todas as regras, cria o lançamento
    novo_lancamento = Lancamento(
        descricao=dados.get('descricao'),
        valor=float(valor),
        tipo=tipo,
        usuario_id=dados.get('usuario_id'),
        conta_id=dados.get('conta_id'),
        categoria_id=categoria_id,
        data=datetime.strptime(dados.get('data'), '%Y-%m-%d').date() if dados.get('data') else datetime.utcnow()
    )
    
    db.session.add(novo_lancamento)
    db.session.commit()

    return jsonify({"mensagem": "Lançamento registrado com sucesso!", "id": novo_lancamento.id}), 201

if __name__ == '__main__':
    app.run(debug=True)




    
    