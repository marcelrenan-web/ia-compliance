import uuid
from datetime import datetime, date
from services.supabase_client import get_supabase_or_raise # Importa a função de cliente
from postgrest.exceptions import APIError
from typing import List, Dict, Any

# Nome exato da sua tabela no Supabase
TABLE_NAME = "Denuncias" 

def insert_denuncia(setor: str, tipo: str, descricao: str, data_servico: date, sentimento: str = "Neutro") -> str: # CORREÇÃO: 'sentimento' agora tem um valor padrão para evitar erro de argumento ausente.
    """Insere uma nova denúncia no Supabase."""
    try:
        supabase = get_supabase_or_raise() # Garante que o cliente existe
    except ConnectionError as e:
        print(f"Erro: Cliente Supabase não está inicializado. Detalhes: {e}")
        return "Falha na conexão"

    try:
        dados = {
            "id": str(uuid.uuid4()),
            "tipo": tipo,
            "setor": setor,
            "descricao": descricao,
            "sentimento": sentimento,
            # CRÍTICO: O Supabase preenche 'created_at'. Estamos apenas enviando a data do serviço.
            "data_servico": data_servico.isoformat(), 
        }

        # Insere e retorna o resultado
        response = supabase.table(TABLE_NAME).insert(dados).execute()
        
        # O Supabase retorna a linha inserida
        if response.data:
            # Retorna o ID para o usuário acompanhar (opcional)
            return response.data[0].get("id", "ID não disponível")
        else:
            return "Falha na inserção"

    except APIError as e:
        print(f"Erro de API ao inserir denúncia: {e}")
        return "Erro de API"
    except Exception as e:
        print(f"Erro inesperado ao inserir denúncia: {e}")
        return "Erro inesperado"

def get_all_denuncias() -> List[Dict[str, Any]]:
    """Busca todas as denúncias no Supabase e padroniza o nome da coluna de data."""
    try:
        supabase = get_supabase_or_raise()
    except ConnectionError:
        return []

    try:
        # Busca todas as colunas
        # Certifique-se de que a RLS (SELECT) esteja configurada corretamente para o 'authenticated' role!
        response = supabase.table(TABLE_NAME).select("*").execute()
        
        data = response.data

        # CRÍTICO: Mapeia o nome real da coluna 'created_at' (Supabase) para 'data_registro' (Python/Pandas)
        for row in data:
            if 'created_at' in row:
                # Renomeia 'created_at' para 'data_registro' e remove o original
                row['data_registro'] = row.pop('created_at') 
            
        return data
    
    except APIError as e:
        print(f"Erro de API ao buscar denúncias: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado ao buscar denúncias: {e}")
        return []
