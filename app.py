import streamlit as st

st.set_page_config(
    page_title="Vigia Ético",
    page_icon="🕵️",
)

st.title("🕵️ Vigia Ético - Portal de Denúncias")

st.write("Selecione uma página no menu lateral para continuar.")

import streamlit as st
from auth import login_user, signup_user, logout_user
from banco import inserir_paciente, listar_pacientes

st.set_page_config(page_title="Sistema Fisioterapia", page_icon="🧠", layout="wide")

if "usuario" not in st.session_state:
    st.session_state.usuario = None

def tela_login():
    st.title("Login do Fisioterapeuta")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        user = login_user(email, senha)
        if user:
            st.session_state.usuario = email
            st.success("Login realizado!")

    st.write("---")
    st.write("Não possui conta? Crie abaixo:")

    email_cad = st.text_input("Novo Email")
    senha_cad = st.text_input("Nova Senha", type="password")
    
    if st.button("Cadastrar"):
        new_user = signup_user(email_cad, senha_cad)
        if new_user:
            st.success("Usuário cadastrado!")

def tela_sistema():
    st.sidebar.subheader(f"Usuário: {st.session_state.usuario}")
    if st.sidebar.button("Logout"):
        logout_user()
        st.session_state.usuario = None
        st.rerun()

    st.title("Área de trabalho")

    st.subheader("Cadastro de Pacientes")

    nome = st.text_input("Nome do paciente")
    idade = st.number_input("Idade", 0, 110)
    queixa = st.text_area("Queixa principal")

    if st.button("Salvar paciente"):
        inserir_paciente(nome, idade, queixa)
        st.success("Paciente salvo!")

    st.write("---")

    st.subheader("Pacientes cadastrados")
    lista = listar_pacientes()

    if lista:
        for p in lista:
            st.write(f"- {p['nome']} — {p['idade']} anos — {p['queixa']}")
    else:
        st.info("Nenhum paciente cadastrado ainda.")

if st.session_state.usuario:
    tela_sistema()
else:
    tela_login()
