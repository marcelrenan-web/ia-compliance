import streamlit as st
from services.banco import insert_denuncia
from utils.layout import aplicar_layout

# Aplica layout do sistema
aplicar_layout()

st.title("📢 Registrar Denúncia Anônima")

with st.form("form_denuncia"):
    setor = st.selectbox(
        "Setor:",
        ["Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros"]
    )

    tipo = st.selectbox(
        "Tipo de ocorrência:",
        ["Assédio Moral", "Assédio Sexual", "Racismo", "Discriminação", "Outros"]
    )

    descricao = st.text_area("Descreva o ocorrido:", height=200)

    enviado = st.form_submit_button("Enviar")

# ---------------------------
# PROCESSAMENTO DO FORMULÁRIO
# ---------------------------

if enviado:
    if not descricao.strip():
        st.warning("Por favor, descreva o ocorrido.")
    else:
        try:
            codigo = insert_denuncia(setor, tipo, descricao)
            st.success(f"✅ Denúncia registrada com sucesso!")
            st.info(f"📌 Código de acompanhamento: **{codigo}**")
        except Exception as e:
            st.error("Erro ao registrar denúncia. Verifique as credenciais do Supabase.")
            st.write(str(e))
