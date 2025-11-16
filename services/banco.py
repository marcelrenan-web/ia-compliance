# services/banco.py
from datetime import datetime
import uuid
import pandas as pd
from services.supabase_client import get_supabase_or_raise

TABLE_NAME = "denuncias"

def insert_denuncia(setor, tipo_ocorrencia, descricao):
    supabase = get_supabase_or_raise()
    codigo = str(uuid.uuid4())[:8].upper()
    data = {
        "id": codigo,
        "setor": setor,
        "tipo_ocorrencia": tipo_ocorrencia,
        "descricao": descricao,
        "data_envio": datetime.utcnow().isoformat()
    }
    supabase.table(TABLE_NAME).insert(data).execute()
    return codigo
