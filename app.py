import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configurações da Página ---
st.set_page_config(
    page_title="IA de Compliance",
    page_icon="🛡️",
    layout="wide"
)

# --- Estrutura de Seções da Página ---
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

# Lógica de processamento
if botao_enviar:
    if denuncia_texto and setor_escolhido:
        # Ponto 1: Integrar o Modelo de NLP
        #
        # O modelo de NLP deve ser carregado e usado aqui.
        # Por exemplo, com scikit-learn:
        # modelo_nlp = joblib.load('modelo_treinado.pkl')
        # tipo_denuncia = modelo_nlp.predict([denuncia_texto])[0]
        #
        # Por enquanto, usamos um valor padrão para simulação:
        tipo_denuncia = "Assédio Moral"  # Mude isso para a saída do seu modelo
        
        # Ponto 2: Conectar e Salvar no Banco de Dados
        #
        # Você deve ter uma função que se conecta ao banco de dados e salva a nova denúncia.
        # Exemplo:
        # salvar_denuncia(denuncia_texto, setor_escolhido, tipo_denuncia)
        
        st.success("✅ Sua denúncia foi enviada com sucesso! Agradecemos sua colaboração.")
    else:
        st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")

st.markdown("---")

# --- Painel de Visualização de Dados (Dashboard) ---
st.header("Análise de Denúncias (Acesso Restrito)")
st.markdown("""
Este painel fornece uma visão geral das denúncias registradas, permitindo que o RH e a área de Compliance identifiquem tendências e problemas em tempo real.
""")

# Ponto 3: Carregar Dados do Banco de Dados
#
# Crie uma função para ler os dados das denúncias do seu banco de dados
# e carregar em um DataFrame do Pandas para os gráficos.
#
# Exemplo (usando dados de simulação para o exemplo):
dados_denuncias = {
    'tipo_denuncia': ['Assédio Moral', 'Assédio Sexual', 'Racismo', 'Assédio Moral', 'Assédio Sexual', 'Homofobia', 'Assédio Moral'],
    'setor': ['Engenharia', 'Produção', 'Marketing', 'Engenharia', 'Recursos Humanos', 'Engenharia', 'Financeiro'],
    'data': pd.to_datetime(['2025-01-01', '2025-02-15', '2025-03-20', '2025-04-10', '2025-05-05', '2025-06-12', '2025-06-25'])
}
df_denuncias = pd.DataFrame(dados_denuncias)

# --- Gráficos ---

col1, col2, col3 = st.columns(3)

# Gráfico de Barras: Denúncias por Tipo de Assédio
with col1:
    st.subheader("Denúncias por Tipo de Assédio")
    contagem_tipo = df_denuncias['tipo_denuncia'].value_counts().reset_index()
    contagem_tipo.columns = ['Tipo de Assédio', 'Número de Casos']
    fig_barras = px.bar(contagem_tipo, x='Tipo de Assédio', y='Número de Casos', color='Tipo de Assédio',
                        title='Total de Casos por Tipo')
    st.plotly_chart(fig_barras, use_container_width=True)

# Gráfico de Pizza: Denúncias por Setor
with col2:
    st.subheader("Denúncias por Setor")
    contagem_setor = df_denuncias['setor'].value_counts().reset_index()
    contagem_setor.columns = ['Setor', 'Número de Casos']
    fig_pizza = px.pie(contagem_setor, values='Número de Casos', names='Setor', title='Distribuição por Setor')
    st.plotly_chart(fig_pizza, use_container_width=True)
    
# Gráfico de Linha do Tempo: Evolução das Denúncias
with col3:
    st.subheader("Evolução das Denúncias")
    df_denuncias['data_mes'] = df_denuncias['data'].dt.to_period('M')
    contagem_temporal = df_denuncias['data_mes'].value_counts().sort_index().reset_index()
    contagem_temporal.columns = ['Mês', 'Número de Casos']
    fig_linha = px.line(contagem_temporal, x='Mês', y='Número de Casos', title='Número de Casos ao Longo do Tempo')
    st.plotly_chart(fig_linha, use_container_width=True)
