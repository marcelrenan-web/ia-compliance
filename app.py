import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# Nome do arquivo do banco de dados (será criado na pasta do projeto)
DB_NAME = "denuncias.db"

# -----------------------------
# FUNÇÕES DE GERENCIAMENTO DO BANCO DE DADOS
# -----------------------------

def get_db_connection():
    """Estabelece a conexão com o banco de dados."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Cria a tabela de denúncias se ela não existir."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS denuncias (
                id INTEGER PRIMARY KEY,
                setor TEXT,
                tipo_ocorrencia TEXT,
                descricao TEXT,
                data_envio TIMESTAMP
            )""")
    conn.commit()
    conn.close()

def insert_denuncia(setor, tipo_ocorrencia, descricao):
    """Insere uma nova denúncia no banco de dados."""
    conn = get_db_connection()
    c = conn.cursor()
    data_envio = datetime.now()
    c.execute("INSERT INTO denuncias (setor, tipo_ocorrencia, descricao, data_envio) VALUES (?, ?, ?, ?)",
              (setor, tipo_ocorrencia, descricao, data_envio))
    conn.commit()
    conn.close()

def fetch_denuncias():
    """Lê todas as denúncias e retorna um DataFrame."""
    conn = get_db_connection()
    # Utiliza pandas para ler diretamente para um DataFrame
    df = pd.read_sql_query("SELECT * FROM denuncias", conn)
    conn.close()
    return df

# Chama a inicialização do DB uma vez (no carregamento inicial do script)
init_db()

# -----------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------
st.set_page_config(page_title="IA Assistente de Compliance", layout="wide")
st.title("🔒 IA Assistente de Compliance")

# -----------------------------
# LOGIN SIMPLES
# -----------------------------
# (Seu código de login permanece o mesmo)
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

with st.sidebar:
    st.header("Login RH/Compliance")
    usuario = st.text_input("Usuário:")
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        # Se você for usar autenticação real, não use credenciais hardcoded
        if usuario == "admin" and senha == "1234":
            st.session_state['autenticado'] = True
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha incorretos.")

# -----------------------------
# FORMULÁRIO DE DENÚNCIA (ANÔNIMO)
# -----------------------------
st.header("📢 Registrar Denúncia Anônima")

with st.form("denuncia_form"):
    setor = st.selectbox("Selecione o setor relacionado ao fato:",
                         ("Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros"))

    tipo_assedio = st.selectbox("Tipo de ocorrência:",
                                ("Assédio Moral", "Assédio Sexual", "Racismo", "Homofobia", "Discriminação", "Outros"))

    descricao = st.text_area("Descreva o ocorrido:")
    
    submitted = st.form_submit_button("Enviar Denúncia")

    if submitted:
        if descricao.strip() == "":
            st.warning("Por favor, descreva o ocorrido.")
        else:
            # CHAVE: Chamada à função de inserção
            insert_denuncia(setor, tipo_assedio, descricao)
            st.success("✅ Denúncia enviada com sucesso! Sua identidade será preservada.")

# -----------------------------
# PAINEL RH/COMPLIANCE
# -----------------------------
if st.session_state['autenticado']:
    st.markdown("---")
    st.header("📊 Painel de Análise de Denúncias")

    # CHAVE: Chamada à função de leitura
    df = fetch_denuncias()

    if not df.empty:
        # ... (O restante do código de gráficos e dataframe permanece o mesmo) ...

        # Contagens para gráficos
        contagem_tipo = df['tipo_ocorrencia'].value_counts().reset_index()
        contagem_tipo.columns = ['Tipo de Ocorrência', 'Número de Casos']

        contagem_setor = df['setor'].value_counts().reset_index()
        contagem_setor.columns = ['Setor', 'Número de Casos']

        # Garantindo que a coluna data_envio está em datetime para manipulação
        df['data_envio'] = pd.to_datetime(df['data_envio'])
        df['Mês'] = df['data_envio'].dt.to_period('M').astype(str)
        contagem_temporal = df['Mês'].value_counts().sort_index().reset_index()
        contagem_temporal.columns = ['Mês', 'Número de Casos']

        # Gráficos
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Casos por Tipo de Ocorrência")
            fig_bar = px.bar(contagem_tipo,
                             x='Tipo de Ocorrência',
                             y='Número de Casos',
                             color='Tipo de Ocorrência',
                             title="Distribuição de Casos por Tipo")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.subheader("🥧 Distribuição por Setor")
            fig_pizza = px.pie(contagem_setor,
                               names='Setor',
                               values='Número de Casos',
                               title="Denúncias por Setor")
            st.plotly_chart(fig_pizza, use_container_width=True)

        st.markdown("---")
        st.subheader("📈 Evolução das Denúncias ao Longo do Tempo")
        fig_linha = px.line(contagem_temporal,
                            x='Mês',
                            y='Número de Casos',
                            markers=True,
                            title="Denúncias Registradas por Mês")
        st.plotly_chart(fig_linha, use_container_width=True)

        st.markdown("---")
        st.subheader("📄 Base de Denúncias")
        st.dataframe(df.drop(columns=['id']), use_container_width=True)
    else:
        st.info("Nenhuma denúncia registrada ainda.")

# Não precisamos mais do conn.close() no final, pois cada função fecha sua própria conexão.
