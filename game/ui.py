"""
Modul Antarmuka Pengguna (UI & HUD) untuk game Mobil Legend.
Mendukung pemilihan Mobil Balap vs Tank Tempur,
HUD dinamis (Nitro bar untuk mobil, Status Meriam Tembak untuk tank),
Layar Pause, Garasi, dan Layar Game Over.
"""

import math
import pygame
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ROAD_LEFT, ROAD_RIGHT,
    COLOR_WHITE, COLOR_GOLD, COLOR_NITRO_CYAN,
    COLOR_HEALTH_GREEN, COLOR_HEALTH_RED, CARS_DATA,
    EDU_MODE_MATH, EDU_MODE_VOCAB, MATH_GRADES, VOCAB_LEVELS
)

class UIManager:
    def __init__(self):
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Arial", 46, bold=True)
        self.font_subtitle = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_large = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_med = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 14, bold=False)
        self.font_tiny = pygame.font.SysFont("Arial", 11, bold=True)
        self.font_digits = pygame.font.SysFont("Courier New", 22, bold=True)

        self.pulse_timer = 0.0
        self.menu_buttons = {}
        self.garage_cards = []
        self.garage_start_btn = None
        self.name_input_box_rect = None
        self.name_submit_btn_rect = None
        self.confirm_yes_rect = None
        self.confirm_no_rect = None


    def draw_text_with_shadow(self, surface, text, font, color, pos, center=False, shadow_col=(15, 15, 20)):
        rendered_shadow = font.render(text, True, shadow_col)
        rendered_text = font.render(text, True, color)

        if center:
            rect = rendered_text.get_rect(center=pos)
            surface.blit(rendered_shadow, (rect.x + 2, rect.y + 2))
            surface.blit(rendered_text, rect)
            return rect
        else:
            surface.blit(rendered_shadow, (pos[0] + 2, pos[1] + 2))
            surface.blit(rendered_text, pos)
            return rendered_text.get_rect(topleft=pos)

    def draw_menu(self, surface, selected_car_id, highscore, grade_level=2, edu_mode=EDU_MODE_MATH, vocab_level=1, player_name="Khansa", coins=0, mastered_words_count=0):
        self.pulse_timer += 0.05
        bg_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        bg_overlay.fill((12, 14, 22, 220))
        surface.blit(bg_overlay, (0, 0))

        # Profile Badge di bagian atas layar menu
        p_name = (player_name or "Khansa").upper()
        p_badge = f"👤 PEMBALAP: {p_name}   |   🪙 {coins} KOIN   |   📚 {mastered_words_count} KATA DIKUASAI   |   🏆 REKOR: {highscore:,}"
        self.draw_text_with_shadow(surface, p_badge, self.font_small, COLOR_GOLD, (SCREEN_WIDTH // 2, 16), center=True)

        # Judul Utama "MOBIL LEGEND"
        title_y = 50 + int(math.sin(self.pulse_timer) * 3)

        glow_surf = self.font_title.render("MOBIL LEGEND", True, (255, 60, 80))
        glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2, title_y))
        surface.blit(glow_surf, (glow_rect.x + 3, glow_rect.y + 3))

        self.draw_text_with_shadow(
            surface, "MOBIL LEGEND", self.font_title, (255, 220, 50),
            (SCREEN_WIDTH // 2, title_y), center=True
        )

        self.draw_text_with_shadow(
            surface, "— KHANSA RACING & EDUKASI MATEMATIKA & INGGRIS —", self.font_subtitle, COLOR_NITRO_CYAN,
            (SCREEN_WIDTH // 2, title_y + 35), center=True
        )


        # --- 1. TAB PILIHAN MATA PELAJARAN EDUKASI: MATEMATIKA VS ENGLISH ---
        edu_tab_y = 92
        et_w = 185
        et_h = 30
        tab_math_rect = pygame.Rect(SCREEN_WIDTH // 2 - et_w - 6, edu_tab_y, et_w, et_h)
        tab_vocab_rect = pygame.Rect(SCREEN_WIDTH // 2 + 6, edu_tab_y, et_w, et_h)

        is_math_mode = (edu_mode == EDU_MODE_MATH)

        # Tab Matematika
        math_bg = (30, 60, 95) if is_math_mode else (20, 24, 34)
        math_border = COLOR_NITRO_CYAN if is_math_mode else (50, 60, 75)
        pygame.draw.rect(surface, math_bg, tab_math_rect, border_radius=6)
        pygame.draw.rect(surface, math_border, tab_math_rect, width=2 if is_math_mode else 1, border_radius=6)
        math_txt_col = COLOR_WHITE if is_math_mode else (150, 160, 175)
        self.draw_text_with_shadow(surface, "📐 MATEMATIKA SD", self.font_small, math_txt_col, (tab_math_rect.centerx, tab_math_rect.centery), center=True)

        # Tab English Vocab
        vocab_bg = (70, 48, 20) if not is_math_mode else (20, 24, 34)
        vocab_border = COLOR_GOLD if not is_math_mode else (50, 60, 75)
        pygame.draw.rect(surface, vocab_bg, tab_vocab_rect, border_radius=6)
        pygame.draw.rect(surface, vocab_border, tab_vocab_rect, width=2 if not is_math_mode else 1, border_radius=6)
        vocab_txt_col = COLOR_WHITE if not is_math_mode else (150, 160, 175)
        self.draw_text_with_shadow(surface, "🔤 ENGLISH 3000 VOCAB", self.font_small, vocab_txt_col, (tab_vocab_rect.centerx, tab_vocab_rect.centery), center=True)

        # --- 2. PEMILIHAN TINGKAT LEVEL (ADAPTIF MATEMATIKA / VOCAB) ---
        grade_y = 128
        gw = 145
        gh = 30
        gap_g = 10
        gx_start = SCREEN_WIDTH // 2 - int((3 * gw + 2 * gap_g) / 2)

        grade_buttons = {}
        cur_level = grade_level if is_math_mode else vocab_level
        levels_dict = MATH_GRADES if is_math_mode else VOCAB_LEVELS

        for lvl in (1, 2, 3):
            g_info = levels_dict[lvl]
            gx = gx_start + (lvl - 1) * (gw + gap_g)
            g_rect = pygame.Rect(gx, grade_y, gw, gh)
            is_active_grade = (lvl == cur_level)

            bg_c = (35, 65, 50) if (is_active_grade and lvl == 1) else (
                (60, 50, 25) if (is_active_grade and lvl == 2) else (
                    (25, 55, 80) if is_active_grade else (22, 26, 36)
                )
            )
            border_c = g_info["color"] if is_active_grade else (55, 65, 80)
            pygame.draw.rect(surface, bg_c, g_rect, border_radius=6)
            pygame.draw.rect(surface, border_c, g_rect, width=2 if is_active_grade else 1, border_radius=6)

            txt_c = COLOR_WHITE if is_active_grade else (150, 160, 175)
            self.draw_text_with_shadow(surface, g_info["badge"], self.font_tiny, txt_c, (g_rect.centerx, g_rect.centery), center=True)
            grade_buttons[f"grade_{lvl}"] = g_rect

        # Subtitle Materi / Fokus Terpilih
        cur_desc = levels_dict[cur_level]["desc"]
        prefix = "Materi: " if is_math_mode else "Fokus: "
        suffix = "" if is_math_mode else " (Target 3.000 Kata)"
        self.draw_text_with_shadow(surface, f"{prefix}{cur_desc}{suffix}", self.font_tiny, (200, 220, 240), (SCREEN_WIDTH // 2, grade_y + 38), center=True)

        car_data = CARS_DATA[selected_car_id]
        is_tank = car_data.get("type") == "tank"

        # --- 3. TAB PILIHAN CEPAT: MOBIL VS TANK ---
        tab_w = 205
        tab_h = 32
        tab_y = 180

        tab_car_rect = pygame.Rect(SCREEN_WIDTH // 2 - tab_w - 8, tab_y, tab_w, tab_h)
        tab_tank_rect = pygame.Rect(SCREEN_WIDTH // 2 + 8, tab_y, tab_w, tab_h)

        # Tab Mobil
        car_tab_bg = (24, 75, 140) if not is_tank else (22, 26, 36)
        car_tab_border = COLOR_NITRO_CYAN if not is_tank else (55, 65, 80)
        pygame.draw.rect(surface, car_tab_bg, tab_car_rect, border_radius=8)
        pygame.draw.rect(surface, car_tab_border, tab_car_rect, width=2 if not is_tank else 1, border_radius=8)
        car_txt_col = COLOR_WHITE if not is_tank else (160, 170, 185)
        self.draw_text_with_shadow(surface, "🏎️ PILIH MOBIL", self.font_med, car_txt_col, (tab_car_rect.centerx, tab_car_rect.centery), center=True)

        # Tab Tank
        tank_tab_bg = (45, 100, 40) if is_tank else (22, 26, 36)
        tank_tab_border = (255, 200, 50) if is_tank else (55, 65, 80)
        pygame.draw.rect(surface, tank_tab_bg, tab_tank_rect, border_radius=8)
        pygame.draw.rect(surface, tank_tab_border, tab_tank_rect, width=2 if is_tank else 1, border_radius=8)
        tank_txt_col = COLOR_WHITE if is_tank else (160, 170, 185)
        self.draw_text_with_shadow(surface, "🛡️ PILIH TANK", self.font_med, tank_txt_col, (tab_tank_rect.centerx, tab_tank_rect.centery), center=True)

        # --- 4. KARTU KENDARAAN UTAMA DENGAN TOMBOL PANAH KIRI / KANAN ---
        card_w = 420
        card_h = 202
        card_x = SCREEN_WIDTH // 2 - card_w // 2
        card_y = 224
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (25, 30, 44, 240), (0, 0, card_w, card_h), border_radius=14)
        pygame.draw.rect(card_surf, car_data["glow_color"], (0, 0, card_w, card_h), width=2, border_radius=14)
        surface.blit(card_surf, card_rect.topleft)

        # Tombol Panah Kiri (◀) & Kanan (▶)
        btn_arrow_w = 44
        btn_arrow_h = 68
        arrow_y = card_y + card_h // 2 - btn_arrow_h // 2
        prev_btn_rect = pygame.Rect(card_x - btn_arrow_w - 12, arrow_y, btn_arrow_w, btn_arrow_h)
        next_btn_rect = pygame.Rect(card_x + card_w + 12, arrow_y, btn_arrow_w, btn_arrow_h)

        for rect, symbol in ((prev_btn_rect, "◀"), (next_btn_rect, "▶")):
            pygame.draw.rect(surface, (30, 38, 55), rect, border_radius=8)
            pygame.draw.rect(surface, car_data["glow_color"], rect, width=2, border_radius=8)
            self.draw_text_with_shadow(surface, symbol, self.font_title, COLOR_GOLD, (rect.centerx, rect.centery), center=True)

        # Header Kartu: Badge & Nama
        badge_txt = "🛡️ KATEGORI: TANK TEMPUR (BATTLE TANK)" if is_tank else "🏎️ KATEGORI: MOBIL BALAP (RACING CAR)"
        badge_col = (255, 200, 50) if is_tank else COLOR_NITRO_CYAN
        self.draw_text_with_shadow(surface, badge_txt, self.font_tiny, badge_col, (SCREEN_WIDTH // 2, card_y + 16), center=True)

        self.draw_text_with_shadow(
            surface, car_data["name"], self.font_large, COLOR_WHITE,
            (SCREEN_WIDTH // 2, card_y + 40), center=True
        )

        # Preview Mini Kendaraan
        preview_x = card_x + 65
        preview_y = card_y + 115
        self._draw_vehicle_preview(surface, car_data, preview_x, preview_y, True, is_tank)

        # Statistik Lengkap di Dalam Kartu
        stat_x = card_x + 130
        self._draw_mini_stat(surface, "Kecepatan", car_data["max_speed"] / 20.0, stat_x, card_y + 72, (255, 90, 90))
        self._draw_mini_stat(surface, "Armor HP", car_data["max_hp"] / 300.0, stat_x, card_y + 94, COLOR_HEALTH_GREEN)
        self._draw_mini_stat(surface, "Kelincahan", car_data["handling"] / 6.0, stat_x, card_y + 116, (140, 180, 255))
        
        if is_tank:
            self._draw_mini_stat(surface, "Meriam Blast", 1.0, stat_x, card_y + 138, (255, 200, 40))
        else:
            self._draw_mini_stat(surface, "Nitro Boost", car_data["nitro_duration"] / 250.0, stat_x, card_y + 138, COLOR_NITRO_CYAN)

        # Deskripsi Kemampuan
        skill_desc = "💣 [SPACE] Tembak Meriam Hancurkan Rintangan" if is_tank else "⚡ [SPACE] Turbo Nitro Melesat Cepat"
        skill_col = (255, 220, 80) if is_tank else (100, 240, 255)
        self.draw_text_with_shadow(surface, skill_desc, self.font_tiny, skill_col, (SCREEN_WIDTH // 2, card_y + 176), center=True)

        # Rekor Skor Tertinggi
        self.draw_text_with_shadow(
            surface, f"🏆 SKOR TERTINGGI: {highscore:,}", self.font_med, COLOR_GOLD,
            (SCREEN_WIDTH // 2, 442), center=True
        )

        # --- 5. TOMBOL MULAI & GARASI ---
        pulse_alpha = int(200 + 55 * math.sin(self.pulse_timer * 2.5))
        start_btn_w = 380
        start_btn_h = 44
        start_rect = pygame.Rect(SCREEN_WIDTH // 2 - start_btn_w // 2, 470, start_btn_w, start_btn_h)

        btn_bg = pygame.Surface((start_btn_w, start_btn_h), pygame.SRCALPHA)
        pygame.draw.rect(btn_bg, (220, 35, 55, pulse_alpha), (0, 0, start_btn_w, start_btn_h), border_radius=10)
        pygame.draw.rect(btn_bg, (255, 220, 100), (0, 0, start_btn_w, start_btn_h), width=2, border_radius=10)
        surface.blit(btn_bg, start_rect.topleft)

        btn_label = f"▶ MULAI MAIN & BELAJAR"
        self.draw_text_with_shadow(surface, btn_label, self.font_med, COLOR_WHITE, (start_rect.centerx, start_rect.centery), center=True)

        # Petunjuk Kontrol & Tombol Menu Lengkap
        btn_bar_y = 524
        bw = 120
        gap = 8
        total_w = 4 * bw + 3 * gap
        start_bx = SCREEN_WIDTH // 2 - total_w // 2

        btn_name_rect = pygame.Rect(start_bx, btn_bar_y, bw, 28)
        btn_del_rect = pygame.Rect(start_bx + (bw + gap), btn_bar_y, bw, 28)
        btn_mode_rect = pygame.Rect(start_bx + 2 * (bw + gap), btn_bar_y, bw, 28)
        btn_garage_rect = pygame.Rect(start_bx + 3 * (bw + gap), btn_bar_y, bw, 28)

        for b_rect, label, col in [
            (btn_name_rect, "✏️ [N] Nama", (30, 50, 75)),
            (btn_del_rect, "🗑️ [DEL] Reset", (65, 30, 35)),
            (btn_mode_rect, "🔄 [E] Mode", (30, 55, 45)),
            (btn_garage_rect, "🏎️ [G] Garasi", (40, 45, 65))
        ]:
            pygame.draw.rect(surface, col, b_rect, border_radius=6)
            pygame.draw.rect(surface, (80, 100, 130), b_rect, width=1, border_radius=6)
            self.draw_text_with_shadow(surface, label, self.font_tiny, COLOR_WHITE, (b_rect.centerx, b_rect.centery), center=True)

        hint_txt = f"Halo {p_name}! Lewati Gerbang Jawaban Benar untuk Hadiah Super Selebrasi & Pelindung Kebal!"
        self.draw_text_with_shadow(
            surface, hint_txt,
            self.font_tiny, (180, 220, 245), (SCREEN_WIDTH // 2, 566), center=True
        )

        # Simpan tombol untuk interaksi mouse
        self.menu_buttons = {
            "tab_edu_math": tab_math_rect,
            "tab_edu_vocab": tab_vocab_rect,
            "tab_car": tab_car_rect,
            "tab_tank": tab_tank_rect,
            "prev": prev_btn_rect,
            "next": next_btn_rect,
            "card": card_rect,
            "start": start_rect,
            "btn_name": btn_name_rect,
            "btn_del": btn_del_rect,
            "btn_mode": btn_mode_rect,
            "garage": btn_garage_rect,
            **grade_buttons
        }

    def draw_name_input(self, surface, current_name, cursor_timer):
        self.pulse_timer += 0.05
        bg_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        bg_overlay.fill((10, 14, 22, 245))
        surface.blit(bg_overlay, (0, 0))

        # Dialog Box Card
        card_w, card_h = 520, 360
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = (SCREEN_HEIGHT - card_h) // 2 - 10

        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (22, 28, 42, 250), (0, 0, card_w, card_h), border_radius=16)
        pygame.draw.rect(card_surf, (0, 230, 255), (0, 0, card_w, card_h), width=2, border_radius=16)
        surface.blit(card_surf, (card_x, card_y))

        # Header Title
        self.draw_text_with_shadow(
            surface, "🏎️ PROFIL PEMBALAP KHANSA 🏆", self.font_large, COLOR_GOLD,
            (SCREEN_WIDTH // 2, card_y + 35), center=True
        )
        self.draw_text_with_shadow(
            surface, "Masukkan nama kamu untuk memulai petualangan balapan & edukasi:",
            self.font_small, (200, 215, 235), (SCREEN_WIDTH // 2, card_y + 70), center=True
        )

        # Input Box
        box_w, box_h = 380, 52
        box_x = (SCREEN_WIDTH - box_w) // 2
        box_y = card_y + 115
        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
        self.name_input_box_rect = box_rect

        pygame.draw.rect(surface, (14, 17, 26), box_rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_NITRO_CYAN, box_rect, width=2, border_radius=8)

        # Display typed name or placeholder
        cursor = "|" if (cursor_timer % 40 < 20) else ""
        if current_name.strip():
            display_str = current_name + cursor
            txt_col = COLOR_WHITE
        else:
            display_str = "Ketik nama kamu di sini..." if not cursor else cursor
            txt_col = (130, 140, 160) if not current_name else COLOR_WHITE

        self.draw_text_with_shadow(
            surface, display_str, self.font_large, txt_col,
            (box_rect.centerx, box_rect.centery), center=True
        )

        # Petunjuk Keyboard
        self.draw_text_with_shadow(
            surface, "Maksimal 15 karakter  |  Tekan [ENTER] untuk menyimpan",
            self.font_tiny, (170, 185, 205), (SCREEN_WIDTH // 2, card_y + 185), center=True
        )

        # Tombol Simpan & Lanjutkan
        btn_w, btn_h = 340, 48
        btn_x = (SCREEN_WIDTH - btn_w) // 2
        btn_y = card_y + 215
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        self.name_submit_btn_rect = btn_rect

        pulse_alpha = int(210 + 45 * math.sin(self.pulse_timer * 3))
        btn_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, (220, 35, 55, pulse_alpha), (0, 0, btn_w, btn_h), border_radius=10)
        pygame.draw.rect(btn_surf, (255, 220, 100), (0, 0, btn_w, btn_h), width=2, border_radius=10)
        surface.blit(btn_surf, (btn_x, btn_y))

        self.draw_text_with_shadow(
            surface, "▶ SIMPAN & MULAI BALAPAN", self.font_med, COLOR_WHITE,
            (btn_rect.centerx, btn_rect.centery), center=True
        )

        # Info Penyimpanan Otomatis
        self.draw_text_with_shadow(
            surface, "💾 Data profil, koin, & skor tersimpan otomatis untuk sesi berikutnya!",
            self.font_tiny, (160, 230, 180), (SCREEN_WIDTH // 2, card_y + 295), center=True
        )

    def draw_confirm_delete(self, surface, player_name):
        bg_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        bg_overlay.fill((10, 12, 20, 240))
        surface.blit(bg_overlay, (0, 0))

        card_w, card_h = 480, 260
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = (SCREEN_HEIGHT - card_h) // 2

        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (28, 20, 25, 250), (0, 0, card_w, card_h), border_radius=14)
        pygame.draw.rect(card_surf, (255, 75, 75), (0, 0, card_w, card_h), width=2, border_radius=14)
        surface.blit(card_surf, (card_x, card_y))

        self.draw_text_with_shadow(
            surface, "⚠️ KONFIRMASI HAPUS DATA", self.font_large, (255, 80, 80),
            (SCREEN_WIDTH // 2, card_y + 35), center=True
        )
        self.draw_text_with_shadow(
            surface, f"Apakah kamu yakin ingin mereset profil '{player_name}'?",
            self.font_med, COLOR_WHITE, (SCREEN_WIDTH // 2, card_y + 75), center=True
        )
        self.draw_text_with_shadow(
            surface, "Seluruh rekor skor, koin, dan progres edukasi akan dihapus.",
            self.font_small, (220, 180, 180), (SCREEN_WIDTH // 2, card_y + 110), center=True
        )

        # Pilihan Tombol
        btn_y = card_y + 160
        y_rect = pygame.Rect(SCREEN_WIDTH // 2 - 190, btn_y, 175, 44)
        pygame.draw.rect(surface, (180, 30, 40), y_rect, border_radius=8)
        pygame.draw.rect(surface, (255, 100, 100), y_rect, width=2, border_radius=8)
        self.draw_text_with_shadow(surface, "[Y] YA, HAPUS", self.font_small, COLOR_WHITE, (y_rect.centerx, y_rect.centery), center=True)
        self.confirm_yes_rect = y_rect

        n_rect = pygame.Rect(SCREEN_WIDTH // 2 + 15, btn_y, 175, 44)
        pygame.draw.rect(surface, (35, 45, 65), n_rect, border_radius=8)
        pygame.draw.rect(surface, (100, 140, 190), n_rect, width=2, border_radius=8)
        self.draw_text_with_shadow(surface, "[N] BATAL", self.font_small, COLOR_WHITE, (n_rect.centerx, n_rect.centery), center=True)
        self.confirm_no_rect = n_rect


    def draw_garage(self, surface, current_idx, car_keys):
        self.pulse_timer += 0.05
        surface.fill((15, 18, 26))

        self.draw_text_with_shadow(
            surface, "GARASI: PILIH MOBIL ATAU TANK", self.font_title, COLOR_GOLD,
            (SCREEN_WIDTH // 2, 45), center=True
        )
        self.draw_text_with_shadow(
            surface, "Klik pada kendaraan untuk memilih langsung, lalu tekan MULAI!",
            self.font_med, (200, 215, 235), (SCREEN_WIDTH // 2, 85), center=True
        )

        # Tampilkan 5 Kendaraan Side-by-Side
        card_w = 136
        card_h = 360
        gap = 14
        total_w = len(car_keys) * card_w + (len(car_keys) - 1) * gap
        start_x = (SCREEN_WIDTH - total_w) // 2

        self.garage_cards = []

        for i, key in enumerate(car_keys):
            data = CARS_DATA[key]
            is_tank = data.get("type") == "tank"
            cx = start_x + i * (card_w + gap)
            cy = 120
            is_selected = (i == current_idx)

            this_card_rect = pygame.Rect(cx, cy, card_w, card_h)
            self.garage_cards.append((this_card_rect, key, i))

            card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
            bg_color = (32, 40, 58, 245) if is_selected else (20, 24, 34, 190)
            pygame.draw.rect(card_surf, bg_color, (0, 0, card_w, card_h), border_radius=10)

            border_col = data["glow_color"] if is_selected else (60, 68, 82)
            border_w = 3 if is_selected else 1
            pygame.draw.rect(card_surf, border_col, (0, 0, card_w, card_h), width=border_w, border_radius=10)
            surface.blit(card_surf, (cx, cy))

            # Tipe Badge
            badge_txt = "🛡️ TANK" if is_tank else "🏎️ MOBIL"
            badge_col = (255, 190, 40) if is_tank else COLOR_NITRO_CYAN
            self.draw_text_with_shadow(surface, badge_txt, self.font_tiny, badge_col, (cx + card_w // 2, cy + 18), center=True)

            # Nama Kendaraan
            self.draw_text_with_shadow(
                surface, data["name"], self.font_small, COLOR_WHITE if is_selected else (170, 175, 190),
                (cx + card_w // 2, cy + 38), center=True
            )

            # Preview Kendaraan
            preview_y = cy + 115
            self._draw_vehicle_preview(surface, data, cx + card_w // 2, preview_y, is_selected, is_tank)

            # Statistik
            stat_y = cy + 175
            self._draw_stat_bar(surface, "Kecepatan", data["max_speed"] / 20.0, cx + 10, stat_y, (255, 80, 80), bar_w=116)
            self._draw_stat_bar(surface, "Daya Tahan HP", data["max_hp"] / 300.0, cx + 10, stat_y + 36, COLOR_HEALTH_GREEN, bar_w=116)

            if is_tank:
                self._draw_stat_bar(surface, "Tembak Meriam", 1.0, cx + 10, stat_y + 72, (255, 200, 40), bar_w=116)
            else:
                self._draw_stat_bar(surface, "Nitro Boost", data["nitro_duration"] / 250.0, cx + 10, stat_y + 72, COLOR_NITRO_CYAN, bar_w=116)

            # Keahlian Spesial Text
            skill_txt = "💥 TEMBAK [SPACE]" if is_tank else "⚡ NITRO [SPACE]"
            skill_col = (255, 210, 50) if is_tank else COLOR_NITRO_CYAN
            self.draw_text_with_shadow(surface, skill_txt, self.font_tiny, skill_col, (cx + card_w // 2, cy + 295), center=True)

            if is_selected:
                sel_badge = self.font_small.render("▶ TERPILIH ◀", True, COLOR_GOLD)
                surface.blit(sel_badge, sel_badge.get_rect(center=(cx + card_w // 2, cy + card_h - 22)))

        # Tombol Mulai di Bawah Garasi
        start_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 160, 500, 320, 42)
        pygame.draw.rect(surface, (220, 35, 55), start_btn_rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_GOLD, start_btn_rect, width=2, border_radius=8)
        self.draw_text_with_shadow(surface, "▶ MULAI BALAPAN [SPACE]", self.font_med, COLOR_WHITE, (start_btn_rect.centerx, start_btn_rect.centery), center=True)
        self.garage_start_btn = start_btn_rect

        # Petunjuk Kontrol Garasi
        self.draw_text_with_shadow(
            surface, "[PANAH KIRI / KANAN] Ganti Kendaraan   |   [ENTER / SPACE] Mulai   |   [ESC] Menu",
            self.font_small, (200, 210, 230), (SCREEN_WIDTH // 2, 560), center=True
        )

    def _draw_mini_stat(self, surface, label, ratio, x, y, color):
        lbl = self.font_small.render(label, True, (200, 205, 215))
        surface.blit(lbl, (x, y))
        bar_w = 160
        bar_h = 8
        bx = x + 130
        pygame.draw.rect(surface, (40, 45, 60), (bx, y + 4, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(surface, color, (bx, y + 4, int(bar_w * min(1.0, ratio)), bar_h), border_radius=4)

    def _draw_stat_bar(self, surface, label, ratio, x, y, color, bar_w=180):
        lbl = self.font_tiny.render(label, True, (190, 200, 215))
        surface.blit(lbl, (x, y))
        bar_h = 8
        pygame.draw.rect(surface, (35, 40, 52), (x, y + 15, bar_w, bar_h), border_radius=3)
        fill_w = int(bar_w * max(0.0, min(1.0, ratio)))
        pygame.draw.rect(surface, color, (x, y + 15, fill_w, bar_h), border_radius=3)

    def _draw_vehicle_preview(self, surface, data, cx, cy, is_selected, is_tank):
        w, h = (38, 62) if is_tank else (32, 60)
        hw, hh = w // 2, h // 2

        if is_selected:
            glow = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*data["glow_color"], 75), (0, 0, w + 20, h + 20), border_radius=12)
            surface.blit(glow, (cx - hw - 10, cy - hh - 10))

        if is_tank:
            # Render Tank Mini
            # Rantai
            tread_w = 8
            for tx in (cx - hw, cx + hw - tread_w):
                pygame.draw.rect(surface, (30, 32, 35), (tx, cy - hh, tread_w, h), border_radius=3)
            # Bodi
            pygame.draw.rect(surface, data["primary_color"], (cx - hw + 6, cy - hh + 4, w - 12, h - 8), border_radius=4)
            # Laras Meriam
            pygame.draw.rect(surface, (60, 65, 70), (cx - 3, cy - hh - 12, 6, 20), border_radius=1)
            # Kubah Turret
            pygame.draw.rect(surface, data["stripe_color"], (cx - 9, cy - 8, 18, 18), border_radius=5)
        else:
            # Render Mobil Mini
            for wx in (cx - hw - 1, cx + hw - 4):
                for wy in (cy - hh + 5, cy + hh - 16):
                    pygame.draw.rect(surface, (25, 25, 30), (wx, wy, 5, 11), border_radius=2)
            pygame.draw.rect(surface, data["primary_color"], (cx - hw, cy - hh, w, h), border_radius=6)
            pygame.draw.rect(surface, data["stripe_color"], (cx - 3, cy - hh + 2, 6, h - 4), border_radius=1)
            pygame.draw.rect(surface, (30, 45, 60), (cx - hw + 4, cy - hh + 12, w - 8, 10), border_radius=2)
            # Kaca Belakang & Lampu Lengkap
            pygame.draw.rect(surface, (25, 35, 50), (cx - hw + 5, cy + hh - 18, w - 10, 8), border_radius=2)
            # Lampu Depan
            pygame.draw.rect(surface, (255, 255, 220), (cx - hw + 2, cy - hh + 1, 5, 3), border_radius=1)
            pygame.draw.rect(surface, (255, 255, 220), (cx + hw - 7, cy - hh + 1, 5, 3), border_radius=1)
            # Lampu Belakang
            pygame.draw.rect(surface, (255, 40, 40), (cx - hw + 2, cy + hh - 4, 5, 3), border_radius=1)
            pygame.draw.rect(surface, (255, 40, 40), (cx + hw - 7, cy + hh - 4, 5, 3), border_radius=1)

    def draw_hud(self, surface, player, score, highscore, biome, math_manager=None, vocab_manager=None, edu_mode=EDU_MODE_MATH):
        # 1. Panel Atas (Skor, Koin, Jarak, Tipe)
        header_surf = pygame.Surface((SCREEN_WIDTH, 48), pygame.SRCALPHA)
        header_surf.fill((16, 20, 30, 220))
        pygame.draw.line(header_surf, (60, 70, 90), (0, 47), (SCREEN_WIDTH, 47), 1)
        surface.blit(header_surf, (0, 0))

        self.draw_text_with_shadow(surface, f"SKOR: {score:,}", self.font_med, COLOR_WHITE, (20, 14))
        self.draw_text_with_shadow(surface, f"TOP: {highscore:,}", self.font_small, COLOR_GOLD, (190, 16))

        # Koin
        coin_icon = pygame.Surface((18, 18), pygame.SRCALPHA)
        pygame.draw.circle(coin_icon, COLOR_GOLD, (9, 9), 8)
        pygame.draw.circle(coin_icon, (255, 255, 180), (9, 9), 5)
        surface.blit(coin_icon, (315, 15))
        self.draw_text_with_shadow(surface, f"x {player.coins}", self.font_med, COLOR_GOLD, (338, 14))

        # Informasi Kosa Kata Dikuasai / Jarak
        if edu_mode == EDU_MODE_VOCAB and vocab_manager:
            m_cnt = len(getattr(vocab_manager, 'words_learned', set()))
            self.draw_text_with_shadow(surface, f"📚 {m_cnt}/3000 KATA", self.font_med, COLOR_GOLD, (420, 14))
        else:
            distance_km = player.distance / 1000.0
            self.draw_text_with_shadow(surface, f"JARAK: {distance_km:.2f} km", self.font_med, COLOR_NITRO_CYAN, (440, 14))

        # Tipe Kendaraan Tag
        is_tank = (player.vehicle_type == "tank")
        veh_tag = "🛡️ TANK" if is_tank else "🏎️ MOBIL"
        tag_col = (255, 200, 40) if is_tank else COLOR_NITRO_CYAN
        self.draw_text_with_shadow(surface, veh_tag, self.font_med, tag_col, (635, 14))

        # --- 2. BANNER EDUKASI (MATEMATIKA / KOSA KATA INGGRIS) DI ATAS JALUR ---
        active_edu = vocab_manager if (edu_mode == EDU_MODE_VOCAB) else math_manager
        if active_edu and active_edu.current_question:
            q_text = active_edu.current_question.question_text
            banner_w = 480
            banner_h = 36
            bx = ROAD_LEFT - 10
            by = 54

            b_surf = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
            pygame.draw.rect(b_surf, (15, 20, 34, 230), (0, 0, banner_w, banner_h), border_radius=8)
            border_banner = COLOR_GOLD if (edu_mode == EDU_MODE_VOCAB) else (0, 235, 255)
            pygame.draw.rect(b_surf, border_banner, (0, 0, banner_w, banner_h), width=2, border_radius=8)
            surface.blit(b_surf, (bx, by))

            # Icon & Teks Soal / Kosa Kata
            if edu_mode == EDU_MODE_VOCAB:
                m_cnt = len(getattr(vocab_manager, 'words_learned', set()))
                is_incoming = getattr(vocab_manager, 'active_gate', None) is None
                prefix = "🔔 GERBANG DI DEPAN: " if is_incoming else "🔤 "
                q_label = f"{prefix}{q_text} 👉 PILIH GERBANG! (📚 {m_cnt}/3000)"
            else:
                is_incoming = getattr(math_manager, 'active_gate', None) is None
                prefix = "🔔 GERBANG DI DEPAN: " if is_incoming else "📐 SOAL: "
                q_label = f"{prefix}{q_text} 👉 PILIH GERBANG JAWABAN!"
            self.draw_text_with_shadow(surface, q_label, self.font_small, COLOR_WHITE, (bx + banner_w // 2, by + 18), center=True)

        # --- 3. POP-UP PUJIAN / FEEDBACK EDUKASI ---
        if active_edu and active_edu.feedback_timer > 0:
            fb_w = 540
            fb_h = 38
            fx = SCREEN_WIDTH // 2 - fb_w // 2
            fy = 96
            fb_surf = pygame.Surface((fb_w, fb_h), pygame.SRCALPHA)
            pygame.draw.rect(fb_surf, (20, 25, 40, 240), (0, 0, fb_w, fb_h), border_radius=8)
            pygame.draw.rect(fb_surf, active_edu.feedback_color, (0, 0, fb_w, fb_h), width=2, border_radius=8)
            surface.blit(fb_surf, (fx, fy))

            self.draw_text_with_shadow(
                surface, active_edu.feedback_text, self.font_small, active_edu.feedback_color,
                (SCREEN_WIDTH // 2, fy + 19), center=True
            )

        # --- 4. DASHBOARD BAWAH (SPEEDOMETER, HP, WEAPON) ---
        # Ditempatkan sepenuhnya di bahu kiri jalan (x=8 sampai 152) agar TIDAK PERNAH menutupi kendaraan atau jalur jalan!
        dash_w, dash_h = 144, 120
        dash_x = 8
        dash_y = SCREEN_HEIGHT - dash_h - 10
        dash_surf = pygame.Surface((dash_w, dash_h), pygame.SRCALPHA)
        pygame.draw.rect(dash_surf, (15, 18, 28, 230), (0, 0, dash_w, dash_h), border_radius=10)
        border_c = (255, 180, 40) if is_tank else (55, 65, 85)
        pygame.draw.rect(dash_surf, border_c, (0, 0, dash_w, dash_h), width=2, border_radius=10)
        surface.blit(dash_surf, (dash_x, dash_y))

        # Speedometer Digital
        speed_kmh = int(player.speed * 16.5)
        speed_col = (255, 210, 50) if is_tank else COLOR_WHITE
        if player.is_nitro_active:
            speed_col = COLOR_NITRO_CYAN

        self.draw_text_with_shadow(surface, f"{speed_kmh:03d} km/h", self.font_med, speed_col, (dash_x + dash_w // 2, dash_y + 16), center=True)

        # Bar HP
        hp_ratio = max(0.0, player.hp / player.max_hp)
        hp_color = COLOR_HEALTH_GREEN if hp_ratio > 0.4 else COLOR_HEALTH_RED
        self.draw_text_with_shadow(surface, "HP", self.font_tiny, hp_color, (dash_x + 18, dash_y + 44), center=True)
        pygame.draw.rect(surface, (40, 45, 55), (dash_x + 36, dash_y + 38, 96, 12), border_radius=3)
        pygame.draw.rect(surface, hp_color, (dash_x + 36, dash_y + 38, int(96 * hp_ratio), 12), border_radius=3)

        # Bar Kedua: MERIAM (untuk Tank) atau NITRO (untuk Mobil)
        if is_tank:
            cannon_ready = (player.shoot_timer <= 0)
            c_col = (255, 210, 40) if cannon_ready else (140, 145, 155)
            c_txt = "CAN"
            self.draw_text_with_shadow(surface, c_txt, self.font_tiny, c_col, (dash_x + 18, dash_y + 68), center=True)
            reload_ratio = 1.0 if cannon_ready else 1.0 - (player.shoot_timer / player.cannon_cooldown)
            pygame.draw.rect(surface, (40, 45, 55), (dash_x + 36, dash_y + 62, 96, 12), border_radius=3)
            pygame.draw.rect(surface, c_col, (dash_x + 36, dash_y + 62, int(96 * reload_ratio), 12), border_radius=3)
        else:
            nitro_ratio = max(0.0, player.nitro / player.max_nitro)
            self.draw_text_with_shadow(surface, "N2O", self.font_tiny, COLOR_NITRO_CYAN, (dash_x + 18, dash_y + 68), center=True)
            pygame.draw.rect(surface, (40, 45, 55), (dash_x + 36, dash_y + 62, 96, 12), border_radius=3)
            pygame.draw.rect(surface, COLOR_NITRO_CYAN, (dash_x + 36, dash_y + 62, int(96 * nitro_ratio), 12), border_radius=3)

        # Bar Ketiga: PERISAI SUPER KEBAL (jika aktif) / Nama Pemain
        if player.super_shield_timer > 0:
            shield_ratio = player.super_shield_timer / 420.0
            shield_hue = int((pygame.time.get_ticks() / 20) % 360)
            shield_color = pygame.Color(0)
            shield_color.hsva = (shield_hue, 100, 100, 100)
            self.draw_text_with_shadow(surface, "KEBAL", self.font_tiny, shield_color, (dash_x + dash_w // 2, dash_y + 88), center=True)
            pygame.draw.rect(surface, (30, 35, 50), (dash_x + 14, dash_y + 98, 116, 8), border_radius=2)
            pygame.draw.rect(surface, shield_color, (dash_x + 14, dash_y + 98, int(116 * shield_ratio), 8), border_radius=2)
        else:
            name_label = getattr(player, 'player_name', 'Khansa')
            self.draw_text_with_shadow(surface, f"👤 {name_label}", self.font_tiny, (170, 185, 205), (dash_x + dash_w // 2, dash_y + 94), center=True)

        if player.speed > 12.0:
            self._draw_speed_lines(surface, player.speed)


    def draw_math_gates(self, surface, math_manager=None, vocab_manager=None, edu_mode=EDU_MODE_MATH):
        """Menggambar gerbang jawaban edukasi (Matematika / Kosa Kata) pada lintasan jalan."""
        if edu_mode == EDU_MODE_VOCAB and vocab_manager and vocab_manager.active_gate:
            vocab_manager.active_gate.draw(surface, (self.font_med, self.font_small, self.font_tiny))
        elif math_manager and math_manager.active_gate:
            math_manager.active_gate.draw(surface, self.font_large)

    def _draw_speed_lines(self, surface, speed):
        import random
        intensity = int((speed - 12.0) * 4)
        line_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for _ in range(intensity):
            lx = random.choice([random.randint(0, ROAD_LEFT - 10), random.randint(ROAD_RIGHT + 10, SCREEN_WIDTH)])
            ly = random.randint(0, SCREEN_HEIGHT - 80)
            len_line = random.randint(30, 90)
            alpha = random.randint(40, 110)
            pygame.draw.line(line_surf, (255, 255, 255, alpha), (lx, ly), (lx, ly + len_line), 2)
        surface.blit(line_surf, (0, 0))

    def draw_pause(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 12, 20, 180))
        surface.blit(overlay, (0, 0))

        self.draw_text_with_shadow(surface, "GAME DIHENTIKAN SEMENTARA", self.font_title, COLOR_WHITE, (SCREEN_WIDTH // 2, 250), center=True)
        self.draw_text_with_shadow(surface, "Tekan [P] atau [ESC] untuk melanjutkan balapan", self.font_med, COLOR_NITRO_CYAN, (SCREEN_WIDTH // 2, 310), center=True)
        self.draw_text_with_shadow(surface, "Tekan [M] untuk kembali ke Menu Utama", self.font_small, (200, 210, 220), (SCREEN_WIDTH // 2, 350), center=True)

    def draw_game_over(self, surface, score, highscore, coins, distance, is_new_record, math_manager=None, vocab_manager=None, edu_mode=EDU_MODE_MATH):
        self.pulse_timer += 0.05
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((18, 10, 15, 225))
        surface.blit(overlay, (0, 0))

        self.draw_text_with_shadow(surface, "KENDARAAN HANCUR!", self.font_title, (255, 60, 60), (SCREEN_WIDTH // 2, 60), center=True)
        self.draw_text_with_shadow(surface, "GAME OVER", self.font_large, COLOR_WHITE, (SCREEN_WIDTH // 2, 105), center=True)

        if is_new_record:
            rec_glow = int(math.sin(self.pulse_timer * 3) * 20)
            self.draw_text_with_shadow(surface, "🎉 REKOR SKOR BARU DICAPAI! 🎉", self.font_large, (255, 230 + rec_glow, 50), (SCREEN_WIDTH // 2, 142), center=True)

        # Kartu Hasil Balapan Kiri
        res_rect = pygame.Rect(SCREEN_WIDTH // 2 - 270, 160, 260, 220)
        res_surf = pygame.Surface((res_rect.width, res_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(res_surf, (28, 24, 34, 230), (0, 0, res_rect.width, res_rect.height), border_radius=12)
        pygame.draw.rect(res_surf, (80, 50, 65), (0, 0, res_rect.width, res_rect.height), width=2, border_radius=12)
        surface.blit(res_surf, res_rect.topleft)

        self.draw_text_with_shadow(surface, "🏁 HASIL BALAPAN", self.font_med, COLOR_GOLD, (res_rect.centerx, 180), center=True)
        self.draw_text_with_shadow(surface, f"Skor: {score:,}", self.font_large, COLOR_WHITE, (res_rect.centerx, 218), center=True)
        self.draw_text_with_shadow(surface, f"Jarak: {(distance / 1000.0):.2f} km", self.font_small, COLOR_NITRO_CYAN, (res_rect.centerx, 260), center=True)
        self.draw_text_with_shadow(surface, f"Koin: {coins} koin", self.font_small, COLOR_GOLD, (res_rect.centerx, 290), center=True)
        self.draw_text_with_shadow(surface, f"Top: {highscore:,}", self.font_tiny, (200, 190, 210), (res_rect.centerx, 345), center=True)

        # Kartu Rapor Belajar Edukasi Kanan (Matematika atau English Vocab)
        rap_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, 160, 260, 220)
        rap_surf = pygame.Surface((rap_rect.width, rap_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(rap_surf, (20, 32, 48, 235), (0, 0, rap_rect.width, rap_rect.height), border_radius=12)
        border_rap = COLOR_GOLD if (edu_mode == EDU_MODE_VOCAB) else (0, 200, 255)
        pygame.draw.rect(rap_surf, border_rap, (0, 0, rap_rect.width, rap_rect.height), width=2, border_radius=12)
        surface.blit(rap_surf, rap_rect.topleft)

        if edu_mode == EDU_MODE_VOCAB and vocab_manager:
            self.draw_text_with_shadow(surface, "📚 RAPOR KOSA KATA", self.font_med, COLOR_GOLD, (rap_rect.centerx, 180), center=True)
            v_name = vocab_manager.get_level_name()
            acc = vocab_manager.get_accuracy_percent()
            stars = "⭐" * vocab_manager.get_star_rating()
            title = vocab_manager.get_grade_title()

            self.draw_text_with_shadow(surface, v_name, self.font_tiny, (200, 220, 245), (rap_rect.centerx, 208), center=True)
            self.draw_text_with_shadow(surface, f"Benar: {vocab_manager.correct_answers} / {vocab_manager.total_questions} Kata", self.font_small, (50, 255, 120), (rap_rect.centerx, 236), center=True)
            self.draw_text_with_shadow(surface, f"Akurasi: {acc}%", self.font_med, COLOR_WHITE, (rap_rect.centerx, 262), center=True)
            self.draw_text_with_shadow(surface, f"{stars}", self.font_large, COLOR_GOLD, (rap_rect.centerx, 295), center=True)
            self.draw_text_with_shadow(surface, title, self.font_tiny, COLOR_GOLD, (rap_rect.centerx, 332), center=True)
            m_cnt = len(getattr(vocab_manager, 'words_learned', set()))
            self.draw_text_with_shadow(surface, f"🎯 Dikuasai: {m_cnt} / 3.000 Kata", self.font_tiny, (180, 210, 240), (rap_rect.centerx, 356), center=True)
        elif math_manager:
            self.draw_text_with_shadow(surface, "📊 RAPOR MATEMATIKA", self.font_med, (0, 230, 255), (rap_rect.centerx, 180), center=True)
            g_name = math_manager.get_grade_name()
            acc = math_manager.get_accuracy_percent()
            stars = "⭐" * math_manager.get_star_rating()
            title = math_manager.get_grade_title()

            self.draw_text_with_shadow(surface, g_name, self.font_tiny, (200, 220, 245), (rap_rect.centerx, 208), center=True)
            self.draw_text_with_shadow(surface, f"Benar: {math_manager.correct_answers} / {math_manager.total_questions} Soal", self.font_small, (50, 255, 120), (rap_rect.centerx, 236), center=True)
            self.draw_text_with_shadow(surface, f"Akurasi: {acc}%", self.font_med, COLOR_WHITE, (rap_rect.centerx, 262), center=True)
            self.draw_text_with_shadow(surface, f"{stars}", self.font_large, COLOR_GOLD, (rap_rect.centerx, 295), center=True)
            self.draw_text_with_shadow(surface, title, self.font_tiny, COLOR_GOLD, (rap_rect.centerx, 335), center=True)
        else:
            self.draw_text_with_shadow(surface, "Modul Belajar Aktif", self.font_small, COLOR_WHITE, (rap_rect.centerx, 260), center=True)

        self.draw_text_with_shadow(
            surface, "TEKAN [SPACE] / [ENTER] UNTUK MAIN LAGI", self.font_med, (255, 255, 255),
            (SCREEN_WIDTH // 2, 420), center=True
        )
        self.draw_text_with_shadow(
            surface, "[M] Menu Utama   |   [G] Garasi Kendaraan", self.font_small, (190, 200, 215),
            (SCREEN_WIDTH // 2, 460), center=True
        )
