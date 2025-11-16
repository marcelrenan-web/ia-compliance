import streamlit as st
from services.banco import insert_denuncia
from utils.layout import aplicar_layout

aplicar_layout()
st.title("📢 Registrar Denúncia Anônima")

with st.form("form_denuncia"):
    setor = st.selectbox("Setor:", ["Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros"])
    tipo = st.selectbox("Tipo de ocorrência:", ["Assédio Moral", "Assédio Sexual", "Racismo", "Discriminação", "Outros"])
    descricao = st.text_area("Descreva o ocorrido:", height=200)
    enviado = st.form_submit_button("Enviar")

if enviado:
    if descricao.strip() == "":
        st.warning("Por favor, descreva o ocorrido.")
    else:
        codigo = insert_denuncia(setor, tipo, descricao)
        st.success(f"✅ Denúncia registrada! Código de acompanhamento: **{codigo}**")
        st.info("Anote o código para acompanhar o caso.")
