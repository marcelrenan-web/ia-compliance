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

    # QR Code apontando automaticamente para a raiz do app
    st.subheader("📱 Acesse via QR Code")
    try:
        # Streamlit >=1.24.0
        url_a_
