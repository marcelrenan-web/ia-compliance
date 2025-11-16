from auth import require_login
import streamlit as st

require_login()  # <- isso força login antes do conteúdo privado

st.title("Painel de Análises")

import streamlit as st
import plotly.express as px
from services.banco import fetch_denuncias
from services.auth import ensure_logged_in
from utils.layout import aplicar_layout

aplicar_layout()
# exige autenticação
if not ensure_logged_in():
    st.stop()

st.title("📊 Painel RH / Compliance")

df = fetch_denuncias()
if df.empty:
    st.info("Nenhuma denúncia registrada.")
else:
    # preparo
    df["data_envio"] = st.to_datetime(df["data_envio"])
    st.subheader("Base de denúncias")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Casos por Tipo")
        ct = df["tipo_ocorrencia"].value_counts().reset_index()
        ct.columns = ["Tipo", "Quantidade"]
        fig1 = px.bar(ct, x="Tipo", y="Quantidade", title="Casos por Tipo")
        st.plotly_chart(fig1, use_container_width=True, key="fig_tipo")

    with col2:
        st.subheader("Distribuição por Setor")
        cs = df["setor"].value_counts().reset_index()
        cs.columns = ["Setor", "Quantidade"]
        fig2 = px.pie(cs, names="Setor", values="Quantidade", title="Por Setor")
        st.plotly_chart(fig2, use_container_width=True, key="fig_setor")
