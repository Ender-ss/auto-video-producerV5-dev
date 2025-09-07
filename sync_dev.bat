@echo off
echo 🔄 Auto Video Producer - Sincronização de Desenvolvimento
echo ============================================================
echo.

echo 📥 Fazendo pull do repositório de PRODUÇÃO...
git pull origin main
if %errorlevel% neq 0 (
    echo ❌ Erro no pull de produção!
    echo ⚠️  Verifique sua conexão com o repositório principal.
    pause
    exit /b 1
)
echo ✅ Pull de produção concluído!
echo.

echo 📤 Sincronizando com repositório de DESENVOLVIMENTO...
git push dev main
if %errorlevel% neq 0 (
    echo ❌ Erro na sincronização com desenvolvimento!
    echo ⚠️  Verifique se o repositório dev está configurado.
    echo 💡 Consulte: VERIFICACAO_REPOSITORIO_DEV.md
    pause
    exit /b 1
)
echo ✅ Sincronização concluída!
echo.

echo 🎉 SUCCESS! Repositórios sincronizados:
echo    🏭 Produção ← Atualizado
echo    🔬 Desenvolvimento ← Sincronizado
echo.
echo 📊 Status atual:
git status --short
echo.
echo 📋 Remotes configurados:
git remote -v
echo.
pause
