import streamlit as st

st.set_page_config(
    page_title="FitLife - Rotina Fitness Integrada",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inicializar session state
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

# Se o usuário está autenticado, redirecionar para dashboard
if st.session_state["usuario"] is not None:
    st.switch_page("pages/dashboard.py")

# Caso contrário, redirecionar para login
st.switch_page("pages/login.py")