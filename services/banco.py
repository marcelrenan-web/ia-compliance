from services.supabase_client import get_supabase_or_raise # CORRIGIDO (Importação Absoluta)
from datetime import datetime, date
import uuid

TABLE_NAME = "Denuncias" # Nome da tabela no Supabase

# Função para inserir nova denúncia (requer RLS INSERT para 'anon')
def insert_denuncia(setor, tipo, descricao, data_servico: date, sentimento="Neutro"):
    """Insere uma nova denúncia anônima no Supabase."""
    supabase = get_supabase_or_raise()

    data = {
        "sua_id": str(uuid.uuid4()), 
        "setor": setor,
        "tipo": tipo, 
        "descricao": descricao,
        "sentimento": sentimento,
        # NOME PADRONIZADO: data_registro
        "data_registro": datetime.utcnow().isoformat(), 
        "data_servico": data_servico.isoformat() 
    }from services.supabase_client import get_supabase_or_raise # CORRIGIDO (Importação Absoluta)
from datetime import datetime, date
import uuid

TABLE_NAME = "Denuncias" # Nome da tabela no Supabase

# Função para inserir nova denúncia (requer RLS INSERT para 'anon')
def insert_denuncia(setor, tipo, descricao, data_servico: date, sentimento="Neutro"):
    """Insere uma nova denúncia anônima no Supabase."""
    supabase = get_supabase_or_raise()

    data = {
        "sua_id": str(uuid.uuid4()), 
        "setor": setor,
        "tipo": tipo, 
        "descricao": descricao,
        "sentimento": sentimento,
        # CORREÇÃO CRÍTICA: O nome da coluna no seu DB é 'data_poste' (não 'data_registro')
        "data_poste": datetime.utcnow().isoformat(), 
        "data_servico": data_servico.isoformat() 
    }

    # Executa a inserção
    supabase.table(TABLE_NAME).insert(data).execute()

    return data["sua_id"]

# Função para buscar todos os dados de denúncias para o painel de análise (requer RLS SELECT para 'authenticated')
def get_all_denuncias():
    """Busca todas as denúncias da tabela para visualização no painel."""
    supabase = get_supabase_or_raise()
    
    # Busca todos os dados da tabela 'Denuncias'
    response = supabase.table(TABLE_NAME).select("*").execute()
    
    # O resultado vem em 'data' dentro da resposta
    return response.data

    # Executa a inserção
    supabase.table(TABLE_NAME).insert(data).execute()

    return data["sua_id"]

# Função para buscar todos os dados de denúncias para o painel de análise (requer RLS SELECT para 'authenticated')
def get_all_denuncias():
    """Busca todas as denúncias da tabela para visualização no painel."""
    supabase = get_supabase_or_raise()
    
    # Busca todos os dados da tabela 'Denuncias'
    response = supabase.table(TABLE_NAME).select("*").execute()
    
    # O resultado vem em 'data' dentro da resposta
    return response.data
