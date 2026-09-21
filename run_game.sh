#!/usr/bin/env bash
# Script Peluncur Game Mobil Legend (GameKhansa) untuk macOS / Linux

cd "$(dirname "$0")"

echo "=============================================="
echo "🏎️  MEMULAI GAME MOBIL LEGEND (GameKhansa) 🏎️"
echo "=============================================="

# Cek Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 belum terinstal di sistem Anda."
    echo "Silakan install Python 3 terlebih dahulu dari https://www.python.org/"
    exit 1
fi

# Cek modul Pygame
python3 -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚙️ Menginstal pustaka Pygame secara otomatis..."
    python3 -m pip install pygame
    if [ $? -ne 0 ]; then
        echo "⚠️ Gagal menginstal via pip standar, mencoba dengan flag --user..."
        python3 -m pip install --user pygame
    fi
fi

# Jalankan Game
echo "🚀 Meluncurkan game..."
python3 main.py
