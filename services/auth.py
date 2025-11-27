
@@ -1,19 +1,25 @@

import streamlit as st
from utils.sessao import set_user, is_logged_in, logout_user

def autenticar(usuario, senha):
    return usuario == "admin" and senha == "1234"
# credenciais demo (substitua por Supabase Auth se quiser)
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASS = "1234"

def login():
    st.title("🔐 Login")
def ensure_logged_in():
    # se já autenticado, apenas retorna
    if is_logged_in():
        return True

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.session_state.logado = True
            st.success("Login realizado!")
            st.switch_page("app.py")
    st.sidebar.markdown("---")
    st.sidebar.header("🔐 Login RH/Compliance")
    email = st.sidebar.text_input("Email", key="login_email")
    pwd = st.sidebar.text_input("Senha", type="password", key="login_pwd")
    if st.sidebar.button("Entrar"):
        if email == ADMIN_EMAIL and pwd == ADMIN_PASS:
            set_user({"email": email})
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")
            st.sidebar.error("Credenciais inválidas.")
    # se não logou, stop para páginas privadas
    return is_logged_in()
