# 🏦 API RESTful - Sistema de Gestão Financeira Pessoal

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Status-Conclu%C3%ADdo-success?style=for-the-badge" alt="Status">
</div>

<br>

> **Descrição:** Uma API Backend robusta desenvolvida para o registro e controle de movimentações financeiras. O sistema garante a integridade dos dados através de validações rigorosas e relacionamentos complexos de banco de dados.

---

## 📑 Índice
- [Arquitetura e Tecnologias](#-arquitetura-e-tecnologias)
- [Diagrama de Entidade-Relacionamento (DER)](#-diagrama-do-banco-de-dados)
- [Regras de Negócio e Segurança](#-regras-de-negócio-e-segurança)
- [Guia de Instalação e Execução](#-guia-de-instalação-e-execução)
- [Documentação da API (Endpoints)](#-documentação-da-api-endpoints)

---

## 🛠 Arquitetura e Tecnologias

O projeto adota o padrão de desenvolvimento de APIs modernas, focando em separação de responsabilidades e segurança:

* **Framework Web:** `Flask` (Microframework de alta performance)
* **ORM (Mapeamento Objeto-Relacional):** `SQLAlchemy`
* **Controle de Versão do Banco:** `Flask-Migrate` (Baseado em Alembic)
* **Banco de Dados:** `SQLite` (Padrão ACID)
* **Segurança de Variáveis:** `python-dotenv`

---

## 📊 Diagrama do Banco de Dados

O sistema foi modelado utilizando as melhores práticas de banco de dados relacional (1:N):

```mermaid
erDiagram
    USUARIO ||--o{ CONTA : possui
    USUARIO ||--o{ LANCAMENTO : registra
    CONTA ||--o{ LANCAMENTO : contem
    CATEGORIA ||--o{ LANCAMENTO : classifica

    USUARIO {
        int id PK
        string nome
        string email
        string senha_hash
    }
    CATEGORIA {
        int id PK
        string nome
        string descricao
    }
    CONTA {
        int id PK
        string nome
        int usuario_id FK
    }
    LANCAMENTO {
        int id PK
        string descricao
        float valor
        string tipo "entrada/saida"
        date data
        int usuario_id FK
        int conta_id FK
        int categoria_id FK
    }