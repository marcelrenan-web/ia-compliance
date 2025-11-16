from datetime import datetime
import uuid
import pandas as pd
from services.supabase_client import supabase

TABLE_NAME = "denuncias"  # nome exato da sua tabela no Supabase

def gerar_codigo():
    return str(uuid.uuid4())[:8].upper()

def insert_denuncia(setor, tipo_ocorrencia, descricao):
    codigo = gerar_codigo()
    data = {
        "id": codigo,  # usamos id como chave textual curta
        "setor": setor,
        "tipo_ocorrencia": tipo_ocorrencia,
        "descricao": descricao,
        "data_envio": datetime.utcnow().isoformat()
    }
    supabase.table(TABLE_NAME).insert(data).execute()
    return codigo

def fetch_denuncias():
    resp = supabase.table(TABLE_NAME).select("*").order("data_envio", desc=False).execute()
    if resp.data:
        return pd.DataFrame(resp.data)
    return pd.DataFrame()
