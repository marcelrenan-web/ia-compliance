# services/banco.py (VERSÃO FINAL, COMPLETA E CORRIGIDA)

from datetime import date, datetime
from typing import List, Tuple, Optional, Any
import traceback
# Importa Streamlit, pois é usado dentro da função 'upload_evidencia'
import streamlit as st 

# --- CONEXÃO SUPABASE ---
# Tenta importar o cliente Supabase. Se falhar, define como None para evitar o crash imediato.
try:
    from services.supabase_client import supabase
except Exception:
    supabase = None

# --- CONSTANTES ---
TABLE_DENUNCIAS = "Denuncias"
TABLE_RESOLUCOES = "Resolucoes"
BUCKET_EVIDENCIAS = "evidencias"


def _ensure_client():
    """Garante que o cliente Supabase existe ou levanta um erro de configuração."""
    if supabase is None:
        raise RuntimeError("Supabase client não encontrado. Verifique services/supabase_client.py ou as credenciais.")
    return supabase


def insert_denuncia(setor: str,
                    tipo: str,
                    descricao: str,
                    data_servico: date,
                    sentimento: str = "Neutro",
                    anexo_url: Optional[str] = None) -> Any:
    """Insere nova denúncia na tabela TABLE_DENUNCIAS."""
    client = _ensure_client()
    try:
        if isinstance(data_servico, (date, datetime)):
            data_str = data_servico.strftime("%Y-%m-%d")
        else:
            data_str = str(data_servico)

        payload = {
            "setor": setor,
            "tipo": tipo,
            "descricao": descricao,
            "data_registro": data_str,
            "sentimento": sentimento,
            "anexo_url": anexo_url
        }

        # Executa a inserção e retorna os dados inseridos
        resp = client.table(TABLE_DENUNCIAS).insert(payload).execute()
        return resp.data[0] if hasattr(resp, "data") and resp.data else resp

    except Exception as e:
        raise RuntimeError(f"Erro ao inserir denúncia: {e}\n{traceback.format_exc()}")


def get_all_denuncias() -> List[dict]:
    """Retorna todas as denúncias."""
    client = _ensure_client()
    try:
        resp = client.table(TABLE_DENUNCIAS).select("*").order('id', desc=True).execute()
        return resp.data if hasattr(resp, "data") and resp.data else []

    except Exception as e:
        raise RuntimeError(f"Erro ao buscar denúncias: {e}\n{traceback.format_exc()}")


def obter_resumo_para_graficos() -> dict:
    """Contagem por setor e tipo para o painel de análise."""
    dados = get_all_denuncias()
    resumo = {"por_tipo": {}, "por_setor": {}}
    try:
        for item in dados:
            t = item.get("tipo", "Não informado")
            s = item.get("setor", "Não informado")
            resumo["por_tipo"][t] = resumo["por_tipo"].get(t, 0) + 1
            resumo["por_setor"][s] = resumo["por_setor"].get(s, 0) + 1
    except Exception:
        pass
    return resumo


def upload_evidencia(file_name: str, file_bytes: bytes, user_path: str = "") -> str:
    """Upload de imagens e PDF para o Storage do Supabase."""
    client = _ensure_client()
    try:
        # Cria um caminho único para o arquivo
        path = f"{user_path}/{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_name}"
        
        # Realiza o upload
        client.storage.from_(BUCKET_EVIDENCIAS).upload(
            path, 
            file_bytes, 
            file_options={"content-type": "application/octet-stream"}
        )
        return path # Retorna o caminho ou a URL do arquivo no bucket
        
    except Exception as e:
        # Usa st.error para mostrar no Streamlit, já que estamos no contexto de uma função de página
        st.error(f"Erro ao fazer upload de evidência: {e}") 
        return "" # Retorna vazio em caso de erro.
