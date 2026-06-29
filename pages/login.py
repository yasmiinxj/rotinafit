import streamlit as st
from services.auth_service import autenticar_usuario

st.set_page_config(
    page_title="Login - FitLife",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado para melhor aparência
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
            margin-bottom: 10px;
        }
        .login-subtitle {
            font-size: 1.2em;
            color: #666;
            margin-bottom: 20px;
        }
        .login-form {
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="login-header">
        <div class="login-title">🏋️ FitLife</div>
        <div class="login-subtitle">Sua rotina fitness integrada</div>
    </div>
""", unsafe_allow_html=True)

# Verificar se usuário já está autenticado
if "usuario" in st.session_state and st.session_state["usuario"] is not None:
    st.switch_page("pages/dashboard.py")

# Formulário de login
st.markdown("### Bem-vindo de volta!")
st.markdown("Entre com suas credenciais para acessar o dashboard.")

with st.form("login_form", border=True):
    email = st.text_input(
        "📧 Email",
        placeholder="seu-email@exemplo.com"
    )
    senha = st.text_input(
        "🔐 Senha",
        type="password",
        placeholder="Digite sua senha"
    )
    
    submit_button = st.form_submit_button(
        "🚀 Entrar",
        use_container_width=True,
        type="primary"
    )

# Processar login
if submit_button:
    if not email or not senha:
        st.error("❌ Por favor, preencha todos os campos.")
    else:
        try:
            # Autenticar usuário
            usuario = autenticar_usuario(email, senha)
            
            # Armazenar na sessão
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
            
            # Redirecionar para dashboard
            import time
            time.sleep(1)
            st.switch_page("pages/dashboard.py")
            
        except ValueError as e:
            st.error(f"❌ {str(e)}")
        except Exception as e:
            st.error(f"❌ Erro ao realizar login: {str(e)}")

# Divisor
st.divider()

# Links adicionais
col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Criar conta", use_container_width=True):
        st.switch_page("pages/cadastro.py")

with col2:
    if st.button("🔑 Esqueci minha senha", use_container_width=True):
        st.info("ℹ️ Funcionalidade em breve...", icon="ℹ️")

# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #999; font-size: 0.9em;'>"
    "© 2026 FitLife - Todos os direitos reservados"
    "</div>",
    unsafe_allow_html=True
)
