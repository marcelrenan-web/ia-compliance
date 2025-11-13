import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from supabase import create_client, Client
import uuid

# -----------------------------
# CONFIGURAÇÕES DO SUPABASE
# -----------------------------
SUPABASE_URL = "https://SEU-PROJETO.supabase.co"  # substitua
SUPABASE_KEY = "SUA-CHAVE-API"  # substitua
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# FUNÇÕES DE BANCO DE DADOS
# -----------------------------
def gerar_codigo_unico():
    """Gera um código curto e único para a denúncia."""
    return str(uuid.uuid4())[:8].upper()

def insert_denuncia(setor, tipo_ocorrencia, descricao):
    """Insere nova denúncia na tabela Supabase."""
    data_envio = datetime.now().isoformat()
    codigo = gerar_codigo_unico()
    denuncia = {
        "id": codigo,
        "setor": setor,
        "tipo": tipo_ocorrencia,
        "descricao": descricao,
        "data_envio": data_envio
    }
    supabase.table("denuncias").insert(denuncia).execute()
    return codigo

def fetch_denuncias():
    """Lê todas as denúncias do Supabase."""
    response = supabase.table("denuncias").select("*").execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame()

def insert_resolucao(denuncia_id, versao_denunciado, medidas, status_final):
    """Registra a resolução de um caso."""
    data_encerramento = datetime.now().isoformat()
    resolucao = {
        "denuncia_id": denuncia_id,
