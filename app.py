import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# -----------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------
st.set_page_config(page_title="IA Assistente de Compliance", layout="wide")
st.title("🔒 IA Assistente de Compliance")

# -----------------------------
# LOGIN SIMPLES
# -----------------------------
usuario = st.text_input("Usuário:")
senha = st.text_input("Senha:", type="password")

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if st.button("Entrar"):
    if usuario == "admin" and senha == "1234":
        st.session_state['autenticado'] = True
        st.success("Login realizado com sucesso!")
    else:
        st.error("Usuário ou senha incorretos.")

# -----------------------------
# CONEXÃO COM BANCO DE DADOS
# -----------------------------
conn = sqlite3.connect("denuncias.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS denuncias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        setor TEXT,
        tipo_ocorrencia TEXT,
        descricao TEXT,
        data_envio TIMESTAMP
    )
''')
conn.commit()

# -----------------------------
# FORMULÁRIO DE DENÚNCIA (SEM LOGIN)
# -----------------------------
st.header("📢 Registrar Denúncia Anônima")

setor = st.selectbox("Selecione o setor relacionado ao fato:",
                     ("Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros"))

tipo_assedio = st.selectbox("Tipo de ocorrência:",
                            ("Assédio Moral", "Assédio Sexual", "Racismo", "Homofobia", "Discriminação", "Outros"))

descricao = st.text_area("Descreva o ocorrido:")

if st.button("Enviar Denúncia"):
    if descricao.strip() == "":
        st.warning("Por favor, descreva o ocorrido.")
    else:
        c.execute("INSERT INTO denuncias (setor, tipo_ocorrencia, descricao, data_envio) VALUES (?, ?, ?, ?)",
                  (setor, tipo_assedio, descricao, datetime.now()))
        conn.commit()
        st.success("✅ Denúncia enviada com sucesso! Sua identidade será preservada.")

# -----------------------------
# PAINEL RH/COMPLIANCE
# -----------------------------
if st.session_state['autenticado']:
    st.markdown("---")
    st.header("📊 Painel de Análise de Denúncias")

    df = pd.read_sql_query("SELECT * FROM denuncias", conn)

    if not df.empty:
        # Gráfico por tipo
        contagem_tipo = df['tipo_ocorrencia'].value_counts().reset_index()
        contagem_tipo.columns = ['Tipo de Ocorrência', 'Número de Casos']

        # Gráfico por setor
        contagem_setor = df['setor'].value_counts().reset_index()
        contagem_setor.columns = ['Setor', 'Número de Casos']

        # Gráfico temporal
        df['Mês'] = pd.to_datetime(df['data_envio']).dt.to_period('M').astype(str)
        contagem_temporal = df['Mês'].value_counts().sort_index().reset_index()
        contagem_temporal.columns = ['Mês', 'Número de Casos']

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Casos por Tipo de Ocorrência")
            fig_bar = px.bar(contagem_tipo, x='Tipo de Ocorrência', y='Número de Casos',
                             color='Tipo de Ocorrência', title="Distribuição de Casos por Tipo")
            st.plotly_chart(fig_bar
