# 🎯 Fluxo Completo do Sistema FitLife

## 📊 Mapa de Navegação

```
┌──────────────────────────────────────────────────────────────────┐
│                         FITLIFE FLUXO                            │
└──────────────────────────────────────────────────────────────────┘

                        Usuário não autenticado
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │     APP.PY             │
                    │ Verifica autenticação  │
                    └────────┬───────────────┘
                             │
                             ▼
                    ┌────────────────────────┐
                    │    PAGES/LOGIN.PY      │
                    │  • Email + Senha       │
                    │  • Validação           │
                    │  • Link criar conta    │
                    └────────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
            Já tem conta?        Criar conta?
                    │                 │
                   SIM                NÃO
                    │                 │
                    ▼                 ▼
            Login bem-sucedido   PAGES/CADASTRO.PY
            Armazena usuário      • Dados pessoais
            em session_state      • Métricas (IMC)
                    │             • Credenciais
                    │             (3 abas)
                    │                 │
                    │          Validar dados
                    │                 │
                    │            ✅ OK
                    │                 │
                    │          Salvar no BD
                    │                 │
                    └────────┬────────┘
                             │
                             ▼
                    ┌────────────────────────┐
                    │  PAGES/DASHBOARD.PY    │
                    │  • Cabeçalho           │
                    │  • Resumo do dia       │
                    │  • Menu principal      │
                    │  • Botão logout        │
                    └────────┬───────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   🍽️ ALIMENTAÇÃO     📋 DIETAS           🏃 TREINOS
   ✅ ATIVO           🚧 EM DEV.          🚧 EM DEV.
        │
        ▼
 PAGES/ALIMENTACAO.PY
 • Adicionar refeição
 • Visualizar refeições
 • Tabela de alimentos
        │
        └─────────────────────┐
                              │
                         ⬅️ Voltar
                              │
                              ▼
                    PAGES/DASHBOARD.PY
                              │
                         🚪 Logout
                              │
                              ▼
                    Limpa session_state
                              │
                              ▼
                    PAGES/LOGIN.PY
```

---

## 🔄 Fluxo de Autenticação Completo

### 1️⃣ **Sem Autenticação** → Login

```
app.py
  ↓
Verifica st.session_state["usuario"]
  ↓
❌ Não existe ou é None
  ↓
st.switch_page("pages/login.py")
```

### 2️⃣ **Login** → Dashboard

```
pages/login.py
  ↓
Preencher: Email + Senha
  ↓
Clicar "Entrar"
  ↓
auth_service.autenticar_usuario(email, senha)
  ↓
✅ Sucesso: Retorna Usuario
  ↓
st.session_state["usuario"] = {
    "id": ...,
    "nome": ...,
    "email": ...,
    "objetivo": ...,
    "peso": ...,
    "altura": ...
}
  ↓
st.switch_page("pages/dashboard.py")
```

### 3️⃣ **Cadastro** → Login

```
pages/cadastro.py (3 abas)
  ↓
Preencher formulário
  ↓
Clicar "Cadastrar"
  ↓
Validar todos os campos
  ↓
✅ OK: Chamar auth_service.cadastrar_usuario()
  ↓
Salvar no banco de dados
  ↓
Mensagem de sucesso
  ↓
Redirecionar para login em 2s
```

### 4️⃣ **Dashboard** → Alimentação

```
pages/dashboard.py
  ↓
Exibir menu com 4 opções:
  🍽️ Alimentação (ATIVO)
  📋 Dietas (Em dev.)
  🏃 Treinos (Em dev.)
  📏 Medidas (Em dev.)
  ↓
Clicar "🍽️ Alimentação"
  ↓
st.switch_page("pages/alimentacao.py")
```

### 5️⃣ **Alimentação** → Dashboard

```
pages/alimentacao.py
  ↓
Registrar refeições (3 abas)
  ↓
Clicar "⬅️ Voltar"
  ↓
st.switch_page("pages/dashboard.py")
  ↓
Dados de refeições persistem em session_state
```

### 6️⃣ **Logout** → Login

```
pages/dashboard.py
  ↓
Clicar "🚪 Sair"
  ↓
logout()
  ↓
st.session_state["usuario"] = None
  ↓
st.switch_page("pages/login.py")
```

---

## 📁 Estrutura de Arquivos

```
ROTINAFIT/
│
├── app.py                          [Gerenciador de autenticação]
│   ├─ Inicializa session_state
│   ├─ Verifica autenticação
│   └─ Redireciona para login ou dashboard
│
├── pages/                          [Páginas Streamlit]
│   ├── login.py                    [Tela de login]
│   │   ├─ Formulário email + senha
│   │   ├─ auth_service.autenticar_usuario()
│   │   ├─ Armazena em session_state
│   │   └─ Link para cadastro
│   │
│   ├── cadastro.py                 [Tela de cadastro]
│   │   ├─ Aba 1: Dados pessoais
│   │   ├─ Aba 2: Métricas
│   │   ├─ Aba 3: Credenciais
│   │   ├─ Validações completas
│   │   └─ auth_service.cadastrar_usuario()
│   │
│   ├── dashboard.py                [Dashboard principal]
│   │   ├─ Cabeçalho com usuário
│   │   ├─ Resumo do dia (calorias)
│   │   ├─ Feedback motivacional
│   │   ├─ Menu principal
│   │   └─ Botão logout
│   │
│   └── alimentacao.py              [Página de alimentação]
│       ├─ Aba 1: Adicionar refeição
│       ├─ Aba 2: Minhas refeições
│       ├─ Aba 3: Tabela de alimentos
│       └─ Botão voltar para dashboard
│
├── services/                       [Lógica de negócio]
│   ├── auth_service.py             [Autenticação]
│   │   ├─ autenticar_usuario()
│   │   ├─ cadastrar_usuario()
│   │   └─ buscar_usuario()
│   │
│   ├── alimento_service.py
│   ├── dieta_service.py
│   └── refeicao_service.py
│
├── models/                         [Modelos de dados]
│   └── usuario.py
│
└── database/                       [Banco de dados]
    ├── database.py
    └── fitlife.db
```

---

## 🎯 Session State Structure

```python
# Usuário autenticado
st.session_state = {
    "usuario": {
        "id": 1,
        "nome": "Maria Silva",
        "email": "maria@email.com",
        "objetivo": "emagrecer",
        "peso": 65.0,
        "altura": 168.0
    },
    "pagina_ativa": "dashboard",  # dashboard, alimentacao, dietas, treinos, medidas
    "refeicoes_hoje": [
        {
            "tipo": "Almoço",
            "data": "2026-06-29",
            "horario": "12:30:00",
            "calorias": 750.0,
            "descricao": "Frango com arroz"
        }
    ]
}

# Usuário não autenticado
st.session_state = {
    "usuario": None,
    "pagina_ativa": "dashboard",
    "refeicoes_hoje": []
}
```

---

## 🔐 Proteção de Acesso

### ✅ Páginas Protegidas
```python
# Em cada página (dashboard, alimentacao, etc)
if "usuario" not in st.session_state or st.session_state["usuario"] is None:
    st.switch_page("pages/login.py")
```

### ✅ Páginas Públicas
```
login.py    → Sem proteção (acessível a todos)
cadastro.py → Sem proteção (acessível a todos)
```

---

## 📊 Ciclo de Vida da Sessão

```
┌────────────────────────────────────┐
│   1. INICIALIZAÇÃO (app.py)        │
│   ├─ session_state["usuario"] = None
│   └─ Redireciona para login.py
└────────────┬───────────────────────┘
             │
┌────────────▼───────────────────────┐
│   2. LOGIN (pages/login.py)        │
│   ├─ Email + Senha inseridos       │
│   ├─ auth_service.autenticar()    │
│   └─ session_state["usuario"] armazenado
└────────────┬───────────────────────┘
             │
┌────────────▼───────────────────────┐
│   3. DASHBOARD (pages/dashboard.py)│
│   ├─ Mostra dados do usuário       │
│   ├─ Navega para alimentacao       │
│   └─ Ou clica logout
└────────────┬───────────────────────┘
             │
        ┌────┴─────────┐
        │              │
    ALIMENTACAO    LOGOUT
        │              │
        │        ┌─────▼─────────────┐
        │        │ 4. LOGOUT         │
        └─────┬──┤ session_state = None
             │  └──────────────────┘
             │
        ┌────▼──────────────────────┐
        │ 5. VOLTA PARA LOGIN       │
        └──────────────────────────┘
```

---

## 🧪 Teste do Fluxo Completo

### Cenário 1: Novo Usuário
```
1. Abrir http://localhost:8501
2. ✅ Redireciona para login
3. Clicar "Criar conta"
4. ✅ Vai para cadastro.py
5. Preencher formulário (3 abas)
6. Clicar "Cadastrar"
7. ✅ Mensagem de sucesso
8. ✅ Redireciona para login em 2s
9. ✅ Pode fazer login com novo usuário
```

### Cenário 2: Usuário Existente
```
1. Abrir http://localhost:8501
2. ✅ Redireciona para login
3. Inserir email e senha válidos
4. Clicar "Entrar"
5. ✅ Login bem-sucedido
6. ✅ Redireciona para dashboard
7. ✅ Mostra dados do usuário
```

### Cenário 3: Navegação Alimentação
```
1. Estar no dashboard
2. Clicar "🍽️ Alimentação"
3. ✅ Vai para alimentacao.py
4. Adicionar refeição
5. ✅ Refeição listada em "Minhas Refeições"
6. Clicar "⬅️ Voltar"
7. ✅ Retorna ao dashboard
8. ✅ Resumo atualizado com refeição registrada
```

### Cenário 4: Logout
```
1. Estar no dashboard
2. Clicar "🚪 Sair"
3. ✅ Redireciona para login
4. ✅ Session foi limpa
5. ✅ Pode fazer novo login
```

---

## 💡 Pontos-Chave

### ✅ Session State
- Persiste dados durante navegação
- Limpo ao fazer logout
- Inicializado em app.py

### ✅ Proteção de Acesso
- Cada página protegida verifica autenticação
- Redirecionamento automático se não autenticado
- Botões "Voltar" e "Logout" gerenciam navegação

### ✅ Navegação
- Uso de `st.switch_page()` para trocar página
- `st.session_state["pagina_ativa"]` para controlar estado
- Sem recarga desnecessária

### ✅ Dados
- Usuário: armazenado em `session_state["usuario"]`
- Refeições: armazenadas em `session_state["refeicoes_hoje"]`
- Futuramente: persistidos no banco de dados

---

## 🚀 Próximos Passos

### Fase 2: Persistência
- [ ] Salvar refeições no banco de dados
- [ ] Histórico de refeições por data
- [ ] Cálculo de meta baseado em perfil

### Fase 3: Outras Páginas
- [ ] Implementar páginas/dietas.py
- [ ] Implementar páginas/treinos.py
- [ ] Implementar páginas/medidas.py

### Fase 4: Avançado
- [ ] Gráficos de progresso
- [ ] Recomendações personalizadas
- [ ] Notificações
- [ ] Integração com APIs

---

## 📝 Resumo Visual

```
                LOGIN
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
CADASTRO       ENTRAR        RECUPERAR
    │             │          (Futuro)
    │         ┌───┴───┐
    │         │       │
    └─────────┤  ✅   ├─────────┐
              └───┬───┘         │
                  │             │
              DASHBOARD    (Pendente)
                  │
                  ├─ 🍽️ ALIMENTACAO
                  ├─ 📋 DIETAS (Dev.)
                  ├─ 🏃 TREINOS (Dev.)
                  ├─ 📏 MEDIDAS (Dev.)
                  └─ 🚪 LOGOUT
```

---

**Data:** 29/06/2026  
**Versão:** 2.0  
**Status:** ✅ Dashboard + Alimentação Implementados
