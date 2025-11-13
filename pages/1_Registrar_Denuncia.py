import streamlit as st
from services.banco import inserir_denuncia
from utils.session import verificar_login
from utils.layout import aplicar_layout

aplicar_layout()

st.title("📝 Registrar Denúncia")

usuario = verificar_login()

st.markdown("""
Aqui você pode registrar uma denúncia de forma **anônima**, simples e segura.
Preencha os campos abaixo e envie para análise.
""")

with st.form("form_denuncia"):
    categoria = st.selectbox(
        "Categoria da denúncia:",
        ["Assédio", "Discriminação", "Conduta antiética", "Outros"]
    )
    descricao = st.text_area("Descreva o ocorrido", height=200)
    enviado = st.form_submit_button("Enviar")

    if enviado:
        if descricao.strip() == "":
            st.error("A descrição não pode estar vazia.")
        else:
            inserir_denuncia(categoria, descricao, usuario)
            st.success("Denúncia enviada com sucesso!")
