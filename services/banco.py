from supabase import create_client, Client
import streamlit as st

@st.cache_resource
def get_supabase_or_raise() -> Client:
    """
    Inicializa e retorna o cliente Supabase.
    As credenciais devem ser definidas como secrets no Streamlit.
    """
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except KeyError as e:
        st.error(f"Erro: Credencial SUPABASE_{e.args[0].upper()} não encontrada nos segredos do Streamlit. Por favor, adicione-a.")
        st.stop()
        
    return create_client(url, key)

# OBS: Para o Streamlit Cloud, defina SUPABASE_URL e SUPABASE_KEY no arquivo .streamlit/secrets.toml
