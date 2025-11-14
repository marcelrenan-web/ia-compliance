# services/supabase.py

from supabase import create_client
import os
import streamlit as st

# Lê as credenciais do ambiente do Streamlit
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Cria o cliente
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
