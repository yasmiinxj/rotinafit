"""
Página de Alimentação - Gerenciamento de refeições e consumo nutricional
Histórias de usuário: EU2, EU3, EU4, EU7
"""

import streamlit as st
from datetime import datetime, timedelta
from services.nutrition_api import nutrition_api

# Configuração da página
st.set_page_config(
    page_title="🍽️ Alimentação - FitLife",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# RN01: Verificar autenticação
if "usuario" not in st.session_state or st.session_state["usuario"] is None:
    st.switch_page("pages/login.py")

# Inicializar session state
if "refeicoes_hoje" not in st.session_state:
    st.session_state["refeicoes_hoje"] = {}

# Corrige versões antigas que salvaram como lista
if isinstance(st.session_state["refeicoes_hoje"], list):
    st.session_state["refeicoes_hoje"] = {}

if "historico_alimentar" not in st.session_state:
    st.session_state["historico_alimentar"] = []

if "data_selecionada" not in st.session_state:
    st.session_state["data_selecionada"] = datetime.now().date()

# ============================================================================
# CABEÇALHO
# ============================================================================

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Voltar", use_container_width=True):
        st.switch_page("pages/dashboard.py")

with col2:
    st.title("🍽️ Alimentação")

with col3:
    if st.button("📋 Minhas Dietas", use_container_width=True):
        st.info("📋 Funcionalidade em desenvolvimento")

st.divider()

# Informações do usuário
usuario = st.session_state["usuario"]
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"👋 {usuario['nome']}")
with col2:
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
with col3:
    st.caption(f"⏰ {datetime.now().strftime('%H:%M')}")

st.divider()

# ============================================================================
# SELETOR DE DATA
# ============================================================================

data_selecionada = st.date_input(
    "📅 Selecionar data",
    value=st.session_state["data_selecionada"],
    key="data_alimentacao",
)

if data_selecionada != st.session_state["data_selecionada"]:
    st.session_state["data_selecionada"] = data_selecionada

# ============================================================================
# RESUMO DO DIA
# ============================================================================

st.subheader("📊 Resumo do Dia")

# Calcular totais do dia
refeicoes_dia = st.session_state["refeicoes_hoje"].get(str(data_selecionada), {})

# Função auxiliar para somar nutrientes
def calcular_totais_dia(refeicoes_dict):
    totais = {
        "calorias": 0,
        "proteinas": 0,
        "carboidratos": 0,
        "gorduras": 0,
        "fibras": 0,
    }

    for refeicao_tipo, alimentos in refeicoes_dict.items():
        if isinstance(alimentos, list):
            for alimento in alimentos:
                totais["calorias"] += alimento.get("calorias", 0)
                totais["proteinas"] += alimento.get("proteinas", 0)
                totais["carboidratos"] += alimento.get("carboidratos", 0)
                totais["gorduras"] += alimento.get("gorduras", 0)
                totais["fibras"] += alimento.get("fibras", 0)

    return totais


totais_dia = calcular_totais_dia(refeicoes_dia)

# Meta de calorias (pode vir de perfil do usuário - usamos 2000 como padrão)
meta_calorias = 2000

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🎯 Meta", f"{meta_calorias} kcal")

with col2:
    st.metric("🔥 Consumido", f"{totais_dia['calorias']:.0f} kcal")

with col3:
    percentual = (totais_dia["calorias"] / meta_calorias * 100) if meta_calorias > 0 else 0
    st.metric("📈 Progresso", f"{percentual:.1f}%")

with col4:
    st.metric("💪 Proteína", f"{totais_dia['proteinas']:.1f}g")

with col5:
    st.metric("🌾 Carbos", f"{totais_dia['carboidratos']:.1f}g")

# Macros em colunas
col1, col2 = st.columns(2)

with col1:
    st.metric("🥑 Gorduras", f"{totais_dia['gorduras']:.1f}g")

with col2:
    st.metric("🌱 Fibras", f"{totais_dia['fibras']:.1f}g")

st.divider()

# ============================================================================
# ABAS PRINCIPAIS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(
    ["🔍 Pesquisar Alimentos", "📝 Minhas Refeições", "📊 Histórico", "ℹ️ Info Nutricionais"]
)

# ============================================================================
# ABA 1: PESQUISAR ALIMENTOS
# ============================================================================

with tab1:
    st.subheader("🔍 Pesquisar Alimento")

    col1, col2 = st.columns([3, 1])

    with col1:
        busca = st.text_input(
            "Digite o nome do alimento",
            placeholder="Ex: Frango, Maçã, Arroz...",
            key="busca_alimento",
        )

    with col2:
        if st.button("🔎 Buscar", use_container_width=True):
            st.session_state["pesquisa_ativa"] = True

    if st.session_state.get("pesquisa_ativa") and busca:
        with st.spinner("🔄 Buscando alimentos..."):
            alimentos = nutrition_api.buscar_alimentos(busca)

        if alimentos:
            st.success(f"✅ {len(alimentos)} alimentos encontrados")

            # Exibir alimentos em cards
            for idx, alimento in enumerate(alimentos):
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**{alimento['nome']}**")
                        if alimento.get("marca"):
                            st.caption(f"Marca: {alimento['marca']}")

                        # Nutrientes por 100g
                        col_a, col_b, col_c, col_d, col_e = st.columns(5)
                        with col_a:
                            st.caption(f"🔥 {alimento['calorias']:.0f} kcal")
                        with col_b:
                            st.caption(f"💪 {alimento['proteinas']:.1f}g prot")
                        with col_c:
                            st.caption(f"🌾 {alimento['carboidratos']:.1f}g carb")
                        with col_d:
                            st.caption(f"🥑 {alimento['gorduras']:.1f}g gord")
                        with col_e:
                            st.caption(f"🌱 {alimento['fibras']:.1f}g fib")

                    with col2:
                        if st.button("✅ Selecionar", key=f"sel_{idx}", use_container_width=True):
                            st.session_state["alimento_selecionado"] = alimento
                            st.session_state["pesquisa_ativa"] = False
                            st.rerun()

            st.divider()

        else:
            st.warning("❌ Nenhum alimento encontrado. Tente outro nome.")

    # Se alimento selecionado, mostrar formulário de adição
    if st.session_state.get("alimento_selecionado"):
        alimento_selecionado = st.session_state["alimento_selecionado"]

        st.subheader(f"➕ Adicionar: {alimento_selecionado['nome']}")

        with st.form("form_adicionar_refeicao"):
            col1, col2 = st.columns(2)

            with col1:
                tipo_refeicao = st.selectbox(
                    "🍽️ Tipo de Refeição",
                    ["Café da manhã", "Almoço", "Jantar", "Lanche"],
                    key="tipo_refeicao",
                )

            with col2:
                quantidade = st.number_input(
                    "📏 Quantidade (g)",
                    min_value=1,
                    max_value=1000,
                    value=100,
                    step=10,
                    key="quantidade",
                )

            # RN03: Validar quantidade
            if quantidade <= 0:
                st.error("⚠️ Quantidade deve ser maior que zero")

            # Calcular nutrientes
            nutrientes = nutrition_api.obter_nutrientes(alimento_selecionado, quantidade)

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("🔥", f"{nutrientes['calorias']:.0f} kcal")
            with col2:
                st.metric("💪", f"{nutrientes['proteinas']:.1f}g")
            with col3:
                st.metric("🌾", f"{nutrientes['carboidratos']:.1f}g")
            with col4:
                st.metric("🥑", f"{nutrientes['gorduras']:.1f}g")
            with col5:
                st.metric("🌱", f"{nutrientes['fibras']:.1f}g")

            if st.form_submit_button("✅ Adicionar à Refeição", use_container_width=True):
                # RN04: Registrar alimento consumido
                data_str = str(data_selecionada)

                if data_str not in st.session_state["refeicoes_hoje"]:
                    st.session_state["refeicoes_hoje"][data_str] = {}

                if tipo_refeicao not in st.session_state["refeicoes_hoje"][data_str]:
                    st.session_state["refeicoes_hoje"][data_str][tipo_refeicao] = []

                # Criar registro do alimento
                registro = {
                    "id": len(st.session_state["refeicoes_hoje"][data_str][tipo_refeicao]),
                    "nome": alimento_selecionado["nome"],
                    "marca": alimento_selecionado.get("marca", ""),
                    "quantidade": quantidade,
                    "calorias": nutrientes["calorias"],
                    "proteinas": nutrientes["proteinas"],
                    "carboidratos": nutrientes["carboidratos"],
                    "gorduras": nutrientes["gorduras"],
                    "fibras": nutrientes["fibras"],
                    "horario": datetime.now().strftime("%H:%M"),
                }

                st.session_state["refeicoes_hoje"][data_str][tipo_refeicao].append(
                    registro
                )

                # RN06: Adicionar ao histórico
                st.session_state["historico_alimentar"].append(
                    {
                        "data": data_selecionada,
                        "refeicao_tipo": tipo_refeicao,
                        **registro,
                    }
                )

                st.success("✅ Alimento adicionado com sucesso!")
                st.session_state["alimento_selecionado"] = None
                st.rerun()

# ============================================================================
# ABA 2: MINHAS REFEIÇÕES
# ============================================================================

with tab2:
    st.subheader("📝 Minhas Refeições")

    if not refeicoes_dia:
        st.info("ℹ️ Nenhuma refeição registrada para este dia.")
    else:
        # Ícones e nomes de refeições
        tipos_refeicao = {
            "Café da manhã": "☀️",
            "Almoço": "🍛",
            "Jantar": "🌙",
            "Lanche": "🍎",
        }

        for tipo, emoji in tipos_refeicao.items():
            if tipo in refeicoes_dia and refeicoes_dia[tipo]:
                st.subheader(f"{emoji} {tipo}")

                alimentos_tipo = refeicoes_dia[tipo]

                # Calcular totais por refeição
                totais_refeicao = {
                    "calorias": sum(a.get("calorias", 0) for a in alimentos_tipo),
                    "proteinas": sum(a.get("proteinas", 0) for a in alimentos_tipo),
                    "carboidratos": sum(a.get("carboidratos", 0) for a in alimentos_tipo),
                    "gorduras": sum(a.get("gorduras", 0) for a in alimentos_tipo),
                    "fibras": sum(a.get("fibras", 0) for a in alimentos_tipo),
                }

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🔥", f"{totais_refeicao['calorias']:.0f} kcal")
                with col2:
                    st.metric("💪", f"{totais_refeicao['proteinas']:.1f}g")
                with col3:
                    st.metric("🌾", f"{totais_refeicao['carboidratos']:.1f}g")
                with col4:
                    st.metric("🥑", f"{totais_refeicao['gorduras']:.1f}g")

                # Listar alimentos
                for idx, alimento in enumerate(alimentos_tipo):
                    with st.container(border=True):
                        col1, col2 = st.columns([4, 1])

                        with col1:
                            st.write(f"**{alimento['nome']}**")
                            col_info1, col_info2, col_info3 = st.columns(3)
                            with col_info1:
                                st.caption(f"📏 {alimento['quantidade']}g")
                            with col_info2:
                                st.caption(f"🔥 {alimento['calorias']:.0f} kcal")
                            with col_info3:
                                st.caption(f"⏰ {alimento['horario']}")

                        with col2:
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                if st.button(
                                    "👁️",
                                    key=f"viz_{tipo}_{idx}",
                                    help="Visualizar detalhes",
                                    use_container_width=True,
                                ):
                                    st.session_state["alimento_vizualizar"] = alimento

                            with col_btn2:
                                if st.button(
                                    "🗑️",
                                    key=f"del_{tipo}_{idx}",
                                    help="Remover",
                                    use_container_width=True,
                                ):
                                    st.session_state["refeicoes_hoje"][str(data_selecionada)][
                                        tipo
                                    ].pop(idx)
                                    st.success("✅ Alimento removido!")
                                    st.rerun()

                st.divider()

# ============================================================================
# ABA 3: HISTÓRICO ALIMENTAR
# ============================================================================

with tab3:
    st.subheader("📊 Histórico Alimentar")

    if not st.session_state["historico_alimentar"]:
        st.info("ℹ️ Nenhum histórico registrado.")
    else:
        # Filtrar por data
        col1, col2 = st.columns(2)

        with col1:
            data_inicio = st.date_input("📅 Data Início")

        with col2:
            data_fim = st.date_input("📅 Data Fim")

        # Filtrar histórico
        historico_filtrado = [
            h
            for h in st.session_state["historico_alimentar"]
            if data_inicio <= h["data"] <= data_fim
        ]

        if historico_filtrado:
            # Exibir em dataframe
            dados_historico = []
            for h in historico_filtrado:
                dados_historico.append(
                    {
                        "📅 Data": h["data"],
                        "🍽️ Refeição": h["refeicao_tipo"],
                        "🍖 Alimento": h["nome"],
                        "📏 Qtd (g)": h["quantidade"],
                        "🔥 Kcal": h["calorias"],
                        "💪 Prot": h["proteinas"],
                        "🌾 Carb": h["carboidratos"],
                        "🥑 Gord": h["gorduras"],
                        "🌱 Fib": h["fibras"],
                    }
                )

            st.dataframe(dados_historico, use_container_width=True, hide_index=True)

            # Totais do período
            st.subheader("📊 Totais do Período")

            totais_periodo = {
                "calorias": sum(h["calorias"] for h in historico_filtrado),
                "proteinas": sum(h["proteinas"] for h in historico_filtrado),
                "carboidratos": sum(h["carboidratos"] for h in historico_filtrado),
                "gorduras": sum(h["gorduras"] for h in historico_filtrado),
                "fibras": sum(h["fibras"] for h in historico_filtrado),
            }

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("🔥 Kcal Total", f"{totais_periodo['calorias']:.0f}")
            with col2:
                st.metric("💪 Proteína", f"{totais_periodo['proteinas']:.1f}g")
            with col3:
                st.metric("🌾 Carbos", f"{totais_periodo['carboidratos']:.1f}g")
            with col4:
                st.metric("🥑 Gorduras", f"{totais_periodo['gorduras']:.1f}g")
            with col5:
                st.metric("🌱 Fibras", f"{totais_periodo['fibras']:.1f}g")

        else:
            st.warning("❌ Nenhum registro no período selecionado.")

# ============================================================================
# ABA 4: INFORMAÇÕES NUTRICIONAIS
# ============================================================================

with tab4:
    st.subheader("ℹ️ Visualizar Alimento")

    if st.session_state.get("alimento_vizualizar"):
        alimento = st.session_state["alimento_vizualizar"]

        with st.container(border=True):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.title(alimento["nome"])
                if alimento.get("marca"):
                    st.write(f"**Marca:** {alimento['marca']}")

            with col2:
                if st.button("❌ Fechar", use_container_width=True):
                    st.session_state["alimento_vizualizar"] = None
                    st.rerun()

            st.divider()

            # Tabela nutricional
            st.write("**Informação Nutricional (por 100g)**")

            tabela = {
                "Nutriente": [
                    "Calorias",
                    "Proteínas",
                    "Carboidratos",
                    "Gorduras",
                    "Fibras",
                ],
                "Quantidade": [
                    f"{alimento['calorias']:.0f} kcal",
                    f"{alimento['proteinas']:.1f}g",
                    f"{alimento['carboidratos']:.1f}g",
                    f"{alimento['gorduras']:.1f}g",
                    f"{alimento['fibras']:.1f}g",
                ],
            }

            st.dataframe(
                tabela,
                use_container_width=True,
                hide_index=True,
            )

    else:
        st.info("ℹ️ Selecione um alimento para visualizar detalhes.")

st.divider()

# Rodapé
st.caption("© 2026 FitLife - Gerenciador de Fitness")
