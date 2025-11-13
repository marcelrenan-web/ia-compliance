import streamlit as st
import pandas as pd
import plotly.express as px
from services.banco import fetch_denuncias
from utils.layout import aplicar_layout

aplicar_layout()

st.title("📊 Painel de Análise de Denúncias")

if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    st.warning("Esta área é restrita ao RH/Compliance. Faça login no menu lateral.")
    st.stop()

df = fetch_denuncias()

if df.empty:
    st.info("📭 Nenhuma denúncia registrada ainda.")
    st.stop()

# Conversão e processamento
df["data_envio"] = pd.to_datetime(df["data_envio"])
df["Mês"] = df["data_envio"].dt.to_period("M").astype(str)

# Contagem por tipo
contagem_tipo = df["tipo_ocorrencia"].value_counts().reset_index()
contagem_tipo.columns = ["Tipo de Ocorrência", "Número de Casos"]

# Contagem por setor
contagem_setor = df["setor"].value_counts().reset_index()
contagem_setor.columns = ["Setor", "Número de Casos"]

# Linha temporal
contagem_tempo = df["Mês"].value_counts().sort_index().reset_index()
contagem_tempo.columns = ["Mês", "Número de Casos"]

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Casos por Tipo de Ocorrência")
    fig_bar = px.bar(contagem_tipo, x="Tipo de Ocorrência", y="Número de Casos")
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🥧 Distribuição por Setor")
    fig_pizza = px.pie(contagem_setor, names="Setor", values="Número de Casos")
    st.plotly_chart(fig_pizza, use_container_width=True)

st.markdown("---")
st.subheader("📈 Evolução das Denúncias por Mês")
fig_line = px.line(contagem_tempo, x="Mês", y="Número de Casos", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")
st.subheader("📄 Base de Denúncias")
st.dataframe(
    df[["id", "setor", "tipo_ocorrencia", "descricao", "data_envio"]],
    use_container_width=True
)
