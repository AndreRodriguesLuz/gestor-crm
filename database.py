import sqlite3

DB_NAME = "gestor_crm.db"


def get_connection():
  """Estabelece a conexão com a base de dados SQLite."""
  conn = sqlite3.connect(DB_NAME)
  # Habilita suporte a chaves estrangeiras no SQLite
  conn.execute("PRAGMA foreign_keys = ON;")
  return conn


def init_db():
  """Cria as tabelas relacionais caso não existam."""
  with get_connection() as conn:
    cursor = conn.cursor()

    # Tabela 1: Clientes / Leads
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefone TEXT,
                status TEXT DEFAULT 'Novo',
                ativo INTEGER DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

    # Tabela 2: Histórico de Interações / Atendimentos (Relacionada por FK)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS interacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                tipo_contato TEXT NOT NULL,
                observacao TEXT NOT NULL,
                data_interacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
            );
        """)
    conn.commit()


# --- OPERAÇÕES CRUD: CLIENTES ---


def adicionar_cliente(nome, email, telefone, status="Novo"):
  """CREATE: Insere um novo cliente com consulta parametrizada."""
  try:
    with get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute(
          """
                INSERT INTO clientes (nome, email, telefone, status)
                VALUES (?, ?, ?, ?)
            """,
          (nome, email, telefone, status),
      )
      conn.commit()
      return True, "Cliente cadastrado com sucesso!"
  except sqlite3.IntegrityError:
    return False, "Erro: E-mail já cadastrado na base de dados."
  except sqlite3.Error as e:
    return False, f"Erro na base de dados: {e}"


def listar_clientes(apenas_ativos=True, filtro_status=None):
  """READ: Retorna a lista de clientes com filtros dinâmicos."""
  with get_connection() as conn:
    cursor = conn.cursor()
    query = "SELECT id, nome, email, telefone, status, ativo, data_criacao FROM clientes WHERE 1=1"
    params = []

    if apenas_ativos:
      query += " AND ativo = 1"
    if filtro_status and filtro_status != "Todos":
      query += " AND status = ?"
      params.append(filtro_status)

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    return cursor.fetchall()


def atualizar_status_cliente(cliente_id, novo_status):
  """UPDATE: Atualiza o status do pipeline do cliente."""
  with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clientes SET status = ? WHERE id = ?",
        (novo_status, cliente_id),
    )
    conn.commit()


def atualizar_dados_cliente(cliente_id, nome, email, telefone):
  """UPDATE: Atualiza as informações cadastrais do cliente."""
  try:
    with get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute(
          """
                UPDATE clientes 
                SET nome = ?, email = ?, telefone = ? 
                WHERE id = ?
            """,
          (nome, email, telefone, cliente_id),
      )
      conn.commit()
      return True, "Dados cadastrais atualizados com sucesso!"
  except sqlite3.IntegrityError:
    return False, "Erro: Este e-mail já pertence a outro cliente."
  except sqlite3.Error as e:
    return False, f"Erro na base de dados: {e}"


def arquivar_cliente(cliente_id):
  """DELETE (SOFT DELETE): Arquiva o cliente sem apagar o histórico."""
  with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clientes SET ativo = 0 WHERE id = ?", (cliente_id,)
    )
    conn.commit()


def reativar_cliente(cliente_id):
  """UPDATE (REATIVAR / DESARQUIVAR): Restaura um cliente arquivado (ativo = 1)."""
  with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clientes SET ativo = 1 WHERE id = ?", (cliente_id,)
    )
    conn.commit()


# --- OPERAÇÕES CRUD: INTERAÇÕES (RELACIONAMENTO) ---


def registrar_interacao(cliente_id, tipo_contato, observacao):
  """CREATE: Registra um atendimento vinculado a um cliente."""
  with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO interacoes (cliente_id, tipo_contato, observacao)
            VALUES (?, ?, ?)
        """,
        (cliente_id, tipo_contato, observacao),
    )
    conn.commit()


def listar_interacoes_cliente(cliente_id):
  """READ: Retorna todo o histórico de um cliente."""
  with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT tipo_contato, observacao, data_interacao 
            FROM interacoes 
            WHERE cliente_id = ? 
            ORDER BY data_interacao DESC
        """,
        (cliente_id,),
    )
    return cursor.fetchall()


# Inicializa a base de dados ao importar
init_db()