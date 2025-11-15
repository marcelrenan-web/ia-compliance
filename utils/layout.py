import streamlit as st

def aplicar_layout():
    st.markdown("""
        <style>
            .main {
                background-color: #f5f7fa;
            }

            .stButton > button {
                background-color: #23324d;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
            }

            h1, h2, h3 {
                color: #23324d;
            }
        </style>
    """, unsafe_allow_html=True)

def titulo_central(texto):
    st.markdown(f"<h2 style='text-align:center'>{texto}</h2>", unsafe_allow_html=True)
