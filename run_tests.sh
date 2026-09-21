#!/bin/bash
# ====================================================================
# 🧪 GAMEKHANSA COMPREHENSIVE TEST RUNNER
# Menjalankan Unit Testing, Automated Testing, Integrity Testing, & Performance Testing
# ====================================================================

set -e
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "===================================================================="
echo "🏎️  GAMEKHANSA (MOBIL LEGEND) — SUITE PENGUJIAN OTOMATIS LENGKAP 🧪"
echo "===================================================================="
echo "Waktu Pengujian: $(date)"
echo "Direktori Kerja: $ROOT_DIR"
echo ""

# 1. Unit Testing (UT-001 s.d. UT-025)
echo "--------------------------------------------------------------------"
echo "📌 [1/4] MENJALANKAN UNIT TESTING (25 KASUS UJI)"
echo "--------------------------------------------------------------------"
python3 tests/test_unit.py

# 2. Automated Regression Testing (AT-001 s.d. AT-010)
echo ""
echo "--------------------------------------------------------------------"
echo "📌 [2/4] MENJALANKAN AUTOMATED REGRESSION TESTING (10 KASUS UJI)"
echo "--------------------------------------------------------------------"
python3 tests/test_automated.py

# 3. Integrity & Integration Testing (IT-001 s.d. IT-015)
echo ""
echo "--------------------------------------------------------------------"
echo "📌 [3/4] MENJALANKAN INTEGRITY & INTEGRATION TESTING (15 KASUS UJI)"
echo "--------------------------------------------------------------------"
python3 tests/test_integrity.py

# 4. Performance & Benchmark Testing (PT-001 s.d. PT-008)
echo ""
echo "--------------------------------------------------------------------"
echo "📌 [4/4] MENJALANKAN PERFORMANCE & BENCHMARK TESTING (8 KASUS UJI)"
echo "--------------------------------------------------------------------"
python3 tests/test_performance.py

echo ""
echo "===================================================================="
echo "🎉 SELURUH PENGUJIAN (58 KASUS UJI) BERHASIL 100% LOLOS DENGAN SUKSES!"
echo "Dokumentasi Lengkap Tersedia di folder: docs/"
echo "===================================================================="
