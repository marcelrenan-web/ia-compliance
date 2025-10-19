import streamlit as st
import pandas as pd
import plotly.express as px
import qrcode
from io import BytesIO

# --- Configuração da Página ---
st.set_page_config(
    page_title="IA de Compliance",
    page_icon="🛡️",
    layout="wide"
)

# --- Função para gerar QR Code ---
def gerar_qr_code(url):
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="Aponte a câmera para acessar o formulário")

# --- Navegação ---
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione uma opção:", ["Página Inicial", "Painel RH/Compliance"])

# --- Página Inicial ---
if page == "Página Inicial":
    st.title("🛡️ IA Assistente de Compliance")
    st.markdown("""
    Sua voz é essencial para construirmos um ambiente de trabalho mais ético e seguro.
    **Todas as denúncias são anônimas.** Sua identidade será totalmente protegida.
    """)
    st.markdown("---")

    # QR Code apontando para link público do app (substitua pelo seu link após deploy)
    st.subheader("📱 Acesse via QR Code")
    gerar_qr_code("https://seu-usuario.streamlit.app")  # substitua pelo link do seu app

    # Formulário de denúncia
    st.header("Formulário de Denúncia Anônima")
    denuncia_texto = st.text_area("Descreva o ocorrido:", height=200)
    setor_escolhido = st.selectbox(
        "Selecione o setor onde ocorreu:",
        ("", "Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outro")
    )
    botao_enviar = st.button("Enviar Denúncia")

    if botao_enviar:
        if denuncia_texto and setor_escolhido:
            tipo_denuncia = "Assédio Moral"  # Placeholder
            st.success("✅ Sua denúncia foi enviada com sucesso! Obrigado pela colaboração.")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")

# --- Painel RH/Compliance ---
elif page == "Painel RH/Compliance":
    st.subheader("🔒 Login RH/Compliance")
    senha_digitada = st.text_input("Digite a senha de acesso:", type="password")
    senha_correta = "12345"  # Substitua por senha segura

    if senha_digitada == senha_correta:
        st.success("✅ Acesso autorizado")
        st.title("📊 Painel de Análise de Denúncias")
        st.markdown("---")

        # Dados de simulação
        dados_denuncias_simulacao = {
            'tipo_denuncia': ['Assédio Moral', 'Assédio Sexual', 'Racismo', 'Assédio Moral', 'Assédio Sexual', 'Homofobia', 'Assédio Moral'],
            'setor': ['Engenharia', 'Produção', 'Marketing', 'Engenharia', 'Recursos Humanos', 'Engenharia', 'Financeiro'],
