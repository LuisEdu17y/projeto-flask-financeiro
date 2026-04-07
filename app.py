import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÕES INICIAIS
# ==========================================
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///financeiro.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ==========================================
# 2. MODELAGEM DO BANCO DE DADOS (4 Tabelas)
# ==========================================
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    
    contas = db.relationship('Conta', backref='usuario', lazy=True)
    lancamentos = db.relationship('Lancamento', backref='usuario', lazy=True)

class Conta(db.Model):
    __tablename__ = 'contas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    lancamentos = db.relationship('Lancamento', backref='conta', lazy=True)

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200))
    
    lancamentos = db.relationship('Lancamento', backref='categoria', lazy=True)

class Lancamento(db.Model):
    __tablename__ = 'lancamentos'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    data = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    conta_id = db.Column(db.Integer, db.ForeignKey('contas.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)


# ==========================================
# 3. ROTAS - USUÁRIOS, CONTAS E CATEGORIAS
# ==========================================
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    novo_usuario = Usuario(
        nome=dados.get('nome'),
        email=dados.get('email'),
        senha_hash=dados.get('senha')
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário criado com sucesso!", "id": novo_usuario.id}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    resultado = [{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios]
    return jsonify(resultado), 200

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

@app.route('/categorias', methods=['POST'])
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
# 4. ROTAS - LANÇAMENTOS (CRUD COMPLETO E REGRAS)
# ==========================================

# CREATE - Criar Lançamento (Com Regras de Negócio)
@app.route('/lancamentos', methods=['POST'])
def criar_lancamento():
    dados = request.get_json()
    valor = dados.get('valor')
    tipo = dados.get('tipo')
    categoria_id = dados.get('categoria_id')

    # Regra 1: Valor positivo
    if valor is None or float(valor) <= 0:
        return jsonify({"erro": "Regra violada: O valor do lançamento deve ser maior que zero."}), 400
    
    # Regra 2: Tipo estrito
    if tipo not in ['entrada', 'saida']:
        return jsonify({"erro": "Regra violada: O tipo deve ser exclusivamente 'entrada' ou 'saida'."}), 400
    
    # Regra 3: Categoria obrigatória
    if not categoria_id:
        return jsonify({"erro": "Regra violada: Todo lançamento deve estar associado a uma categoria."}), 400

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

# READ - Listar todos os lançamentos
@app.route('/lancamentos', methods=['GET'])
def listar_lancamentos():
    lancamentos = Lancamento.query.all()
    resultado = []
    for l in lancamentos:
        resultado.append({
            "id": l.id,
            "descricao": l.descricao,
            "valor": l.valor,
            "tipo": l.tipo,
            "data": l.data.strftime('%Y-%m-%d') if l.data else None,
            "usuario_id": l.usuario_id,
            "conta_id": l.conta_id,
            "categoria_id": l.categoria_id
        })
    return jsonify(resultado), 200

# UPDATE - Atualizar um lançamento existente
@app.route('/lancamentos/<int:id>', methods=['PUT'])
def atualizar_lancamento(id):
    lancamento = Lancamento.query.get(id)
    if not lancamento:
        return jsonify({"erro": "Lançamento não encontrado."}), 404
    
    dados = request.get_json()
    
    if 'descricao' in dados:
        lancamento.descricao = dados.get('descricao')
        
    if 'valor' in dados:
        novo_valor = float(dados.get('valor'))
        if novo_valor <= 0:
            return jsonify({"erro": "Regra violada: O valor deve ser maior que zero."}), 400
        lancamento.valor = novo_valor

    if 'tipo' in dados:
        if dados.get('tipo') not in ['entrada', 'saida']:
            return jsonify({"erro": "Regra violada: O tipo deve ser exclusivamente 'entrada' ou 'saida'."}), 400
        lancamento.tipo = dados.get('tipo')

    db.session.commit()
    return jsonify({"mensagem": "Lançamento atualizado com sucesso!"}), 200

# DELETE - Apagar um lançamento
@app.route('/lancamentos/<int:id>', methods=['DELETE'])
def apagar_lancamento(id):
    lancamento = Lancamento.query.get(id)
    if not lancamento:
        return jsonify({"erro": "Lançamento não encontrado."}), 404
    
    db.session.delete(lancamento)
    db.session.commit()
    return jsonify({"mensagem": "Lançamento removido com sucesso!"}), 200


# ==========================================
# 5. INÍCIO DO SERVIDOR
# ==========================================
if __name__ == '__main__':
    app.run(debug=True)



    
    