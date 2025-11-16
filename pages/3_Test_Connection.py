import streamlit as st
from supabase import create_client

st.title("Teste de Conexão com Supabase")

url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")

st.write("URL carregada:", url)
st.write("Key carregada:", key[:20] + "..." if key else "N/A")

try:
    supabase = create_client(url, key)
    res = supabase.table("denuncias").select("*").limit(1).execute()
    st.success("Conexão bem-sucedida!")
    st.write("Resposta da tabela:")
    st.write(res.data)
except Exception as e:
    st.error("Erro ao conectar no Supabase")
    st.write(e)
