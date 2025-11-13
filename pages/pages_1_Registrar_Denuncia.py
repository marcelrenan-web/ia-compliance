import streamlit as st
from services.banco import insert_denuncia
from utils.layout import aplicar_layout, titulo_central

aplicar_layout()

st.title("📢 Registrar Denúncia Anônima")

with st.form("form_denuncia"):
    setor = st.selectbox(
        "Selecione o setor relacionado ao fato:",
        ("Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros")
    )

    tipo_assedio = st.selectbox(
        "Tipo de ocorrência:",
        ("Assédio Moral", "Assédio Sexual", "Racismo", "Homofobia", "Discriminação", "Outros")
    )

    descricao = st.text_area("Descreva o ocorrido:")

    enviar = st.form_submit_button("Enviar Denúncia")

    if enviar:
        if descricao.strip() == "":
            st.warning("⚠️ Por favor, descreva o ocorrido.")
        else:
            codigo = insert_denuncia(setor, tipo_assedio, descricao)
            st.success(
                f"✅ Denúncia enviada com sucesso! "
                f"Guarde o código de acompanhamento: **{codigo}**"
            )
