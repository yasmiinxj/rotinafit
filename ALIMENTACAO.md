# 🍽️ Página de Alimentação - Documentação

## ✅ O Que Foi Implementado

Página completa para gerenciamento de refeições com 3 abas principais.

---

## 📋 Estrutura da Página

### **Cabeçalho**
```
🍽️ Alimentação | 👋 [Nome do Usuário] | Data: [DD/MM/YYYY] | ⬅️ Voltar
```
- Título da página
- Nome do usuário
- Data de hoje
- Botão para voltar ao dashboard

### **Resumo do Dia**
```
┌─────────────────────────────────────────────────────┐
│ 🎯 Meta: 2000 kcal | 🍽️ Consumido: 0 kcal (0%) | 🥗 Refeições: 0
└─────────────────────────────────────────────────────┘
```
- Meta diária (padrão 2000 kcal)
- Total de calorias consumidas
- Percentual da meta atingido
- Número de refeições registradas

---

## 🗂️ Três Abas Principais

### **Aba 1: ➕ Adicionar Refeição**

#### Formulário com campos:
```
Tipo de Refeição: [Dropdown]
  - Café da manhã
  - Almoço
  - Lanche
  - Jantar

Horário: [Time Picker] (padrão: agora)
Data: [Date Picker] (padrão: hoje)
Calorias (kcal): [Number Input] (mínimo: 0)
Descrição: [Text Area]
```

#### Validações:
- ✅ Tipo de refeição obrigatório
- ✅ Calorias maior que zero
- ✅ Hora e data automáticas

#### Ações:
```
┌──────────────────────────────────────────┐
│ ✅ Registrar Refeição | ❌ Limpar Form.  │
└──────────────────────────────────────────┘
```

**Ao registrar:**
- ✅ Mensagem de sucesso
- ✅ Confetes (animação)
- ✅ Refeição adicionada à lista
- ✅ Totais atualizados automaticamente

---

### **Aba 2: 📋 Minhas Refeições**

#### Se nenhuma refeição foi registrada:
```
ℹ️ Nenhuma refeição registrada hoje.
Comece pela aba 'Adicionar Refeição'...
```

#### Se houver refeições registradas:
```
Total de calorias: 1500 kcal (75% da meta)

┌─────────────────────────────────────────────┐
│ 🍽️ ALMOÇO · 12:30                           │
│ 📅 29/06/2026 | 🔥 750 kcal                │
│ Descrição: Frango com arroz e brócolis     │
│                                   [🗑️ Deletar] │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ 🍽️ CAFÉ DA MANHÃ · 08:00                   │
│ 📅 29/06/2026 | 🔥 350 kcal                │
│ Descrição: Ovos, pão e café                │
│                                   [🗑️ Deletar] │
└─────────────────────────────────────────────┘
```

#### Funcionalidades:
- ✅ Total de calorias calculado automaticamente
- ✅ Cada refeição em card separado
- ✅ Botão para deletar refeição
- ✅ Atualização em tempo real

---

### **Aba 3: 🗂️ Alimentos**

#### Status Atual:
```
🚧 Funcionalidade em Desenvolvimento

Aqui você poderá:
• Consultar tabela de alimentos com calorias
• Buscar por nome ou categoria
• Adicionar alimentos customizados
• Filtrar por macronutrientes
```

#### Exemplo de Alimentos (Placeholder):
```
┌────────────────┬────────────────┬────────────────┬────────────────┐
│ 🍗 Frango      │ 🥚 Ovos        │ 🍚 Arroz       │ 🥦 Brócolis    │
│ 165 kcal/100g  │ 155 kcal/100g  │ 111 kcal/100g  │ 34 kcal/100g   │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

**Futuramente:**
- [ ] Integração com tabela `alimentos` do BD
- [ ] Busca por nome
- [ ] Filtros por categoria
- [ ] Adição de alimentos customizados

---

## 🔄 Fluxo de Dados

```
Adicionar Refeição (Aba 1)
    ↓
Validar dados
    ↓
✅ Salvar em st.session_state["refeicoes_hoje"]
    ↓
Atualizar resumo do dia
    ↓
Exibir em "Minhas Refeições" (Aba 2)
    ↓
Calcular total de calorias automaticamente
```

---

## 💾 Session State

```python
st.session_state["usuario"] = {
    "id": int,
    "nome": str,
    "email": str,
    "objetivo": str,
    "peso": float,
    "altura": float
}

st.session_state["refeicoes_hoje"] = [
    {
        "tipo": "Almoço",
        "data": "2026-06-29",
        "horario": "12:30:00",
        "calorias": 750.0,
        "descricao": "Frango com arroz"
    },
    # ... mais refeições
]
```

---

## 🔐 Segurança

- ✅ Verifica autenticação antes de carregarpágina
- ✅ Redireciona para login se não autenticado
- ✅ Botão "Voltar" redireciona para dashboard
- ✅ Usa dados do `st.session_state["usuario"]`

---

## 🎨 Componentes Utilizados

- ✅ `st.selectbox()` - Seleção de tipo de refeição
- ✅ `st.time_input()` - Seleção de horário
- ✅ `st.date_input()` - Seleção de data
- ✅ `st.number_input()` - Entrada de calorias
- ✅ `st.text_area()` - Descrição da refeição
- ✅ `st.button()` - Botões de ação
- ✅ `st.metric()` - Exibição de métricas
- ✅ `st.tabs()` - Organização em abas
- ✅ `st.container(border=True)` - Cards de refeições
- ✅ `st.columns()` - Layout com colunas
- ✅ `st.info()`, `st.success()` - Mensagens

---

## 📊 Valores Padrão

```python
meta_calorias = 2000  # Valor fixo (futuramente será personalizado)
data_default = date.today()
horario_default = datetime.now().time()
calorias_consumidas = sum([r["calorias"] for r in refeicoes])
percentual = (calorias_consumidas / meta_calorias) * 100
```

**Futuramente**:
- Meta será calculada baseada em perfil do usuário
- Dados serão persistidos no banco de dados
- Histórico será mantido por dia/mês/ano

---

## 🧪 Como Testar

### Teste 1: Adicionar Refeição
```
1. Clicar na aba "Adicionar Refeição"
2. Selecionar tipo: "Almoço"
3. Deixar horário automático (agora)
4. Deixar data automática (hoje)
5. Inserir calorias: 750
6. Adicionar descrição: "Frango com arroz"
7. Clicar "Registrar Refeição"
8. ✅ Deve exibir mensagem de sucesso
9. ✅ Deve animar confetes
```

### Teste 2: Verificar Resumo
```
1. Após adicionar refeição
2. Verificar se o resumo foi atualizado:
   - 🍽️ Consumido: 750 kcal (37.5%)
   - 🥗 Refeições: 1
```

### Teste 3: Visualizar Refeição
```
1. Clicar na aba "Minhas Refeições"
2. Deve exibir a refeição adicionada
3. Deve mostrar:
   - Tipo e horário
   - Data e calorias
   - Descrição
   - Botão para deletar
```

### Teste 4: Deletar Refeição
```
1. Na aba "Minhas Refeições"
2. Clicar no botão "🗑️ Deletar"
3. ✅ Refeição deve ser removida
4. ✅ Totais devem ser recalculados
```

### Teste 5: Voltar ao Dashboard
```
1. Clicar em "⬅️ Voltar"
2. ✅ Deve retornar ao dashboard
3. ✅ Refeições registradas devem persistir
```

---

## 📈 Próximos Passos

### Integração com Banco de Dados
```python
# Salvar em database.refeicoes
cursor.execute("""
    INSERT INTO refeicoes (usuario_id, tipo_refeicao, data_refeicao, calorias_totais)
    VALUES (?, ?, ?, ?)
""", (usuario_id, tipo, data, calorias))
```

### Implementar Alimentos
```python
# Consultar database.alimentos
cursor.execute("SELECT * FROM alimentos")
alimentos = cursor.fetchall()
# Exibir em tabela/grid
```

### Adicionar Macronutrientes
```python
{
    "proteinas": 50,
    "carboidratos": 60,
    "gorduras": 20
}
```

### Gráficos
```
- Gráfico de calorias ao longo do dia
- Distribuição por tipo de refeição
- Comparação com meta
```

---

## ✨ Características Especiais

### 1. **Validação em Tempo Real**
- Campos obrigatórios marcados com *
- Mensagens de erro específicas
- Números só aceitam valores positivos

### 2. **UX Melhorada**
- Valores padrão inteligentes (data/hora de agora)
- Abas bem organizadas
- Cards com bordas para legibilidade
- Emojis para melhor visualização

### 3. **Dados em Tempo Real**
- Resumo atualiza automaticamente
- Total de calorias recalculado
- Percentual atualizado
- Sem recarga necessária

### 4. **Responsivo**
- Layouts adaptáveis
- Botões full-width em colunas
- Teste em diferentes resoluções

---

## 📝 Código-Chave

### Adicionar Refeição
```python
nova_refeicao = {
    "tipo": tipo_refeicao,
    "data": str(data_refeicao),
    "horario": str(horario),
    "calorias": calorias,
    "descricao": descricao if descricao else "Sem descrição"
}
st.session_state["refeicoes_hoje"].append(nova_refeicao)
st.success("✅ Refeição registrada com sucesso!")
st.balloons()
```

### Calcular Total
```python
total_calorias = sum([r["calorias"] for r in refeicoes])
percentual = (total_calorias / 2000) * 100
```

### Deletar Refeição
```python
if st.button("🗑️ Deletar", key=f"delete_{idx}"):
    st.session_state["refeicoes_hoje"].pop(idx)
    st.rerun()
```

---

## 🎯 Status

| Funcionalidade | Status |
|---|---|
| Adicionar Refeição | ✅ Completo |
| Validações | ✅ Completo |
| Visualizar Refeições | ✅ Completo |
| Deletar Refeição | ✅ Completo |
| Cálculo de Calorias | ✅ Completo |
| Tabela de Alimentos | 🚧 Em desenvolvimento |
| Persistência BD | 🚧 Próximo passo |

---

**Data de Conclusão:** 29/06/2026  
**Versão:** 1.0  
**Status:** ✅ Funcional e Testado
