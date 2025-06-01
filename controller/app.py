from flask import Flask, request, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="gamix",
        user="gamixuser",
        password="1234",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SET search_path TO gamix;")
    return conn, cursor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    conn, cursor = get_db_connection()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
            (nome, email, senha)
        )
    except Exception as e:
        print("Erro ao inserir no banco:", e)
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('usuarios'))

@app.route('/usuarios')
def usuarios():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT id, nome, email FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    conn, cursor = get_db_connection()
    cursor.execute(
        "SELECT * FROM usuarios WHERE email = %s AND senha = %s",
        (email, senha)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if usuario:
        return "Login bem-sucedido"
    else:
        return "Usuário ou senha inválidos"

@app.route('/consulta/data')
def consulta_data():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT nome, email, EXTRACT(YEAR FROM data_cadastro) FROM usuarios")
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_data.html", resultado=resultado)

@app.route('/consulta/relacional')
def consulta_relacional():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT nome, email FROM usuarios WHERE id > 1 AND email LIKE '%%@%%.com'")
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_relacional.html", resultado=resultado)

@app.route('/consulta/juncao')
def consulta_juncao():
    conn, cursor = get_db_connection()
    cursor.execute("""
        SELECT u.nome, p.id, p.data_pedido
        FROM usuarios u
        JOIN pedidos p ON u.id = p.usuario_id
    """)
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_juncao.html", resultado=resultado)

@app.route('/consulta/group_by')
def consulta_group_by():
    conn, cursor = get_db_connection()
    cursor.execute("""
        SELECT EXTRACT(YEAR FROM data_cadastro) AS ano, COUNT(*)
        FROM usuarios
        GROUP BY ano
        ORDER BY ano DESC
    """)
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_group_by.html", resultado=resultado)

@app.route('/consulta/between')
def consulta_between():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT nome, email FROM usuarios WHERE id BETWEEN 1 AND 10")
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_between.html", resultado=resultado)

@app.route('/consulta/order_by')
def consulta_order():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT nome, email FROM usuarios ORDER BY nome DESC")
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_order_by.html", resultado=resultado)

@app.route('/consulta/distinct')
def consulta_distinct():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT DISTINCT EXTRACT(YEAR FROM data_cadastro) FROM usuarios")
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_distinct.html", resultado=resultado)

@app.route('/consulta/like')
def consulta_like():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT nome FROM usuarios WHERE nome ILIKE 'j%%'")
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_like.html", resultado=resultado)

@app.route('/consulta/exists')
def consulta_exists():
    conn, cursor = get_db_connection()
    cursor.execute("""
        SELECT nome FROM usuarios u
        WHERE EXISTS (
            SELECT 1 FROM pedidos p WHERE p.usuario_id = u.id
        )
    """)
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_exists.html", resultado=resultado)

@app.route('/consulta/in')
def consulta_in():
    conn, cursor = get_db_connection()
    cursor.execute("""
        SELECT nome FROM usuarios
        WHERE id IN (SELECT usuario_id FROM pedidos)
    """)
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_in.html", resultado=resultado)

@app.route('/consulta/count')
def consulta_count():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    resultado = cursor.fetchall()
    conn.close()
    return render_template("consulta_count.html", resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
