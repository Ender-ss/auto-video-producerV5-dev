@echo off
echo 🔄 Sincronizando repositório de desenvolvimento...
echo.
echo 📥 Fazendo pull do repositório principal:
git pull origin main
if %errorlevel% neq 0 (
    echo ❌ Erro no pull de produção
    pause
    exit /b 1
)
echo ✅ Pull de produção concluído!
echo.
echo 📤 Fazendo push para desenvolvimento:
git push dev main
if %errorlevel% neq 0 (
    echo ❌ Erro no push para desenvolvimento
    pause
    exit /b 1
)
echo ✅ Push para desenvolvimento concluído!
echo.
echo 🎉 Sincronização concluída!
pause
