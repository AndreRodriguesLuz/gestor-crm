# 💼 Gestor CRM & Pipeline de Atendimento

Aplicação desenvolvida em *Python, Streamlit e SQLite* para simular um pipeline de atendimento e gestão de clientes, aplicando conceitos de CRUD, modelagem relacional, persistência de dados e histórico de interações.

## 🚀 Diferenciais Técnicos

1. *Operações CRUD*
   - *Create:* cadastro de clientes e registro de interações vinculadas.
   - *Read:* consultas com filtros por status e visualização do histórico de atendimentos.
   - *Update:* edição de dados cadastrais e atualização das etapas do pipeline.
   - *Soft Delete:* arquivamento lógico dos clientes por meio do campo ativo, preservando o histórico e permitindo posterior reativação.

2. *Modelagem Relacional com SQLite*
   - Tabelas clientes e interacoes relacionadas por FOREIGN KEY.
   - Integridade referencial habilitada no SQLite.
   - E-mail definido como único para evitar duplicidade de clientes.

3. *Consultas Parametrizadas*
   - Uso de placeholders ? nas consultas com dados dinâmicos.
   - Redução do risco de SQL Injection ao evitar concatenação direta de entradas do usuário nas queries.

4. *Separação de Responsabilidades*
   - app.py: interface, navegação e interação com o usuário.
   - database.py: conexão, criação das tabelas e operações de persistência.

5. *Histórico de Atendimentos*
   - Registro de contatos vinculados a cada cliente.
   - Rastreamento de alterações de status e atualizações cadastrais.

## 🛠️ Tecnologias Utilizadas

- *Linguagem:* Python 3.x
- *Banco de Dados:* SQLite3
- *Interface:* Streamlit
- *Manipulação de Dados:* Pandas
- *Versionamento:* Git / GitHub