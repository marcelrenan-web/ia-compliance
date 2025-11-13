import streamlit as st

def aplicar_layout():
    st.markdown(
        """
        <style>
            /* Cor de fundo */
            .main {
                background-color: #f5f7fa;
            }

            /* Caixa dos inputs */
            .stTextInput > div > div > input,
            .stTextArea textarea,
            .stSelectbox select {
                border-radius: 12px !important;
                border: 1px solid #c8d1dc !important;
                padding: 10px !important;
            }

            /* Botões */
            .stButton > button {
                background-color: #374b73 !important;
                color: white !important;
                padding: 10px 18px !important;
                border-radius: 10px !important;
                border: none !important;
            }

            .stButton > button:hover {
                background-color: #23324d !important;
            }

            /* Títulos */
            h1, h2, h3 {
                color: #23324d !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def titulo_central(texto):
    st.markdown(
        f"<h2 style='text-align:center; color:#23324d;'>{texto}</h2>",
        unsafe_allow_html=True
    )
