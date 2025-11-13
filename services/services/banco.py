from supabase import create_client
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def inserir_denuncia(categoria, descricao, usuario):
    supabase.table("denuncias").insert({
        "categoria": categoria,
        "descricao": descricao,
        "usuario": usuario
    }).execute()


def listar_denuncias():
    dados = supabase.table("denuncias").select("*").execute()
    
    if not dados.data:
        return []
    
    return dados.data
