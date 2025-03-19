@echo off

REM Change to the directory where the script is located
cd /d %~dp0

REM Creation, installation & activation of local env
IF NOT EXIST .env (
    echo Creation of the environment...
    python -m venv .env
    cd .env\Scripts
    call activate.bat
    cd ../..
    pip install -r requirements.txt
) ELSE (
    echo Environnement activation...
    cd .env\Scripts
    call activate.bat
    cd ../..
)

start cmd /k uvicorn cot_api:app --host 0.0.0.0 --port 7996

timeout /t 4

pytest test_cot_api.py -s

IF %ERRORLEVEL% EQU 0 (
    exit
) ELSE (
    echo "Error during testing, please check logs"
    pause
)

netstat -aon | find "11434"
if %errorlevel% neq 0 (
    start cmd /k ollama serve
) else (
    exit
)