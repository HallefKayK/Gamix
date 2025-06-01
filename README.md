# 🎮 Gamix – Loja de Jogos Online

Gamix é um sistema de gerenciamento de uma loja de jogos digitais inspirado na Steam. Este projeto foi desenvolvido como avaliação da disciplina de Banco de Dados, com foco na criação e manipulação de dados em PostgreSQL via ODBC, utilizando Python com arquitetura MVC.

## 🧱 Estrutura do Banco de Dados

O banco de dados foi modelado com 6 tabelas principais, organizadas em um schema próprio. Abaixo estão as tabelas e seus relacionamentos:

### 🗂️ Tabelas

- **jogos**
  - Armazena os dados dos jogos disponíveis na loja.
  - Relaciona-se com: `desenvolvedores`, `generos`.

- **clientes**
  - Registra os usuários da plataforma.
  - Relaciona-se com: `compras`.

- **compras**
  - Registra o histórico de compras feitas pelos clientes.
  - Relaciona-se com: `clientes`, `jogos`.

- **generos**
  - Contém os gêneros dos jogos (RPG, Ação, etc.).
  - Relaciona-se com: `jogos`.

- **desenvolvedores**
  - Empresas ou estúdios responsáveis pelos jogos.
  - Relaciona-se com: `jogos`.

- **avaliacoes**
  - Notas e comentários de clientes sobre os jogos.
  - Relaciona-se com: `clientes`, `jogos`.

### 🔗 Relacionamentos

- `clientes (1) ⟶ (N) compras`
- `jogos (1) ⟶ (N) compras`
- `clientes (1) ⟶ (N) avaliacoes`
- `jogos (1) ⟶ (N) avaliacoes`
- `generos (1) ⟶ (N) jogos`
- `desenvolvedores (1) ⟶ (N) jogos`

## 🛠️ Tecnologias Utilizadas

- **PostgreSQL** com schema exclusivo
- **Python** com padrão **MVC**
- **Conexão via ODBC**
- **Interface Web** com formulários para CRUD
- **Consultas SQL complexas** com:
  - JOINs
  - Subconsultas (`IN`, `ANY`, `ALL`, `EXISTS`)
  - Agrupamentos (`GROUP BY`)
  - Operações com datas
  - Ordenações e filtros (`LIKE`, `BETWEEN`)
  - Comandos de conjunto (`UNION`, `INTERSECT`, `EXCEPT`)

## 📝 Regras de Modelagem

- Todas as tabelas têm **chave primária (PK)** autoincremental com uso de `SEQUENCE`.
- Tabelas com relacionamentos N:M usam **chave primária composta**.
- Foram aplicadas restrições de:
  - **NOT NULL**
  - **CHECK**
  - **UNIQUE**
- Relacionamentos representados por **chaves estrangeiras (FK)**.

## 👨‍💻 Desenvolvido por

- Hallef KayK Damacena Oliveira


---

