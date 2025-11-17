import streamlit as st
import sys
import os

# --- CORREÇÃO DE CAMINHO ---
# Garante que os módulos 'services' e 'utils' sejam encontrados a partir de 'pages'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------------------

# Dependências necessárias para a função de teste
from services.supabase_client import get_supabase_or_raise
from utils.layout import aplicar_layout

aplicar_layout()

st.title("🚀 Teste de Conexão com Supabase")
st.markdown("Verifica se as credenciais e a visibilidade da tabela estão corretas.")

try:
    # Tenta obter as credenciais para exibição (apenas para debug)
    supabase_url = st.secrets.get("SUPABASE_URL", "Não Definido")
    st.info(f"URL carregada: `{supabase_url}`")
    supabase_key = st.secrets.get("SUPABASE_KEY", "Não Definido")
    st.info(f"Key carregada: `{supabase_key[:20]}...`")

    # 1. Obter o cliente Supabase
    supabase = get_supabase_or_raise()

    # 2. Executar uma consulta de teste
    TABLE_NAME = "Denuncias" 
    
    # A consulta agora usa o nome da tabela com a capitalização correta.
    # O comando execute() irá levantar uma exceção se a conexão falhar.
    res = supabase.table(TABLE_NAME).select("*").limit(1).execute()
    
    # Se a execução for bem-sucedida, a conexão está ok
    st.success(f"✅ Conexão com Supabase e acesso à tabela '{TABLE_NAME}' bem-sucedidos!")
    st.write("Dados encontrados (Apenas a primeira linha):", res.data) # Acessa a lista de dados
    
except Exception as e:
    st.error("Erro ao conectar no Supabase ou ao consultar a tabela")
    st.write(f"Detalhes do Erro: {e}")
    st.warning("Se o erro persistir, verifique se o nome da tabela no Supabase é **exatamente** 'Denuncias' (com D maiúsculo) e se as credenciais estão corretas no `secrets.toml`.")
