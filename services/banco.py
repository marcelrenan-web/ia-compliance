from serviços.supabase_client import supabase
import datetime

# ==========================
# FUNÇÕES DE BANCO DE DADOS
# ==========================

def insert_denuncia(setor, tipo, descricao, data_ocorrencia, anexo_url=None):
    """
    Insere denúncia no banco de dados.
    setor: string
    tipo: string
    descricao: string
    data_ocorrencia: datetime.date
    anexo_url: string (opcional)
    """
    try:
        data_str = data_ocorrencia.strftime("%Y-%m-%d")

        dados = {
            "setor": setor,
            "tipo": tipo,
            "descricao": descricao,
            "data_ocorrencia": data_str,
            "anexo": anexo_url
        }

        result = supabase.table("denuncias").insert(dados).execute()
        return True, result.data

    except Exception as e:
        return False, str(e)


def obter_denuncias():
    """ retorna todas as denúncias em ordem cronológica inversa """
    try:
        resp = supabase.table("denuncias").select("*").order('id', desc=True).execute()
        return True, resp.data
    except Exception as e:
        return False, str(e)


def obter_resumo_para_graficos():
    """ Contagem por tipo e setor """

    try:
        resp = supabase.table("denuncias").select("tipo, setor").execute()

        dados = resp.data

        resumo = {
            "por_tipo": {},
            "por_setor": {}
        }

        for item in dados:
            # contagem por tipo
            t = item['tipo']
            resumo["por_tipo"][t] = resumo["por_tipo"].get(t, 0) + 1

            # contagem por setor
            s = item['setor']
            resumo["por_setor"][s] = resumo["por_setor"].get(s, 0) + 1

        return True, resumo

    except Exception as e:
        return False, str(e)
