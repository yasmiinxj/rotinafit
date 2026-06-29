import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Dashboard - FitLife",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Verificar se usuário está autenticado
if "usuario" not in st.session_state or st.session_state["usuario"] is None:
    st.switch_page("pages/login.py")

# Inicializar session state para navegação
if "pagina_ativa" not in st.session_state:
    st.session_state["pagina_ativa"] = "dashboard"

# Inicializar dados de refeições (placeholder para futura integração com BD)
if "refeicoes_hoje" not in st.session_state:
    st.session_state["refeicoes_hoje"] = {}

# Função de logout
def logout():
    """Limpa a sessão do usuário e retorna ao login."""
    st.session_state["usuario"] = None
    st.session_state["pagina_ativa"] = "dashboard"
    st.switch_page("pages/login.py")

def definir_pagina(pagina):
    """Define a página ativa"""
    st.session_state["pagina_ativa"] = pagina

# Obter dados do usuário
usuario = st.session_state["usuario"]

# ============================================================================
# CABEÇALHO
# ============================================================================

col_logo, col_info, col_logout = st.columns([2, 3, 1])

with col_logo:
    st.markdown("## 🏋️ FitLife")

with col_info:
    st.markdown(f"### 👋 Bem-vindo, **{usuario['nome']}**")
    col_obj, col_email = st.columns(2)
    with col_obj:
        objetivo_map = {
            "emagrecer": "🔻 Emagrecer",
            "ganhar peso": "📈 Ganhar Peso",
            "manter peso": "➡️ Manter Peso"
        }
        st.markdown(f"**Objetivo:** {objetivo_map.get(usuario['objetivo'], usuario['objetivo'])}")
    with col_email:
        st.markdown(f"**Email:** {usuario['email']}")

with col_logout:
    if st.button("🚪 Sair", use_container_width=True, type="secondary"):
        logout()

st.divider()

# ============================================================================
# ÁREA DE RESUMO - CALORIAS E REFEIÇÕES
# ============================================================================

st.markdown("### 📊 Resumo do Dia")

# Calcular valores (dados de exemplo, futuramente virão do BD)
meta_calorias = 2000  # Valor padrão (futuramente será calculado baseado em objetivo/peso/altura)
calorias_consumidas = 0  # Será atualizado com registros de refeições
from datetime import datetime

hoje = str(datetime.now().date())

if hoje in st.session_state["refeicoes_hoje"]:
    num_refeicoes = sum(
        len(alimentos)
        for alimentos in st.session_state["refeicoes_hoje"][hoje].values()
    )
else:
    num_refeicoes = 0

# Calcular percentual
if meta_calorias > 0:
    percentual = (calorias_consumidas / meta_calorias) * 100
else:
    percentual = 0

# Criar cards com métricas
col_meta, col_consumidas, col_percentual, col_refeicoes = st.columns(4)

with col_meta:
    st.metric(
        label="🎯 Meta de Calorias",
        value=f"{meta_calorias} kcal",
        delta="Diária"
    )

with col_consumidas:
    st.metric(
        label="🍽️ Calorias Consumidas",
        value=f"{calorias_consumidas} kcal",
        delta=f"{percentual:.1f}% da meta"
    )

with col_percentual:
    st.metric(
        label="📈 Progresso",
        value=f"{percentual:.1f}%",
        delta="Hoje"
    )

with col_refeicoes:
    st.metric(
        label="🥗 Refeições",
        value=num_refeicoes,
        delta="Registradas hoje"
    )

st.divider()

# ============================================================================
# ÁREA DE FEEDBACK
# ============================================================================

st.markdown("### 💬 Feedback Motivacional")

if num_refeicoes == 0:
    st.info(
        "ℹ️ **Você ainda não registrou refeições hoje.**\n\n"
        "Comece agora para acompanhar sua alimentação e atingir suas metas!",
        icon="🎯"
    )
elif percentual < 50:
    st.info(
        "ℹ️ **Você está começando bem!**\n\n"
        "Você já registrou algumas refeições. Continue assim para atingir sua meta diária.",
        icon="💪"
    )
elif percentual < 100:
    st.success(
        "✅ **Excelente! Você está acompanhando sua alimentação.**\n\n"
        "Continue registrando para atingir sua meta de calorias!",
        icon="🌟"
    )
else:
    st.success(
        "🎉 **Parabéns! Você atingiu sua meta diária!**\n\n"
        "Continue assim para manter seu objetivo em dia.",
        icon="🏆"
    )

st.divider()

# ============================================================================
# MENU PRINCIPAL
# ============================================================================

st.markdown("### 🗂️ Menu Principal")

col1, col2, col3, col4 = st.columns(4)

# Botão Alimentação (ativo)
with col1:
    if st.button(
        "🍽️ Alimentação",
        use_container_width=True,
        key="btn_alimentacao",
        type="primary"
    ):
        st.switch_page("pages/alimentacao.py")

# Botão Dietas (em desenvolvimento)
with col2:
    if st.button(
        "📋 Dietas",
        use_container_width=True,
        key="btn_dietas",
        type="primary" if st.session_state["pagina_ativa"] == "dietas" else "secondary"
    ):
        definir_pagina("dietas")

# Botão Treinos (em desenvolvimento)
with col3:
    if st.button(
        "🏃 Treinos",
        use_container_width=True,
        key="btn_treinos",
        type="primary" if st.session_state["pagina_ativa"] == "treinos" else "secondary"
    ):
        definir_pagina("treinos")

# Botão Medidas (em desenvolvimento)
with col4:
    if st.button(
        "📏 Medidas",
        use_container_width=True,
        key="btn_medidas",
        type="primary" if st.session_state["pagina_ativa"] == "medidas" else "secondary"
    ):
        definir_pagina("medidas")

st.divider()

# Rodapé
st.markdown(
    "<div style='text-align: center; color: #999; font-size: 0.9em; margin-top: 30px;'>"
    "© 2026 FitLife - Todos os direitos reservados"
    "</div>",
    unsafe_allow_html=True
)
