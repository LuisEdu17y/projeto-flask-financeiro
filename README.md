# 🏦 Finanças Premium - Sistema de Gestão Full-Stack

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/UI--UX-Premium-4F46E5?style=for-the-badge" alt="UI-UX">
  <img src="https://img.shields.io/badge/Status-Conclu%C3%ADdo-success?style=for-the-badge" alt="Status">
</div>

<br>

> **Descrição:** Uma solução Full-Stack completa que evoluiu de uma ferramenta simples para um ecossistema financeiro automatizado. O sistema agora conta com uma interface **Premium**, eliminando a necessidade de lidar com IDs manuais e focando totalmente na experiência do usuário.

---

## 📑 Índice
- [Arquitetura e Tecnologias](#-arquitetura-e-tecnologias)
- [✨ O Grande Upgrade de Hoje](#-o-grande-upgrade-de-hoje)
- [Diagrama de Entidade-Relacionamento (DER)](#-diagrama-do-banco-de-dados)
- [Guia de Instalação e Execução](#-guia-de-instalação-e-execução)
- [Regras de Negócio e Segurança](#-regras-de-negócio-e-segurança)

---

## 🛠 Arquitetura e Tecnologias

O projeto adota o padrão de desenvolvimento de aplicações modernas, focando em separação de responsabilidades:

* **Backend:** `Flask` (Microframework) integrado com `SQLAlchemy` para gestão de dados.
* **Frontend:** Interface moderna com `JavaScript (Fetch API)` e `CSS Grid/Flexbox` para responsividade.
* **Banco de Dados:** Transição concluída para `MySQL`, garantindo robustez e escalabilidade.
* **Controle de Versão do Banco:** `Flask-Migrate` para versionamento de esquemas.
* **Segurança:** Proteção de chaves com `python-dotenv` e controle de acesso via `Flask-CORS`.

---

## ✨ O Grande Upgrade de Hoje

Nesta versão, focamos em **Automação e Estética**:

* **Automação de IDs:** O usuário não precisa mais saber ou digitar o ID de uma categoria ou conta. O sistema carrega os nomes dinamicamente do banco de dados para campos de seleção (dropdowns).
* **Design Premium:** Implementação de uma interface limpa, com sombras suaves, tipografia "Inter" e badges coloridos para diferenciar receitas (verde) de despesas (vermelho).
* **Sincronização em Tempo Real:** Ao registrar um lançamento, a tabela é atualizada instantaneamente sem necessidade de recarregar a página.

---

## 📊 Diagrama do Banco de Dados

Modelagem relacional (1:N) garantindo a integridade dos dados:

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