# services/supabase_client.py
import os
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client():
    # tenta st.secrets primeiro, depois variáveis de ambiente
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
    except Exception:
        url = None
        key = None

    if not url:
        url = os.environ.get("SUPABASE_URL")
    if not key:
        key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        # Não lançamos aqui — retornamos None para evitar quebrar o import
        # O código que exigir supabase deverá verificar e mostrar mensagem de erro amigável.
        return None

    return create_client(url, key)

def get_supabase_or_raise():
    client = get_supabase_client()
    if client is None:
        raise RuntimeError("Supabase credentials not found. Configure SUPABASE_URL and SUPABASE_KEY in Streamlit secrets or env.")
    return client
