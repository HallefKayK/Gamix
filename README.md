# 🎮 Gamix - Sistema de Gerenciamento de Usuários

Sistema completo de gerenciamento de usuários com consultas SQL avançadas, desenvolvido em Flask com PostgreSQL.

## 📋 Funcionalidades

### 🔐 Autenticação e Segurança
- ✅ Cadastro de usuários com hash de senha
- ✅ Sistema de login/logout com sessões
- ✅ Validação de dados e tratamento de erros
- ✅ Proteção contra SQL injection

### 📊 Dashboard e Consultas
- ✅ Dashboard interativo com navegação
- ✅ 11 tipos diferentes de consultas SQL:
  - **Consulta por Data**: Extração de ano de cadastro
  - **Consulta Relacional**: Operadores AND e LIKE
  - **Consulta com JOIN**: Relacionamento entre tabelas
  - **Consulta GROUP BY**: Agrupamento e contagem
  - **Consulta BETWEEN**: Intervalos de valores
  - **Consulta ORDER BY**: Ordenação de resultados
  - **Consulta DISTINCT**: Valores únicos
  - **Consulta LIKE**: Busca por padrões
  - **Consulta EXISTS**: Verificação de existência
  - **Consulta IN**: Valores em lista
  - **Consulta COUNT**: Contagem de registros

### 🎨 Interface
- ✅ Design responsivo e moderno
- ✅ Navegação intuitiva com dropdown
- ✅ Tabelas interativas com busca
- ✅ Mensagens de feedback (flash messages)
- ✅ Tema escuro profissional

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask
- **Banco de Dados**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Segurança**: Werkzeug (hash de senhas)
- **Gerenciamento**: Pool de conexões, Context managers

## 📁 Estrutura do Projeto

```
Gamix/
├── controller/
│   └── app.py              # Aplicação Flask principal
├── model/
│   ├── __init__.py
│   └── database.py         # Gerenciamento de banco de dados
├── templates/
│   ├── base.html           # Template base
│   ├── index.html          # Página inicial
│   ├── dashboard.html      # Dashboard principal
│   ├── usuarios.html       # Lista de usuários
│   └── consulta_*.html     # Templates de consultas
├── static/
│   ├── styles.css          # Estilos CSS
│   └── script.js           # JavaScript
├── config.py               # Configurações da aplicação
├── requirements.txt        # Dependências Python
├── init_db.py             # Script de inicialização do BD
├── test_app.py            # Testes de integridade
├── test_db.py             # Testes de banco de dados
├── .env.example           # Exemplo de variáveis de ambiente
└── README.md              # Este arquivo
```

## 🚀 Instalação e Configuração

### 1. Pré-requisitos
- Python 3.7+
- PostgreSQL 12+
- pip (gerenciador de pacotes Python)

### 2. Configuração do Banco de Dados

```sql
-- Conectar ao PostgreSQL como superusuário
sudo -u postgres psql

-- Criar usuário
CREATE USER gamixuser WITH PASSWORD '1234';

-- Criar banco de dados
CREATE DATABASE gamix OWNER gamixuser;

-- Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE gamix TO gamixuser;
```

### 3. Configuração da Aplicação

```bash
# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de configuração
cp .env.example .env

# Inicializar banco de dados
python init_db.py
```

### 4. Executar a Aplicação

```bash
# Método 1: Executar diretamente
python controller/app.py

# Método 2: Usar Flask CLI
python -m flask --app controller/app.py run

# Método 3: Com debug habilitado
python -m flask --app controller/app.py run --debug
```

## 🧪 Testes

```bash
# Teste de integridade da aplicação
python test_app.py

# Teste de conexão com banco de dados
python test_db.py
```

## 📖 Como Usar

### 1. Cadastro de Usuário
- Acesse a página inicial
- Preencha o formulário de cadastro
- Clique em "Cadastrar"

### 2. Login
- Use email e senha cadastrados
- Clique em "Entrar"
- Será redirecionado para o dashboard

### 3. Navegação no Dashboard
- Use o menu dropdown "Consultas SQL"
- Explore as diferentes consultas disponíveis
- Visualize os resultados em tabelas formatadas

### 4. Gerenciamento de Usuários
- Acesse "Ver Usuários" no menu
- Use a busca para filtrar usuários
- Visualize informações dos usuários cadastrados

## 🔧 Configurações (.env)

```env
# Banco de Dados
DB_NAME=gamix
DB_USER=gamixuser
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432

# Flask
SECRET_KEY=gamix-secret-key-2024
FLASK_DEBUG=True

# Schema
DB_SCHEMA=gamix
```

## 🐛 Solução de Problemas

### Erro de Conexão com Banco
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar usuário e banco
sudo -u postgres psql -c "\du"
sudo -u postgres psql -c "\l"
```

### Erro de Dependências
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

## 📝 Logs e Debugging

Os logs da aplicação são exibidos no console. Para debugging:

1. Habilite o modo debug no Flask
2. Verifique os logs no terminal
3. Use as ferramentas de desenvolvedor do navegador

---

**🎮 Gamix** - Sistema completo de gerenciamento com consultas SQL avançadas
