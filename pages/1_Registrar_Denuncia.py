from services.banco import insert_denuncia, upload_evidencia

import streamlit as st
from services.banco import insert_denuncia
...
# remover a linha aplicar_layout()

st.title("📢 Registrar Denúncia Anônima")

with st.form("form_denuncia"):
    
    setor = st.selectbox(
        "Setor onde ocorreu o incidente:",
        ["Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros"],
        key="setor"
    )

    setor_outros = ""
    if setor == "Outros":
        setor_outros = st.text_input("Qual setor?", key="setor_outros")

    tipo = st.selectbox(
        "Tipo de ocorrência:",
        ["Assédio Moral", "Assédio Sexual", "Racismo", "Discriminação", "Outros"],
        key="tipo"
    )

    tipo_outros = ""
    if tipo == "Outros":
        tipo_outros = st.text_input("Qual tipo de incidente?", key="tipo_outros")

    data_servico = st.date_input("Data aproximada da ocorrência:")
    descricao = st.text_area("Descreva o ocorrido", height=200)

    arquivos = st.file_uploader("Anexar evidências (opcional)", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)

    enviado = st.form_submit_button("Enviar Denúncia")

if enviado:
    try:
        # normalização
        if setor == "Outros" and setor_outros.strip():
            setor_final = setor_outros
        else:
            setor_final = setor

        if tipo == "Outros" and tipo_outros.strip():
            tipo_final = tipo_outros
        else:
            tipo_final = tipo

        # upload de evidências
        url_final = None

        if arquivos:
            for arquivo in arquivos:
                bytes_arquivo = arquivo.read()
                url_final = upload_evidencia(arquivo.name, bytes_arquivo)
                # OBS: última URL será registrada na denúncia

        # salvar denúncia
        resp = insert_denuncia(setor_final, tipo_final, descricao, data_servico, "Neutro", url_final)

        st.success("Denúncia registrada com sucesso! 🙌")
        st.write(resp)

    except Exception as e:
        st.error("Erro ao registrar denúncia")
        st.write(str(e))
