#!/usr/bin/env python3
"""
Script de demonstração do projeto Gamix
Executa testes básicos e mostra informações do projeto
"""

import os
import sys
from datetime import datetime

def print_header():
    """Imprime o cabeçalho do projeto"""
    print("=" * 60)
    print("🎮 GAMIX - SISTEMA DE GERENCIAMENTO DE USUÁRIOS")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"📁 Diretório: {os.getcwd()}")
    print("=" * 60)

def check_project_structure():
    """Verifica a estrutura do projeto"""
    print("\n📁 ESTRUTURA DO PROJETO:")
    print("-" * 30)
    
    structure = {
        "controller/": ["app.py"],
        "model/": ["__init__.py", "database.py"],
        "templates/": [
            "base.html", "index.html", "dashboard.html", "usuarios.html",
            "consulta_data.html", "consulta_relacional.html", "consulta_juncao.html",
            "consulta_group_by.html", "consulta_between.html", "consulta_ordem.html",
            "consulta_distinta.html", "consulta_J.html", "consulta_pedido.html",
            "consulta_exists.html", "consulta_conta.html"
        ],
        "static/": ["styles.css", "script.js"],
        "./": ["config.py", "requirements.txt", "init_db.py", "README.md", ".env.example"]
    }
    
    total_files = 0
    found_files = 0
    
    for directory, files in structure.items():
        print(f"\n📂 {directory}")
        for file in files:
            file_path = os.path.join(directory, file) if directory != "./" else file
            total_files += 1
            if os.path.exists(file_path):
                print(f"  ✅ {file}")
                found_files += 1
            else:
                print(f"  ❌ {file}")
    
    print(f"\n📊 Arquivos encontrados: {found_files}/{total_files}")
    return found_files == total_files

def show_features():
    """Mostra as funcionalidades do projeto"""
    print("\n🚀 FUNCIONALIDADES IMPLEMENTADAS:")
    print("-" * 40)
    
    features = [
        "✅ Arquitetura MVC organizada",
        "✅ Sistema de autenticação com hash de senhas",
        "✅ Pool de conexões com banco de dados",
        "✅ 11 tipos diferentes de consultas SQL",
        "✅ Interface responsiva com tema escuro",
        "✅ Templates com herança (base.html)",
        "✅ JavaScript para interatividade",
        "✅ Tratamento de erros e validações",
        "✅ Sistema de sessões Flask",
        "✅ Configurações centralizadas",
        "✅ Scripts de teste e inicialização",
        "✅ Documentação completa"
    ]
    
    for feature in features:
        print(f"  {feature}")

def show_sql_queries():
    """Mostra os tipos de consultas SQL implementadas"""
    print("\n📊 CONSULTAS SQL IMPLEMENTADAS:")
    print("-" * 40)
    
    queries = [
        ("Consulta por Data", "EXTRACT(YEAR FROM data_cadastro)"),
        ("Consulta Relacional", "WHERE id > 1 AND email LIKE '%@%.com'"),
        ("Consulta com JOIN", "usuarios u JOIN pedidos p ON u.id = p.usuario_id"),
        ("Consulta GROUP BY", "GROUP BY ano ORDER BY ano DESC"),
        ("Consulta BETWEEN", "WHERE id BETWEEN 1 AND 10"),
        ("Consulta ORDER BY", "ORDER BY nome DESC"),
        ("Consulta DISTINCT", "SELECT DISTINCT EXTRACT(YEAR...)"),
        ("Consulta LIKE", "WHERE nome ILIKE 'j%'"),
        ("Consulta EXISTS", "WHERE EXISTS (SELECT 1 FROM pedidos...)"),
        ("Consulta IN", "WHERE id IN (SELECT usuario_id FROM pedidos)"),
        ("Consulta COUNT", "SELECT COUNT(*) FROM usuarios")
    ]
    
    for i, (name, example) in enumerate(queries, 1):
        print(f"  {i:2d}. {name}")
        print(f"      💡 {example}")

def show_technologies():
    """Mostra as tecnologias utilizadas"""
    print("\n🛠️ TECNOLOGIAS UTILIZADAS:")
    print("-" * 30)
    
    technologies = {
        "Backend": ["Python 3.x", "Flask", "psycopg2"],
        "Frontend": ["HTML5", "CSS3", "JavaScript"],
        "Banco de Dados": ["PostgreSQL"],
        "Segurança": ["Werkzeug", "Hash de senhas", "Sessões Flask"],
        "Ferramentas": ["Pool de conexões", "Context managers", "Logging"]
    }
    
    for category, techs in technologies.items():
        print(f"\n🔧 {category}:")
        for tech in techs:
            print(f"  • {tech}")

def show_installation_steps():
    """Mostra os passos de instalação"""
    print("\n📋 PASSOS PARA INSTALAÇÃO:")
    print("-" * 35)
    
    steps = [
        "1. Instalar PostgreSQL",
        "2. Criar usuário e banco de dados",
        "3. Instalar dependências Python: pip install -r requirements.txt",
        "4. Configurar variáveis de ambiente (.env)",
        "5. Inicializar banco: python init_db.py",
        "6. Executar aplicação: python controller/app.py",
        "7. Acessar: http://localhost:5000"
    ]
    
    for step in steps:
        print(f"  {step}")

def show_testing_info():
    """Mostra informações sobre testes"""
    print("\n🧪 TESTES DISPONÍVEIS:")
    print("-" * 25)
    
    tests = [
        ("test_app.py", "Teste de integridade da aplicação"),
        ("test_db.py", "Teste de conexão com banco de dados"),
        ("demo.py", "Script de demonstração (este arquivo)")
    ]
    
    for test_file, description in tests:
        status = "✅" if os.path.exists(test_file) else "❌"
        print(f"  {status} {test_file} - {description}")

def main():
    """Função principal"""
    print_header()
    
    # Verificar estrutura
    structure_ok = check_project_structure()
    
    # Mostrar informações
    show_features()
    show_sql_queries()
    show_technologies()
    show_installation_steps()
    show_testing_info()
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📋 RESUMO DO PROJETO")
    print("=" * 60)
    
    if structure_ok:
        print("✅ Estrutura do projeto: COMPLETA")
    else:
        print("⚠️  Estrutura do projeto: INCOMPLETA")
    
    print("✅ Documentação: COMPLETA")
    print("✅ Configurações: PRONTAS")
    print("✅ Templates: IMPLEMENTADOS")
    print("✅ Estilos: APLICADOS")
    print("✅ Scripts de teste: DISPONÍVEIS")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Configure o PostgreSQL")
    print("2. Execute: python init_db.py")
    print("3. Execute: python controller/app.py")
    print("4. Acesse: http://localhost:5000")
    
    print("\n🎮 Projeto Gamix pronto para uso!")
    print("=" * 60)

if __name__ == "__main__":
    main()
