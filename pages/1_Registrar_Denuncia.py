import streamlit as st
from datetime import date
import sys
import os

# --- CORREÇÃO DE CAMINHO ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --------------------------

from services.banco import insert_denuncia, insert_anexo
from utils.layout import aplicar_layout

aplicar_layout()

st.title("📢 Registrar Denúncia Anônima")

with st.form("form_denuncia"):

    setor = st.selectbox(
        "Setor onde ocorreu o incidente:",
        ["Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros"]
    )

    if setor == "Outros":
        setor_outros = st.text_input("Qual setor?")
    else:
        setor_outros = None

    tipo = st.selectbox(
        "Tipo de ocorrência:",
        ["Assédio Moral", "Assédio Sexual", "Racismo", "Discriminação", "Outros"]
    )

    if tipo == "Outros":
        tipo_outros = st.text_input("Qual tipo de ocorrência?")
    else:
        tipo_outros = None

    data_servico = st.date_input("Data aproximada da ocorrência:")

    descricao = st.text_area("Descreva o ocorrido (seja detalhado, mas mantenha o foco):", height=200)

    arquivos = st.file_uploader("📎 Anexar imagens / provas (opcional)", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)

    enviado = st.form_submit_button("Enviar Denúncia")

if enviado:
    try:
        # Substitui valor se "Outros" foi selecionado
        setor_final = setor_outros if setor == "Outros" else setor
        tipo_final = tipo_outros if tipo == "Outros" else tipo

        codigo = insert_denuncia(setor_final, tipo_final, descricao, data_servico)

        if arquivos:
            for arquivo in arquivos:
                insert_anexo(codigo, arquivo)

        st.success(f"✅ Denúncia registrada! Código: **{codigo}**")

    except Exception as e:
        st.error("Erro ao registrar denúncia.")
        st.write(str(e))
