import pyodbc

class Database:
    def __init__(self):
        self.conn = pyodbc.connect(

            "DRIVER={PostgreSQL Unicode(x64)};"
            "SERVER=localhost;"
            "PORT=5432;"
            "DATABASE=Gamix;"
            "UID=gamixuser;"
            "PWD=1234;"
        )
        self.cursor = self.conn.cursor()

    def executar(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.conn.commit()

    def consultar(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()
