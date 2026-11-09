# 💼 Gestor CRM & Pipeline de Atendimento (Python + SQLite)

Aplicação desenvolvida para simular um pipeline de atendimento e vendas corporativo, demonstrando arquitetura de dados relacional, boas práticas de SQL e operações completas de CRUD.

## 🚀 Diferenciais Técnicos & Operações CRUD

1. **Operações CRUD Completas:**
   - **Create:** Cadastro de novos leads e registro de interações vinculadas.
   - **Read:** Consultas com filtragem dinâmica por status de atendimento e histórico de contatos.
   - **Update:** Atualização reativa das etapas do pipeline do cliente.
   - **Delete (Soft Delete):** Exclusão lógica de registros (`ativo = 0`), preservando o histórico para auditoria sem perder dados.

2. **Modelagem Relacional SQLite:** Uso de duas tabelas conectadas via `FOREIGN KEY` (`clientes` e `interacoes`), garantindo integridade referencial.

3. **Consultas Parametrizadas:** Proteção contra **SQL Injection** em todas as queries.

4. **Arquitetura Limpa:** Separação de responsabilidades entre a camada de persistência (`database.py`) e a camada de interface (`app.py`).

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.x
- **Banco de Dados:** SQLite3
- **Interface:** Streamlit & Pandas