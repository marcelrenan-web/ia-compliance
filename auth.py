import streamlit as st
from utils.session import set_user, is_logged_in, logout_user
from services.supabase_client import supabase

# Simple admin auth using a small credentials table in Supabase or fallback hardcoded for demo.
ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASS = '1234'

def ensure_logged_in():
    # if user already in session, show logout
    if is_logged_in():
        st.sidebar.success('Logado como: ' + st.session_state['auth_user']['email'])
        if st.sidebar.button('Sair'):
            logout_user()
            st.experimental_rerun()
        return

    st.sidebar.markdown('---')
    st.sidebar.header('🔐 Login RH/Compliance (demo)')
    email = st.sidebar.text_input('Email', key='login_email')
    senha = st.sidebar.text_input('Senha', type='password', key='login_pwd')
    if st.sidebar.button('Entrar'):
        # Try to check against Supabase auth (if enabled) otherwise simple check.
        try:
            # If using Supabase Auth
            user = None
            # Fallback demo check
            if email == ADMIN_EMAIL and senha == ADMIN_PASS:
                user = {'email': email}
        except Exception:
            user = None
        if user:
            set_user(user)
            st.experimental_rerun()
        else:
            st.sidebar.error('Credenciais inválidas.')
