import streamlit as st
import os
from supabase import create_client, Client

# Prefer st.secrets (Streamlit Cloud), fallback para env vars (local)
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials not found. Configure SUPABASE_URL and SUPABASE_KEY in Streamlit secrets or environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
