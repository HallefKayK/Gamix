import psycopg2

class Database:
    def __init__(self):
        self.conexao = psycopg2.connect(
            dbname="gamix",
            user="gamixuser",
            password="1234",
            host="localhost",
            port="5432"
        )
        self.conexao.autocommit = True
        self.cursor = self.conexao.cursor()
        self.cursor.execute("SET search_path TO gamix;")

    def executar(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
        except Exception as e:
            print("Erro ao executar:", e)

    def consultar(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Exception as e:
            print("Erro ao consultar:", e)
            return []

    def fechar(self):
        self.cursor.close()
        self.conexao.close()
