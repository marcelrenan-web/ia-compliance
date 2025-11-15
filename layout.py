import streamlit as st

def aplicar_layout():
    # minimal, safe CSS that avoids fragile selectors
    st.markdown(
        """<style>
        .stApp {{ background-color: #E6F3F8; }}
        .css-1d391kg {{ padding-top: 1rem; }}
        h1, h2, h3 {{ color: #0A466E; }}
        .stButton>button {{ border-radius:8px; }}
        </style>""", unsafe_allow_html=True
    )
