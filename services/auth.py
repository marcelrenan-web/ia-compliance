import streamlit as st
from supabase import create_client
from utils.session import salvar_sessao, limpar_sessao

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login(email, senha):
    try:
        resposta = supabase.auth.sign_in_with_password({
            "email": email,
            "password": senha
        })

        if resposta.user is not None:
            salvar_sessao(resposta.user.email)
            return True
        else:
            return False

    except Exception:
        return False


def logout():
    limpar_sessao()
    st.success("Você saiu com sucesso.")
