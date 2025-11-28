import streamlit as st
import pandas as pd
import plotly.express as px
from services.banco import get_all_denuncias, obter_resumo_para_graficos
from services.auth import ensure_logged_in # Presume que o arquivo services/auth.py existe
from utils.layout import aplicar_layout

aplicar_layout()
ensure_logged_in() # Garante que o usuário está logado

st.title("📊 Painel de Análise de Denúncias")
st.markdown("Visualize as estatísticas e os dados das denúncias registradas.")

# --- Obter dados ---
try:
    dados_dict = get_all_denuncias()
    if not dados_dict:
        st.info("Nenhuma denúncia encontrada no banco de dados.")
        st.stop()
        
    df = pd.DataFrame(dados_dict)
    
    # Garantindo que a coluna 'data_registro' seja do tipo datetime para gráficos
    df['data_registro'] = pd.to_datetime(df['data_registro'])
    
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# --- Resumo Geral ---
resumo = obter_resumo_para_graficos()
total_denuncias = len(df)

col1, col2, col3 = st.columns(3)
col1.metric("Total de Denúncias", total_denuncias)
# Outras métricas podem ser adicionadas aqui (ex: Tipos Únicos, Denúncias Resolvidas, etc.)
# col2.metric("Tipos Únicos", len(resumo['por_tipo']))
# col3.metric("Setores Envolvidos", len(resumo['por_setor']))

st.markdown("---")

# --- Distribuição por Tipo e Setor ---

st.header("Distribuição por Categoria e Setor")
col_grafico1, col_grafico2 = st.columns(2)

# Gráfico 1: Por Tipo
df_tipo = pd.DataFrame(resumo['por_tipo'].items(), columns=['Tipo', 'Contagem'])
fig_tipo = px.pie(df_tipo, values='Contagem', names='Tipo', title='Distribuição por Tipo de Denúncia')
col_grafico1.plotly_chart(fig_tipo, use_container_width=True)

# Gráfico 2: Por Setor
df_setor = pd.DataFrame(resumo['por_setor'].items(), columns=['Setor', 'Contagem'])
fig_setor = px.bar(df_setor, x='Setor', y='Contagem', title='Distribuição por Setor')
col_grafico2.plotly_chart(fig_setor, use_container_width=True)

st.markdown("---")

# --- Evolução Temporal ---
st.header("Evolução Temporal das Denúncias")
# Agrupa por dia e conta o número de denúncias
df_tempo = df.groupby(df['data_registro'].dt.date)['id'].count().reset_index()
df_tempo.columns = ['Data', 'Contagem']

fig_tempo = px.line(df_tempo, x='Data', y='Contagem', 
                    title='Contagem de Denúncias ao Longo do Tempo')
st.plotly_chart(fig_tempo, use_container_width=True)

st.markdown("---")

# --- Tabela de Denúncias Recentes ---
st.header("Denúncias Recentes")
recent = df.head(10)

# Lista de colunas a exibir - AGORA SEM 'sentimento'
colunas_exibir = [
    "data_registro",
    "denuncia",
    "tipo",
    "setor", 
    "arquivo_url"
]

# Trata a ausência da coluna 'setor' para evitar erro se for nula
if 'setor' not in recent.columns:
    recent['setor'] = 'Não Informado'

st.dataframe(recent[colunas_exibir], hide_index=True, use_container_width=True)
