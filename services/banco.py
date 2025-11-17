import uuid
from datetime import datetime
from services.supabase_client import supabase # Importa o cliente inicializado
from postgrest.exceptions import APIError

# Nome exato da sua tabela no Supabase
TABLE_NAME = "denuncias"  

def insert_denuncia(tipo, setor, descricao, sentimento):
    """Insere uma nova denúncia no Supabase, usando a coluna data_poste."""
    if not supabase:
        print("Erro: Cliente Supabase não está inicializado.")
        return False
        
    try:
        dados = {
            "id": str(uuid.uuid4()),
            "tipo": tipo,
            "setor": setor,
            "descricao": descricao,
            "sentimento": sentimento,
            # CRUCIAL: Usamos 'data_poste' para registrar a data e hora
            "data_poste": datetime.now().isoformat()
        }
        
        # O método execute() é a forma correta de interagir com o Supabase Python SDK
        response = supabase.table(TABLE_NAME).insert(dados).execute()
        
        # Verifica se a inserção foi bem-sucedida
        if response.data:
            return True
        return False

    except APIError as e:
        print(f"Erro na inserção do Supabase: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado ao inserir denúncia: {e}")
        return False

def get_all_denuncias():
    """Busca todas as denúncias no Supabase."""
    if not supabase:
        print("Erro: Cliente Supabase não está inicializado.")
        return []
        
    try:
        # Buscamos explicitamente todas as colunas, incluindo 'data_poste'
        response = supabase.table(TABLE_NAME).select('*').execute()
        return response.data if response.data else []
    except APIError as e:
        print(f"Erro ao buscar dados do Supabase: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado ao buscar denúncias: {e}")
        return []
