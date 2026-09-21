"""
Modul Edukasi Kosa Kata Bahasa Inggris (3000 Vocab) - GameKhansa Mobil Legend.
Menyediakan bank 3.000 kosa kata bahasa Inggris - Indonesia bertingkat (Level 1 - 3),
gerbang portal jawaban adaptif di lajur jalan, sistem penilaian, dan pelacak rapor belajar anak.
"""

import math
import os
import json

import random
import pygame
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ROAD_LEFT, ROAD_RIGHT,
    NUM_LANES, LANE_WIDTH, LANE_CENTERS, COLOR_GOLD, COLOR_WHITE,
    VOCAB_LEVELS
)

# Cache data kosa kata agar dimuat sekali ke memori
_VOCAB_CACHE = None
_VOCAB_BY_LEVEL = {1: [], 2: [], 3: []}

def _load_vocab_data():
    global _VOCAB_CACHE, _VOCAB_BY_LEVEL
    if _VOCAB_CACHE is not None:
        return _VOCAB_CACHE

    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocab_data.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            _VOCAB_CACHE = json.load(f)
    except Exception as e:
        print(f"[Vocab] Gagal memuat vocab_data.json: {e}, memakai cadangan default.")
        _VOCAB_CACHE = [
            {"en": "car", "id": "Mobil", "level": 1, "category": "vehicles"},
            {"en": "speed", "id": "Kecepatan", "level": 1, "category": "racing"},
            {"en": "road", "id": "Jalan", "level": 1, "category": "racing"},
            {"en": "winner", "id": "Pemenang", "level": 1, "category": "racing"}
        ]

    # Kelompokkan berdasarkan level (1, 2, 3)
    _VOCAB_BY_LEVEL = {1: [], 2: [], 3: []}
    for item in _VOCAB_CACHE:
        lvl = item.get("level", 1)
        if lvl not in _VOCAB_BY_LEVEL:
            _VOCAB_BY_LEVEL[lvl] = []
        _VOCAB_BY_LEVEL[lvl].append(item)

    return _VOCAB_CACHE


class VocabQuestion:
    """Kelas penghasil pertanyaan kosa kata bahasa Inggris dengan pilihan jawaban di lajur balap."""
    def __init__(self, vocab_level=1):
        self.vocab_level = max(1, min(3, vocab_level))
        self.mode = "en_to_id"  # 'en_to_id' atau 'id_to_en'
        self.question_text = ""
        self.correct_answer = ""
        self.source_word = ""
        self.options = []  # 4 pilihan kata untuk 4 lajur
        self.generate()

    def generate(self):
        _load_vocab_data()
        pool = _VOCAB_BY_LEVEL.get(self.vocab_level)
        if not pool or len(pool) < 4:
            pool = _VOCAB_CACHE

        target_item = random.choice(pool)
        self.mode = random.choice(["en_to_id", "en_to_id", "id_to_en"])  # Dominan Inggris -> Indonesia

        if self.mode == "en_to_id":
            # Soal: Bahasa Inggris -> Tebak Arti Bahasa Indonesia
            en_word = target_item["en"].capitalize()
            id_word = target_item["id"]
            # Potong arti yang terlalu panjang agar pas di lajur
            if len(id_word) > 16:
                id_word = id_word.split()[0].capitalize()
            else:
                id_word = id_word.capitalize()

            self.source_word = en_word
            self.correct_answer = id_word
            self.question_text = f"Arti kata: '{en_word.upper()}' ?"

            # Cari 3 pengecoh (distractors) unik dari level yang sama
            options_set = {self.correct_answer}
            tries = 0
            while len(options_set) < NUM_LANES and tries < 50:
                tries += 1
                cand = random.choice(pool)["id"]
                if len(cand) > 16:
                    cand = cand.split()[0].capitalize()
                else:
                    cand = cand.capitalize()
                if cand not in options_set:
                    options_set.add(cand)

            self.options = list(options_set)

        else:
            # Soal: Bahasa Indonesia -> Tebak Kata Bahasa Inggris
            en_word = target_item["en"].capitalize()
            id_word = target_item["id"].split()[0].capitalize() if len(target_item["id"]) > 16 else target_item["id"].capitalize()

            self.source_word = id_word
            self.correct_answer = en_word
            self.question_text = f"B. Inggris: '{id_word.upper()}' ?"

            options_set = {self.correct_answer}
            tries = 0
            while len(options_set) < NUM_LANES and tries < 50:
                tries += 1
                cand = random.choice(pool)["en"].capitalize()
                if cand not in options_set:
                    options_set.add(cand)

            self.options = list(options_set)

        # Acak urutan opsi agar jawaban benar berada di lajur acak
        random.shuffle(self.options)


class VocabGate:
    """Gerbang Jawaban Kosa Kata yang melayang di atas jalur balap."""
    def __init__(self, question, start_y=-80):
        self.question = question
        self.y = start_y
        self.height = 44
        self.passed = False
        self.resolved = False
        self.blocked_lanes = {}  # lane_idx -> timer
        self.anim_tick = 0

    def update(self, scroll_speed):
        self.y += scroll_speed
        self.anim_tick += 1
        for k in list(self.blocked_lanes.keys()):
            self.blocked_lanes[k] -= 1
            if self.blocked_lanes[k] <= 0:
                del self.blocked_lanes[k]

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 60

    def check_collision(self, player_x, player_y, player_car=None):
        """Mengecek apakah kendaraan pemain melewati salah satu portal gerbang kosa kata."""
        if self.resolved:
            return None

        # Cek jika kendaraan mendekati gerbang
        if abs(player_y - self.y) < 32:
            closest_lane = 0
            min_dist = float("inf")
            for i, cx in enumerate(LANE_CENTERS):
                dist = abs(player_x - cx)
                if dist < min_dist:
                    min_dist = dist
                    closest_lane = i

            if min_dist < (LANE_WIDTH // 2 - 2):
                chosen_val = self.question.options[closest_lane]
                is_correct = (chosen_val == self.question.correct_answer)

                if is_correct:
                    self.resolved = True
                    return {
                        "is_correct": True,
                        "chosen_val": chosen_val,
                        "correct_val": self.question.correct_answer,
                        "question_text": self.question.question_text,
                        "source_word": self.question.source_word,
                        "lane": closest_lane
                    }
                else:
                    # Jawaban salah: TIDAK BISA LEWAT! Terblokir & terpental mundur
                    self.blocked_lanes[closest_lane] = 35
                    if player_car:
                        max_safe_y = SCREEN_HEIGHT - (player_car.height // 2 if hasattr(player_car, 'height') else 38) - 24
                        player_car.y = min(max_safe_y, max(player_car.y, self.y + 42))
                        player_car.speed = -3.5
                    return {
                        "is_correct": False,
                        "chosen_val": chosen_val,
                        "correct_val": self.question.correct_answer,
                        "question_text": self.question.question_text,
                        "source_word": self.question.source_word,
                        "lane": closest_lane,
                        "blocked": True
                    }

        return None

    def draw(self, surface, fonts):
        """Menggambar barisan portal bercahaya dengan teks kosa kata di tiap lajur jalan."""
        y_int = int(self.y)
        if y_int < -50 or y_int > SCREEN_HEIGHT + 40:
            return

        font_med, font_small, font_tiny = fonts

        # Garis balok horizontal penghubung antar portal kosa kata
        pygame.draw.line(surface, (85, 95, 125), (ROAD_LEFT + 10, y_int), (ROAD_RIGHT - 10, y_int), 4)

        # Overhead Gantry Penunjuk Soal Kosa Kata Langsung di Atas Gerbang
        board_w = ROAD_RIGHT - ROAD_LEFT - 16
        board_h = 28
        board_x = ROAD_LEFT + 8
        board_y = y_int - 48

        # Tiang gantry di kiri dan kanan jalan
        pygame.draw.rect(surface, (70, 80, 100), (ROAD_LEFT + 2, board_y - 2, 8, board_h + 52), border_radius=2)
        pygame.draw.rect(surface, (70, 80, 100), (ROAD_RIGHT - 10, board_y - 2, 8, board_h + 52), border_radius=2)

        # Plang Soal
        board_surf = pygame.Surface((board_w, board_h), pygame.SRCALPHA)
        pygame.draw.rect(board_surf, (15, 22, 38, 245), (0, 0, board_w, board_h), border_radius=6)
        pygame.draw.rect(board_surf, (255, 215, 0), (0, 0, board_w, board_h), width=2, border_radius=6)
        surface.blit(board_surf, (board_x, board_y))

        # Teks Soal di atas gerbang (Bersih & Rapi)
        q_label = f"🔤 ARTI KATA: \"{self.question.source_word.upper()}\""
        q_surf = font_small.render(q_label, True, (255, 225, 50))
        q_rect = q_surf.get_rect(center=(SCREEN_WIDTH // 2, board_y + board_h // 2))
        surface.blit(q_surf, q_rect)

        # Gambar setiap gerbang portal di tiap lajur
        for i, cx in enumerate(LANE_CENTERS):
            val = str(self.question.options[i])
            pw = LANE_WIDTH - 12
            ph = 44
            px = cx - pw // 2
            py = y_int - ph // 2

            is_blocked = (i in self.blocked_lanes and self.blocked_lanes[i] > 0)

            # Efek neon portal bercahaya
            gate_surf = pygame.Surface((pw, ph), pygame.SRCALPHA)

            if is_blocked:
                # Perisai Merah Berkedip TERTUTUP / SALAH!
                pygame.draw.rect(gate_surf, (220, 20, 20, 240), (0, 0, pw, ph), border_radius=10)
                pygame.draw.rect(gate_surf, (255, 80, 80), (0, 0, pw, ph), width=4, border_radius=10)
                pygame.draw.line(gate_surf, (255, 255, 255, 200), (4, 4), (pw - 4, ph - 4), 3)
                pygame.draw.line(gate_surf, (255, 255, 255, 200), (4, ph - 4), (pw - 4, 4), 3)
                surface.blit(gate_surf, (px, py))

                # Teks ⛔ SALAH
                warn_surf = font_small.render("⛔ SALAH", True, (255, 255, 255))
                w_rect = warn_surf.get_rect(center=(cx, y_int))
                surface.blit(warn_surf, w_rect)
                continue
            else:
                # Portal Netral Seragam untuk Seluruh Lajur (Bebas Petunjuk - User Berpikir & Memilih Sendiri)
                pygame.draw.rect(gate_surf, (16, 24, 40, 235), (0, 0, pw, ph), border_radius=10)
                border_col = (0, 225, 255)
                pygame.draw.rect(gate_surf, border_col, (0, 0, pw, ph), width=3, border_radius=10)

            surface.blit(gate_surf, (px, py))

            # Pilih font yang pas dengan lebar portal
            chosen_font = font_med
            if chosen_font.size(val)[0] > pw - 12:
                chosen_font = font_small
            if chosen_font.size(val)[0] > pw - 10:
                chosen_font = font_tiny

            # Pangkas jika masih kepanjangan
            rendered_str = val
            while len(rendered_str) > 3 and chosen_font.size(rendered_str)[0] > pw - 8:
                rendered_str = rendered_str[:-2] + ".."

            # Teks Pilihan Kosa Kata
            txt_surf = chosen_font.render(rendered_str, True, COLOR_WHITE)
            txt_rect = txt_surf.get_rect(center=(cx, y_int))
            shadow_surf = chosen_font.render(rendered_str, True, (10, 15, 25))
            surface.blit(shadow_surf, (txt_rect.x + 2, txt_rect.y + 2))
            surface.blit(txt_surf, txt_rect)

            # Dekorasi Lampu Indikator Atas
            pygame.draw.circle(surface, border_col, (cx, py - 4), 4)


class VocabManager:
    """Manajer Kuis & Edukasi Kosa Kata Bahasa Inggris GameKhansa (Target 3000 Kata)."""
    def __init__(self, vocab_level=1):
        self.vocab_level = vocab_level  # 1: Level 1, 2: Level 2, 3: Level 3
        self.current_question = None
        self.active_gate = None
        self.spawn_timer = 0
        self.spawn_interval = 520  # Muncul gerbang setiap ~8.5 detik

        # Feedback & Pujian
        self.feedback_text = ""
        self.feedback_color = COLOR_GOLD
        self.feedback_timer = 0

        # Rapor & Statistik Belajar
        self.total_questions = 0
        self.correct_answers = 0
        self.current_streak = 0
        self.best_streak = 0
        self.total_vocab_score = 0
        self.words_learned = set()
        self.last_quote = None

        # Inisialisasi Bank Kata & Soal Pertama
        _load_vocab_data()
        self.generate_new_question()

    def set_level(self, level):
        self.vocab_level = max(1, min(3, level))
        self.generate_new_question()

    def reset_stats(self, clear_mastered=False):
        self.total_questions = 0
        self.correct_answers = 0
        self.current_streak = 0
        self.best_streak = 0
        self.total_vocab_score = 0
        if clear_mastered:
            self.words_learned.clear()
        self.active_gate = None
        self.feedback_timer = 0
        self.spawn_timer = 180  # Jeda awal sebelum gerbang pertama
        self.generate_new_question()

    def generate_new_question(self):
        self.current_question = VocabQuestion(self.vocab_level)

    def update(self, player_speed, player):
        """Memperbarui posisi gerbang kosa kata dan menghitung tabrakan jawaban pemain."""
        # 1. Update Timer Feedback
        if self.feedback_timer > 0:
            self.feedback_timer -= 1

        # 2. Spawner Gerbang Kosa Kata
        if self.active_gate is None:
            self.spawn_timer += 1
            # SETENGAH JALAN (HALFWAY): Munculkan soal baru jauh sebelum gerbang tiba!
            if self.spawn_timer == self.spawn_interval // 2:
                self.generate_new_question()
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                if self.current_question is None:
                    self.generate_new_question()
                self.active_gate = VocabGate(self.current_question, start_y=-90)

        # 3. Update & Deteksi Benturan Gerbang
        result = None
        if self.active_gate:
            self.active_gate.update(player_speed)

            # Cek tabrakan kendaraan pemain dengan gerbang
            col_res = self.active_gate.check_collision(player.x, player.y, player)
            if col_res:
                result = self._handle_answer(col_res, player)

            # Jika gerbang sudah lewat layar
            if self.active_gate.is_offscreen():
                if not self.active_gate.resolved:
                    # Terlewatkan tanpa memilih
                    corr = self.current_question.correct_answer
                    src = self.current_question.source_word
                    self.feedback_text = f"Terlewat! {src} = {corr}"
                    self.feedback_color = (255, 170, 70)
                    self.feedback_timer = 90
                self.active_gate = None

        return result

    def _handle_answer(self, res, player):
        is_corr = res["is_correct"]
        src = res.get("source_word", "")
        corr = res["correct_val"]

        if is_corr:
            self.total_questions += 1
            self.correct_answers += 1
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
            self.total_vocab_score += 500
            self.words_learned.add(src.lower())

            # Hadiah Super Istimewa dalam Balapan!
            player.super_shield_timer = 420  # 7 detik kebal bintang pelangi
            player.coins += 35               # Hujan 35 koin emas langsung
            player.add_hp(50)

            if player.vehicle_type == "tank":
                player.shoot_timer = 0       # Amunisi seketika siap tembak
                player.speed = min(player.base_max_speed * 1.25, max(player.speed + 4.0, 11.0))
            else:
                player.add_nitro(150)        # Isi penuh Nitro Turbo
                player.speed = min(player.base_max_speed * 1.35, max(player.speed + 5.0, 13.0))

            from .constants import MOTIVATION_TEMPLATES, GREAT_MINDS_QUOTES
            player_name = getattr(player, 'player_name', 'Khansa').upper()
            template = random.choice(MOTIVATION_TEMPLATES)
            praise = template.format(name=player_name)
            self.last_motivation = praise
            self.last_quote = random.choice(GREAT_MINDS_QUOTES)

            streak_txt = f" 🔥 Streak x{self.current_streak}" if self.current_streak > 1 else ""
            m_cnt = len(self.words_learned)
            self.feedback_text = f"🎁 {praise} '{src}' = '{corr}' (📚 {m_cnt}/3000 KATA){streak_txt}"
            self.feedback_color = (50, 255, 120)
            self.feedback_timer = 150
            return "correct"
        else:
            # Jawaban salah: Terblokir / Tidak bisa lewat!
            self.current_streak = 0
            self.feedback_text = f"⛔ ARTINYA SALAH! LAJUR TERBLOKIR! '{src}' ≠ '{res['chosen_val']}'. Belok cari arti yang benar!"
            self.feedback_color = (255, 60, 60)
            self.feedback_timer = 90
            return "wrong_blocked"

    def get_mastered_count(self):
        return len(self.words_learned)


    def get_accuracy_percent(self):
        if self.total_questions == 0:
            return 100
        return int((self.correct_answers / self.total_questions) * 100)

    def get_star_rating(self):
        if self.total_questions == 0:
            return 3
        acc = self.get_accuracy_percent()
        if acc >= 80:
            return 3
        elif acc >= 50:
            return 2
        return 1

    def get_grade_title(self):
        stars = self.get_star_rating()
        if stars == 3:
            return "🌟 VOCABULARY MASTER KHANSA 🌟"
        elif stars == 2:
            return "⭐ ENGLISH STAR KHANSA ⭐"
        return "🌱 ENGLISH EXPLORER 🌱"

    def get_level_name(self):
        info = VOCAB_LEVELS.get(self.vocab_level, VOCAB_LEVELS[1])
        return info["name"]
