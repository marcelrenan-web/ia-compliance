import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da página ---
st.set_page_config(page_title="IA Compliance - Denúncias Éticas", layout="wide")

# --- Tela inicial: envio de denúncia ---
st.title("📢 Canal de Denúncias Éticas Anônimas")

st.write("""
Este canal é **100% anônimo** e tem como objetivo promover um ambiente de trabalho ético, 
seguro e respeitoso.  
Preencha abaixo sua denúncia, descrevendo a situação da forma mais clara possível.
""")

denuncia_texto = st.text_area("✍️ Descreva o ocorrido:")

if st.button("Enviar denúncia"):
    if denuncia_texto.strip():
        st.success("✅ Denúncia enviada com sucesso! Obrigado por contribuir para um ambiente mais ético.")
    else:
        st.warning("⚠️ Por favor, descreva o ocorrido antes de enviar.")

st.divider()

# --- Tela de Login para acesso interno ---
st.header("🔒 Acesso Restrito (Somente Equipe de Compliance)")

usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

usuario_correto = "admin"
senha_correta = "1234"

# --- Área restrita ---
if st.button("Entrar"):
    if usuario == usuario_correto and senha == senha_correta:
        st.success("Login realizado com sucesso!")
        
        # Dados simulados de denúncias
        dados_denuncias_simulacao = {
            'Setor': ['Engenharia', 'Produção', 'Recursos Humanos', 'Logística', 'Qualidade', 'Produção', 'Engenharia', 'RH'],
            'Gravidade': ['Alta', 'Média', 'Alta', 'Baixa', 'Média', 'Alta', 'Baixa', 'Média'],
            'Status': ['Aberta', 'Em análise', 'Concluída', 'Aberta', 'Concluída', 'Aberta', 'Concluída', 'Em análise'],
            'Data': pd.date_range('2025-01-01', periods=8, freq='M')
        }

        df = pd.DataFrame(dados_denuncias_simulacao)
        st.subheader("📊 Painel de Indicadores de Ética")

        # --- KPI Cards ---
        total_casos = len(df)
        casos_abertos = (df['Status'] == 'Aberta').sum()
        concluidos = (df['Status'] == 'Concluída').sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Casos", total_casos)
        col2.metric("Casos Abertos", casos_abertos)
        col3.metric("Casos Concluídos", concluidos)

        # --- Gráficos ---
        st.divider()
        col4, col5 = st.columns(2)

        # Gráfico 1 - Denúncias por Setor
        with col4:
            fig_setor = px.bar(df, x='Setor', title="Denúncias por Setor", color='Gravidade')
            st.plotly_chart(fig_setor, use_container_width=True)

        # Gráfico 2 - Evolução Temporal
        with col5:
            contagem_temporal = df.groupby(df['Data'].dt.strftime("%b"))['Setor'].count().reset_index()
            contagem_temporal.columns = ['Mês', 'Número de Casos']

            fig_linha = px.line(
                contagem_temporal,
                x='Mês',
                y='Número de Casos',
                markers=True,
                title="Evolução das Denúncias ao Longo do Tempo"
            )
            st.plotly_chart(fig_linha, use_container_width=True)

    else:
        st.error("Usuário ou senha incorretos.")
