import streamlit as st
import os
from supabase import create_client, Client

# Prefer Streamlit secrets, fallback to environment variables
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    # Raise early with helpful message in logs
    raise RuntimeError('Supabase credentials not found. Add SUPABASE_URL and SUPABASE_KEY to Streamlit secrets or environment variables.')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
