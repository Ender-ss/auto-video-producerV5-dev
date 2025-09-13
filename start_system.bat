@echo off
echo 🚀 Auto Video Producer - Inicialização do Sistema
echo =================================================
echo.

echo 🔍 Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! Instale o Python 3.8+ e adicione ao PATH.
    pause
    exit /b 1
)

echo 🔍 Verificando Node.js...
node --version
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado! Instale o Node.js e adicione ao PATH.
    pause
    exit /b 1
)

echo.
echo 📁 Criando diretórios necessários...
if not exist "backend\uploads" mkdir "backend\uploads"
if not exist "outputs" mkdir "outputs"
if not exist "temp" mkdir "temp"
if not exist "logs" mkdir "logs"

echo.
echo 📦 Instalando dependências do backend...
cd backend
pip install -r requirements.txt
cd ..

echo.
echo 📦 Instalando dependências do frontend...
cd frontend
npm install
cd ..

echo.
echo 🚀 Iniciando backend em novo terminal...
start "Backend - Auto Video Producer" cmd /k "cd /d \"%~dp0backend\" && python app.py"

echo.
echo 🚀 Iniciando frontend em novo terminal...
start "Frontend - Auto Video Producer" cmd /k "cd /d \"%~dp0frontend\" && npm run dev"

echo.
echo ✅ Sistema iniciado com sucesso!
echo.
echo 📋 Endereços de acesso:
echo    Backend: /api
echo    Frontend: http://localhost:5173
echo.
echo ⚠️  Mantenha ambos os terminais abertos para o sistema funcionar.
echo.
pause