import streamlit as st

# ---------- ROTINAS DE SESSÃO/LOGIN (substitua o login antigo) ----------
def reset_session():
    """Limpa a sessão (útil para depuração)."""
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.experimental_rerun()

def is_logged():
    return st.session_state.get("logged_in", False)

def do_login(username, password):
    # credenciais do protótipo
    if username == "admin" and password == "1234":
        st.session_state["logged_in"] = True
        st.session_state["user"] = {"username": "admin"}
        return True
    return False

def login_ui():
    """Mostra o formulário de login e controla o fluxo."""
    st.title("🔐 Login - Portal Vigia Ético (protótipo)")
    username = st.text_input("Usuário", key="ui_user")
    password = st.text_input("Senha", type="password", key="ui_pwd")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Entrar", key="btn_enter"):
            ok = do_login(username, password)
            if ok:
                st.success("Login efetuado com sucesso.")
                st.experimental_rerun()
            else:
                st.error("Usuário ou senha incorretos.")
    with col2:
        if st.button("Resetar sessão (dev)", key="btn_reset"):
            reset_session()

# ---------- Uso: chamar login_check() no topo da página privada ----------
def ensure_login_or_stop():
    if is_logged():
        return True
    # se não está logado, mostrar UI e interromper execução
    login_ui()
    st.stop()

