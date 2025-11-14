# services/banco.py

from services.supabase import supabase
import uuid
from datetime import datetime

def insert_denuncia(setor, tipo, descricao):
    codigo = str(uuid.uuid4())[:8]

    data = {
        "codigo": codigo,
        "setor": setor,
        "tipo": tipo,
        "descricao": descricao,
        "sentimento": None,
        "data_envio": datetime.now().isoformat()
    }

    supabase.table("denuncias").insert(data).execute()

    return codigo
