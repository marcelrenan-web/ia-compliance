import streamlit as st

def aplicar_layout():
    """Aplica a configuração de página padrão para toda a aplicação Streamlit."""
    st.set_page_config(
        page_title="IA Assistente de Compliance",
        page_icon="⚖️",
        layout="wide", # Usa a largura máxima da tela
        initial_sidebar_state="expanded",
    )
    # Adiciona estilo CSS customizado (opcional, mas recomendado)
    st.markdown("""
        <style>
        .css-1d391kg { padding-top: 3.5rem; }
        .css-1av0v0d { padding-top: 1rem; }
        </style>
        """, unsafe_allow_html=True)
