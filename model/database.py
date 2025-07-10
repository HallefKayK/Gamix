import psycopg2
from psycopg2 import pool
from config import Config
import logging

class Database:
    """Classe para gerenciar conexões com o banco de dados PostgreSQL"""
    
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls):
        """Inicializa o pool de conexões"""
        try:
            cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,  # min e max conexões
                **Config.DB_CONFIG
            )
            logging.info("Pool de conexões inicializado com sucesso")
        except Exception as e:
            logging.error(f"Erro ao inicializar pool de conexões: {e}")
            raise
    
    @classmethod
    def get_connection(cls):
        """Obtém uma conexão do pool"""
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
        """Retorna uma conexão para o pool"""
        if cls._connection_pool and conn:
            cls._connection_pool.putconn(conn)
    
    @classmethod
    def close_pool(cls):
        """Fecha o pool de conexões"""
        if cls._connection_pool:
            cls._connection_pool.closeall()
            cls._connection_pool = None
    
    def __init__(self):
        """Inicializa uma instância da classe Database"""
        self.conn = None
        self.cursor = None
        self._connect()
    
    def _connect(self):
        """Estabelece conexão com o banco"""
        try:
            self.conn, self.cursor = self.get_connection()
        except Exception as e:
            logging.error(f"Erro na conexão: {e}")
            raise
    
    def executar(self, sql, params=None):
        """Executa uma query SQL (INSERT, UPDATE, DELETE)"""
        try:
            self.cursor.execute(sql, params)
            return True
        except Exception as e:
            logging.error(f"Erro ao executar query: {e}")
            return False
    
    def consultar(self, sql, params=None):
        """Executa uma consulta SQL (SELECT) e retorna os resultados"""
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Erro ao consultar: {e}")
            return []
    
    def consultar_um(self, sql, params=None):
        """Executa uma consulta SQL e retorna apenas um resultado"""
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchone()
        except Exception as e:
            logging.error(f"Erro ao consultar um registro: {e}")
            return None
    
    def fechar(self):
        """Fecha a conexão atual"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.return_connection(self.conn)
        except Exception as e:
            logging.error(f"Erro ao fechar conexão: {e}")
    
    def __enter__(self):
        self.cursor.execute(f"SET search_path TO {Config.DB_SCHEMA};")
        return self

    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager - saída"""
        self.fechar()


class DatabaseManager:
    """Classe utilitária para operações específicas do banco"""
    
    @staticmethod
    def criar_schema_e_tabelas():
        """Cria o schema e tabelas necessárias"""
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
                    logging.info(f"Comando executado com sucesso")
                else:
                    logging.error(f"Erro ao executar comando: {sql}")
    
    @staticmethod
    def inserir_dados_exemplo():
        """Insere dados de exemplo nas tabelas"""
        with Database() as db:
            # Inserir desenvolvedores
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
            
            # Inserir gêneros
            generos = ["Ação", "RPG", "Aventura", "Estratégia", "Simulação", "Esportes"]
            for genero in generos:
                db.executar(
                    "INSERT INTO generos (nome) VALUES (%s) ON CONFLICT DO NOTHING",
                    (genero,)
                )
