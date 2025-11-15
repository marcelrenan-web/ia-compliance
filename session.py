import streamlit as st

def is_logged_in():
    return st.session_state.get('auth_user') is not None

def set_user(user_info):
    st.session_state['auth_user'] = user_info

def logout_user():
    if 'auth_user' in st.session_state:
        del st.session_state['auth_user']
