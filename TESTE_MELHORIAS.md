# 🧪 GUIA DE TESTE - Melhorias Implementadas

**Data:** Dezembro 2025

---

## ✅ CHECKLIST DE TESTES

### 1. **Card Abre ao Clicar**
- [ ] Clique em um card (sem arrastar)
- [ ] Verificar se o dialog de edição abre
- [ ] Editar algo e salvar
- [ ] Verificar se as mudanças foram aplicadas

### 2. **Engrenagem no Canto Superior Direito**
- [ ] Verificar se a engrenagem está no topo direito do card
- [ ] Verificar se não tem quadradinho (apenas ícone)
- [ ] Clicar na engrenagem
- [ ] Verificar se o menu abre

### 3. **Tamanho Personalizado Persistente**
- [ ] Arrastar a borda direita de um card
- [ ] Arrastar o canto inferior direito
- [ ] Verificar se o tamanho muda
- [ ] Fechar e reabrir o aplicativo
- [ ] Verificar se o tamanho personalizado foi mantido

### 4. **Copiar Nota**
- [ ] Abrir um card com notas
- [ ] Clicar na engrenagem
- [ ] Selecionar "📋 Copiar Nota"
- [ ] Colar em um editor de texto (Ctrl+V)
- [ ] Verificar se a nota foi copiada

### 5. **Imprimir Nota**
- [ ] Abrir um card com notas
- [ ] Clicar na engrenagem
- [ ] Selecionar "🖨️ Imprimir Nota"
- [ ] Verificar se o dialog de impressão abre
- [ ] (Opcional) Imprimir ou cancelar

### 6. **Menu Configuração do Sistema**
- [ ] Clicar no botão "⚙️ Configuração" no header
- [ ] Verificar se o dialog abre
- [ ] Testar aba "🎨 Aparência"
  - [ ] Clicar em "Alterar Cor" do header
  - [ ] Clicar em "Alterar Cor" dos headers das colunas
- [ ] Testar aba "🔐 Licenciamento"
  - [ ] Verificar informações da licença
  - [ ] (Se não houver licença) Testar ativação
- [ ] Testar aba "ℹ️ Sobre"
  - [ ] Verificar informações do sistema

---

## 🐛 PROBLEMAS CONHECIDOS

### Se algo não funcionar:

1. **Card não abre ao clicar:**
   - Verificar se não está arrastando (movimento < 10 pixels)
   - Tentar clicar no centro do card

2. **Engrenagem não aparece:**
   - Verificar se está no canto superior direito
   - Verificar se não tem fundo (deve ser transparente)

3. **Tamanho não persiste:**
   - Verificar se salvou os dados (fechar e reabrir)
   - Verificar se `custom_width` e `custom_height` estão no JSON

4. **Copiar/Imprimir não funciona:**
   - Verificar se o card tem notas
   - Verificar se o menu da engrenagem mostra as opções

5. **Configuração não abre:**
   - Verificar se o botão está no header
   - Verificar se há erros no console

---

## 📝 NOTAS DE TESTE

**Data do Teste:** _______________

**Testador:** _______________

**Resultados:**
- [ ] Todos os testes passaram
- [ ] Alguns testes falharam (anotar abaixo)
- [ ] Problemas encontrados:

_________________________________________________
_________________________________________________
_________________________________________________

---

**Boa sorte com os testes!** 🚀

