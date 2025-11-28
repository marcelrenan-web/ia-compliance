
import streamlit as st
from utils.sessao import set_user, is_logged_in, logout_user

# credenciais demo (substitua por Supabase Auth se quiser)
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASS = "1234"

def autenticar(usuario, senha):
    """Função de autenticação simples (apenas para o sidebar)"""
    return usuario == ADMIN_EMAIL and senha == ADMIN_PASS

def ensure_logged_in():
    """
    Exibe o formulário de login no sidebar e interrompe a execução
    da página se o usuário não estiver autenticado.
    """
    # 1. Se já autenticado, apenas retorna True
    if is_logged_in():
        return True

    # 2. Se não logado, exibe o formulário no sidebar
    st.sidebar.markdown("---")
    st.sidebar.header("🔐 Login RH/Compliance")
    email = st.sidebar.text_input("Email", key="login_email")
    pwd = st.sidebar.text_input("Senha", type="password", key="login_pwd")
    
    if st.sidebar.button("Entrar"):
        if autenticar(email, pwd):
            # Define o usuário e força um novo carregamento da página
            set_user({"email": email})
            st.success("Login realizado! Recarregando...")
            st.rerun() # Use st.rerun() para atualizar o estado
        else:
            st.sidebar.error("Credenciais inválidas.")
    
    # 3. Se ainda não logou, interrompe a execução da página atual
    if not is_logged_in():
        st.error("Acesso restrito. Por favor, faça login pelo menu lateral.")
        st.stop() # Interrompe a execução da página (Conteúdo privado não será mostrado)

    return True # Retorna True se o usuário estiver logado
