# pages/1_Registrar_Denuncia.py
import streamlit as st
from datetime import date
import sys
import os

# garante que a pasta raiz (onde services está) está no path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.banco import insert_denuncia, upload_evidencia
from utils.layout import aplicar_layout

aplicar_layout()

st.title("📢 Registrar Denúncia Anônima")

with st.form("form_denuncia"):
    setor = st.selectbox(
        "Setor onde ocorreu o incidente:",
        ["Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros"]
    )
    # campo condicional para setor "Outros"
    setor_custom = None
    if setor == "Outros":
        setor_custom = st.text_input("Por favor, especifique o setor:")

    tipo = st.selectbox(
        "Tipo de ocorrência:",
        ["Assédio Moral", "Assédio Sexual", "Racismo", "Discriminação", "Outros"]
    )
    tipo_custom = None
    if tipo == "Outros":
        tipo_custom = st.text_input("Por favor, descreva o tipo:")

    data_servico = st.date_input("Data aproximada da ocorrência:", value=date.today())

    descricao = st.text_area("Descreva o ocorrido (seja detalhado, mas mantenha o foco):", height=200)

    # upload opcional de evidência
    arquivo = st.file_uploader("Anexar evidência (imagem ou PDF) — opcional", type=["png", "jpg", "jpeg", "pdf"])
    enviado = st.form_submit_button("Enviar Denúncia")

if enviado:
    # validação básica
    if not descricao or not descricao.strip():
        st.warning("Por favor, descreva o ocorrido.")
    else:
        # valores finais priorizando entradas custom quando "Outros" selecionado
        setor_final = setor_custom.strip() if setor == "Outros" and setor_custom else setor
        tipo_final = tipo_custom.strip() if tipo == "Outros" and tipo_custom else tipo

        anexo_url = None
        if arquivo:
            try:
                file_bytes = arquivo.getvalue()
                # opcional: incluir prefix com data/hora para evitar colisão
                user_path = ""  # se tiver user id, coloque aqui
                anexo_url = upload_evidencia(arquivo.name, file_bytes, user_path=user_path)
            except Exception as e:
                st.error(f"Falha no upload do arquivo: {e}")
                anexo_url = None

        try:
            inserted = insert_denuncia(setor_final, tipo_final, descricao, data_servico, anexo_url=anexo_url)
            # tenta extrair id/código do retorno
            codigo = None
            if isinstance(inserted, list) and len(inserted) > 0 and isinstance(inserted[0], dict):
                codigo = inserted[0].get("id") or inserted[0].get("codigo") or inserted[0].get("uuid")
            elif isinstance(inserted, dict):
                codigo = inserted.get("id") or inserted.get("codigo")
            else:
                codigo = inserted
            st.success(f"✅ Denúncia registrada! Código de acompanhamento: **{codigo}**")
            st.info("Anote o código para acompanhar o caso.")
        except Exception as e:
            st.error("Erro ao registrar denúncia. Verifique logs/credenciais ou regras RLS do Supabase.")
            st.write(f"Detalhes do Erro: {str(e)}")
