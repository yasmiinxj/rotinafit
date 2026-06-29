# 🏋️ FitLife - Plataforma Integrada de Rotina Fitness

Projeto acadêmico de Engenharia de Software desenvolvido com **Python, Streamlit e SQLite**.

## 📋 Características

- ✅ **Sistema de Autenticação**: Login e cadastro de usuários
- ✅ **Perfil de Usuário**: Armazenamento de dados pessoais e métricas
- ✅ **Cálculo de IMC**: Visualização automática em tempo real
- ✅ **Interface Responsiva**: 100% Streamlit nativo
- 🔄 **Funcionalidades em desenvolvimento**: Dietas, refeições, alimentos e histórico

## 🚀 Como Começar

### 1. Pré-requisitos

- Python 3.8+
- pip ou conda

### 2. Instalação

```bash
# Clone ou baixe o projeto
cd ROTINAFIT

# Instale as dependências
pip install streamlit
```

### 3. Inicialização

```bash
# Execute o script de inicialização (cria o banco de dados)
python init.py
```

**Saída esperada:**
```
🏋️  Inicializando FitLife...
✅ Banco de dados criado/verificado com sucesso!

📝 Próximos passos:
1. Execute: streamlit run app.py
2. Abra http://localhost:8501 no navegador
3. Crie uma conta e faça login
```

### 4. Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá no navegador em `http://localhost:8501`

## 🔐 Sistema de Autenticação

### Fluxo de Login

```
[Tela de Login]
     ↓
  Email + Senha
     ↓
[Validar credenciais]
     ↓
Sucesso ✅ → [Dashboard]
Erro ❌ → [Mensagem de erro]
```

### Fluxo de Cadastro

```
[Tela de Cadastro]
     ↓
Preencher formulário em 3 abas
  • Dados Pessoais (nome, data, sexo, objetivo)
  • Métricas (peso, altura, IMC)
  • Credenciais (email, senha)
     ↓
[Validar dados]
     ↓
Sucesso ✅ → [Mensagem de sucesso] → [Login]
Erro ❌ → [Listar erros] → [Corrigir]
```

### Dados de Teste

Para testar a aplicação, crie uma conta:

**Exemplo de Cadastro:**
- Nome: João Silva
- Data: 1995-05-15
- Sexo: Masculino
- Peso: 75 kg
- Altura: 180 cm
- Objetivo: Ganhar peso
- Email: joao@email.com
- Senha: senha123

## 📁 Estrutura do Projeto

```
ROTINAFIT/
├── app.py                          # Arquivo principal
├── init.py                         # Script de inicialização
├── README.md                       # Este arquivo
├── AUTHENTICATION.md               # Documentação de autenticação
│
├── pages/                          # Páginas Streamlit
│   ├── login.py                    # Tela de login
│   ├── cadastro.py                 # Tela de cadastro
│   └── dashboard.py                # Dashboard principal
│
├── services/                       # Lógica de negócio
│   ├── auth_service.py             # Autenticação
│   ├── alimento_service.py         # Gerenciamento de alimentos
│   ├── dieta_service.py            # Gerenciamento de dietas
│   └── refeicao_service.py         # Gerenciamento de refeições
│
├── models/                         # Modelos de dados
│   ├── usuario.py                  # Modelo de usuário
│   ├── alimento.py                 # Modelo de alimento
│   ├── dieta.py                    # Modelo de dieta
│   ├── refeicao.py                 # Modelo de refeição
│   └── item_refeicao.py            # Modelo de item de refeição
│
└── database/                       # Banco de dados
    ├── database.py                 # Configuração SQLite
    └── fitlife.db                  # Arquivo SQLite (gerado)
```

## 🔑 Funcionalidades de Autenticação

### Login
- ✅ Email e senha obrigatórios
- ✅ Validação no backend com `auth_service.autenticar_usuario()`
- ✅ Armazenamento em `st.session_state["usuario"]`
- ✅ Redirecionamento automático para dashboard
- ✅ Link para criar conta
- ✅ Link "Esqueci minha senha" (visual)

### Cadastro
- ✅ Formulário em 3 abas para melhor UX
- ✅ Validação de campos obrigatórios
- ✅ Email único (verifica no banco)
- ✅ Email em formato válido
- ✅ Senha com confirmação (mínimo 6 caracteres)
- ✅ Cálculo de IMC em tempo real
- ✅ Objetivo limitado a: emagrecer, ganhar peso, manter peso
- ✅ Mensagem de sucesso com redirecionamento

### Sessão do Usuário
```python
st.session_state["usuario"] = {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com",
    "objetivo": "ganhar peso",
    "peso": 75.0,
    "altura": 180.0
}
```

### Logout
- ✅ Botão no sidebar do dashboard
- ✅ Limpa `st.session_state["usuario"]`
- ✅ Retorna para tela de login

## 🎨 Interface

A aplicação utiliza **apenas componentes nativos do Streamlit**:

- `st.form()` - Formulários de login e cadastro
- `st.tabs()` - Organização em abas no cadastro
- `st.session_state` - Gerenciamento de sessão
- `st.switch_page()` - Navegação entre páginas
- `st.sidebar` - Painel lateral com perfil
- Emojis e markdown para melhor UX

## 📊 Sessão de Usuário

A sessão persiste durante toda a navegação:

```python
# Verificar se usuário está logado
if "usuario" in st.session_state and st.session_state["usuario"] is not None:
    usuario = st.session_state["usuario"]
    st.write(f"Bem-vindo, {usuario['nome']}!")
```

## 🚫 Proteção de Página

Todas as páginas autenticadas verificam se o usuário está logado:

```python
if "usuario" not in st.session_state or st.session_state["usuario"] is None:
    st.switch_page("pages/login.py")
```

## 🔍 Validações Implementadas

### Email
- Formato válido (regex): `usuario@dominio.com`
- Único no banco de dados
- Obrigatório

### Senha
- Mínimo 6 caracteres
- Confirmação obrigatória no cadastro
- Sem criptografia (TODO: implementar hash em produção)

### Métricas
- Peso > 0 kg
- Altura > 0 cm
- IMC calculado: peso / (altura em metros)²

### Objetivo
- Emagrecer
- Ganhar peso
- Manter peso

## 📝 Próximas Funcionalidades

- [ ] Dashboard completo com resumo
- [ ] Gerenciamento de alimentos
- [ ] Criação e edição de dietas
- [ ] Registro de refeições
- [ ] Histórico com gráficos
- [ ] Edição de perfil
- [ ] Recuperação de senha via email
- [ ] Temas (claro/escuro)
- [ ] Exportar dados

## 🔒 Notas de Segurança

⚠️ **IMPORTANTE**: Esta é uma aplicação acadêmica. Para produção:

1. **Hash de Senha**: Use `bcrypt` ou `argon2` em vez de armazenar em texto plano
2. **Validação**: Implementar CSRF, SQL injection prevention
3. **HTTPS**: Usar SSL/TLS em produção
4. **Database**: Migrar para PostgreSQL ou MySQL
5. **Autenticação 2FA**: Implementar autenticação de dois fatores
6. **Rate Limiting**: Proteção contra força bruta

## 📞 Suporte

Para dúvidas sobre a implementação, consulte:
- `AUTHENTICATION.md` - Documentação detalhada de autenticação
- `services/auth_service.py` - Funções de autenticação
- `models/usuario.py` - Modelo de usuário

## 📄 Licença

Projeto acadêmico - Engenharia de Software 2026

---

**Desenvolvido com ❤️ usando Python e Streamlit**
