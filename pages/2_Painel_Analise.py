import streamlit as st
import pandas as pd
import plotly.express as px
from services.banco import get_all_denuncias
from utils.layout import aplicar_layout
import time # Necessário para o spinner/loading

# Aplica o layout global
aplicar_layout()

# --- 1. CONFIGURAÇÃO DE AUTENTICAÇÃO ---

# Inicializar o estado de autenticação (CRUCIAL para gerenciar a sessão)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

def check_login(username, password):
    """Verifica as credenciais fixas e define o estado da sessão."""
    if username == USUARIO_CORRETO and password == SENHA_CORRETA:
        st.session_state['authenticated'] = True
        st.experimental_rerun() # Recarrega para exibir o painel
    else:
        st.error("Credenciais inválidas. Tente novamente.")

# --- 2. CONTROLE DE ACESSO (O PORTÃO) ---

if not st.session_state['authenticated']:
    # EXIBE O FORMULÁRIO DE LOGIN se não estiver autenticado
    st.title("🔐 Acesso Restrito ao Painel de Análise")
    st.markdown("Apenas para usuários de Compliance e RH.")
    
    with st.form("form_login"):
        username = st.text_input("Usuário:", key="login_user")
        password = st.text_input("Senha:", type="password", key="login_pass")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            check_login(username, password)

else:
    # --- 3. CONTEÚDO PRINCIPAL DO PAINEL (Se Autenticado) ---
    st.title("📊 Painel de Análise e Insights")
    st.success(f"Bem-vindo(a), {USUARIO_CORRETO}! Dados atualizados em tempo real.")

    # Função para buscar e preparar os dados (com cache para performance)
    # Nota: A RLS SELECT precisa estar ativada para 'authenticated' no Supabase!
    @st.cache_data(ttl=600) # Atualiza a cada 10 minutos
    def load_data():
        """Busca dados do Supabase e retorna como DataFrame."""
        try:
            data_list = get_all_denuncias()
            if data_list:
                df = pd.DataFrame(data_list)
                # Converte a coluna de data para o tipo datetime para análise temporal
                df['data_registro'] = pd.to_datetime(df['data_registro'])
                return df
            return pd.DataFrame()
        except Exception as e:
             st.error(f"Falha ao carregar dados. Verifique a RLS 'SELECT' para o 'authenticated' role no Supabase. Detalhe: {e}")
             return pd.DataFrame()


    # Carrega os dados com indicador visual
    with st.spinner('Carregando e processando dados de denúncias...'):
        time.sleep(1) # Simula o tempo de processamento
        df_denuncias = load_data()

    if df_denuncias.empty:
        st.warning("Nenhuma denúncia encontrada no banco de dados. Insira alguns dados na página 'Registrar Denúncia'.")
    else:
        # TABS para organização dos gráficos
        tab1, tab2, tab3 = st.tabs(["Resumo Geral", "Distribuição por Setor", "Evolução Temporal"])

        with tab1:
            st.header("Resumo de Casos por Classificação (IA)")
            
            # Gráfico de Barras: Denúncias por Tipo de Assédio/Ocorrência
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
            
            # KPI
            st.metric(label="Total de Denúncias Registradas", value=len(df_denuncias))


        with tab2:
            st.header("Distribuição de Ocorrências por Setor")
            
            # Gráfico de Pizza: Denúncias por Setor
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
            
            # Agrupamento para Evolução Temporal (Gráfico de Linha)
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
            
            
    # Adicionar botão de logout
    st.markdown("---")
    if st.button("Sair (Logout)", type="secondary"):
        st.session_state['authenticated'] = False
        st.experimental_rerun()
