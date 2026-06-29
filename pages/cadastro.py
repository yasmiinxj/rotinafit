import streamlit as st
from datetime import date, datetime
from services.auth_service import cadastrar_usuario
import re

st.set_page_config(
    page_title="Cadastro - FitLife",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado
st.markdown("""
    <style>
        .signup-header {
            text-align: center;
            margin-bottom: 20px;
        }
        .signup-title {
            font-size: 2em;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="signup-header">
        <div class="signup-title">🏋️ FitLife - Cadastro</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Crie sua conta e comece sua jornada fitness!")

# Função para validar email
def validar_email(email: str) -> bool:
    """Valida se o email tem formato correto."""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

# Criar formulário em abas
tab1, tab2, tab3 = st.tabs(["👤 Dados Pessoais", "📊 Métricas", "🔐 Credenciais"])

with tab1:
    st.subheader("Informações Pessoais")
    
    nome = st.text_input(
        "👤 Nome Completo *",
        placeholder="Seu nome completo",
        key="nome"
    )
    
    data_nascimento = st.date_input(
        "📅 Data de Nascimento *",
        value=date(2000, 1, 1),
        min_value=date(1950, 1, 1),
        max_value=date.today()
    )
    
    sexo = st.selectbox(
        "⚧ Sexo *",
        options=["Selecione...", "Feminino", "Masculino"],
        key="sexo"
    )
    
    objetivo = st.selectbox(
        "🎯 Objetivo *",
        options=["Selecione...", "Emagrecer", "Ganhar peso", "Manter peso"],
        key="objetivo"
    )

with tab2:
    st.subheader("Métricas Físicas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input(
            "⚖️ Peso (kg) *",
            min_value=0.0,
            value=70.0,
            step=0.1,
            key="peso"
        )
    
    with col2:
        altura = st.number_input(
            "📏 Altura (cm) *",
            min_value=0.0,
            value=170.0,
            step=0.1,
            key="altura"
        )
    
    # Calcular e exibir IMC
    if peso > 0 and altura > 0:
        imc = peso / ((altura / 100) ** 2)
        
        if imc < 18.5:
            categoria = "Abaixo do peso"
            cor = "🔵"
        elif imc < 25:
            categoria = "Peso normal"
            cor = "🟢"
        elif imc < 30:
            categoria = "Sobrepeso"
            cor = "🟡"
        else:
            categoria = "Obesidade"
            cor = "🔴"
        
        st.metric(
            "📊 IMC",
            f"{imc:.1f}",
            f"{categoria} {cor}"
        )

with tab3:
    st.subheader("Credenciais de Acesso")
    
    email = st.text_input(
        "📧 Email *",
        placeholder="seu-email@exemplo.com",
        key="email"
    )
    
    senha = st.text_input(
        "🔐 Senha *",
        type="password",
        placeholder="Crie uma senha forte",
        key="senha"
    )
    
    confirmar_senha = st.text_input(
        "🔐 Confirmar Senha *",
        type="password",
        placeholder="Confirme sua senha",
        key="confirmar_senha"
    )
    
    st.markdown("**Dicas de segurança:**")
    st.info(
        "✅ Use pelo menos 8 caracteres\n"
        "✅ Combine letras, números e símbolos\n"
        "✅ Não use informações pessoais",
        icon="🔒"
    )

# Botões de ação
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Cadastrar", use_container_width=True, type="primary"):
        # Validações
        erros = []
        
        # Campos obrigatórios
        if not nome:
            erros.append("Nome completo é obrigatório")
        if sexo == "Selecione...":
            erros.append("Sexo é obrigatório")
        if objetivo == "Selecione...":
            erros.append("Objetivo é obrigatório")
        if not email:
            erros.append("Email é obrigatório")
        if not senha:
            erros.append("Senha é obrigatória")
        if not confirmar_senha:
            erros.append("Confirmação de senha é obrigatória")
        
        # Validações de formato
        if email and not validar_email(email):
            erros.append("Email inválido")
        
        if peso <= 0:
            erros.append("Peso deve ser maior que zero")
        if altura <= 0:
            erros.append("Altura deve ser maior que zero")
        
        # Validar senhas
        if senha and confirmar_senha:
            if senha != confirmar_senha:
                erros.append("Senha e confirmação não conferem")
            if len(senha) < 6:
                erros.append("Senha deve ter pelo menos 6 caracteres")
        
        # Exibir erros ou processar cadastro
        if erros:
            st.error("❌ Erros encontrados:")
            for erro in erros:
                st.markdown(f"• {erro}")
        else:
            try:
                # Converter objetivo para minúsculas
                objetivo_map = {
                    "Emagrecer": "emagrecer",
                    "Ganhar peso": "ganhar peso",
                    "Manter peso": "manter peso"
                }
                objetivo_normalizado = objetivo_map[objetivo]
                
                # Chamar serviço de cadastro
                resultado = cadastrar_usuario(
                    nome=nome,
                    data_nascimento=data_nascimento,
                    sexo=sexo,
                    peso=peso,
                    altura=altura,
                    objetivo=objetivo_normalizado,
                    email=email,
                    senha=senha
                )
                
                st.success("✅ Cadastro realizado com sucesso!")
                st.balloons()
                
                st.markdown("### 🎉 Bem-vindo ao FitLife!")
                st.markdown(f"Olá **{nome}**! Sua conta foi criada com sucesso.")
                st.markdown("Agora você pode fazer login e começar sua jornada fitness.")
                
                # Redirecionar para login após 2 segundos
                import time
                time.sleep(2)
                st.switch_page("pages/login.py")
                
            except ValueError as e:
                st.error(f"❌ Erro: {str(e)}")
            except Exception as e:
                st.error(f"❌ Erro ao cadastrar: {str(e)}")

with col2:
    if st.button("❌ Voltar", use_container_width=True):
        st.switch_page("pages/login.py")

# Divisor
st.divider()

# Rodapé
st.markdown(
    "<div style='text-align: center; color: #999; font-size: 0.9em;'>"
    "© 2026 FitLife - Todos os direitos reservados"
    "</div>",
    unsafe_allow_html=True
)
