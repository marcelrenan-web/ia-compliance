@@ -32,10 +32,91 @@
# -----------------------------
conn = sqlite3.connect("denuncias.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS denuncias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        setor TEXT,
        tipo_ocorrencia TEXT,
        descricao TEXT,
        d
c.execute("""CREATE TABLE IF NOT EXISTS denuncias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setor TEXT,
                tipo_ocorrencia TEXT,
                descricao TEXT,
                data_envio TIMESTAMP
            )""")
conn.commit()

# -----------------------------
# FORMULÁRIO DE DENÚNCIA (ANÔNIMO)
# -----------------------------
st.header("📢 Registrar Denúncia Anônima")

setor = st.selectbox("Selecione o setor relacionado ao fato:",
                     ("Engenharia", "Produção", "Marketing", "Recursos Humanos", "Financeiro", "Outros"))

tipo_assedio = st.selectbox("Tipo de ocorrência:",
                            ("Assédio Moral", "Assédio Sexual", "Racismo", "Homofobia", "Discriminação", "Outros"))

descricao = st.text_area("Descreva o ocorrido:")

if st.button("Enviar Denúncia"):
    if descricao.strip() == "":
        st.warning("Por favor, descreva o ocorrido.")
    else:
        c.execute("INSERT INTO denuncias (setor, tipo_ocorrencia, descricao, data_envio) VALUES (?, ?, ?, ?)",
                  (setor, tipo_assedio, descricao, datetime.now()))
        conn.commit()
        st.success("✅ Denúncia enviada com sucesso! Sua identidade será preservada.")

# -----------------------------
# PAINEL RH/COMPLIANCE
# -----------------------------
if st.session_state['autenticado']:
    st.markdown("---")
    st.header("📊 Painel de Análise de Denúncias")

    df = pd.read_sql_query("SELECT * FROM denuncias", conn)

    if not df.empty:
        # Contagens para gráficos
        contagem_tipo = df['tipo_ocorrencia'].value_counts().reset_index()
        contagem_tipo.columns = ['Tipo de Ocorrência', 'Número de Casos']

        contagem_setor = df['setor'].value_counts().reset_index()
        contagem_setor.columns = ['Setor', 'Número de Casos']

        df['Mês'] = pd.to_datetime(df['data_envio']).dt.to_period('M').astype(str)
        contagem_temporal = df['Mês'].value_counts().sort_index().reset_index()
        contagem_temporal.columns = ['Mês', 'Número de Casos']

        # Gráficos
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Casos por Tipo de Ocorrência")
            fig_bar = px.bar(contagem_tipo,
                             x='Tipo de Ocorrência',
                             y='Número de Casos',
                             color='Tipo de Ocorrência',
                             title="Distribuição de Casos por Tipo")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.subheader("🥧 Distribuição por Setor")
            fig_pizza = px.pie(contagem_setor,
                               names='Setor',
                               values='Número de Casos',
                               title="Denúncias por Setor")
            st.plotly_chart(fig_pizza, use_container_width=True)

        st.markdown("---")
        st.subheader("📈 Evolução das Denúncias ao Longo do Tempo")
        fig_linha = px.line(contagem_temporal,
                            x='Mês',
                            y='Número de Casos',
                            markers=True,
                            title="Denúncias Registradas por Mês")
        st.plotly_chart(fig_linha, use_container_width=True)

        st.markdown("---")
        st.subheader("📄 Base de Denúncias")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhuma denúncia registrada ainda.")

conn.close()
