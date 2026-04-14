# 🏦 Finanças Premium - Sistema de Gestão Full-Stack

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/CRUD-Completo-success?style=for-the-badge" alt="CRUD">
</div>

<br>

> **Descrição:** Uma solução Full-Stack robusta para gestão financeira pessoal. O sistema oferece um ecossistema automatizado com CRUD completo, validação rigorosa de regras de negócio e uma interface premium desenvolvida para facilitar o controle de gastos e receitas.

📺 **Confira a demonstração do projeto:** [Assista ao vídeo no YouTube](https://youtu.be/dkhkaEB4u1A)

---

## 📑 Índice
- [Arquitetura e Tecnologias](#-arquitetura-e-tecnologias)
- [✨ Funcionalidades Principais](#-funcionalidades-principais)
- [🛣️ Rotas da API](#️-rotas-da-api)
- [📊 Modelagem do Banco de Dados](#-modelagem-do-banco-de-dados)
- [⚖️ Regras de Negócio](#️-regras-de-negócio)
- [🚀 Instalação e Execução](#-instalação-e-execução)

---

## 🛠 Arquitetura e Tecnologias

O projeto adota o padrão de separação de responsabilidades (Client-Server), garantindo uma manutenção simplificada e escalabilidade:

* **Backend:** `Flask` (Python) utilizando `SQLAlchemy` como ORM para abstração do banco de dados.
* **Frontend:** Interface SPA (*Single Page Application*) construída com `HTML5`, `CSS3 (Modern UI)` e `JavaScript (Fetch API)`.
* **Banco de Dados:** `MySQL 8.0` para persistência de dados relacionais.
* **Migrações:** `Flask-Migrate` para controle de versão do esquema do banco de dados.
* **Ambiente:** Gestão de dependências via `requirements.txt` e variáveis de ambiente com `python-dotenv`.

---

## ✨ Funcionalidades Principais

* **Gestão Completa (CRUD):** Possibilidade de Criar, Listar, Atualizar e Deletar lançamentos financeiros em tempo real.
* **Dashboard de Saldo:** Painel dinâmico que calcula o saldo atualizado e altera a identidade visual (cores) baseando-se na saúde financeira (positivo/negativo).
* **Seleção Inteligente:** Carregamento dinâmico de `Contas` e `Categorias` diretamente do banco de dados, eliminando erros de entrada manual de IDs.
* **Interface Responsiva:** Design otimizado para proporcionar uma experiência fluida tanto em desktop quanto em dispositivos móveis.

---

## 🛣️ Rotas da API

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/lancamentos` | Lista todos os lançamentos registrados. |
| `POST` | `/lancamentos` | Cria um novo registro financeiro. |
| `PUT` | `/lancamentos/<id>` | Atualiza os dados de um lançamento específico. |
| `DELETE` | `/lancamentos/<id>` | Remove um registro do banco de dados. |
| `GET` | `/categorias` | Retorna as categorias disponíveis para classificação. |
| `GET` | `/contas` | Retorna as contas bancárias cadastradas. |

---

## 📊 Modelagem do Banco de Dados

O sistema utiliza uma estrutura relacional normalizada com 4 tabelas principais:

```mermaid
erDiagram
    USUARIO ||--o{ CONTA : possui
    USUARIO ||--o{ LANCAMENTO : registra
    CONTA ||--o{ LANCAMENTO : contem
    CATEGORIA ||--o{ LANCAMENTO : classifica

    LANCAMENTO {
        int id PK
        string descricao
        float valor
        string tipo "entrada/saida"
        int usuario_id FK
        int conta_id FK
        int categoria_id FK
    }