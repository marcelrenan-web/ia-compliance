import streamlit as st
import pandas as pd
from services.auth import ensure_logged_in
from services.supabase_client import get_supabase_or_raise

# ---------------------------------------------------------
# AUTENTICAÇÃO (somente RH / Compliance)
# ---------------------------------------------------------
if not ensure_logged_in():
    st.stop()

st.title("📊 Painel de Análise de Denúncias")

st.markdown("""
Este painel permite visualizar todas as denúncias registradas no sistema,
com filtros por setor, tipo e busca por palavras-chave.
""")

# ---------------------------------------------------------
# LER DADOS DO SUPABASE
# ---------------------------------------------------------
def load_data():
    try:
        supabase = get_supabase_or_raise()
        result = supabase.table("denuncias").select("*").execute()
        return pd.DataFrame(result.data)
    except Exception as e:
        st.error("Erro ao carregar dados do Supabase.")
        st.write(str(e))
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Nenhum registro encontrado no banco de dados.")
    st.stop()

# Converte datas somente se existir
if "data_servico" in df.columns:
    df["data_servico"] = pd.to_datetime(df["data_servico"], errors="coerce")

# ---------------------------------------------------------
# FILTROS
# ---------------------------------------------------------
st.subheader("🔍 Filtros")

col1, col2, col3 = st.columns(3)

setores = ["Todos"] + sorted(df["setor"].dropna().unique().tolist())
f_setor = col1.selectbox("Filtrar por setor", setores)

tipos = ["Todos"] + sorted(df["tipo"].dropna().unique().tolist())
f_tipo = col2.selectbox("Filtrar por tipo", tipos)

f_busca = col3.text_input("Busca na descrição")

df_filtrado = df.copy()

if f_setor != "Todos":
    df_filtrado = df_filtrado[df_filtrado["setor"] == f_setor]

if f_tipo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["tipo"] == f_tipo]

if f_busca:
    df_filtrado = df_filtrado[df_filtrado["descricao"].str.contains(f_busca, case=False, na=False)]

st.write("### 📄 Registros encontrados:", len(df_filtrado))

# ---------------------------------------------------------
# TABELA DE RESULTADOS
# ---------------------------------------------------------
st.dataframe(
    df_filtrado.sort_values(by="data_servico", ascending=False),
    use_container_width=True,
)

# ---------------------------------------------------------
# GRÁFICO DE SENTIMENTOS
# ---------------------------------------------------------
st.subheader("📈 Distribuição de Sentimentos")

if "sentimento" in df.columns:
    sentimento_count = df_filtrado["sentimento"].fillna("Indefinido").value_counts()
    st.bar_chart(sentimento_count)
else:
    st.info("Nenhum dado de sentimento encontrado.")
