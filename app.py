import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from supabase import create_client, Client
import uuid

# -----------------------------
# CONFIGURAÇÕES DO SUPABASE
# -----------------------------
SUPABASE_URL = "https://SEU-PROJETO.supabase.co"  # substitua pelo seu
SUPABASE_KEY = "SUA-CHAVE-API"  # substitua pela sua chave
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# FUNÇÕES DE BANCO DE DADOS
# -----------------------------
def gerar_codigo_unico():
    """Gera um código curto e único para a denúncia."""
    return str(uuid.uuid4())[:8].upper()

def insert_denuncia(setor, tipo_ocorrencia, descricao):
    """Insere nova denúncia na tabela Supabase."""
    data_envio = datetime.now().isoformat()
    codigo = gerar_codigo_unico()
    denuncia = {
        "id": codigo,
        "setor": setor,
        "tipo_ocorrencia": tipo_ocorrencia,
        "descricao": descricao,
        "data_envio": data_envio
    }
    supabase.table("denuncias").insert(denuncia).execute()
    return codigo

def fetch_denuncias():
    """Lê todas as denúncias do Supabase."""
    response = supabase.table("denuncias").select("*").execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame()

# -----------------------------
# CONFIGURAÇÃO STREAMLIT
# -----------------------------
st.set_page_config(page_title="IA Assistente de Compliance", layout="wide")
st.title("🔒 IA Assistente de Compliance")

# -----------------------------
# LOGIN
# -----------------------------
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

with st.sidebar:
    st.header("Login RH/Compliance")
    usuario = st.text_input("Usuário:")
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if usuario == "admin" and senha == "1234":
            st.session_state['autenticado'] = True
            st.success("✅ Login realizado com sucesso!")
        else:
            st.error("❌ Usuário ou senha incorretos.")

# -----------------------------
# FORMULÁRIO DE DENÚNCIA
# -----------------------------
st.markdown("---")
st.header("📢 Registrar Denúncia Anônima")

with st.form("denuncia_form"):
    setor = st.selectbox(
        "Selecione o setor relacionado ao fato:",
        ("Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros")
    )

    tipo_assedio = st.selectbox(
        "Tipo de ocorrência:",
        ("Assédio Moral", "Assédio Sexual", "Racismo", "Homofobia", "Discriminação", "Outros")
    )

    descricao = st.text_area("Descreva o ocorrido:")

    submitted = st.form_submit_button("Enviar Denúncia")

    if submitted:
        if descricao.strip() == "":
            st.warning("⚠️ Por favor, descreva o ocorrido.")
        else:
            codigo = insert_denuncia(setor, tipo_assedio, descricao)
            st.success(f"✅ Denúncia enviada com sucesso! Código de acompanhamento: **{codigo}**")

# -----------------------------
# PAINEL DE ANÁLISE RH/COMPLIANCE
# -----------------------------
if st.session_state['autenticado']:
    st.markdown("---")
    st.header("📊 Painel de Análise de Denúncias")

    df = fetch_denuncias()

    if not df.empty:
        # Conversão de data
        df['data_envio'] = pd.to_datetime(df['data_envio'])
        df['Mês'] = df['data_envio'].dt.to_period('M').astype(str)

        # Contagens
        contagem_tipo = df['tipo_ocorrencia'].value_counts().reset_index()
        contagem_tipo.columns = ['Tipo de Ocorrência', 'Número de Casos']

        contagem_setor = df['setor'].value_counts().reset_index()
        contagem_setor.columns = ['Setor', 'Número de Casos']

        contagem_temporal = df['Mês'].value_counts().sort_index().reset_index()
        contagem_temporal.columns = ['Mês', 'Número de Casos']

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Casos por Tipo de Ocorrência")
            fig_bar = px.bar(contagem_tipo, x='Tipo de Ocorrência', y='Número de Casos', color='Tipo de Ocorrência')
            st.plotly_chart(fig_bar, use_container_width=True)import streamlit as st
from utils.session import verificar_login
from utils.layout import aplicar_layout
from services.auth import realizar_logout

st.set_page_config(
    page_title="Portal Vigia Ético",
    page_icon="🛡️",
    layout="wide"
)

aplicar_layout()

# Verificar sessão
usuario_logado = verificar_login()

st.sidebar.markdown("## 🛡️ Portal Vigia Ético")

if usuario_logado:
    st.sidebar.success(f"Bem-vindo, {usuario_logado['email']}")
    if st.sidebar.button("Sair"):
        realizar_logout()
        st.rerun()

st.title("Portal Vigia Ético")
st.write("Bem-vindo ao sistema de denúncias anônimas com análise de sentimento.")

st.markdown("""
### O que você pode fazer:
- Enviar denúncias de forma anônima  
- Analisar denúncias recebidas  
- Visualizar métricas e sentimentos  
""")


        with col2:
            st.subheader("🥧 Distribuição por Setor")
            fig_pizza = px.pie(contagem_setor, names='Setor', values='Número de Casos')
            st.plotly_chart(fig_pizza, use_container_width=True)

        st.markdown("---")
        st.subheader("📈 Evolução das Denúncias ao Longo do Tempo")
        fig_linha = px.line(contagem_temporal, x='Mês', y='Número de Casos', markers=True)
        st.plotly_chart(fig_linha, use_container_width=True)

        st.markdown("---")
        st.subheader("📄 Base de Denúncias Registradas")
        st.dataframe(df[['id', 'setor', 'tipo_ocorrencia', 'descricao', 'data_envio']], use_container_width=True)

    else:
        st.info("📭 Nenhuma denúncia registrada ainda.")
