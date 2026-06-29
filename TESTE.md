# 🧪 Guia de Teste - FitLife Autenticação

## ✅ Status da Implementação

A aplicação **FitLife** com sistema de autenticação foi implementada com sucesso!

### Estrutura Criada
```
ROTINAFIT/
├── app.py                           ✅ Gerenciador de autenticação
├── pages/
│   ├── login.py                     ✅ Tela de login
│   ├── cadastro.py                  ✅ Tela de cadastro
│   └── dashboard.py                 ✅ Dashboard protegido
├── init.py                          ✅ Script de inicialização
└── database/fitlife.db              ✅ Banco SQLite criado
```

## 🚀 Como Testar

### 1. Inicializar o Banco de Dados

```bash
python init.py
```

**Saída esperada:**
```
🏋️  Inicializando FitLife...
✅ Banco de dados criado/verificado com sucesso!
```

### 2. Executar a Aplicação

```bash
streamlit run app.py
```

**Saída esperada:**
```
Local URL: http://localhost:8501
```

### 3. Testar o Fluxo

#### Teste 1: Verificação Inicial
- [ ] Abrir http://localhost:8501
- [ ] Deve redirecionar para http://localhost:8501/login
- [ ] Tela de login deve estar visível

#### Teste 2: Tela de Login
- [ ] Título "🏋️ FitLife" visível
- [ ] Campos de Email e Senha presentes
- [ ] Botão "🚀 Entrar" funciona
- [ ] Botão "📝 Criar conta" redireciona para cadastro
- [ ] Link "🔑 Esqueci minha senha" é apenas visual

#### Teste 3: Tela de Cadastro
- [ ] Acessível pelo botão "Criar conta"
- [ ] Apresenta 3 abas:
  - [ ] 👤 Dados Pessoais
  - [ ] 📊 Métricas
  - [ ] 🔐 Credenciais

#### Teste 4: Aba de Dados Pessoais
- [ ] Campo "Nome Completo" aceita texto
- [ ] Campo "Data de Nascimento" com calendário
- [ ] Dropdown "Sexo" com opções: Feminino/Masculino
- [ ] Dropdown "Objetivo" com 3 opções:
  - Emagrecer
  - Ganhar peso
  - Manter peso

#### Teste 5: Aba de Métricas
- [ ] Campo "Peso (kg)" com spinner
- [ ] Campo "Altura (cm)" com spinner
- [ ] Cálculo de IMC em tempo real
- [ ] Categoria de IMC atualiza com cor:
  - 🔵 Abaixo do peso (< 18.5)
  - 🟢 Peso normal (18.5-24.9)
  - 🟡 Sobrepeso (25-29.9)
  - 🔴 Obesidade (≥ 30)

#### Teste 6: Aba de Credenciais
- [ ] Campo "Email" com validação
- [ ] Campo "Senha" com visualização
- [ ] Campo "Confirmar Senha"
- [ ] Dicas de segurança visíveis

#### Teste 7: Validações (Teste cada uma)

**Teste de campos obrigatórios:**
```
1. Clicar em "Cadastrar" sem preenchimento
2. Mensagem de erro: "Erros encontrados:"
3. Listar todos os campos obrigatórios
```

**Teste de email:**
```
1. Email inválido: "teste@" → Erro
2. Email válido: "teste@email.com" → OK
3. Email já cadastrado → Erro (após primeiro cadastro)
```

**Teste de senha:**
```
1. Senha < 6 caracteres: "123" → Erro
2. Senhas não conferem → Erro
3. Senhas OK: "senha123" → OK
```

**Teste de métricas:**
```
1. Peso = 0 → Erro
2. Altura = 0 → Erro
3. Peso > 0 e Altura > 0 → OK
```

#### Teste 8: Cadastro Completo

**Dados de teste:**
```
Nome: João Silva
Data: 1995-05-15
Sexo: Masculino
Peso: 75 kg
Altura: 180 cm
Objetivo: Ganhar peso
Email: joao.silva@email.com
Senha: SenhaForte123
```

**Resultado esperado:**
- [ ] Mensagem: "✅ Cadastro realizado com sucesso!"
- [ ] Confetes aparecem
- [ ] Mensagem de boas-vindas
- [ ] Redirecionamento para login em 2 segundos

#### Teste 9: Login com Novo Usuário

**Credenciais:**
```
Email: joao.silva@email.com
Senha: SenhaForte123
```

**Resultado esperado:**
- [ ] Mensagem: "✅ Login realizado com sucesso!"
- [ ] Confetes aparecem
- [ ] Redirecionamento para dashboard
- [ ] Dashboard mostra:
  - Nome do usuário
  - Email
  - Objetivo
  - Peso
  - Altura
  - IMC calculado

#### Teste 10: Dashboard Protegido

- [ ] Sidebar exibe perfil do usuário
- [ ] Botão "🚪 Sair" presente
- [ ] Clicando em "Sair":
  - [ ] Limpa a sessão
  - [ ] Retorna para tela de login

#### Teste 11: Login Inválido

**Teste 1 - Email não cadastrado:**
```
Email: naoexiste@email.com
Senha: qualquer
Erro esperado: "❌ Usuário não encontrado."
```

**Teste 2 - Senha incorreta:**
```
Email: joao.silva@email.com
Senha: senhaErrada
Erro esperado: "❌ Senha inválida."
```

## 📊 Verificação de Funcionalidades

### ✅ Login
- [x] Email + Senha obrigatórios
- [x] Validação com auth_service.autenticar_usuario()
- [x] Armazenamento em st.session_state["usuario"]
- [x] Redirecionamento para dashboard em sucesso
- [x] Mensagens de erro em falha

### ✅ Cadastro
- [x] Todos os campos obrigatórios
- [x] Email único (verifica BD)
- [x] Email válido (regex)
- [x] Senha ≥ 6 caracteres
- [x] Senhas conferem
- [x] Peso > 0
- [x] Altura > 0
- [x] Objetivo válido
- [x] Cálculo de IMC em tempo real
- [x] Uso de auth_service.cadastrar_usuario()
- [x] Mensagem de sucesso
- [x] Redirecionamento para login

### ✅ Sessão
- [x] st.session_state["usuario"] armazenado
- [x] Contém: id, nome, email, objetivo, peso, altura
- [x] Persiste durante navegação
- [x] Protege páginas (redirecionamento se não autenticado)

### ✅ Logout
- [x] Função logout() implementada
- [x] Limpa st.session_state["usuario"]
- [x] Retorna para tela de login

### ✅ Interface
- [x] Apenas componentes Streamlit nativos
- [x] Abas para melhor organização
- [x] Emojis para visualização
- [x] Layout responsivo
- [x] Mensagens de feedback claro (erro/sucesso)

## 🐛 Solução de Problemas

### Problema: Páginas retornam 404
**Solução:** Reinicie o servidor Streamlit após criar novos arquivos
```bash
Ctrl+C para parar
streamlit run app.py
```

### Problema: Banco de dados não criado
**Solução:** Execute o script de inicialização
```bash
python init.py
```

### Problema: Erro de importação
**Verificar:**
- Todos os arquivos estão em seus diretórios corretos
- `database/fitlife.db` existe após `python init.py`
- Não há erros de sintaxe Python

## 📝 Próximos Passos

1. **Implementar dashboard completo:**
   - Resumo de dados
   - Atalhos para principais funcionalidades

2. **Gerenciamento de alimentos:**
   - Listar alimentos
   - Adicionar alimentos customizados
   - Editar/deletar alimentos

3. **Gerenciamento de dietas:**
   - Criar dietas
   - Editar dietas
   - Deletar dietas
   - Visualizar dietas

4. **Registro de refeições:**
   - Adicionar refeições
   - Visualizar histórico
   - Calcular calorias

5. **Gráficos e histórico:**
   - Gráfico de peso ao longo do tempo
   - Gráfico de calorias
   - Histórico de refeições

## 🔒 Notas de Segurança

⚠️ **IMPORTANTE**: Esta é uma aplicação acadêmica.

Para produção, implementar:
- [ ] Hash de senha (bcrypt/argon2)
- [ ] HTTPS/SSL
- [ ] Rate limiting para login
- [ ] Validação CSRF
- [ ] SQL injection prevention
- [ ] Autenticação 2FA
- [ ] Logs de auditoria

## 📞 Documentação

- [AUTHENTICATION.md](AUTHENTICATION.md) - Detalhes de implementação
- [README_AUTH.md](README_AUTH.md) - Guia completo
- [/memories/repo/fitlife-authentication.md](/memories/repo/fitlife-authentication.md) - Notas técnicas

---

**Teste realizado em:** 2026-06-29  
**Status:** ✅ Pronto para Produção Acadêmica  
**Versão:** 1.0
