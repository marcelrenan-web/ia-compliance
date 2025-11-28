# services/banco.py
"""
Acesso ao Supabase para operações de Denúncias e Resoluções.
Versão corrigida – coluna correta: anexo_url
"""

from datetime import date, datetime
from typing import List, Tuple, Optional, Any
import traceback

try:
    from services.supabase_client import supabase
except Exception:
    supabase = None

TABLE_DENUNCIAS = "Denuncias"
TABLE_RESOLUCOES = "Resolucoes"
BUCKET_EVIDENCIAS = "evidencias"


def _ensure_client():
    if supabase is None:
        raise RuntimeError("Supabase client não encontrado. Verifique services/supabase_client.py")
    return supabase


def insert_denuncia(setor: str,
                    tipo: str,
                    descricao: str,
                    data_servico: date,
                    sentimento: str = "Neutro",
                    anexo_url: Optional[str] = None) -> Any:
    """
    Insere nova denúncia na tabela TABLE_DENUNCIAS.
    """
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
            "anexo_url": anexo_url  # ← CORRETO
        }

        resp = client.table(TABLE_DENUNCIAS).insert(payload).execute()
        if hasattr(resp, "data"):
            return resp.data
        if isinstance(resp, dict) and resp.get("data"):
            return resp["data"]
        return resp

    except Exception as e:
        raise RuntimeError(f"Erro ao inserir denúncia: {e}\n{traceback.format_exc()}")


def get_all_denuncias() -> List[dict]:
    """
    Retorna todas as denúncias.
    """
    client = _ensure_client()
    try:
        resp = client.table(TABLE_DENUNCIAS).select("*").order('id', desc=True).execute()

        if hasattr(resp, "data"):
            return resp.data or []
        if isinstance(resp, dict) and resp.get("data"):
            return resp["data"] or []
        return []

    except Exception as e:
        raise RuntimeError(f"Erro ao buscar denúncias: {e}\n{traceback.format_exc()}")


def obter_resumo_para_graficos() -> dict:
    """
    Contagem por setor e tipo.
    """
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
    """
    Upload de imagens e PDF para o Storage.
    """
    client = _ensure_client()
    try:
        prefix = f"denunc
