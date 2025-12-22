@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║        PINFLOW PRO - LIMPEZA DE ARQUIVOS                 ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo Removendo arquivos temporários e de teste...
echo.

REM Scripts de teste .bat
del /Q test.bat 2>nul
del /Q teste_v2.bat 2>nul
del /Q teste_final_win11.bat 2>nul
del /Q teste_windows11.bat 2>nul
del /Q testar_notificacoes.bat 2>nul
del /Q debug_notificacoes.bat 2>nul
del /Q corrigir_notificacoes.bat 2>nul
del /Q registrar_python_win11.bat 2>nul
del /Q instalar_notificacoes.bat 2>nul
del /Q criar_instalador.bat 2>nul

REM Scripts Python de teste
del /Q teste_notificacao_isolado.py 2>nul
del /Q test_system.py 2>nul

REM Documentação antiga
del /Q ATUALIZACAO_*.txt 2>nul
del /Q CORRECAO_*.txt 2>nul
del /Q CORRECOES_*.txt 2>nul
del /Q GUIA_*.txt 2>nul
del /Q NOTIFICACOES_*.txt 2>nul
del /Q SOLUCAO_*.txt 2>nul
del /Q VERSAO_*.txt 2>nul
del /Q PINFLOW_*.txt 2>nul
del /Q NOTEFLOW_*.txt 2>nul
del /Q RESUMO_*.txt 2>nul
del /Q STATUS.txt 2>nul
del /Q LEIA-ME.txt 2>nul
del /Q LEIA-ME_PRIMEIRO.txt 2>nul

REM Arquivos de versão antigos
del /Q 0.9 2>nul
del /Q 2.1.0 2>nul

REM Ícones temporários (manter apenas icon.png)
del /Q icon_16.png 2>nul
del /Q icon_24.png 2>nul
del /Q icon_32.png 2>nul
del /Q icon_48.png 2>nul
del /Q icon_64.png 2>nul
del /Q icon_128.png 2>nul
del /Q icon_256.png 2>nul

echo.
echo ✓ Limpeza concluída!
echo.
echo Arquivos mantidos:
echo   - main.py
echo   - requirements.txt
echo   - README.md
echo   - Arquivos de build/instalação
echo   - Scripts úteis (run.bat, etc)
echo.
pause

