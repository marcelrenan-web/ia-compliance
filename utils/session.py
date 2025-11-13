import streamlit as st

def salvar_sessao(usuario):
    st.session_state["logado"] = True
    st.session_state["usuario"] = usuario

def limpar_sessao():
    st.session_state["logado"] = False
    st.session_state["usuario"] = None

def usuario_logado():
    return st.session_state.get("logado", False)

def pegar_usuario():
    return st.session_state.get("usuario", None)
