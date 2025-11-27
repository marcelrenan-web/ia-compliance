
import streamlit as st
from supabase import create_client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

def login_user(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Erro no login: {str(e)}")
        return None

def signup_user(email, password):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Erro no cadastro: {str(e)}")
        return None

def logout_user():
    try:
        supabase.auth.sign_out()
        st.success("Logout efetuado!")
    except Exception as e:
        st.error(f"Erro ao sair: {str(e)}")
