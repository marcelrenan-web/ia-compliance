from services.supabase_client import get_supabase_or_raise
from datetime import datetime
import uuid

TABLE_NAME = "Denuncias"  # Nome exatamente igual ao Supabase

def insert_denuncia(setor, tipo, descricao, sentimento="Neutro"):
    supabase = get_supabase_or_raise()

    data = {
        "sua_id": str(uuid.uuid4()),
        "setor": setor,
        "tipo": tipo,
        "descricao": descricao,
        "sentimento": sentimento,
        "data_poste": datetime.utcnow().isoformat()
    }

    supabase.table(TABLE_NAME).insert(data).execute()

    return data["sua_id"]
