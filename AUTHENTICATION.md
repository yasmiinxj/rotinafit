# 🏋️ FitLife - Sistema de Autenticação

## Estrutura Implementada

```
ROTINAFIT/
├── app.py (principal - gerencia autenticação)
├── pages/
│   ├── login.py (tela de login)
│   ├── cadastro.py (tela de cadastro)
│   └── dashboard.py (dashboard principal)
├── services/
│   └── auth_service.py (funções de autenticação)
├── models/
│   └── usuario.py (modelo de usuário)
└── database/
    └── database.py (conexão SQLite)
```

## Fluxo de Autenticação

```
app.py
  ↓
[Usuário autenticado?]
  ├─ SIM  → dashboard.py
  └─ NÃO  → login.py
              ├─ Login bem-sucedido → dashboard.py
              ├─ Criar conta → cadastro.py
              │                ├─ Cadastro bem-sucedido → login.py
              │                └─ Erro → Permanecer em cadastro.py
              └─ Esqueci senha → (Funcionalidade futura)
```

## Sessão do Usuário

Armazenada em `st.session_state["usuario"]`:
```python
{
    "id": int,
    "nome": str,
    "email": str,
    "objetivo": str,  # "emagrecer", "ganhar peso", "manter peso"
    "peso": float,
    "altura": float
}
```

## Funcionalidades Implementadas

### ✅ Tela de Login (`pages/login.py`)
- [x] Logo e título "FitLife"
- [x] Texto de boas-vindas
- [x] Campo Email
- [x] Campo Senha
- [x] Botão "Entrar"
- [x] Link "Criar conta"
- [x] Link "Esqueci minha senha" (visual)
- [x] Validação de credenciais com `auth_service.autenticar_usuario()`
- [x] Armazenamento em `st.session_state["usuario"]`
- [x] Redirecionamento para dashboard em sucesso
- [x] Mensagens de erro em falha

### ✅ Tela de Cadastro (`pages/cadastro.py`)
- [x] Nome completo
- [x] Data de nascimento
- [x] Sexo (Feminino/Masculino)
- [x] Peso e Altura
- [x] Objetivo (Emagrecer/Ganhar peso/Manter peso)
- [x] Email
- [x] Senha e Confirmação
- [x] Abas com organização por seção
- [x] Validações:
  - [x] Campos obrigatórios
  - [x] Email único (via BD)
  - [x] Email válido (regex)
  - [x] Senha mínimo 6 caracteres
  - [x] Senhas coincidentes
  - [x] Peso > 0
  - [x] Altura > 0
- [x] Cálculo de IMC em tempo real
- [x] Uso de `auth_service.cadastrar_usuario()`
- [x] Mensagem de sucesso
- [x] Redirecionamento para login após cadastro

### ✅ Dashboard (`pages/dashboard.py`)
- [x] Sidebar com informações do usuário
- [x] Função logout() que limpa sessão
- [x] Proteção de acesso (redirecionamento se não autenticado)
- [x] Placeholder para funcionalidades futuras

### ✅ App Principal (`app.py`)
- [x] Verificação de autenticação
- [x] Redirecionamento automático
- [x] Gerenciamento de sessão inicial

### ✅ Funções de Autenticação (`services/auth_service.py`)
- [x] `autenticar_usuario()` - login com validação
- [x] `cadastrar_usuario()` - registro com validações
- [x] `buscar_usuario()` - busca por ID

## Como Executar

1. **Instalar dependências:**
   ```bash
   pip install streamlit
   ```

2. **Criar banco de dados:**
   ```python
   from database.database import criar_banco
   criar_banco()
   ```

3. **Executar a aplicação:**
   ```bash
   streamlit run app.py
   ```

## Validações Implementadas

### Login
- Email e senha obrigatórios
- Email deve existir no BD
- Senha deve estar correta

### Cadastro
- Todos os campos obrigatórios
- Email único no BD
- Email em formato válido
- Senha com mínimo 6 caracteres
- Senhas coincidentes
- Peso > 0
- Altura > 0
- Objetivo em lista permitida

## Interfaces e UX

- Interface simples e responsiva
- Apenas componentes nativos do Streamlit
- Emojis para melhor visualização
- Abas no cadastro para organização
- Mensagens de erro claras
- Feedback visual (sucesso/erro)
- Layout centrado para login/cadastro
- Sidebar para dashboard

## Próximos Passos (Não Implementados)

- [ ] Dashboard completo
- [ ] Gerenciamento de alimentação
- [ ] Gerenciamento de dietas
- [ ] Histórico de refeições
- [ ] Gráficos de progresso
- [ ] Recuperação de senha
- [ ] Edição de perfil
- [ ] Notificações
- [ ] Temas escuro/claro

## Notas Importantes

1. **Session State**: Persiste durante a sessão do Streamlit. Ao recarregar a página, a sessão é mantida.
2. **Segurança**: Implementar hash de senha em produção (bcrypt, argon2).
3. **Database**: SQLite local, ideal para desenvolvimento. Para produção, considerar PostgreSQL/MySQL.
4. **Redirecionamento**: Usa `st.switch_page()` do Streamlit para navegação entre páginas.
