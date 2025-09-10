@echo off
echo 🔬 Workflow de Desenvolvimento
echo ============================
echo.
echo 1. Mudando para branch develop
git checkout develop
if %errorlevel% neq 0 (
    echo ⚠️  Branch develop não existe. Criando...
    git checkout -b develop
)
echo.
echo 2. Fazendo pull das últimas mudanças
git pull dev develop
echo.
echo 3. Pronto para desenvolvimento!
echo.
echo 📝 Próximos passos:
echo    - Faça suas mudanças
echo    - git add .
echo    - git commit -m "Sua mensagem"
echo    - git push dev develop
echo.
pause
