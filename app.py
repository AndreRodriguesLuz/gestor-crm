import pandas as pd

import database as db
import streamlit as st

st.set_page_config(
    page_title="Gestor CRM | Pipeline & Atendimento",
    page_icon="💼",
    layout="wide",
)

# Injeção de Design System Moderno (Removendo a faixa branca superior e aplicando o tema escuro)
st.markdown("""
    <style>
        /* Oculta o cabeçalho superior padrão do Streamlit (faixa branca) */
        header[data-testid="stHeader"] {
            background: transparent !important;
            visibility: hidden;
        }
        
        /* Fundo principal */
        .stApp {
            background-color: #0f172a;
            color: #f8fafc;
            margin-top: -40px;
        }
        
        /* Estilização da Sidebar e legibilidade dos textos */
        section[data-testid="stSidebar"] {
            background-color: #1e293b;
        }
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] .stRadio p,
        section[data-testid="stSidebar"] span {
            color: #ffffff !important;
            font-size: 15px !important;
        }
        
        /* Força todos os labels/títulos de inputs e textos explicativos a ficarem em BRANCO VIVO */
        label, .stTextInput label, .stSelectbox label, .stCheckbox label, p {
            color: #ffffff !important;
        }
        
        /* Títulos com destaque visual Ciano */
        h1, h2, h3 {
            color: #38bdf8 !important;
            font-weight: 600;
        }
        
        /* Inputs, Selectboxes e Text Areas */
        div[data-baseweb="select"] > div, input, textarea {
            background-color: #1e293b !important;
            color: #ffffff !important;
            border-color: #334155 !important;
        }
        
        /* Correção GLOBAL para todos os botões do Streamlit */
        div.stButton > button, div.stFormSubmitButton > button {
            background-color: #1e293b !important;
            color: #38bdf8 !important;
            border: 2px solid #38bdf8 !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        
        /* Efeito de passar o rato nos botões */
        div.stButton > button:hover, div.stFormSubmitButton > button:hover {
            background-color: #38bdf8 !important;
            color: #0f172a !important;
            border-color: #38bdf8 !important;
        }
        
        /* Força a cor do texto interno dos botões */
        div.stButton > button p, div.stFormSubmitButton > button p {
            color: inherit !important;
            font-weight: 600 !important;
        }
        
        /* Estilização das tabelas */
        .stDataFrame, div[data-testid="stTable"] {
            background-color: #1e293b;
            border-radius: 8px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Gestor CRM & Atendimentos")
st.caption(
    "Aplicação de Gestão de Leads com CRUD Relacional em SQLite, Soft Delete e"
    " Arquitetura Limpa."
)

# Sidebar - Navegação
st.sidebar.header("📌 Menu Principal")

menu = st.sidebar.radio(
    "Navegação",
    ["Pipeline de Clientes", "Cadastrar Cliente", "Registrar Atendimento"],
)

# -------------------------------------------------------------------
# ABA 1: PIPELINE DE CLIENTES (READ, UPDATE, SOFT DELETE & RESTORE)
# -------------------------------------------------------------------
if menu == "Pipeline de Clientes":
  st.subheader("📋 Gestão de Leads e Clientes")

  col_f1, col_f2 = st.columns(2)
  with col_f1:
    filtro = st.selectbox(
        "Filtrar por Status",
        ["Todos", "Novo", "Em Atendimento", "Fechado", "Perdido"],
    )
  with col_f2:
    mostrar_arquivados = st.checkbox("Mostrar Clientes Arquivados", value=False)

  dados = db.listar_clientes(
      apenas_ativos=not mostrar_arquivados,
      filtro_status=filtro if filtro != "Todos" else None,
  )

  if dados:
    df = pd.DataFrame(
        dados,
        columns=[
            "ID",
            "Nome",
            "E-mail",
            "Telefone",
            "Status",
            "Ativo",
            "Data Criação",
        ],
    )
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("⚡ Atualizar / Gerenciar Cliente")
    col_sel, col_act1, col_act2 = st.columns([2, 2, 2])

    with col_sel:
      opcoes_clientes = {
          d[0]: f"ID {d[0]} - {d[1]} ({'Ativo' if d[5] == 1 else 'Arquivado'})"
          for d in dados
      }
      cliente_selecionado = st.selectbox(
          "Selecione o Cliente (ID)",
          options=list(opcoes_clientes.keys()),
          format_func=lambda x: opcoes_clientes[x],
      )

    # Busca isolada e segura do cliente selecionado
    cliente_info = next((d for d in dados if d[0] == cliente_selecionado), None)
    status_ativo = cliente_info[5] if cliente_info else 1

    with col_act1:
      novo_status = st.selectbox(
          "Novo Status", ["Novo", "Em Atendimento", "Fechado", "Perdido"]
      )
      if st.button("Atualizar Status"):
        db.atualizar_status_cliente(cliente_selecionado, novo_status)
        db.registrar_interacao(
            cliente_selecionado,
            "Atualização de Sistema",
            f"Status alterado para: {novo_status}",
        )
        st.success(
            f"Status do ID {cliente_selecionado} atualizado e registado no"
            " histórico!"
        )
        st.rerun()

    with col_act2:
      st.write("Gestão de Estado (Ativo / Arquivado)")

      if status_ativo == 0:
        if st.button("Desarquivar / Reativar Cliente"):
          db.reativar_cliente(cliente_selecionado)
          st.success(f"Cliente ID {cliente_selecionado} desarquivado com sucesso!")
          st.rerun()
      else:
        if st.button("Arquivar Cliente"):
          db.arquivar_cliente(cliente_selecionado)
          st.warning(f"Cliente ID {cliente_selecionado} arquivado!")
          st.rerun()

    # --- Seção para Editar Dados Cadastrais do Cliente ---
    if cliente_info:
      st.markdown("---")
      with st.expander(
          f"✏️ Editar Dados Cadastrais (ID {cliente_selecionado})"
      ):
        with st.form(f"form_editar_{cliente_selecionado}"):
          col_e1, col_e2, col_e3 = st.columns(3)
          with col_e1:
            novo_nome = st.text_input("Nome Completo", value=cliente_info[1])
          with col_e2:
            novo_email = st.text_input("E-mail", value=cliente_info[2])
          with col_e3:
            novo_telefone = st.text_input(
                "Telefone", value=cliente_info[3] if cliente_info[3] else ""
            )

          btn_salvar_edicao = st.form_submit_button("Salvar Alterações")
          if btn_salvar_edicao:
            if novo_nome and novo_email:
              sucesso, msg = db.atualizar_dados_cliente(
                  cliente_selecionado, novo_nome, novo_email, novo_telefone
              )
              if sucesso:
                db.registrar_interacao(
                    cliente_selecionado,
                    "Atualização Cadastral",
                    f"Dados editados para - Nome: {novo_nome}, E-mail:"
                    f" {novo_email}, Telefone: {novo_telefone}",
                )
                st.success(msg)
                st.rerun()
              else:
                st.error(msg)
            else:
              st.warning("Nome e e-mail são obrigatórios.")

    # Histórico de Atendimentos
    st.markdown("---")
    st.subheader(f"📜 Histórico do Cliente ID: {cliente_selecionado}")
    historico = db.listar_interacoes_cliente(cliente_selecionado)
    if historico:
      df_hist = pd.DataFrame(
          historico, columns=["Tipo Contato", "Observação", "Data"]
      )
      st.table(df_hist)
    else:
      st.info("Nenhuma interação registrada para este cliente ainda.")
  else:
    st.info("Nenhum cliente encontrado com os filtros selecionados.")

# -------------------------------------------------------------------
# ABA 2: CADASTRAR CLIENTE (CREATE)
# -------------------------------------------------------------------
elif menu == "Cadastrar Cliente":
  st.subheader("➕ Novo Cliente")
  with st.form("form_cadastrar"):
    nome = st.text_input("Nome Completo *")
    email = st.text_input("E-mail *")
    telefone = st.text_input("Telefone / WhatsApp")
    status = st.selectbox(
        "Status Inicial", ["Novo", "Em Atendimento", "Fechado"]
    )

    submitted = st.form_submit_button("Salvar Cliente")
    if submitted:
      if nome and email:
        sucesso, msg = db.adicionar_cliente(nome, email, telefone, status)
        if sucesso:
          st.success(msg)
        else:
          st.error(msg)
      else:
        st.warning("Preencha todos os campos obrigatórios (*).")

# -------------------------------------------------------------------
# ABA 3: REGISTRAR ATENDIMENTO (CREATE RELACIONAL)
# -------------------------------------------------------------------
elif menu == "Registrar Atendimento":
  st.subheader("💬 Novo Registro de Atendimento")
  clientes_ativos = db.listar_clientes(apenas_ativos=True)

  if clientes_ativos:
    opcoes_clientes = {c[0]: f"{c[0]} - {c[1]} ({c[2]})" for c in clientes_ativos}
    cliente_id = st.selectbox(
        "Selecione o Cliente",
        options=list(opcoes_clientes.keys()),
        format_func=lambda x: opcoes_clientes[x],
    )
    tipo_contato = st.selectbox(
        "Canal de Atendimento",
        ["WhatsApp / Chat", "E-mail", "Telefone", "Reunião Online"],
    )
    observacao = st.text_area("Notas do Atendimento")

    if st.button("Salvar Histórico"):
      if observacao:
        db.registrar_interacao(cliente_id, tipo_contato, observacao)
        st.success("Interação gravada no banco de dados!")
      else:
        st.warning("Escreva uma breve nota sobre o atendimento.")
  else:
    st.warning("Nenhum cliente ativo disponível. Cadastre um cliente primeiro.")