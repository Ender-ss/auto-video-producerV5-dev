@echo off
echo 🚀 Fazendo push para ambos os repositórios...
echo.
echo 📤 Push para produção (origin):
git push origin main
if %errorlevel% neq 0 (
    echo ❌ Erro no push para produção
    pause
    exit /b 1
)
echo ✅ Push para produção concluído!
echo.
echo 📤 Push para desenvolvimento (dev):
git push dev main
if %errorlevel% neq 0 (
    echo ❌ Erro no push para desenvolvimento
    pause
    exit /b 1
)
echo ✅ Push para desenvolvimento concluído!
echo.
echo 🎉 Push concluído em ambos os repositórios!
pause
