import streamlit as st
import pandas as pd
import plotly.express as px

def gerar_graficos(denuncias):
    df = pd.DataFrame(denuncias)

    # Gráfico de categorias
    fig_cat = px.bar(
        df.groupby("categoria").size().reset_index(name="quantidade"),
        x="categoria",
        y="quantidade",
        title="Quantidade de denúncias por categoria"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    # Gráfico de sentimentos (placeholder até IA ser implementada)
    df["sentimento"] = "Neutro"
    fig_sent = px.pie(
        df,
        names="sentimento",
        title="Classificação de Sentimentos (a ser implementado)"
    )
    st.plotly_chart(fig_sent, use_container_width=True)
