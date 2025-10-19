import streamlit as st
import pandas as pd
import plotly.express as px
import qrcode
from io import BytesIO
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- Configuração da Página ---
st.set_page_config(
    page_title="IA de Compliance",
    page_icon="🛡️",
    layout="wide"
)

# --- Função para gerar QR Code ---
def gerar_qr_code(url):
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="Aponte a câmera para acessar o formulário")

# --- Configuração de Login ---
config_yaml = """
credentials:
  usernames:
    rhadmin:
      email: rh@empresa.com
      name: RH Conformidade
      password: '12345'
cookie:
  expiry_days: 30
  key: 'chave_unica_segura'
  name: 'cookie_compliance'
"""
config = yaml.load(config_yaml, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- Navegação ---
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione uma opção:", ["Página Inicial", "Painel RH/Compliance"])

# --- Página Inicial ---
if page == "Página Inicial":
    st.title("🛡️ IA Assistente de Compliance")
    st.markdown("""
    Sua voz é essencial para construirmos um ambiente de trabalho mais ético e seguro.
    **Todas as denúncias são anônimas.** Sua identidade será totalmente protegida.
    """)
    st.markdown("---")

    # QR Code
    st.subheader("📱 Acesse via QR Code")
    gerar_qr_code("https://seuapp.streamlit.app")  # Substitua pelo link real do app

    # Formulário de denúncia
    st.header("Formulário de Denúncia Anônima")
    denuncia_texto = st.text_area("Descreva o ocorrido:", height=200)
    setor_escolhido = st.selectbox(
        "Selecione o setor onde ocorreu:",
        ("", "Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outro")
    )
    botao_enviar = st.button("Enviar Denúncia")

    if botao_enviar:
        if denuncia_texto and setor_escolhido:
            tipo_denuncia = "Assédio Moral"  # Placeholder
            st.success("✅ Sua denúncia foi enviada com sucesso! Obrigado pela colaboração.")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")

# --- Painel RH/Compliance ---
elif page == "Painel RH/Compliance":
    name, auth_status, username = authenticator.login("Login RH", "main")

    if auth_status:
        st.title("📊 Painel de Análise de Denúncias")
        st.success(f"Bem-vindo(a), {name}!")
        st.markdown("---")

        # Simulação de dados
        dados_denuncias_simulacao = {
            'tipo_denuncia': ['Assédio Moral', 'Assédio Sexual', 'Racismo', 'Assédio Moral', 'Assédio Sexual', 'Homofobia', 'Assédio Moral'],
            'setor': ['Engenharia', 'Produção', 'Marketing', 'Engenharia', 'Recursos Humanos', 'Engenharia', 'Financeiro'],
            'data': pd.to_datetime(['2025-01-01', '2025-02-15', '2025-03-20', '2025-04-10', '2025-05-05', '2025-06-12', '2025-06-25'])
        }
        df_denuncias = pd.DataFrame(dados_denuncias_simulacao)

        # --- Gráficos ---
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

        # Registro de ações
        st.header("Registro de Ações e Soluções")
        st.markdown("Use esta seção para documentar o desfecho das denúncias e as medidas tomadas.")

        denuncias_abertas = [101, 102, 103]
        denuncia_id = st.selectbox("Selecione a Denúncia para Acompanhamento:", [""] + denuncias_abertas)

        if denuncia_id:
            st.subheader(f"Documentando Denúncia #{denuncia_id}")
            status_denuncia = st.selectbox("Status da Apuração:", ["", "Verídica", "Não Verídica"])
            medidas_tomadas = st.text_area("Descreva as medidas tomadas:", height=150)
            tempo_solucao = st.number_input("Tempo de Solução (em dias):", min_value=0, step=1)
            botao_salvar_acao = st.button("Salvar Registro")

            if botao_salvar_acao:
                st.success("✅ Ação registrada com sucesso!")

    elif auth_status is False:
        st.error("Usuário ou senha incorretos.")
    else:
        st.warning("Por favor, insira suas credenciais para acessar o painel.")
