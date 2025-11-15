import streamlit as st
from services.banco import insert_denuncia
from utils.layout import aplicar_layout

aplicar_layout()
st.header('📢 Registrar Denúncia (anônimo)')

with st.form('form_denuncia'):
    setor = st.selectbox('Setor', ['Engenharia','Produção','Marketing','Recursos Humanos','Financeiro','Outros'])
    tipo = st.selectbox('Tipo de ocorrência', ['Assédio Moral','Assédio Sexual','Racismo','Discriminação','Outros'])
    descricao = st.text_area('Descreva o ocorrido', height=200)
    enviar = st.form_submit_button('Enviar denúncia')
    if enviar:
        if not descricao.strip():
            st.warning('Por favor, descreva o ocorrido.')
        else:
            codigo = insert_denuncia(setor, tipo, descricao)
            st.success(f'Denúncia registrada com sucesso! Código: {codigo}')
