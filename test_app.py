#!/usr/bin/env python3
"""
Script de teste para verificar se a aplicação Gamix está funcionando corretamente
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se todas as importações estão funcionando"""
    print("🔍 Testando importações...")
    
    try:
        from config import Config
        print("✅ Config importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar Config: {e}")
        return False
    
    try:
        from model.database import Database, DatabaseManager
        print("✅ Database importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar Database: {e}")
        return False
    
    try:
        from flask import Flask
        print("✅ Flask importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar Flask: {e}")
        return False
    
    return True

def test_config():
    """Testa se as configurações estão corretas"""
    print("\n🔧 Testando configurações...")
    
    try:
        from config import Config
        
        # Verificar se as configurações essenciais existem
        required_configs = ['DB_NAME', 'DB_USER', 'DB_HOST', 'DB_PORT', 'SECRET_KEY']
        
        for config in required_configs:
            if hasattr(Config, config):
                print(f"✅ {config}: {getattr(Config, config)}")
            else:
                print(f"❌ {config}: Não encontrado")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar configurações: {e}")
        return False

def test_templates():
    """Testa se os templates existem"""
    print("\n📄 Testando templates...")
    
    templates_dir = "templates"
    required_templates = [
        "base.html",
        "index.html", 
        "dashboard.html",
        "usuarios.html"
    ]
    
    if not os.path.exists(templates_dir):
        print(f"❌ Diretório {templates_dir} não encontrado")
        return False
    
    for template in required_templates:
        template_path = os.path.join(templates_dir, template)
        if os.path.exists(template_path):
            print(f"✅ {template}")
        else:
            print(f"❌ {template}: Não encontrado")
            return False
    
    return True

def test_static_files():
    """Testa se os arquivos estáticos existem"""
    print("\n🎨 Testando arquivos estáticos...")
    
    static_dir = "static"
    required_files = ["styles.css", "script.js"]
    
    if not os.path.exists(static_dir):
        print(f"❌ Diretório {static_dir} não encontrado")
        return False
    
    for file in required_files:
        file_path = os.path.join(static_dir, file)
        if os.path.exists(file_path):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}: Não encontrado")
            return False
    
    return True

def test_flask_app():
    """Testa se a aplicação Flask pode ser criada"""
    print("\n🌐 Testando aplicação Flask...")
    
    try:
        # Importar sem executar
        import controller.app as app_module
        print("✅ Módulo da aplicação importado com sucesso")
        
        # Verificar se o app foi criado
        if hasattr(app_module, 'app'):
            print("✅ Instância Flask criada com sucesso")
            
            # Verificar algumas rotas
            routes = [rule.rule for rule in app_module.app.url_map.iter_rules()]
            print(f"✅ {len(routes)} rotas registradas")
            
            # Mostrar algumas rotas importantes
            important_routes = ['/', '/usuarios', '/dashboard', '/login', '/cadastrar']
            for route in important_routes:
                if route in routes:
                    print(f"  ✅ {route}")
                else:
                    print(f"  ❌ {route}: Não encontrada")
            
            return True
        else:
            print("❌ Instância Flask não encontrada")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar aplicação Flask: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🎮 GAMIX - TESTE DE INTEGRIDADE DA APLICAÇÃO")
    print("=" * 50)
    
    tests = [
        ("Importações", test_imports),
        ("Configurações", test_config),
        ("Templates", test_templates),
        ("Arquivos Estáticos", test_static_files),
        ("Aplicação Flask", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Executando teste: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSOU")
        else:
            print(f"❌ {test_name}: FALHOU")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO FINAL: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! A aplicação está pronta para uso.")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
