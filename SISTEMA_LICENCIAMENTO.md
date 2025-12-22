# 🔐 Sistema de Licenciamento - PinFlow Pro

## 📋 Visão Geral

Sistema completo de licenciamento para proteger o PinFlow Pro contra uso não autorizado.

---

## ✅ Funcionalidades Implementadas

### 1. **Geração de Licenças**
- Gera chaves únicas de 16 caracteres (formato: XXXX-XXXX-XXXX-XXXX)
- Validade configurável (padrão: 365 dias)
- Vinculação a Hardware ID (HWID)

### 2. **Validação de Licença**
- Verifica chave no startup
- Valida HWID (limita a 1 computador)
- Verifica data de expiração
- Armazena licença localmente

### 3. **Interface de Ativação**
- Dialog profissional para ativar licença
- Formatação automática da chave
- Exibe informações da licença atual
- Mensagens de erro claras

### 4. **Hardware ID (HWID)**
- Gera ID único baseado no sistema
- Limita instalação a 1 computador por licença
- Proteção contra compartilhamento

---

## 🚀 Como Usar

### Para o Desenvolvedor (Gerar Licenças)

#### Opção 1: Script Python
```bash
python gerar_licenca.py "Nome Cliente" "email@cliente.com" 365
```

**Exemplo:**
```bash
python gerar_licenca.py "João Silva" "joao@email.com" 365
```

#### Opção 2: Função Python
```python
from license_manager import generate_license_for_customer

license_key, license_data = generate_license_for_customer(
    "João Silva",
    "joao@email.com",
    365  # dias
)

print(f"Chave gerada: {license_key}")
```

### Para o Cliente (Ativar Licença)

1. **Ao iniciar o software:**
   - Se não houver licença válida, o dialog de ativação aparece automaticamente

2. **Pelo menu:**
   - Clicar em "🔐 Licença" na toolbar
   - Ou pelo menu do tray: "🔐 Ativar Licença"

3. **Digitar chave:**
   - Formato: `XXXX-XXXX-XXXX-XXXX`
   - A formatação é automática

4. **Clicar em "Ativar"**

---

## 📁 Arquivos do Sistema

### `license_manager.py`
- Classe `LicenseManager`: Gerencia licenças
- Função `generate_license_for_customer()`: Gera licenças

### `activate_dialog.py`
- Classe `ActivateDialog`: Interface de ativação

### `gerar_licenca.py`
- Script para gerar licenças via linha de comando

### `license.json` (gerado automaticamente)
- Licença ativada localmente
- **NÃO COMMITAR** (está no .gitignore)

### `valid_licenses.json` (gerado automaticamente)
- Lista de licenças válidas
- **NÃO COMMITAR** (está no .gitignore)

---

## 🔒 Segurança

### Proteções Implementadas

1. **HWID (Hardware ID)**
   - Limita a 1 instalação por licença
   - Baseado em informações do sistema

2. **Validação de Chave**
   - Hash SHA-256 da chave
   - Verificação contra lista de licenças válidas

3. **Data de Expiração**
   - Verificação automática
   - Bloqueio após expiração

4. **Armazenamento Local**
   - Licença salva em `license.json`
   - Não expõe informações sensíveis

### Melhorias Futuras (Opcional)

- [ ] Validação online (servidor)
- [ ] Criptografia da licença
- [ ] Renovação automática
- [ ] Limite de reinstalações
- [ ] Logs de ativação

---

## 📝 Fluxo de Venda

### 1. Cliente Compra
- Recebe email com chave de licença
- Chave no formato: `XXXX-XXXX-XXXX-XXXX`

### 2. Cliente Instala
- Baixa e instala PinFlow Pro
- Ao iniciar, dialog de ativação aparece

### 3. Cliente Ativa
- Digita chave recebida
- Sistema valida e ativa
- Licença vinculada ao HWID

### 4. Uso Normal
- Software verifica licença no startup
- Se válida, funciona normalmente
- Se inválida/expirada, pede reativação

---

## 🛠️ Integração no Código

### No `main.py`:

```python
# Importação
from license_manager import LicenseManager
from activate_dialog import ActivateDialog

# No __init__ da KanbanWindow
self.license_manager = LicenseManager()
if not self.check_license():
    return  # Sair se não houver licença válida

# Verificação no startup
def check_license(self):
    is_valid, message = self.license_manager.check_license()
    if not is_valid:
        dialog = ActivateDialog(self)
        if dialog.exec() != QDialog.Accepted:
            return False
    return True
```

---

## ⚠️ Importante

1. **SECRET_KEY**: Em produção, usar variável de ambiente ou arquivo separado
2. **valid_licenses.json**: Em produção, usar banco de dados ou servidor
3. **HWID**: Pode mudar se hardware mudar significativamente
4. **Backup**: Cliente deve fazer backup de `license.json`

---

## 🐛 Troubleshooting

### "Licença não é válida para este computador"
- HWID mudou (hardware alterado)
- Solução: Gerar nova licença ou resetar HWID

### "Licença expirada"
- Data de validade passou
- Solução: Renovar licença

### "Chave não encontrada"
- Chave digitada incorretamente
- Chave não foi gerada/registrada
- Solução: Verificar chave ou gerar nova

---

## 📞 Suporte

Para problemas com licenciamento:
- Verificar `license.json`
- Verificar `valid_licenses.json`
- Verificar HWID: `python -c "from license_manager import LicenseManager; print(LicenseManager().get_hardware_id())"`

---

**Versão:** 1.0  
**Data:** Dezembro 2025  
**Desenvolvedor:** Ede Machado

