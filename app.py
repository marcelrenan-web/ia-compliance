import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Configurações da Página ---
st.set_page_config(
    page_title="IA de Compliance",
    page_icon="🛡️",
    layout="wide"
)

# --- Barra lateral de navegação ---
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione uma opção:", ["Página Inicial", "Painel RH/Compliance"])

# --- Página Inicial (Denúncias Anônimas) ---
if page == "Página Inicial":
    st.title("🛡️ IA Assistente de Compliance")
    st.markdown("""
    Sua voz é essencial para construirmos um ambiente de trabalho mais ético e seguro.  
    **Todas as denúncias são anônimas.** Nenhum dado de identificação é solicitado.
    """)
    st.markdown("---")

    st.header("📋 Formulário de Denúncia Anônima")

    denuncia_texto = st.text_area("Descreva o ocorrido:", height=200)
    setor_escolhido = st.selectbox(
        "Selecione o setor onde ocorreu:",
        ("", "Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outro")
    )

    botao_enviar = st.button("Enviar Denúncia")

    if botao_enviar:
        if denuncia_texto and setor_escolhido:
            st.success("✅ Sua denúncia foi enviada com sucesso! Agradecemos sua colaboração.")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")

# --- Página Painel RH/Compliance ---
elif page == "Painel RH/Compliance":
    st.title("📊 Painel RH/Compliance")
    st.markdown("---")

    # --- Login simples ---
    st.subheader("🔐 Área Restrita")
    senha_correta = "12345"  # Altere esta senha conforme desejar
    senha = st.text_input("Digite a senha de acesso:", type="password")

    if senha == senha_cor_
