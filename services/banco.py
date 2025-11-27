@@ -7,7 +7,7 @@
# Nome exato da sua tabela no Supabase
TABLE_NAME = "Denuncias" 

def insert_denuncia(setor: str, tipo: str, descricao: str, data_servico: date, sentimento: str) -> str:
def insert_denuncia(setor: str, tipo: str, descricao: str, data_servico: date, sentimento: str = "Neutro") -> str: # CORREÇÃO: 'sentimento' agora tem um valor padrão para evitar erro de argumento ausente.
    """Insere uma nova denúncia no Supabase."""
    try:
        supabase = get_supabase_or_raise() # Garante que o cliente existe
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
