# 🧹 Limpeza de Arquivos - PinFlow Pro

## 📋 Arquivos a DELETAR (temporários/teste)

### Scripts de Teste (.bat)
- `test.bat`
- `teste_v2.bat`
- `teste_final_win11.bat`
- `teste_windows11.bat`
- `testar_notificacoes.bat`
- `debug_notificacoes.bat`
- `corrigir_notificacoes.bat`
- `registrar_python_win11.bat`
- `instalar_notificacoes.bat`
- `criar_instalador.bat` (duplicado de gerar_instalador.bat)

### Scripts Python de Teste
- `teste_notificacao_isolado.py`
- `test_system.py`

### Documentação Antiga/Redundante (.txt)
- `ATUALIZACAO_*.txt` (todos - consolidar em CHANGELOG.md)
- `CORRECAO_*.txt` (todos - consolidar em CHANGELOG.md)
- `CORRECOES_*.txt` (todos - consolidar em CHANGELOG.md)
- `GUIA_*.txt` (exceto GUIA_RAPIDO.txt se necessário)
- `NOTIFICACOES_*.txt` (consolidar)
- `SOLUCAO_*.txt` (consolidar)
- `VERSAO_*.txt` (consolidar)
- `PINFLOW_*.txt` (exceto se for documentação final)
- `NOTEFLOW_*.txt` (nome antigo)
- `RESUMO_*.txt` (consolidar)
- `STATUS.txt` (consolidar)
- `LEIA-ME.txt` (usar README.md)
- `LEIA-ME_PRIMEIRO.txt` (usar README.md)

### Arquivos de Versão Antigos
- `0.9`
- `2.1.0`

### Ícones Temporários (já temos icon.png)
- `icon_16.png`
- `icon_24.png`
- `icon_32.png`
- `icon_48.png`
- `icon_64.png`
- `icon_128.png`
- `icon_256.png`
(Manter apenas `icon.png` e gerar `icon.ico` quando necessário)

## ✅ Arquivos a MANTER

### Essenciais
- `main.py` - Código principal
- `requirements.txt` - Dependências
- `requirements-build.txt` - Dependências de build
- `README.md` - Documentação principal
- `LICENSE` - Licença
- `.gitignore` - Configuração Git

### Build/Instalação
- `build.spec` - PyInstaller
- `version_info.txt` - Versão Windows
- `installer.iss` - Inno Setup
- `gerar_instalador.bat` - Script de build
- `criar_icone.py` - Gerador de ícone
- `EULA.txt` - Termos de uso

### Documentação Principal
- `README.md` - Principal
- `CHANGELOG.md` - Histórico de versões
- `INSTRUCOES_INSTALADOR.md` - Guia de instalação
- `COMO_GERAR_INSTALADOR.txt` - Guia rápido
- `PROXIMOS_PASSOS_COMERCIALIZACAO.txt` - Roadmap

### Scripts Úteis
- `run.bat` - Executar aplicação
- `run_startup.bat` - Inicialização automática
- `instalar_inicializacao.bat` - Configurar startup
- `remover_inicializacao.bat` - Remover startup
- `limpar_cards_brancos.bat` - Utilitário
- `dev.bat` - Modo desenvolvimento

### Dados (não versionar, mas manter localmente)
- `kanban.json` - Dados do usuário
- `kanban_arquivo.json` - Cards arquivados
- `backups/` - Backups automáticos

