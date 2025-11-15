
import streamlit as st

def autenticar(usuario, senha):
    return usuario == "admin" and senha == "1234"

def login():
    st.title("🔐 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.session_state.logado = True
            st.success("Login realizado!")
            st.switch_page("app.py")
        else:
            st.error("Usuário ou senha incorretos.")
