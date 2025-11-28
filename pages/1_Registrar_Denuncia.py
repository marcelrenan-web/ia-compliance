import streamlit as st
# A importação do layout deve ser a primeira chamada executável para st.set_page_config funcionar
from utils.layout import aplicar_layout
from services.banco import insert_denuncia, upload_evidencia

aplicar_layout()

# O nome da página será "1_Registrar_Denuncia" no menu lateral do Streamlit
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
        # Nota: O código está configurado para salvar apenas a URL do ÚLTIMO arquivo enviado.
        url_final = None

        if arquivos:
            for arquivo in arquivos:
                bytes_arquivo = arquivo.read()
                # Passa um caminho base para organizar no storage (ex: 'denuncias_anexos')
                url_final = upload_evidencia(arquivo.name, bytes_arquivo, user_path="denuncias_anexos") 
                # OBS: Para salvar múltiplos arquivos, você precisaria armazenar uma lista de URLs.
        
        # salvar denúncia
        resp = insert_denuncia(setor_final, tipo_final, descricao, data_servico, "Neutro", url_final)

        st.success("Denúncia registrada com sucesso! 🙌")
        # st.write(resp) # Opcional: Remova esta linha em produção
        
        # Limpar o formulário após sucesso (requer um truque ou re-renderização, mas a forma
        # mais simples no Streamlit é com st.rerun se a lógica de submissão estivesse no topo)
        
    except Exception as e:
        st.error(f"Erro ao registrar denúncia: {str(e)}")
        # Remova o st.write(str(e)) em produção para evitar vazar detalhes técnicos
