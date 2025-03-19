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
    pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu118
    pip install -r requirements.txt
) ELSE (
    echo Environnement activation...
    cd .env\Scripts
    call activate.bat
    cd ../..
)

start cmd /k uvicorn translate_api:app --host 0.0.0.0 --port 7995

timeout /t 10

pytest test_translate.py -s

IF %ERRORLEVEL% EQU 0 (
    exit
) ELSE (
    echo "Error during testing, please check logs"
    pause
)