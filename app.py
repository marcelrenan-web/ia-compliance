import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configurações da Página ---
st.set_page_config(
    page_title="IA de Compliance",
    page_icon="🛡️",
    layout="wide"
)

# --- Navegação lateral ---
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione uma opção:", ["Página Inicial", "Painel RH/Compliance"])

# --- Página Inicial ---
if page == "Página Inicial":
    st.title("🛡️ IA Assistente de Compliance")
    st.markdown("""
    Sua voz é essencial para construirmos um ambiente de trabalho mais ético e seguro.  
    **Todas as denúncias são anônimas.** Nenhum dado de identificação é solicitado.
    """)
    st.markdown("---")

    st.header("📋 Formulário de Denúncia Anônima")

    denuncia_texto = st.text_area("Descreva o ocorrido:", height=200)
    setor_escolhido = st.selectbox(
        "Selecione o setor onde ocorreu:",
        ("", "Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outro")
    )

    botao_enviar = st.button("Enviar Denúncia")

    if botao_enviar:
        if denuncia_texto and setor_escolhido:
            st.success("✅ Sua denúncia foi enviada com sucesso! Agradecemos sua colaboração.")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")

# --- Painel RH/Compliance ---
elif page == "Painel RH/Compliance":
    st.title("📊 Painel RH/Compliance")
    st.markdown("---")

    st.subheader("🔐 Área Restrita")
    senha_correta = "12345"  # Altere para sua senha
    senha = st.text_input("Digite a senha de acesso:", type="password")

    # --- Verifica Senha ---
    if senha == senha_correta:
        st.success("Acesso concedido ao painel de denúncias.")
        st.markdown("---")

        # --- Dados simulados ---
        dados_denuncias_simulacao = {
            'tipo_denuncia': [
                'Assédio Moral', 'Assédio Sexual', 'Racismo',
                'Assédio Moral', 'Assédio Sexual', 'Homofobia', 'Assédio Moral'
            ],
            'setor': [
                'Engenharia', 'Produção', 'Marketing',
                'Engenharia', 'Recursos Humanos', 'Engenharia', 'Financeiro'
            ],
            'data': pd.to_datetime([
                '2025-01-01', '2025-02-15', '2025-03-20',
                '2025-04-10', '2025-05-05', '2025-06-12', '2025-06-25'
            ])
        }

        df_denuncias = pd.DataFrame(dados_denuncias_simulacao)

        # --- Gráficos ---
        st.header("📈 Análise de Denúncias Recebidas")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Por Tipo de Assédio")
            contagem_tipo = df_denuncias['tipo_denuncia'].value_counts().reset_index()
            contagem_tipo.columns = ['Tipo de Assédio', 'Número de Casos']
            fig_barras = px.bar(contagem_tipo, x='Tipo de Assédio', y='Número de Casos',
                                color='Tipo de Assédio', title='Total de Casos por Tipo')
            st.plotly_chart(fig_barras, use_container_width=True)

        with col2:
            st.subheader("Por Setor")
            contagem_setor = df_denuncias['setor'].value_counts().reset_index()
            contagem_setor.columns = ['Setor', 'Número de Casos']
            fig_pizza = px.pie(contagem_setor, values='Número de Casos', names='Setor',
                               title='Distribuição por Setor')
            st.plotly_chart(fig_pizza, use_container_width=True)

        with col3:
            st.subheader("Evolução Temporal")
            df_denuncias['data_mes'] = df_denuncias['data'].dt.to_period('M').astype(str)
            contagem_temporal = df_denuncias['data_mes'].value_counts().sort_index().reset_index()
            contagem_temporal.columns = ['Mês', 'Número de Casos']
            fig_linha = px.line(contagem_temporal, x='Mês', y='Número de Casos',
