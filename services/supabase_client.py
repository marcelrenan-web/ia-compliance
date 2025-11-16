import streamlit as st

def login_screen():
    st.title("🔐 Login - Portal Vigia Ético")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username == "admin" and password == "1234":
            st.session_state["logged"] = True
            st.session_state["user"] = username
        else:
            st.error("Credenciais inválidas.")

def require_login():
    """Impede acesso às páginas privadas se não estiver logado."""
    if "logged" not in st.session_state:
        st.session_state["logged"] = False

    if st.session_state["logged"] is False:
        login_screen()
        st.stop()
