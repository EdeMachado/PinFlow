@echo off
echo ========================================
echo   ATUALIZACAO v2.1 - NOTIFICACOES
echo   Post-it Kanban Pro
echo ========================================
echo.
echo Instalando nova dependencia (plyer)...
echo.
pip install plyer>=2.1.0
echo.
if errorlevel 1 (
    echo [ERRO] Falha ao instalar plyer!
    echo Tente manualmente: pip install plyer
    pause
    exit /b 1
)
echo.
echo ========================================
echo   SUCESSO!
echo ========================================
echo.
echo A biblioteca "plyer" foi instalada!
echo.
echo AGORA VOce TEM:
echo   - Notificacoes nativas do Windows 10/11
echo   - Som de alerta
echo   - Toast notifications
echo   - Funciona mesmo com Kanban minimizado!
echo.
echo ========================================
echo   COMO USAR:
echo ========================================
echo.
echo 1. Crie ou edite um card
echo 2. Preencha o alerta com data e hora
echo 3. Quando chegar a hora:
echo    - Card pisca (vermelho)
echo    - Notificacao do Windows aparece!
echo    - Som toca (opcional)
echo.
echo 4. Clique em "Marcar como Lido" para parar
echo.
echo ========================================
echo   PRONTO!
echo ========================================
echo.
echo Agora execute: run.bat
echo.
pause

