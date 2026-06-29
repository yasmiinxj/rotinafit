import streamlit as st

st.set_page_config(
    page_title="FitLife",
    page_icon="🏋️",
    layout="centered"
)

# Inicializar sessão
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

st.title("🏋️ FitLife")

st.write("Sistema de rotina fitness integrada")

# Controle de navegação simples
if st.session_state["usuario"]:
    st.success(f"Logado como {st.session_state['usuario']['nome']}")

    if st.button("Ir para Dashboard"):
        st.switch_page("pages/dashboard.py")

    if st.button("Sair"):
        st.session_state["usuario"] = None
        st.rerun()

else:
    st.warning("Você não está logado")

    if st.button("Ir para Login"):
        st.switch_page("pages/login.py")

    if st.button("Criar conta"):
        st.switch_page("pages/cadastro.py")