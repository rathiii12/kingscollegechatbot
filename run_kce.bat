@echo off
cd /d "%~dp0"
title KCE Chatbot
echo.
echo  Kings College of Engineering chatbot
echo  ------------------------------------
if "%HF_TOKEN%"=="" set /p HF_TOKEN=Paste your Hugging Face token and press Enter (or just press Enter to skip): 
echo.
echo  Opening http://127.0.0.1:5000 ...
start "" cmd /c "timeout /t 4 /nobreak >nul & start http://127.0.0.1:5000"
python app.py
echo.
pause
