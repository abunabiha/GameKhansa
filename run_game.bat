@echo off
title Mobil Legend - Khansa Racing Championship
cd /d "%~dp0"

echo ==============================================
echo 🏎️  MEMULAI GAME MOBIL LEGEND (GameKhansa) 🏎️
echo ==============================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python belum terinstal. Silakan install Python 3 dari https://www.python.org/
        pause
        exit /b 1
    )
    set PY_CMD=python3
) else (
    set PY_CMD=python
)

%PY_CMD% -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚙️ Menginstal pustaka Pygame...
    %PY_CMD% -m pip install pygame
)

echo 🚀 Meluncurkan game...
%PY_CMD% main.py
pause
