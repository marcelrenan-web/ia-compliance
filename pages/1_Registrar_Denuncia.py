import streamlit as st
from datetime import date
import sys
import os

# --- CORREÇÃO DE CAMINHO ---
# Garante que os módulos 'services' e 'utils' sejam encontrados a partir de 'pages'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------------------

from services.banco import insert_denuncia
from utils.layout import aplicar_layout

aplicar_layout()

st.title("📢 Registrar Denúncia Anônima")

with st.form("form_denuncia"):
    setor = st.selectbox(
        "Setor onde ocorreu o incidente:",
        ["Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros"]
    )

    tipo = st.selectbox(
        "Tipo de ocorrência:",
        ["Assédio Moral", "Assédio Sexual", "Racismo", "Discriminação", "Outros"]
    )
    
    data_servico = st.date_input("Data aproximada da ocorrência:")

    descricao = st.text_area("Descreva o ocorrido (seja detalhado, mas mantenha o foco):", height=200)

    enviado = st.form_submit_button("Enviar Denúncia")

if enviado:
    if not descricao.strip():
        st.warning("Por favor, descreva o ocorrido.")
    else:
        try:
            codigo = insert_denuncia(setor, tipo, descricao, data_servico)
            st.success(f"✅ Denúncia registrada! Código de acompanhamento: **{codigo}**")
            st.info("Anote o código para acompanhar o caso.")
        except Exception as e:
            st.error("Erro ao registrar denúncia. Verifique as credenciais ou a política RLS 'INSERT'.")
            st.write(f"Detalhes do Erro: {str(e)}")
