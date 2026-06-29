import streamlit as st
from services.auth_service import autenticar_usuario

st.set_page_config(
    page_title="Login - FitLife",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================
# REDIRECIONAMENTO SE LOGADO
# ==============================
if st.session_state.get("usuario"):
    st.switch_page("pages/dashboard.py")

# ==============================
# ESTILO
# ==============================
st.markdown("""
    <style>
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .login-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #1f77b4;
        }
        .login-subtitle {
            font-size: 1.2em;
            color: #666;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="login-header">
        <div class="login-title">🏋️ FitLife</div>
        <div class="login-subtitle">Sua rotina fitness integrada</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Bem-vindo de volta!")
st.markdown("Entre com suas credenciais para acessar o sistema.")

# ==============================
# INICIALIZA SESSION STATE
# ==============================
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

# ==============================
# FORM LOGIN
# ==============================
with st.form("login_form", border=True):
    email = st.text_input("📧 Email")
    senha = st.text_input("🔐 Senha", type="password")

    submit = st.form_submit_button("🚀 Entrar", use_container_width=True)

# ==============================
# LOGIN LOGIC
# ==============================
if submit:
    if not email or not senha:
        st.error("❌ Preencha todos os campos.")
    else:
        try:
            usuario = autenticar_usuario(email, senha)

            # salva sessão (SEM depender de reload imediato)
            st.session_state["usuario"] = {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "objetivo": usuario.objetivo,
                "peso": usuario.peso,
                "altura": usuario.altura,
            }

            st.success("✅ Login realizado com sucesso!")
            st.balloons()

            # força rerun antes de navegar (evita bug no cloud)
            st.rerun()

        except ValueError as e:
            st.error(f"❌ {str(e)}")

        except Exception as e:
            st.error("❌ Erro inesperado no login.")
            st.exception(e)

# ==============================
# LINKS
# ==============================
st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Criar conta", use_container_width=True):
        st.switch_page("pages/cadastro.py")

with col2:
    if st.button("🔑 Esqueci senha", use_container_width=True):
        st.info("Funcionalidade em desenvolvimento")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #999;'>© 2026 FitLife</div>",
    unsafe_allow_html=True
)