
import streamlit as st
from utils.sessao import set_user, is_logged_in, logout_user

# credenciais demo (substitua por Supabase Auth se quiser)
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASS = "1234"

def ensure_logged_in():
    # se já autenticado, apenas retorna
    if is_logged_in():
        return True

    st.sidebar.markdown("---")
    st.sidebar.header("🔐 Login RH/Compliance")
    email = st.sidebar.text_input("Email", key="login_email")
    pwd = st.sidebar.text_input("Senha", type="password", key="login_pwd")
    if st.sidebar.button("Entrar"):
        if email == ADMIN_EMAIL and pwd == ADMIN_PASS:
            set_user({"email": email})
            st.experimental_rerun()
        else:
            st.sidebar.error("Credenciais inválidas.")
    # se não logou, stop para páginas privadas
    return is_logged_in()
