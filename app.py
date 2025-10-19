import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------
st.set_page_config(page_title="IA Assistente de Compliance", layout="wide")

# -----------------------------
# LOGIN SIMPLES
# -----------------------------
st.title("🔒 IA Assistente de Compliance")

usuario = st.text_input("Usuário:")
senha = st.text_input("Senha:", type="password")

if st.button("Entrar"):
    if usuario == "admin" and senha == "1234":
        st.session_state["autenticado"] = True
        st.success("Login realizado com sucesso!")
    else:
        st.error("Usuário ou senha incorretos.")

# -----------------------------
# PÁGINA PRINCIPAL (APÓS LOGIN)
# -----------------------------
if st.session_state.get("autenticado"):

    st.header("📢 Registrar Denúncia")

    # Campo de seleção do setor
    setor = st.selectbox(
        "Selecione o setor relacionado ao fato:",
        ("Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros")
    )

    # Campo de seleção do tipo de assédio
    tipo_assedio = st.selectbox(
        "Tipo de ocorrência:",
        ("Assédio Moral", "Assédio S
