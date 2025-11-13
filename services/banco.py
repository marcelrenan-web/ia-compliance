from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import uuid
import streamlit as st

# -------------------------------------------
# Carregar credenciais do Streamlit Secrets
# -------------------------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------------------
# Funções do Banco (Denúncias)
# -------------------------------------------

def gerar_codigo_unico():
    return str(uuid.uuid4())[:8].upper()

def insert_denuncia(setor, tipo_ocorrencia, descricao):
    data_envio = datetime.now().isoformat()
    codigo = gerar_codigo_unico()

    denuncia = {
        "id": codigo,
        "setor": setor,
        "tipo_ocorrencia": tipo_ocorrencia,
        "descricao": descricao,
        "data_envio": data_envio
    }

    supabase.table("denuncias").insert(denuncia).execute()
    return codigo

def fetch_denuncias():
    response = supabase.table("denuncias").select("*").execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame()
