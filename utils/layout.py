import streamlit as st

def aplicar_layout():
    # CSS leve e seguro — evita seletores que quebram o DOM do Streamlit
    st.markdown(
        """
        <style>
            .stApp { background-color: #E6F3F8; }
            h1, h2, h3 { color: #0A466E !important; }
            .stButton>button { border-radius: 8px !important; }
            /* esconder footer do Streamlit */
            footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )
