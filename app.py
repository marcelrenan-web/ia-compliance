import streamlit as st
from utils.layout import aplicar_layout
from services.auth import ensure_logged_in, logout_button

st.set_page_config(page_title="Portal Vigia Ético", page_icon="🛡️", layout="wide")
aplicar_layout()

st.sidebar.image("assets/logo.svg", width=140)
st.sidebar.markdown("### Portal Vigia Ético")

# Authentication on sidebar (for RH/Compliance). Public can submit via page.
ensure_logged_in()

st.title("Portal Vigia Ético")
st.markdown("Bem-vindo! Use o menu lateral para navegar entre as páginas.")
