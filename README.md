# 🏎️ Mobil Legend — Khansa Racing Championship 🏆

[![CI/CD Pipeline](https://github.com/abunabiha/GameKhansa/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/abunabiha/GameKhansa/actions/workflows/ci_cd.yml)
[![GitHub Pages](https://img.shields.io/badge/Play%20Online-GitHub%20Pages-brightgreen?logo=github)](https://abunabiha.github.io/GameKhansa/)
[![Tests](https://img.shields.io/badge/Tests-58%20Passed-success)](https://github.com/abunabiha/GameKhansa/actions)
[![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue?logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Desktop%20|%20Web%20Canvas-orange)]()

Game balap mobil edukatif arcade retro ringan, seru, dan responsif bertema **Mobil Legend** yang dibuat khusus untuk **GameKhansa**. Dilengkapi integrasi kurikulum edukasi Matematika SD dan 3.000 Kosa Kata Bahasa Inggris (*Adaptive Educational Gate System*).

> 🌐 **Mainkan Langsung di Browser (Live Demo)**: [https://abunabiha.github.io/GameKhansa/](https://abunabiha.github.io/GameKhansa/)

---

## 🎮 Cara Menjalankan Game

### Opsi 1: Menjalankan via Python (Desktop)
Pastikan Python 3 sudah terinstal. Buka Terminal / Command Prompt di folder ini, lalu:

- **macOS / Linux**:
  ```bash
  ./run_game.sh
  ```
  *(atau `python3 main.py`)*

- **Windows**:
  Klik 2x pada file `run_game.bat` atau jalankan:
  ```cmd
  python main.py
  ```

*Catatan: Jika pustaka Pygame belum terpasang, script peluncur akan otomatis menginstalnya untuk Anda (`pip install pygame`).*

---

### Opsi 2: Main Langsung di Browser (Web Instan)
Anda juga bisa memainkan game ini tanpa instalasi apapun!
- Cukup **klik dua kali** file `game_web.html` untuk langsung membukanya di Google Chrome, Safari, Edge, atau Mozilla Firefox.
- Mendukung kontrol layar sentuh (touch buttons) jika dibuka di smartphone atau tablet!

---

## 🕹️ Kontrol Permainan

| Tombol | Fungsi |
| :--- | :--- |
| **Panah Atas / W** | Tancap Gas (Akselerasi) |
| **Panah Bawah / S** | Rem / Perlambat |
| **Panah Kiri / A** | Belok Kiri |
| **Panah Kanan / D** | Belok Kanan |
| **SPACEBAR / SHIFT** | **Mobil**: Aktifkan **Turbo Nitro Boost** ⚡<br>**Tank**: **Tembak Meriam Tempur** (Hancurkan Mobil & Rintangan) 💣 |
| **G** | Masuk ke Garasi (Pilih Mobil / Tank) |
| **P / ESC** | Pause (Jeda Permainan) |
| **M** | Kembali ke Menu Utama |

---

## 🚘 Pilihan Kendaraan di Garasi (Mobil & Tank)

### 🏎️ Kategori Mobil Balap:
1. **Si Merah Kilat**: Mobil sport lincah dengan akselerasi tinggi dan Turbo Nitro gesit.
2. **Garuda Hitam**: Muscle car tangguh berdaya tahan benturan tinggi (HP 150) + Turbo Nitro.
3. **Cyber Khansa**: Hypercar futuristik dengan kapasitas Nitro ultra besar (250).

### 🛡️ Kategori Tank Tempur (Battle Tank):
4. **Tank Badak Baja**: Tank lapis baja militer berbobot berat (HP 250), roda rantai kokoh, meriam peledak berdaya hancur tinggi untuk meledakkan mobil lalu lintas dan barikade jalan.
5. **Tank Titan Khansa**: Super-tank futuristik dengan armor ultra (HP 300) dan meriam plasma berkecepatan tembak tinggi (cooldown cepat).

---

## 🌟 Fitur & Efek Suara
- **Sistem Audio Prosedural**: Raungan mesin mobil sport & deru mesin diesel tank, desis roket nitro, decitan ban, dentuman meriam, dan ledakan kehancuran.
- **Tembak & Hancurkan**: Tank dapat menghancurkan mobil lalu lintas (+150 poin) dan balok rintangan (+100 poin) dengan ledakan partikel spektakuler.
- **Koleksi Koin (🪙)**: Menambah skor +100 per koin dan multiplier.
- **Tabung Nitro (⚡)**: Mengisi ulang tangki nitro boost seketika.
- **Kotak P3K / Reparasi (➕)**: Memperbaiki bodi dan menambah darah kendaraan (+35 HP).
- **Tumpahan Oli**: Bikin kendaraan tergelincir sesaat (tank lebih stabil terhadap licin).
- **Barikade / Pembatas Jalan**: Rintangan berat di jalan.
- **3 Tema Trek Dinamis**: Lembah Hijau Asri, Gurun Senja, dan Cyber Metropolis.
- **Sistem High Score**: Rekor skor tersimpan otomatis di `highscore.json` (atau browser `localStorage`).

---

## 📚 Dokumentasi Teknis & Akademik (`docs/`)

Project GameKhansa dilengkapi dengan dokumentasi standar industri perangkat lunak dan standar publikasi ilmiah internasional:

| No | Dokumen | Deskripsi |
| :---: | :--- | :--- |
| **01** | [`01_SDLC_METHODOLOGY_AND_FRAMEWORK.md`](docs/01_SDLC_METHODOLOGY_AND_FRAMEWORK.md) | Metodologi Rekayasa Perangkat Lunak Iteratif & Inkremental, Tech Stack, Timeline, & Manajemen Risiko |
| **02** | [`02_REQUIREMENTS_SPECIFICATION_SRS.md`](docs/02_REQUIREMENTS_SPECIFICATION_SRS.md) | Spesifikasi Kebutuhan Perangkat Lunak (52 Kebutuhan Fungsional & Non-Fungsional, Use Cases, User Stories) |
| **03** | [`03_SYSTEM_ARCHITECTURE_AND_DESIGN_SDD.md`](docs/03_SYSTEM_ARCHITECTURE_AND_DESIGN_SDD.md) | Arsitektur Dual-Platform (Python + HTML5), Diagram Kelas, State Machine, & Aliran Data |
| **04** | [`04_ALGORITHMS_AND_MATHEMATICAL_FORMULATIONS.md`](docs/04_ALGORITHMS_AND_MATHEMATICAL_FORMULATIONS.md) | Formulasi Matematis Fisika Kendaraan, Collision Detection, Bounce Barrier, Rainbow Shield, & Audio Sintesis |
| **05** | [`05_VERIFICATION_VALIDATION_AND_TESTING_STD.md`](docs/05_VERIFICATION_VALIDATION_AND_TESTING_STD.md) | Laporan Pengujian Lengkap: Unit Testing, Automated Testing, Integrity Testing, Performance, & User Testing (SUS 84.8) |
| **06** | [`06_SCIENTIFIC_EVALUATION_AND_PEDAGOGICAL_RUBRICS.md`](docs/06_SCIENTIFIC_EVALUATION_AND_PEDAGOGICAL_RUBRICS.md) | Landasan Teori Pedagogis (GBL, Bloom, Dual Coding, Flow), Rubrik Evaluasi Guru, & Panduan Kelas |
| **07** | [`07_JOURNAL_PAPER_IMRAD_SCOPUS_Q1.md`](docs/07_JOURNAL_PAPER_IMRAD_SCOPUS_Q1.md) | Draf Artikel Jurnal Ilmiah Format IMRAD Standar Scopus Q1 (*Computers & Education* / *BJET*) |

---

## 🧪 Menjalankan Suite Pengujian Otomatis

Seluruh 58 kasus uji dapat dijalankan secara otomatis dengan satu perintah:

```bash
./run_tests.sh
```

Atau dijalankan per modul:
```bash
# 1. Unit Testing (25 kasus uji)
python3 tests/test_unit.py

# 2. Automated Regression Testing (10 kasus uji)
python3 tests/test_automated.py

# 3. Integrity & Integration Testing (15 kasus uji)
python3 tests/test_integrity.py

# 4. Performance & 60 FPS Benchmark Testing (8 kasus uji)
python3 tests/test_performance.py
```

