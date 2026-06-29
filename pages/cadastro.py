import streamlit as st
from services.auth_service import cadastrar_usuario


def render(go=None):

    st.title("📝 Criar Conta FitLife")

    st.write("Preencha seus dados para começar 💪")

    # =========================
    # FORMULÁRIO
    # =========================
    with st.form("form_cadastro"):

        nome = st.text_input("👤 Nome completo")
        email = st.text_input("📧 Email")
        senha = st.text_input("🔐 Senha", type="password")

        col1, col2 = st.columns(2)

        with col1:
            peso = st.number_input("⚖️ Peso (kg)", min_value=30.0, max_value=300.0)

        with col2:
            altura = st.number_input("📏 Altura (m)", min_value=1.0, max_value=2.5)

        objetivo = st.selectbox(
            "🎯 Objetivo",
            ["emagrecer", "ganhar peso", "manter peso"]
        )

        submit = st.form_submit_button("🚀 Criar conta")

    # =========================
    # CADASTRO
    # =========================
    if submit:

        if not nome or not email or not senha:
            st.error("❌ Preencha todos os campos obrigatórios.")
            return

        try:
            cadastrar_usuario(
                nome=nome,
                data_nascimento=None,
                sexo=None,
                peso=peso,
                altura=altura,
                objetivo=objetivo,
                email=email,
                senha=senha
            )

            st.success("✅ Conta criada com sucesso!")
            st.balloons()

            st.info("Agora faça login.")

            # se tiver router usa ele, senão fallback seguro
            if go:
                go("login")
            else:
                st.switch_page("pages/login.py")

        except Exception as e:
            st.error(f"❌ Erro: {e}")

    # =========================
    # BACKUP NAVEGAÇÃO
    # =========================
    st.divider()

    if st.button("🔙 Voltar para login"):
        if go:
            go("login")
        else:
            st.switch_page("pages/login.py")


# =========================
# EXECUÇÃO DIRETA (LOCAL TEST)
# =========================
if __name__ == "__main__":
    render()