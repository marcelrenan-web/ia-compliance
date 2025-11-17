import streamlit as st
from services.banco import insert_denuncia
from utils.layout import aplicar_layout
from datetime import date # Importa o objeto date

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
    
    # NOVO CAMPO: Data da Ocorrência
    data_servico = st.date_input("Data aproximada da ocorrência:")

    descricao = st.text_area("Descreva o ocorrido (seja detalhado, mas mantenha o foco):", height=200)

    enviado = st.form_submit_button("Enviar Denúncia")

if enviado:
    if not descricao.strip():
        st.warning("Por favor, descreva o ocorrido.")
    else:
        try:
            # PASSANDO data_servico para a função
            codigo = insert_denuncia(setor, tipo, descricao, data_servico)
            st.success(f"✅ Denúncia registrada! Código de acompanhamento: **{codigo}**")
            st.info("Anote o código para acompanhar o caso.")
        except Exception as e:
            # Mantenha o erro detalhado para debug
            st.error("Erro ao registrar denúncia. Verifique as credenciais do Supabase e o esquema da tabela.")
            st.write(f"Detalhes do Erro: {str(e)}")
