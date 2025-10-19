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
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

with st.sidebar:
    st.header("Login RH/Compliance")
    usuario = st.text_input("Usuário:")
    senha = st.text_input("Senha:", type="password")
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
        d
