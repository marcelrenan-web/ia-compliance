import streamlit as st

def verificar_login():
    return st.session_state.get("logado", False)

def logout():
    st.session_state.logado = False
    st.switch_page("auth.py")
