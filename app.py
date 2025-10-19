import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------
st.set_page_config(page_title="IA Assistente de Compliance", layout="wide")

# -----------------------------
# LOGIN SIMPLES
# -----------------------------
st.title("🔒 IA Assistente de Compliance")

usuario = st.text_input("Usuário:")
senha = st.text_input("Senha:", type="password")

if st.button("Entrar"):
    if usuario == "admin" and senha == "1234":
        st.session_state["autenticado"] = True
        st.success("Login realizado com sucesso!")
    else:
        st.error("Usuário ou senha incorretos.")

# -----------------------------
# PÁGINA PRINCIPAL (APÓS LOGIN)
# -----------------------------
if st.session_state.get("autenticado"):

    st.header("📢 Registrar Denúncia")

    # Campo de seleção do setor
    setor = st.selectbox(
        "Selecione o setor relacionado ao fato:",
        ("Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros")
    )

    # Campo de texto para denúncia
    denuncia_texto = st.text_area("Descreva o ocorrido:")

    if st.button("Enviar Denúncia"):
        st.success("✅ Denúncia enviada com sucesso!")
        st.info("Sua identidade será preservada.")

    st.markdown("---")
    st.header("📊 Análise de Denúncias")

    # -----------------------------
    # SIMULAÇÃO DE DADOS
    # -----------------------------
    dados_denuncias = pd.DataFrame({
        "Setor": [
            "Engenharia", "Produção", "Marketing",
            "Recursos Humanos", "Produção", "Financeiro",
            "Engenharia", "Produção", "Outros", "Engenharia"
        ],
        "Mês": [
            "Jan", "Jan", "Fev", "Fev", "Mar",
            "Mar", "Abr", "Abr", "Mai", "Mai"
        ]
    })

    # Contagem por setor
    contagem_setor = dados_denuncias["Setor"].value_counts().reset_index()
    contagem_setor.columns = ["Setor", "Número de Casos"]

    # Contagem por mês
    contagem_temporal = dados_denuncias["Mês"].value_counts().reset_index()
    contagem_temporal.columns = ["Mês", "Número de Casos"]
    contagem_temporal = contagem_temporal.sort_values("Mês")

    # -----------------------------
    # GRÁFICOS
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Evolução das Denúncias (Linha)")
        fig_linha = px.line(
            contagem_temporal,
            x="Mês",
            y="Número de Casos",
            markers=True,
            title="Denúncias ao Longo dos Meses"
        )
        st.plotly_chart(fig_linha, use_container_width=True)

    with col2:
        st.subheader("🥧 Distribuição por Setor (Pizza)")
        fig_pizza = px.pie(
            contagem_setor,
            names="Setor",
            values="Número de Casos",
            title="Distribuição de Denúncias por Setor"
        )
        st.plotly_chart(fig_pizza, use_container_width=True)

    # -----------------------------
    # TABELA DE DADOS
    # -----------------------------
    st.subheader("📄 Base de Denúncias (Simulada)")
    st.dataframe(dados_denuncias, use_container_width=True)
