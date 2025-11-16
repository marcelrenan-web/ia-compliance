from services.supabase_client import supabase
from datetime import datetime
import uuid

TABLE_NAME = "denuncias"  # Nome real no Supabase

def insert_denuncia(setor, tipo, descricao, sentimento="Neutro"):
    data = {
        "sua_id": str(uuid.uuid4()),
        "setor": setor,
        "tipo": tipo,
        "descricao": descricao,
        "sentimento": sentimento,
        "data_servico": datetime.utcnow().isoformat()
    }

    supabase.table(TABLE_NAME).insert(data).execute()
    return data["sua_id"]
