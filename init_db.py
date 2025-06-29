#!/usr/bin/env python3
"""
Script para inicializar o banco de dados do Gamix
"""

import sys
import os
import logging
from datetime import datetime

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from model.database import Database, DatabaseManager

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def criar_dados_exemplo():
    """Cria dados de exemplo para teste"""
    try:
        with Database() as db:
            # Inserir usuários de exemplo
            usuarios_exemplo = [
                ("João Silva", "joao@email.com", "senha123"),
                ("Maria Santos", "maria@email.com", "senha456"),
                ("Pedro Oliveira", "pedro@email.com", "senha789"),
                ("Ana Costa", "ana@email.com", "senha321"),
                ("Carlos Ferreira", "carlos@email.com", "senha654")
            ]
            
            for nome, email, senha in usuarios_exemplo:
                # Verificar se usuário já existe
                if not db.consultar_um("SELECT id FROM usuarios WHERE email = %s", (email,)):
                    db.executar(
                        "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                        (nome, email, senha)
                    )
                    logging.info(f"Usuário {nome} criado com sucesso")
            
            # Inserir pedidos de exemplo
            pedidos_exemplo = [
                (1, 150.00),
                (2, 89.90),
                (3, 199.99),
                (1, 45.50),
                (4, 120.00)
            ]
            
            for usuario_id, valor in pedidos_exemplo:
                db.executar(
                    "INSERT INTO pedidos (usuario_id, valor_total) VALUES (%s, %s)",
                    (usuario_id, valor)
                )
            
            logging.info("Dados de exemplo criados com sucesso")
            
    except Exception as e:
        logging.error(f"Erro ao criar dados de exemplo: {e}")

def main():
    """Função principal"""
    print("🎮 Inicializando banco de dados do Gamix...")
    
    try:
        # Inicializar pool de conexões
        Database.initialize_pool()
        logging.info("Pool de conexões inicializado")
        
        # Criar schema e tabelas
        DatabaseManager.criar_schema_e_tabelas()
        logging.info("Schema e tabelas criados")
        
        # Inserir dados de exemplo
        DatabaseManager.inserir_dados_exemplo()
        criar_dados_exemplo()
        
        print("✅ Banco de dados inicializado com sucesso!")
        print("\nPróximos passos:")
        print("1. Execute: pip install -r requirements.txt")
        print("2. Execute: python controller/app.py")
        print("3. Acesse: http://localhost:5000")
        
    except Exception as e:
        logging.error(f"Erro na inicialização: {e}")
        print(f"❌ Erro: {e}")
        sys.exit(1)
    
    finally:
        # Fechar pool de conexões
        Database.close_pool()

if __name__ == "__main__":
    main()
