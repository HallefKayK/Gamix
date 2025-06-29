import os

class Config:
    """Configurações da aplicação"""
    
    # Configurações do banco de dados
    DB_CONFIG = {
        'dbname': os.getenv('DB_NAME', 'gamix'),
        'user': os.getenv('DB_USER', 'gamixuser'),
        'password': os.getenv('DB_PASSWORD', '1234'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    # Configurações do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'gamix-secret-key-2024')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Schema do banco
    DB_SCHEMA = 'gamix'
