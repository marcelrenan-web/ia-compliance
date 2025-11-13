import streamlit as st

# ---------------------------------------------------
# Sistema simples de autenticação para RH/Compliance
# ---------------------------------------------------

def login_form():
    """Renderiza o formulário de login na sidebar."""
    st.sidebar.header("🔐 Login RH/Compliance")

    usuario = st.sidebar.text_input("Usuário:")
    senha = st.sidebar.text_input("Senha:", type="password")

    if st.sidebar.button("Entrar"):
        if usuario == "admin" and senha == "1234":
            st.session_state["autenticado"] = True
            st.sidebar.success("Login realizado!")
        else:
            st.sidebar.error("Usuário ou senha incorretos.")


def verificar_login():
    """Garante que apenas usuários autenticados vejam o painel."""
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        login_form()
        st.warning("Área restrita. Faça login para continuar.")
        st.stop()
