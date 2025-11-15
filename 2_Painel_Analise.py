import streamlit as st
import pandas as pd
import plotly.express as px
from services.banco import fetch_denuncias
from services.auth import ensure_logged_in
from utils.layout import aplicar_layout

aplicar_layout()
ensure_logged_in()
st.header('📊 Painel RH / Compliance')

df = fetch_denuncias()
if df.empty:
    st.info('Nenhuma denúncia registrada.')
else:
    df['data_envio'] = pd.to_datetime(df['data_envio'])
    st.subheader('Base de denúncias')
    st.dataframe(df, use_container_width=True)

    st.markdown('---')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Casos por Tipo')
        fig1 = px.bar(df['tipo_ocorrencia'].value_counts().reset_index().rename(columns={'index':'Tipo','tipo_ocorrencia':'Quantidade'}), x='index', y='tipo_ocorrencia')
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.subheader('Por Setor')
        fig2 = px.pie(df, names='setor', values=df['setor'].value_counts())
        st.plotly_chart(fig2, use_container_width=True)
