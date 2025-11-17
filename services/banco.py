from services.supabase_client import get_supabase_or_raise
from datetime import datetime, date
import uuid

TABLE_NAME = "Denuncias" # Nome exatamente igual ao Supabase

# Função agora recebe o novo parâmetro data_servico
def insert_denuncia(setor, tipo, descricao, data_servico: date, sentimento="Neutro"):
    supabase = get_supabase_or_raise()

    data = {
        "sua_id": str(uuid.uuid4()), # ID para acompanhamento
        "setor": setor,
        "tipo": tipo, # O tipo selecionado (Moral, Sexual, etc.)
        "descricao": descricao,
        "sentimento": sentimento,
        "data_poste": datetime.utcnow().isoformat(), # Data de registro no sistema
        
        # CAMPO CORRIGIDO: Agora enviamos 'data_servico' para o banco
        "data_servico": data_servico.isoformat() 
    }

    # Executa a inserção
    # OBS: O nome 'data_poste' no código python é 'data_registro' no CSV/banco? 
    # Mantenha a consistência entre o nome da chave python (data_poste) e o nome da coluna no Supabase.
    supabase.table(TABLE_NAME).insert(data).execute()

    # Retorna o ID para o usuário acompanhar o caso
    return data["sua_id"]
