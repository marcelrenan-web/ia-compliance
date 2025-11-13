import streamlit as st
from services.banco import listar_denuncias
from services.charts import gerar_graficos
from utils.session import verificar_login
from utils.layout import aplicar_layout

aplicar_layout()

st.title("📊 Painel de Análise")

usuario = verificar_login()

st.markdown("Visualização das denúncias registradas e análise de sentimentos.")

denuncias = listar_denuncias()

if not denuncias:
    st.info("Nenhuma denúncia registrada ainda.")
else:
    st.dataframe(denuncias)

    st.markdown("### Gráficos e Métricas")
    gerar_graficos(denuncias)
