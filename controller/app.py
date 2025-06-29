from flask import Flask, request, render_template, redirect, url_for, flash, session
import logging
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from model.database import Database, DatabaseManager

# Configuração de logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Inicializar banco de dados na inicialização da aplicação
def initialize_database():
    """Inicializa o banco de dados e cria tabelas se necessário"""
    try:
        Database.initialize_pool()
        DatabaseManager.criar_schema_e_tabelas()
        logging.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logging.error(f"Erro ao inicializar banco: {e}")

# Chamar inicialização na criação da aplicação
initialize_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])

        with Database() as db:
            # Verificar se email já existe
            if db.consultar_um("SELECT id FROM usuarios WHERE email = %s", (email,)):
                flash('Email já cadastrado', 'error')
                return redirect(url_for('index'))
            
            # Inserir novo usuário
            db.executar(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, senha)
            )
            flash('Cadastro realizado com sucesso!', 'success')
            
        return redirect(url_for('usuarios'))
    except Exception as e:
        logging.error(f"Erro no cadastro: {e}")
        flash('Erro ao realizar cadastro', 'error')
        return redirect(url_for('index'))

@app.route('/usuarios')
def usuarios():
    try:
        with Database() as db:
            usuarios = db.consultar("SELECT id, nome, email FROM usuarios")
        return render_template('usuarios.html', usuarios=usuarios)
    except Exception as e:
        logging.error(f"Erro ao listar usuários: {e}")
        flash('Erro ao carregar usuários', 'error')
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        senha = request.form['senha']

        with Database() as db:
            usuario = db.consultar_um(
                "SELECT id, nome, email, senha FROM usuarios WHERE email = %s",
                (email,)
            )

        if usuario and check_password_hash(usuario[3], senha):
            session['user_id'] = usuario[0]
            session['user_name'] = usuario[1]
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha inválidos', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Erro no login: {e}")
        flash('Erro ao realizar login', 'error')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Rotas de consulta
@app.route('/consulta/data')
def consulta_data():
    try:
        with Database() as db:
            resultado = db.consultar(
                "SELECT nome, email, EXTRACT(YEAR FROM data_cadastro) FROM usuarios"
            )
        return render_template("consulta_data.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta por data: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

@app.route('/consulta/relacional')
def consulta_relacional():
    try:
        with Database() as db:
            resultado = db.consultar(
                "SELECT nome, email FROM usuarios WHERE id > 1 AND email LIKE '%%@%%.com'"
            )
        return render_template("consulta_relacional.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta relacional: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

@app.route('/consulta/juncao')
def consulta_juncao():
    try:
        with Database() as db:
            resultado = db.consultar("""
                SELECT u.nome, p.id, p.data_pedido
                FROM usuarios u
                JOIN pedidos p ON u.id = p.usuario_id
            """)
        return render_template("consulta_juncao.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta de junção: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

@app.route('/consulta/group_by')
def consulta_group_by():
    try:
        with Database() as db:
            resultado = db.consultar("""
                SELECT EXTRACT(YEAR FROM data_cadastro) AS ano, COUNT(*)
                FROM usuarios
                GROUP BY ano
                ORDER BY ano DESC
            """)
        return render_template("consulta_group_by.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta group by: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

@app.route('/consulta/between')
def consulta_between():
    try:
        with Database() as db:
            resultado = db.consultar(
                "SELECT nome, email FROM usuarios WHERE id BETWEEN 1 AND 10"
            )
        return render_template("consulta_between.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta between: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

@app.route('/consulta/order_by')
def consulta_order():
    try:
        with Database() as db:
            resultado = db.consultar(
                "SELECT nome, email FROM usuarios ORDER BY nome DESC"
            )
        return render_template("consulta_ordem.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta ordenada: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

@app.route('/consulta/distinct')
def consulta_distinct():
    try:
        with Database() as db:
            resultado = db.consultar(
                "SELECT DISTINCT EXTRACT(YEAR FROM data_cadastro) FROM usuarios"
            )
        return render_template("consulta_distinta.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta distinct: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

@app.route('/consulta/like')
def consulta_like():
    try:
        with Database() as db:
            resultado = db.consultar(
                "SELECT nome FROM usuarios WHERE nome ILIKE 'j%%'"
            )
        return render_template("consulta_J.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta like: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

@app.route('/consulta/exists')
def consulta_exists():
    try:
        with Database() as db:
            resultado = db.consultar("""
                SELECT nome FROM usuarios u
                WHERE EXISTS (
                    SELECT 1 FROM pedidos p WHERE p.usuario_id = u.id
                )
            """)
        return render_template("consulta_exists.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta exists: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

@app.route('/consulta/in')
def consulta_in():
    try:
        with Database() as db:
            resultado = db.consultar("""
                SELECT nome FROM usuarios
                WHERE id IN (SELECT usuario_id FROM pedidos)
            """)
        return render_template("consulta_pedido.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta in: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

@app.route('/consulta/count')
def consulta_count():
    try:
        with Database() as db:
            resultado = db.consultar("SELECT COUNT(*) FROM usuarios")
        return render_template("consulta_conta.html", resultado=resultado)
    except Exception as e:
        logging.error(f"Erro na consulta count: {e}")
        flash('Erro ao realizar consulta', 'error')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
