import streamlit as st
import pandas as pd
import plotly.express as px
import time 
import sys
import os

# --- CORREÇÃO DE CAMINHO ---
# Garante que os módulos 'services' e 'utils' sejam encontrados a partir de 'pages'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------------------

from services.banco import get_all_denuncias
from utils.layout import aplicar_layout

# Aplica o layout global
aplicar_layout()

# --- 1. CONFIGURAÇÃO DE AUTENTICAÇÃO ---

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

def check_login(username, password):
    """Verifica as credenciais fixas e define o estado da sessão."""
    if username == USUARIO_CORRETO and password == SENHA_CORRETA:
        st.session_state['authenticated'] = True
        st.experimental_rerun() 
    else:
        st.error("Credenciais inválidas. Tente novamente.")

# --- 2. CONTROLE DE ACESSO (O PORTÃO) ---

if not st.session_state['authenticated']:
    st.title("🔐 Acesso Restrito ao Painel de Análise")
    
    with st.form("form_login"):
        username = st.text_input("Usuário:", key="login_user")
        password = st.text_input("Senha:", type="password", key="login_pass")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            check_login(username, password)

else:
    # --- 3. CONTEÚDO PRINCIPAL DO PAINEL (Se Autenticado) ---
    st.title("📊 Painel de Análise e Insights")

    @st.cache_data(ttl=600) 
    def load_data():
        """Busca dados do Supabase e retorna como DataFrame."""
        try:
            data_list = get_all_denuncias()
            if data_list:
                df = pd.DataFrame(data_list)
                # Garante que o nome da coluna é 'data_registro'
                df['data_registro'] = pd.to_datetime(df['data_registro'])
                return df
            return pd.DataFrame()
        except Exception as e:
             # Este erro pode ocorrer se a RLS 'SELECT' para 'authenticated' estiver errada.
             st.error(f"Falha ao carregar dados. Detalhe: {e}")
             return pd.DataFrame()


    with st.spinner('Carregando e processando dados de denúncias...'):
        time.sleep(1) 
        df_denuncias = load_data()

    if df_denuncias.empty:
        st.warning("Nenhuma denúncia encontrada no banco de dados. Insira alguns dados na página 'Registrar Denúncia'.")
    else:
        tab1, tab2, tab3 = st.tabs(["Resumo Geral", "Distribuição por Setor", "Evolução Temporal"])

        with tab1:
            st.header("Resumo de Casos por Classificação")
            
            contagem_tipo = df_denuncias['tipo'].value_counts().reset_index()
            contagem_tipo.columns = ['Tipo de Ocorrência', 'Total de Casos']
            
            fig_bar = px.bar(
                contagem_tipo,
                x='Tipo de Ocorrência',
                y='Total de Casos',
                color='Tipo de Ocorrência',
                title='Denúncias Classificadas por Tipo',
                template='plotly_white'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            st.metric(label="Total de Denúncias Registradas", value=len(df_denuncias))


        with tab2:
            st.header("Distribuição de Ocorrências por Setor")
            
            contagem_setor = df_denuncias['setor'].value_counts().reset_index()
            contagem_setor.columns = ['Setor', 'Total']
            
            fig_pie = px.pie(
                contagem_setor,
                names='Setor',
                values='Total',
                title='Distribuição de Casos por Setor Denunciado',
                hole=.3,
                template='plotly_white'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with tab3:
            st.header("Evolução Mensal das Denúncias")
            
            df_denuncias['Mês/Ano'] = df_denuncias['data_registro'].dt.to_period('M').astype(str)
            contagem_mensal = df_denuncias.groupby('Mês/Ano').size().reset_index(name='Total')

            fig_line = px.line(
                contagem_mensal,
                x='Mês/Ano',
                y='Total',
                title='Evolução do Volume de Denúncias (Registro)',
                markers=True,
                template='plotly_white'
            )
            st.plotly_chart(fig_line, use_container_width=True)
            
            
    st.markdown("---")
    if st.button("Sair (Logout)", type="secondary"):
        st.session_state['authenticated'] = False
        st.experimental_rerun()
