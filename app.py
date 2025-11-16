import streamlit as st
from utils.layout import aplicar_layout
from utils.sessao import is_logged_in, logout_user

st.set_page_config(page_title="Portal Vigia Ético", page_icon="🛡️", layout="wide")
aplicar_layout()

st.sidebar.image("logo.svg", width=140)  # coloque logo.svg na raiz (opcional)
st.sidebar.markdown("### Portal Vigia Ético")

# Menu simples de navegação
st.sidebar.markdown("---")
st.sidebar.markdown("**Navegação**")
st.sidebar.write("[Registrar denúncia](./pages/1_Registrar_Denuncia.py)")
st.sidebar.write("[Painel RH (login)](./pages/2_Painel_Analise.py)")
st.sidebar.markdown("---")

# se estiver logado, mostra botão de logout
if is_logged_in():
    st.sidebar.success(f"Logado como: {st.session_state['auth_user']['email']}")
    if st.sidebar.button("Sair"):
        logout_user()
        st.experimental_rerun()

st.title("🛡️ Portal Vigia Ético")
st.markdown("Bem-vindo! Use o menu lateral para enviar uma denúncia (público) ou acessar o painel (RH).")

