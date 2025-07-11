import psycopg2
from psycopg2 import pool
from config import Config
import logging

class Database:
    _connection_pool = None

    @classmethod
    def initialize_pool(cls):
        try:
            cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,
                **Config.DB_CONFIG
            )
            logging.info("Pool de conexões inicializado com sucesso")
        except Exception as e:
            logging.error(f"Erro ao inicializar pool de conexões: {e}")
            raise

    @classmethod
    def get_connection(cls):
        if cls._connection_pool is None:
            cls.initialize_pool()
        try:
            conn = cls._connection_pool.getconn()
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"SET search_path TO {Config.DB_SCHEMA};")
            return conn, cursor
        except Exception as e:
            logging.error(f"Erro ao obter conexão: {e}")
            raise

    @classmethod
    def return_connection(cls, conn):
        if cls._connection_pool and conn:
            cls._connection_pool.putconn(conn)

    @classmethod
    def close_pool(cls):
        if cls._connection_pool:
            cls._connection_pool.closeall()
            cls._connection_pool = None

    def __init__(self):
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        try:
            self.conn, self.cursor = self.get_connection()
        except Exception as e:
            logging.error(f"Erro na conexão: {e}")
            raise

    def executar(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
            return True
        except Exception as e:
            logging.error(f"Erro ao executar query: {e}")
            return False

    def consultar(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Erro ao consultar: {e}")
            return []

    def consultar_um(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchone()
        except Exception as e:
            logging.error(f"Erro ao consultar um registro: {e}")
            return None

    def fechar(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.return_connection(self.conn)
        except Exception as e:
            logging.error(f"Erro ao fechar conexão: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fechar()


class DatabaseManager:
    @staticmethod
    def criar_schema_e_tabelas():
        sql_commands = [
            f"CREATE SCHEMA IF NOT EXISTS {Config.DB_SCHEMA};",
            f"""
            CREATE TABLE IF NOT EXISTS {Config.DB_SCHEMA}.usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {Config.DB_SCHEMA}.pedidos (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES {Config.DB_SCHEMA}.usuarios(id),
                data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                valor_total DECIMAL(10,2) DEFAULT 0.00
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {Config.DB_SCHEMA}.jogos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(200) NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                descricao TEXT,
                data_lancamento DATE,
                desenvolvedor_id INTEGER,
                genero_id INTEGER
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {Config.DB_SCHEMA}.desenvolvedores (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                pais VARCHAR(100)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {Config.DB_SCHEMA}.generos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {Config.DB_SCHEMA}.avaliacoes (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES {Config.DB_SCHEMA}.usuarios(id),
                jogo_id INTEGER REFERENCES {Config.DB_SCHEMA}.jogos(id),
                nota INTEGER CHECK (nota >= 1 AND nota <= 5),
                comentario TEXT,
                data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        ]

        with Database() as db:
            for sql in sql_commands:
                if db.executar(sql):
                    logging.info("Comando executado com sucesso")
                else:
                    logging.error(f"Erro ao executar comando: {sql}")

    @staticmethod
    def inserir_dados_exemplo():
        with Database() as db:
            desenvolvedores = [
                ("Valve Corporation", "Estados Unidos"),
                ("CD Projekt RED", "Polônia"),
                ("Rockstar Games", "Estados Unidos"),
                ("Nintendo", "Japão")
            ]
            for nome, pais in desenvolvedores:
                db.executar(
                    "INSERT INTO desenvolvedores (nome, pais) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (nome, pais)
                )

            generos = ["Ação", "RPG", "Aventura", "Estratégia", "Simulação", "Esportes"]
            for genero in generos:
                db.executar(
                    "INSERT INTO generos (nome) VALUES (%s) ON CONFLICT DO NOTHING",
                    (genero,)
                )
