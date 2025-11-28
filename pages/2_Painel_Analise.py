# pages/2_Painel_Analise.py
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.banco import get_all_denuncias, obter_resumo_para_graficos
from utils.layout import aplicar_layout

aplicar_layout()

# Autenticação simples (local) - mantenha/ajuste conforme seu fluxo real
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

def check_login(username, password):
    if username == USUARIO_CORRETO and password == SENHA_CORRETA:
        st.session_state['authenticated'] = True
        st.experimental_rerun()
    else:
        st.error("Credenciais inválidas. Tente novamente.")

if not st.session_state['authenticated']:
    st.title("🔐 Acesso Restrito ao Painel de Análise")
    with st.form("form_login"):
        username = st.text_input("Usuário:", key="login_user")
        password = st.text_input("Senha:", type="password", key="login_pass")
        submitted = st.form_submit_button("Entrar")
        if submitted:
            check_login(username, password)
    st.stop()

# Se chegou aqui, está autenticado
st.title("📊 Painel de Análise e Insights")

# Controle manual de atualização
col1, col2 = st.columns([1,4])
with col1:
    if st.button("🔄 Atualizar agora"):
        st.experimental_rerun()
with col2:
    st.write("Dados carregados do Supabase (última carga ao abrir a página).")

# Busca os dados SEM cache (queremos dados atualizados sempre)
try:
    with st.spinner("Carregando denúncias..."):
        time.sleep(0.6)
        dados = get_all_denuncias()
        df = pd.DataFrame(dados) if dados else pd.DataFrame()
        if not df.empty and 'data_registro' in df.columns:
            df['data_registro'] = pd.to_datetime(df['data_registro'], errors='coerce')
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

if df.empty:
    st.warning("Nenhuma denúncia encontrada no banco de dados.")
else:
    tab1, tab2, tab3 = st.tabs(["Resumo Geral", "Distribuição por Setor", "Evolução Temporal"])

    with tab1:
        st.header("Resumo de Casos por Classificação")
        contagem_tipo = df['tipo'].value_counts().reset_index()
        contagem_tipo.columns = ['Tipo de Ocorrência', 'Total de Casos']
        fig_bar = px.bar(contagem_tipo, x='Tipo de Ocorrência', y='Total de Casos',
                         color='Tipo de Ocorrência', title='Denúncias por Tipo', template='plotly_white')
        st.plotly_chart(fig_bar, use_container_width=True)
        st.metric(label="Total de Denúncias Registradas", value=len(df))

        # Lista — shows recent items
        st.subheader("Últimas denúncias")
        recent = df.head(10)
        for _, row in recent.iterrows():
            st.markdown(f"**ID:** {row.get('id','-')} • **Setor:** {row.get('setor','-')} • **Tipo:** {row.get('tipo','-')}")
            st.write(row.get('descricao','-'))
            anexo = row.get('anexo') or row.get('anexo_url')
            if anexo:
                if str(anexo).lower().endswith(".pdf"):
                    st.markdown(f"[📎 Abrir evidência]({anexo})")
                else:
                    st.image(anexo, width=300)

    with tab2:
        st.header("Distribuição de Ocorrências por Setor")
        contagem_setor = df['setor'].value_counts().reset_index()
        contagem_setor.columns = ['Setor', 'Total']
        fig_pie = px.pie(contagem_setor, names='Setor', values='Total', title='Por Setor', hole=.3, template='plotly_white')
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab3:
        st.header("Evolução Mensal das Denúncias")
        if 'data_registro' in df.columns:
            df['MesAno'] = df['data_registro'].dt.to_period('M').astype(str)
            contagem_mensal = df.groupby('MesAno').size().reset_index(name='Total')
            fig_line = px.line(contagem_mensal, x='MesAno', y='Total', title='Evolução Mensal', markers=True, template='plotly_white')
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Sem campo de data para plotar evolução temporal.")

st.markdown("---")
if st.button("Sair (Logout)"):
    st.session_state['authenticated'] = False
    st.experimental_rerun()
