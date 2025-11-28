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
        return None

    return create_client(url, key)

def get_supabase_or_raise():
    client = get_supabase_client()
    if client is None:
        raise RuntimeError(
            """
            ❗ Supabase client não foi configurado.

            Verifique se os parâmetros estão definidos:

            No Streamlit Cloud:
                [secrets]
                SUPABASE_URL="https://xxxxx.supabase.co"
                SUPABASE_KEY="..."

            Ou como variável de ambiente:
                export SUPABASE_URL="..."
                export SUPABASE_KEY="..."
            """
        )
    return client

# ⚠️ AQUI está o conserto principal
supabase = get_supabase_client()
