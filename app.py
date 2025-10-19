import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IA Assistente de Compliance", layout="wide")

# Login simples
st.title("🔒 IA Assistente de Compliance")
usuario = st.text_input("Usuário:")
senha = st.text_input("Senha:", type="password")

if st.button("Entrar"):
    if usuario == "admin" and senha == "1234":
        st.session_state["autenticado"] = True
        st.success("Login realizado com sucesso!")
    else:
        st.error("Usuário ou senha incorretos.")

if st.session_state.get("autenticado"):

    st.header("📢 Registrar Denúncia")

    setor = st.selectbox("Selecione o setor relacionado ao fato:",
                         ("Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros"))

    tipo_assedio = st.selectbox("Tipo de ocorrência:",
                                ("Assédio Moral", "Assédio Sexual", "Racismo", "Homofobia", "Discriminação", "Outros"))

    denuncia_texto = st.text_area("Descreva o ocorrido:")

    if st.button("Enviar Denúncia"):
        st.success("✅ Denúncia enviada com sucesso!")
        st.info("Sua identidade será preservada.")

    st.markdown("---")
    st.header("📊 Painel de Análise de Denúncias")

    # Dados simulados
    dados_denunc_
