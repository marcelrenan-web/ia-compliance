import streamlit as st
from utils.sessao import verificar_login, logout
from utils.layout import aplicar_layout

st.set_page_config(
    page_title="Portal Vigia Ético",
    layout="wide",
    page_icon="🛡️"
)

aplicar_layout()

# Controle de Login
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.switch_page("auth.py")
else:
    st.sidebar.title("Menu")
    st.sidebar.page_link("pages/1_Registrar_Denuncia.py", label="Registrar Denúncia")
    st.sidebar.page_link("pages/2_Painel_Analise.py", label="Painel de Análise")
    st.sidebar.button("Sair", on_click=logout)

    st.title("🛡️ Portal Vigia Ético")
    st.markdown("### Bem-vindo ao sistema de denúncias éticas e anônimas.")
