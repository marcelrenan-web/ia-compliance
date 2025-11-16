import streamlit as st

# --- LOGIN SIMPLES (protótipo) ---
def check_password():
    # Se já está logado, não pede senha de novo
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        return True

    st.title("Login do Sistema de Denúncias")

    # Formulário de login
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    # Botão de login
    if st.button("Entrar"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.rerun()  # força atualizar a página já logado
        else:
            st.error("Usuário ou senha incorretos.")

    return False
