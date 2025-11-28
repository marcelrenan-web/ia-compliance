# services/banco.py
"""
Acesso ao Supabase para operações de Denúncias e Resoluções.
Substitua o arquivo existente por este.
"""

from datetime import date, datetime
from typing import List, Tuple, Optional, Any
import traceback

# Importa o cliente supabase (assume services/supabase_client.py que expõe `supabase`)
try:
    from services.supabase_client import supabase
except Exception:
    supabase = None

# Nomes das tabelas (consistente com seu banco Supabase)
TABLE_DENUNCIAS = "Denuncias"
TABLE_RESOLUCOES = "Resolucoes"

# bucket para evidências (crie esse bucket no Supabase Storage)
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
    Retorna o registro inserido (ou id) em caso de sucesso; lança exceção em erro.
    """
    client = _ensure_client()
    try:
        # Formata a data como string ISO (ajuste conforme seu schema)
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
            "anexo": anexo_url
        }

        resp = client.table(TABLE_DENUNCIAS).insert(payload).execute()
        # retorno: resp.data normalmente é lista com o registro inserido
        if hasattr(resp, "data"):
            return resp.data  # quem chamar pode extrair id / código
        if isinstance(resp, dict) and resp.get("data"):
            return resp["data"]
        return resp
    except Exception as e:
        # melhore o log se necessário
        raise RuntimeError(f"Erro ao inserir denúncia: {e}\n{traceback.format_exc()}")


def get_all_denuncias() -> List[dict]:
    """
    Retorna lista de denúncias (lista de dicts), ordenadas por id/registro descendente.
    Em caso de erro, lança exceção.
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
    Monta um resumo simples por tipo e por setor para uso em dashboards.
    Retorna dicionário com chaves 'por_tipo' e 'por_setor'.
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
        # Se algo inesperado ocorrer, retorna o que já coletou
        pass
    return resumo


def upload_evidencia(file_name: str, file_bytes: bytes, user_path: str = "") -> str:
    """
    Faz upload para Supabase Storage -> BUCKET_EVIDENCIAS.
    Retorna URL pública do arquivo (ou lança exceção).
    Requer que o bucket `BUCKET_EVIDENCIAS` exista e permissões de upload estejam configuradas.
    """
    client = _ensure_client()
    try:
        # caminho interno: denuncias/<user_path>/nome_arquivo
        prefix = f"denuncias/{user_path}".strip("/")
        path = f"{prefix}/{file_name}" if prefix else file_name

        # upload: algumas versões do client aceitam bytes diretamente
        res = client.storage.from_(BUCKET_EVIDENCIAS).upload(path, file_bytes)
        # obter URL pública - diferentes versões retornam estrut. verificamos várias chaves
        try:
            public = client.storage.from_(BUCKET_EVIDENCIAS).get_public_url(path)
            # possíveis formatos: {'publicURL': '...'} ou {'data': {'publicUrl': '...'}} etc.
            if isinstance(public, dict):
                # checa chaves comuns
                for k in ("publicURL", "publicUrl", "public_url", "publicUrl"):
                    if k in public:
                        return public[k]
                # nested data
                data = public.get("data") or public.get("data", {})
                if isinstance(data, dict):
                    for k in ("publicUrl", "public_url", "publicURL"):
                        if k in data:
                            return data[k]
            # fallback: se upload retornou alguma info com path, constroi URL (só se conhecer seu SUPABASE URL)
            if hasattr(res, "data") and res.data:
                # tenta extrair path
                return res.data
            return str(public)
        except Exception:
            return str(public)
    except Exception as e:
        raise RuntimeError(f"Erro ao fazer upload de evidência: {e}\n{traceback.format_exc()}")
