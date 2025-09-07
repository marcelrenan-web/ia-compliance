import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Configurações da Página ---
st.set_page_config(
    page_title="IA de Compliance",
    page_icon="🛡️",
    layout="wide"
)

# --- Navegação na Sidebar ---
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione uma opção:", ["Página Inicial", "Painel RH/Compliance"])

# --- Lógica de Páginas ---
if page == "Página Inicial":
    
    st.title("🛡️ IA Assistente de Compliance")
    st.markdown("""
    Sua voz é essencial para construirmos um ambiente de trabalho mais ético e seguro.
    **Todas as denúncias são anônimas.** Sua identidade será totalmente protegida para que você possa relatar incidentes com segurança.
    """)
    st.markdown("---")
    
    # --- Formulário de Denúncia ---
    st.header("Formulário de Denúncia Anônima")
    
    denuncia_texto = st.text_area("Descreva o ocorrido:", height=200)

    setor_escolhido = st.selectbox(
        "Selecione o setor onde ocorreu:",
        ("", "Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outro")
    )

    botao_enviar = st.button("Enviar Denúncia")

    # Lógica de processamento (Ponto 1)
    if botao_enviar:
        if denuncia_texto and setor_escolhido:
            # INTEGRAR MODELO DE NLP E SALVAR NO BANCO DE DADOS AQUI
            
            # Por enquanto, usamos valores de simulação
            tipo_denuncia = "Assédio Moral"  
            
            # Lógica para salvar:
            # salvar_denuncia(denuncia_texto, setor_escolhido, tipo_denuncia)
            
            st.success("✅ Sua denúncia foi enviada com sucesso! Agradecemos sua colaboração.")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")
            
elif page == "Painel RH/Compliance":
    
    st.title("📊 Painel de Análise de Denúncias")
    st.markdown("---")
    
    # --- Simulação de Dados para o Dashboard ---
    # Ponto 2: CARREGAR DADOS DO BANCO DE DADOS REAL AQUI
    dados_denuncias_simulacao = {
        'tipo_denuncia': ['Assédio Moral', 'Assédio Sexual', 'Racismo', 'Assédio Moral', 'Assédio Sexual', 'Homofobia', 'Assédio Moral'],
        'setor': ['Engenharia', 'Produção', 'Marketing', 'Engenharia', 'Recursos Humanos', 'Engenharia', 'Financeiro'],
        'data': pd.to_datetime(['2025-01-01', '2025-02-15', '2025-03-20', '2025-04-10', '2025-05-05', '2025-06-12', '2025-06-25'])
    }
    df_denuncias = pd.DataFrame(dados_denuncias_simulacao)

    # --- Análise e Visualização (Gráficos Existentes) ---
    st.header("Análise de Denúncias Recebidas")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Por Tipo de Assédio")
        contagem_tipo = df_denuncias['tipo_denuncia'].value_counts().reset_index()
        contagem_tipo.columns = ['Tipo de Assédio', 'Número de Casos']
        fig_barras = px.bar(contagem_tipo, x='Tipo de Assédio', y='Número de Casos', color='Tipo de Assédio', title='Total de Casos por Tipo')
        st.plotly_chart(fig_barras, use_container_width=True)

    with col2:
        st.subheader("Por Setor")
        contagem_setor = df_denuncias['setor'].value_counts().reset_index()
        contagem_setor.columns = ['Setor', 'Número de Casos']
        fig_pizza = px.pie(contagem_setor, values='Número de Casos', names='Setor', title='Distribuição por Setor')
        st.plotly_chart(fig_pizza, use_container_width=True)
        
    with col3:
        st.subheader("Evolução Temporal")
        df_denuncias['data_mes'] = df_denuncias['data'].dt.to_period('M')
        contagem_temporal = df_denuncias['data_mes'].value_counts().sort_index().reset_index()
        contagem_temporal.columns = ['Mês', 'Número de Casos']
        fig_linha = px.line(contagem_temporal, x='Mês', y='Número de Casos', title='Número de Casos ao Longo do Tempo')
        st.plotly_chart(fig_linha, use_container_width=True)

    st.markdown("---")

    # --- Nova Tela: Registro de Ações ---
    st.header("Registro de Ações e Soluções")
    st.markdown("Use esta seção para documentar o desfecho das denúncias e as medidas tomadas.")
    
    # Ponto 3: CARREGAR DADOS DO BANCO DE DADOS PARA PREENCHER AS OPÇÕES
    # Por enquanto, usamos dados de simulação
    denuncias_abertas = [101, 102, 103] # IDs das denúncias no seu banco
    
    denuncia_id = st.selectbox("Selecione a Denúncia para Acompanhamento:", [""] + denuncias_abertas)
    
    if denuncia_id:
        st.subheader(f"Documentando Denúncia #{denuncia_id}")
        
        status_denuncia = st.selectbox("Status da Apuração:", ["", "Verídica", "Não Verídica"])
        
        medidas_tomadas = st.text_area("Descreva as medidas tomadas:", height=150)
        
        tempo_solucao = st.number_input("Tempo de Solução (em dias):", min_value=0, step=1)
        
        botao_salvar_acao = st.button("Salvar Registro")
        
        if botao_salvar_acao:
            # Ponto 4: SALVAR NO BANCO DE DADOS AS INFORMAÇÕES DE FOLLOW-UP
            #
            # Exemplo:
            # salvar_acompanhamento(denuncia_id, status_denuncia, medidas_tomadas, tempo_solucao)
            
            st.success("✅ Ação registrada com sucesso!")
