@echo off
echo 🚀 Auto Video Producer - Push para Ambos os Repositórios
echo ================================================================
echo.

echo 📤 Fazendo push para PRODUÇÃO (origin)...
git push origin main
if %errorlevel% neq 0 (
    echo ❌ Erro no push para produção!
    echo ⚠️  Verifique sua conexão e permissões.
    pause
    exit /b 1
)
echo ✅ Push para produção concluído!
echo.

echo 📤 Fazendo push para DESENVOLVIMENTO (dev)...
git push dev main
if %errorlevel% neq 0 (
    echo ❌ Erro no push para desenvolvimento!
    echo ⚠️  Verifique se o repositório dev está configurado corretamente.
    echo 💡 Execute: git remote -v para verificar
    pause
    exit /b 1
)
echo ✅ Push para desenvolvimento concluído!
echo.

echo 🎉 SUCCESS! Projeto salvo em ambos os repositórios:
echo    🏭 Produção: https://github.com/Ender-ss/auto-video-producerV5.git
echo    🔬 Desenvolvimento: https://github.com/Ender-ss/auto-video-producerV5-dev.git
echo.
echo 📋 Status dos repositórios:
git remote -v
echo.
pause
