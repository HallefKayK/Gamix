#!/usr/bin/env python3
"""
Script para testar a conexão com o banco de dados
"""

import sys
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_db_connection():
    """Testa a conexão com o banco de dados"""
    print("\n🔌 Testando conexão com o banco de dados...")
    
    try:
        # Primeiro tenta conectar ao PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",
            user="gamixuser",
            password="1234",
            host="localhost",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print("✅ Conexão ao PostgreSQL estabelecida")
        
        # Verifica se o banco gamix existe
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='gamix'")
        exists = cursor.fetchone()
        
        if not exists:
            print("⚠️  Banco de dados 'gamix' não encontrado. Criando...")
            cursor.execute("CREATE DATABASE gamix")
            print("✅ Banco de dados 'gamix' criado com sucesso")
        else:
            print("✅ Banco de dados 'gamix' encontrado")
        
        cursor.close()
        conn.close()
        
        # Tenta conectar ao banco gamix
        conn = psycopg2.connect(
            dbname="gamix",
            user="gamixuser",
            password="1234",
            host="localhost",
            port="5432"
        )
        print("✅ Conexão ao banco 'gamix' estabelecida")
        
        # Verifica se o schema existe
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM information_schema.schemata WHERE schema_name='gamix'")
        exists = cursor.fetchone()
        
        if not exists:
            print("⚠️  Schema 'gamix' não encontrado. Criando...")
            cursor.execute("CREATE SCHEMA gamix")
            print("✅ Schema 'gamix' criado com sucesso")
        else:
            print("✅ Schema 'gamix' encontrado")
        
        # Verifica as tabelas necessárias
        tables = ['usuarios', 'pedidos']
        for table in tables:
            cursor.execute(f"""
                SELECT 1 FROM information_schema.tables 
                WHERE table_schema='gamix' AND table_name='{table}'
            """)
            exists = cursor.fetchone()
            if exists:
                print(f"✅ Tabela '{table}' encontrada")
                # Conta registros
                cursor.execute(f"SELECT COUNT(*) FROM gamix.{table}")
                count = cursor.fetchone()[0]
                print(f"  └─ {count} registros encontrados")
            else:
                print(f"❌ Tabela '{table}' não encontrada")
        
        cursor.close()
        conn.close()
        print("\n✅ Teste de banco de dados concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar banco de dados: {e}")
        return False

if __name__ == "__main__":
    success = test_db_connection()
    sys.exit(0 if success else 1)
