"""
Modul Edukasi Matematika untuk Anak SD (Kelas 1 - 6) - GameKhansa Mobil Legend.
Menyediakan generator soal matematika adaptif sesuai kurikulum SD,
manajemen gerbang jawaban (Math Gates) di jalur balap, dan pelacak rapor prestasi anak.
"""

import math
import random
import pygame
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ROAD_LEFT, ROAD_RIGHT,
    NUM_LANES, LANE_WIDTH, LANE_CENTERS, COLOR_GOLD, COLOR_WHITE
)


class MathQuestion:
    """Kelas penghasil soal matematika ramah anak SD kelas 1 - 6."""
    def __init__(self, grade_level=2):
        self.grade_level = grade_level  # 1: Kelas 1-2, 2: Kelas 3-4, 3: Kelas 5-6
        self.question_text = ""
        self.correct_answer = 0
        self.options = []  # List of numbers for the lanes
        self.generate()

    def generate(self):
        if self.grade_level == 1:
            self._generate_grade_1_2()
        elif self.grade_level == 3:
            self._generate_grade_5_6()
        else:
            self._generate_grade_3_4()

        # Buat pilihan jawaban pengecoh (distractors)
        self.options = [self.correct_answer]
        while len(self.options) < NUM_LANES:
            delta = random.choice([-3, -2, -1, 1, 2, 3, 5, 10])
            wrong = self.correct_answer + delta
            if wrong >= 0 and wrong not in self.options:
                self.options.append(wrong)

        # Acak urutan agar jawaban benar berada di lajur acak
        random.shuffle(self.options)

    def _generate_grade_1_2(self):
        """Kelas 1 - 2 SD: Penjumlahan & Pengurangan dasar 1 - 20."""
        op = random.choice(["+", "-"])
        if op == "+":
            a = random.randint(1, 12)
            b = random.randint(1, 10)
            self.question_text = f"{a} + {b} = ?"
            self.correct_answer = a + b
        else:
            a = random.randint(4, 20)
            b = random.randint(1, a)
            self.question_text = f"{a} - {b} = ?"
            self.correct_answer = a - b

    def _generate_grade_3_4(self):
        """Kelas 3 - 4 SD: Perkalian tabel 1-10, Pembagian tanpa sisa, Penjumlahan puluhan."""
        op = random.choice(["x", ":", "+", "-"])
        if op == "x":
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            self.question_text = f"{a} x {b} = ?"
            self.correct_answer = a * b
        elif op == ":":
            b = random.randint(2, 9)
            ans = random.randint(2, 9)
            a = b * ans
            self.question_text = f"{a} : {b} = ?"
            self.correct_answer = ans
        elif op == "+":
            a = random.randint(15, 55)
            b = random.randint(10, 45)
            self.question_text = f"{a} + {b} = ?"
            self.correct_answer = a + b
        else:
            a = random.randint(30, 85)
            b = random.randint(10, a - 5)
            self.question_text = f"{a} - {b} = ?"
            self.correct_answer = a - b

    def _generate_grade_5_6(self):
        """Kelas 5 - 6 SD: Perkalian 2 digit, Pembagian cepat, Operasi campuran sederhana."""
        mode = random.choice(["mul2", "div2", "mixed1", "mixed2"])
        if mode == "mul2":
            a = random.randint(11, 22)
            b = random.randint(3, 8)
            self.question_text = f"{a} x {b} = ?"
            self.correct_answer = a * b
        elif mode == "div2":
            b = random.randint(4, 9)
            ans = random.randint(11, 18)
            a = b * ans
            self.question_text = f"{a} : {b} = ?"
            self.correct_answer = ans
        elif mode == "mixed1":
            # (a + b) x c
            a = random.randint(3, 12)
            b = random.randint(2, 8)
            c = random.randint(2, 5)
            self.question_text = f"({a} + {b}) x {c} = ?"
            self.correct_answer = (a + b) * c
        else:
            # a x b - c
            a = random.randint(4, 9)
            b = random.randint(4, 8)
            c = random.randint(3, 15)
            self.question_text = f"{a} x {b} - {c} = ?"
            self.correct_answer = (a * b) - c


class MathGate:
    """Gerbang Jawaban Matematika yang melayang di atas jalur balap."""
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
        # Kurangi timer blokir lajur salah
        for k in list(self.blocked_lanes.keys()):
            self.blocked_lanes[k] -= 1
            if self.blocked_lanes[k] <= 0:
                del self.blocked_lanes[k]

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 60

    def check_collision(self, player_x, player_y, player_car=None):
        """Mengecek benturan pemain dengan gerbang. Jawaban salah menahan mobil (tidak bisa lewat)."""
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
                    # Jawaban benar: Gerbang terbuka, mobil melesat tembus!
                    self.resolved = True
                    return {
                        "is_correct": True,
                        "chosen_val": chosen_val,
                        "correct_val": self.question.correct_answer,
                        "question_text": self.question.question_text,
                        "lane": closest_lane
                    }
                else:
                    # Jawaban salah: TIDAK BISA LEWAT! Dinding perisai menolak mobil mundur
                    self.blocked_lanes[closest_lane] = 35
                    if player_car:
                        # Tahan mobil di depan gerbang & pantulkan mundur (dibatasi agar selalu terlihat penuh)
                        max_safe_y = SCREEN_HEIGHT - (player_car.height // 2 if hasattr(player_car, 'height') else 38) - 24
                        player_car.y = min(max_safe_y, max(player_car.y, self.y + 42))
                        player_car.speed = -3.5
                    return {
                        "is_correct": False,
                        "chosen_val": chosen_val,
                        "correct_val": self.question.correct_answer,
                        "question_text": self.question.question_text,
                        "lane": closest_lane,
                        "blocked": True
                    }

        return None

    def draw(self, surface, font):
        """Menggambar barisan gerbang portal bercahaya di masing-masing lajur jalan."""
        y_int = int(self.y)
        if y_int < -50 or y_int > SCREEN_HEIGHT + 40:
            return

        # Garis balok horizontal penghubung antar portal
        pygame.draw.line(surface, (70, 85, 115), (ROAD_LEFT + 10, y_int), (ROAD_RIGHT - 10, y_int), 4)

        # Overhead Gantry Penunjuk Soal Matematika Langsung di Atas Gerbang
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
        pygame.draw.rect(board_surf, (0, 230, 255), (0, 0, board_w, board_h), width=2, border_radius=6)
        surface.blit(board_surf, (board_x, board_y))

        # Teks Soal di atas gerbang
        q_label = f"📐 SOAL: {self.question.question_text} = ? 👉 PILIH JAWABAN BENAR!"
        q_surf = font.render(q_label, True, (0, 240, 255))
        q_rect = q_surf.get_rect(center=(SCREEN_WIDTH // 2, board_y + board_h // 2))
        surface.blit(q_surf, q_rect)

        # Gambar setiap gerbang portal di tiap lajur
        for i, cx in enumerate(LANE_CENTERS):
            val = self.question.options[i]
            pw = LANE_WIDTH - 16
            ph = 44
            px = cx - pw // 2
            py = y_int - ph // 2

            is_blocked = (i in self.blocked_lanes and self.blocked_lanes[i] > 0)
            is_correct_opt = (val == self.question.correct_answer)

            # Efek neon portal bercahaya
            gate_surf = pygame.Surface((pw, ph), pygame.SRCALPHA)
            
            if is_blocked:
                # Perisai Merah Berkedip TERTUTUP / SALAH!
                pygame.draw.rect(gate_surf, (220, 20, 20, 240), (0, 0, pw, ph), border_radius=10)
                pygame.draw.rect(gate_surf, (255, 80, 80), (0, 0, pw, ph), width=4, border_radius=10)
                # Garis silang laser perisai
                pygame.draw.line(gate_surf, (255, 255, 255, 200), (4, 4), (pw - 4, ph - 4), 3)
                pygame.draw.line(gate_surf, (255, 255, 255, 200), (4, ph - 4), (pw - 4, 4), 3)
                surface.blit(gate_surf, (px, py))

                # Teks ⛔ SALAH
                warn_surf = font.render(f"⛔ {val}", True, (255, 255, 255))
                w_rect = warn_surf.get_rect(center=(cx, y_int))
                surface.blit(warn_surf, w_rect)
                continue

            elif is_correct_opt:
                # Portal Hijau-Emas Berkilau Menarik untuk Jawaban Benar
                glow_pulse = int(180 + 60 * math.sin(self.anim_tick * 0.15))
                pygame.draw.rect(gate_surf, (20, 48, 30, 235), (0, 0, pw, ph), border_radius=10)
                pygame.draw.rect(gate_surf, (50, 255, 120), (0, 0, pw, ph), width=3, border_radius=10)
                # Lingkaran halo luar
                pygame.draw.rect(gate_surf, (0, 255, 180, glow_pulse // 3), (0, 0, pw, ph), width=1, border_radius=10)
                border_col = (50, 255, 120)
            else:
                # Portal Netral
                pygame.draw.rect(gate_surf, (18, 25, 42, 230), (0, 0, pw, ph), border_radius=10)
                border_col = (0, 235, 255) if (i % 2 == 0) else (255, 190, 40)
                pygame.draw.rect(gate_surf, border_col, (0, 0, pw, ph), width=3, border_radius=10)

            surface.blit(gate_surf, (px, py))

            # Nomor Pilihan Jawaban
            num_surf = font.render(str(val), True, COLOR_WHITE)
            num_rect = num_surf.get_rect(center=(cx, y_int))
            shadow_surf = font.render(str(val), True, (10, 15, 25))
            surface.blit(shadow_surf, (num_rect.x + 2, num_rect.y + 2))
            surface.blit(num_surf, num_rect)

            # Dekorasi Lampu Indikator Atas
            pygame.draw.circle(surface, border_col, (cx, py - 4), 4)


class MathManager:
    """Manajer Kuis & Edukasi Matematika GameKhansa."""
    def __init__(self, grade_level=2):
        self.grade_level = grade_level  # 1: Kelas 1-2, 2: Kelas 3-4, 3: Kelas 5-6
        self.current_question = None
        self.active_gate = None
        self.spawn_timer = 0
        self.spawn_interval = 520  # Muncul gerbang setiap ~8.5 detik

        # Feedback & Pujian
        self.feedback_text = ""
        self.feedback_color = COLOR_GOLD
        self.feedback_timer = 0

        # Rapor & Statistik
        self.total_questions = 0
        self.correct_answers = 0
        self.current_streak = 0
        self.best_streak = 0
        self.total_math_score = 0
        self.last_quote = None

        # Inisialisasi Soal Pertama
        self.generate_new_question()

    def set_grade(self, grade):
        self.grade_level = max(1, min(3, grade))
        self.generate_new_question()

    def reset_stats(self):
        self.total_questions = 0
        self.correct_answers = 0
        self.current_streak = 0
        self.best_streak = 0
        self.total_math_score = 0
        self.active_gate = None
        self.feedback_timer = 0
        self.spawn_timer = 180  # Jeda awal sebelum gerbang pertama
        self.generate_new_question()

    def generate_new_question(self):
        self.current_question = MathQuestion(self.grade_level)

    def update(self, player_speed, player):
        """Memperbarui posisi gerbang matematika dan menghitung tabrakan jawaban."""
        # 1. Update Timer Feedback
        if self.feedback_timer > 0:
            self.feedback_timer -= 1

        # 2. Spawner Gerbang Matematika
        if self.active_gate is None:
            self.spawn_timer += 1
            # SETENGAH JALAN (HALFWAY): Munculkan soal baru jauh sebelum gerbang tiba!
            if self.spawn_timer == self.spawn_interval // 2:
                self.generate_new_question()
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                if self.current_question is None:
                    self.generate_new_question()
                self.active_gate = MathGate(self.current_question, start_y=-90)

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
                    self.feedback_text = f"Terlewat! Jawaban: {self.current_question.correct_answer}"
                    self.feedback_color = (255, 170, 70)
                    self.feedback_timer = 90
                self.active_gate = None

        return result

    def _handle_answer(self, res, player):
        is_corr = res["is_correct"]

        if is_corr:
            self.total_questions += 1
            self.correct_answers += 1
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
            self.total_math_score += 500

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
            self.feedback_text = f"🎁 {praise} (+500 SKOR, SHIELD BINTANG & 35 KOIN!){streak_txt}"
            self.feedback_color = (50, 255, 120)
            self.feedback_timer = 150
            return "correct"
        else:
            # Jawaban salah: Terblokir / Tidak bisa lewat!
            self.current_streak = 0
            self.feedback_text = f"⛔ SALAH! LAJUR TERBLOKIR! {res['question_text'].replace(' = ?', '')} ≠ {res['chosen_val']}. Belok cari jawaban benar!"
            self.feedback_color = (255, 60, 60)
            self.feedback_timer = 90
            return "wrong_blocked"


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
            return "🌟 PROFESOR CILIK KHANSA 🌟"
        elif stars == 2:
            return "⭐ BINTANG MATEMATIKA HEBAT ⭐"
        return "🌱 PENJELAJAH MATEMATIKA MUDA 🌱"

    def get_grade_name(self):
        if self.grade_level == 1:
            return "SD Kelas 1 - 2 (Pemula)"
        elif self.grade_level == 3:
            return "SD Kelas 5 - 6 (Mahir)"
        return "SD Kelas 3 - 4 (Menengah)"
