"""
Titik Masuk Utama (Main Entrypoint) Game Mobil Legend (GameKhansa).
Game Balap Mobil Arcade Ringan, Seru, dan Responsif.
"""

import sys
import os
import json
import random
import math
import pygame

from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    ROAD_LEFT, ROAD_RIGHT,
    STATE_MENU, STATE_GARAGE, STATE_PLAYING, STATE_PAUSED, STATE_GAMEOVER,
    STATE_NAME_INPUT, STATE_CONFIRM_DELETE,
    CARS_DATA, NUM_LANES, LANE_CENTERS,
    EDU_MODE_MATH, EDU_MODE_VOCAB
)
from game.sound import SoundManager
from game.car import PlayerCar, TrafficCar, Explosion, Particle
from game.obstacle import Coin, NitroBottle, RepairKit, OilSlick, RoadBlock
from game.road import Road
from game.ui import UIManager
from game.math_quiz import MathManager
from game.vocab_quiz import VocabManager

HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")
PROFILE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "player_profile.json")

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                data = json.load(f)
                return int(data.get("highscore", 0))
        except Exception:
            return 0
    return 0

def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"highscore": int(score)}, f, indent=2)
    except Exception as e:
        print(f"[Save] Gagal menyimpan highscore: {e}")

def load_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def save_profile(profile_data):
    try:
        with open(PROFILE_FILE, "w") as f:
            json.dump(profile_data, f, indent=2)
        if "highscore" in profile_data:
            save_highscore(profile_data["highscore"])
    except Exception as e:
        print(f"[Save] Gagal menyimpan profil: {e}")

def delete_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            os.remove(PROFILE_FILE)
        except Exception as e:
            print(f"[Delete] Gagal menghapus profil: {e}")
    save_highscore(0)


class ConfettiParticle:
    """Partikel Konfeti Warna-Warni untuk Selebrasi Hadiah Edukasi."""
    def __init__(self):
        self.x = random.uniform(ROAD_LEFT - 20, ROAD_RIGHT + 20)
        self.y = random.uniform(-40, 120)
        self.vx = random.uniform(-2.5, 2.5)
        self.vy = random.uniform(3.5, 7.5)
        self.w = random.uniform(7, 13)
        self.h = random.uniform(5, 9)
        self.angle = random.uniform(0, 360)
        self.rot_speed = random.uniform(-9, 9)
        self.color = random.choice([
            (255, 215, 0), (0, 235, 255), (255, 75, 200),
            (50, 255, 120), (255, 130, 40), (245, 245, 255)
        ])
        self.lifetime = random.randint(75, 130)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.angle += self.rot_speed
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0 and -20 < self.y < SCREEN_HEIGHT + 20:
            c_surf = pygame.Surface((int(self.w), int(self.h)), pygame.SRCALPHA)
            c_surf.fill(self.color)
            rot_surf = pygame.transform.rotate(c_surf, self.angle)
            surface.blit(rot_surf, (int(self.x), int(self.y)))


class MobilLegendGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Mobil Legend — Khansa Racing Championship")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Inisialisasi Modul
        self.sound = SoundManager()
        self.ui = UIManager()
        self.road = Road()
        
        # Pilihan Mobil
        self.car_keys = list(CARS_DATA.keys())

        # Muat Profil Pemain Persisten
        profile = load_profile()
        if profile and profile.get("player_name"):
            self.player_name = profile.get("player_name", "Khansa")
            self.highscore = int(profile.get("highscore", load_highscore()))
            self.coins = int(profile.get("coins", 0))
            saved_car = profile.get("selected_car", self.car_keys[0])
            self.selected_car_id = saved_car if saved_car in self.car_keys else self.car_keys[0]
            self.selected_car_idx = self.car_keys.index(self.selected_car_id)
            self.edu_mode = profile.get("edu_mode", EDU_MODE_MATH)
            self.grade_level = int(profile.get("grade_level", 2))
            self.vocab_level = int(profile.get("vocab_level", 1))
            self.state = STATE_MENU
        else:
            self.player_name = ""
            self.highscore = load_highscore()
            self.coins = 0
            self.selected_car_idx = 0
            self.selected_car_id = self.car_keys[0]
            self.edu_mode = EDU_MODE_MATH
            self.grade_level = 2
            self.vocab_level = 1
            self.state = STATE_NAME_INPUT

        self.input_name_text = self.player_name
        self.cursor_timer = 0

        self.player = PlayerCar(self.selected_car_id)
        self.player.player_name = self.player_name or "Khansa"
        self.player.coins = self.coins

        # Koleksi Objek Dinamis
        self.traffic_cars = []
        self.items = []       # Coin, NitroBottle, RepairKit
        self.hazards = []     # OilSlick, RoadBlock
        self.explosions = []  # Efek ledakan peluru tank

        self.score = 0
        self.is_new_record = False

        # Mode & Modul Edukasi (Matematika SD & English 3000 Vocab)
        self.math_manager = MathManager(self.grade_level)
        self.vocab_manager = VocabManager(self.vocab_level)
        if profile and "mastered_words" in profile and isinstance(profile["mastered_words"], list):
            self.vocab_manager.words_learned = set(profile["mastered_words"])

        # Timer Spawner
        self.spawn_traffic_timer = 0
        self.spawn_item_timer = 0
        self.spawn_hazard_timer = 0

        # Efek Selebrasi Hadiah Edukasi
        self.confetti_particles = []
        self.celebration_banner_timer = 0

    def _save_current_profile(self):
        """Menyimpan seluruh progres profil pemain ke file JSON lokal."""
        profile_data = {
            "player_name": self.player_name or "Khansa",
            "highscore": int(self.highscore),
            "coins": int(getattr(self.player, 'coins', self.coins)),
            "selected_car": self.selected_car_id,
            "edu_mode": self.edu_mode,
            "grade_level": int(self.grade_level),
            "vocab_level": int(self.vocab_level),
            "mastered_words": list(self.vocab_manager.words_learned),
            "mastered_count": len(self.vocab_manager.words_learned)
        }
        save_profile(profile_data)

    def start_new_game(self):
        self.player = PlayerCar(self.selected_car_id)
        self.player.player_name = self.player_name or "Khansa"
        self.player.coins = self.coins
        self.road = Road()
        self.traffic_cars.clear()
        self.items.clear()
        self.hazards.clear()
        self.explosions.clear()
        self.confetti_particles.clear()
        self.celebration_banner_timer = 0
        self.math_manager.reset_stats()
        self.vocab_manager.reset_stats()

        self.score = 0
        self.is_new_record = False
        self.spawn_traffic_timer = 0
        self.spawn_item_timer = 0
        self.state = STATE_PLAYING
        self.sound.start_bgm()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self._handle_events()
            self._update()
            self._draw()

        pygame.quit()
        sys.exit(0)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.state == STATE_NAME_INPUT:
                    if self.ui.name_submit_btn_rect and self.ui.name_submit_btn_rect.collidepoint(mx, my):
                        name = self.input_name_text.strip() or "Khansa"
                        self.player_name = name
                        self.player.player_name = name
                        self._save_current_profile()
                        self.state = STATE_MENU
                        self.sound.play("coin")
                elif self.state == STATE_CONFIRM_DELETE:
                    if self.ui.confirm_yes_rect and self.ui.confirm_yes_rect.collidepoint(mx, my):
                        delete_profile()
                        self.player_name = ""
                        self.input_name_text = ""
                        self.highscore = 0
                        self.coins = 0
                        self.player.coins = 0
                        self.state = STATE_NAME_INPUT
                        self.sound.play("horn")
                    elif self.ui.confirm_no_rect and self.ui.confirm_no_rect.collidepoint(mx, my):
                        self.state = STATE_MENU
                elif self.state == STATE_MENU:
                    mb = getattr(self.ui, 'menu_buttons', {})
                    if mb.get("btn_name") and mb["btn_name"].collidepoint(mx, my):
                        self.input_name_text = self.player_name
                        self.state = STATE_NAME_INPUT
                        self.sound.play("coin")
                    elif mb.get("btn_del") and mb["btn_del"].collidepoint(mx, my):
                        self.state = STATE_CONFIRM_DELETE
                        self.sound.play("horn")
                    elif mb.get("btn_mode") and mb["btn_mode"].collidepoint(mx, my):
                        self.edu_mode = EDU_MODE_VOCAB if (self.edu_mode == EDU_MODE_MATH) else EDU_MODE_MATH
                        self._save_current_profile()
                        self.sound.play("coin")
                    elif mb.get("tab_car") and mb["tab_car"].collidepoint(mx, my):
                        # Pilih Mobil Pertama
                        for idx, k in enumerate(self.car_keys):
                            if CARS_DATA[k].get("type") == "car":
                                self.selected_car_idx = idx
                                self.selected_car_id = k
                                self.player = PlayerCar(self.selected_car_id)
                                self.player.player_name = self.player_name
                                self.player.coins = self.coins
                                self._save_current_profile()
                                break
                    elif mb.get("tab_tank") and mb["tab_tank"].collidepoint(mx, my):
                        # Pilih Tank Pertama
                        for idx, k in enumerate(self.car_keys):
                            if CARS_DATA[k].get("type") == "tank":
                                self.selected_car_idx = idx
                                self.selected_car_id = k
                                self.player = PlayerCar(self.selected_car_id)
                                self.player.player_name = self.player_name
                                self.player.coins = self.coins
                                self._save_current_profile()
                                break
                    elif mb.get("prev") and mb["prev"].collidepoint(mx, my):
                        self.selected_car_idx = (self.selected_car_idx - 1) % len(self.car_keys)
                        self.selected_car_id = self.car_keys[self.selected_car_idx]
                        self.player = PlayerCar(self.selected_car_id)
                        self.player.player_name = self.player_name
                        self.player.coins = self.coins
                        self._save_current_profile()
                    elif (mb.get("next") and mb["next"].collidepoint(mx, my)) or (mb.get("card") and mb["card"].collidepoint(mx, my)):
                        self.selected_car_idx = (self.selected_car_idx + 1) % len(self.car_keys)
                        self.selected_car_id = self.car_keys[self.selected_car_idx]
                        self.player = PlayerCar(self.selected_car_id)
                        self.player.player_name = self.player_name
                        self.player.coins = self.coins
                        self._save_current_profile()
                    elif mb.get("start") and mb["start"].collidepoint(mx, my):
                        self.start_new_game()
                    elif mb.get("garage") and mb["garage"].collidepoint(mx, my):
                        self.state = STATE_GARAGE
                    elif mb.get("tab_edu_math") and mb["tab_edu_math"].collidepoint(mx, my):
                        self.edu_mode = EDU_MODE_MATH
                        self._save_current_profile()
                        self.sound.play("coin")
                    elif mb.get("tab_edu_vocab") and mb["tab_edu_vocab"].collidepoint(mx, my):
                        self.edu_mode = EDU_MODE_VOCAB
                        self._save_current_profile()
                        self.sound.play("coin")
                    # Pilihan Tingkat Level (Matematika atau Vocab)
                    for lvl in (1, 2, 3):
                        g_key = f"grade_{lvl}"
                        if mb.get(g_key) and mb[g_key].collidepoint(mx, my):
                            if self.edu_mode == EDU_MODE_MATH:
                                self.grade_level = lvl
                                self.math_manager.set_grade(self.grade_level)
                            else:
                                self.vocab_level = lvl
                                self.vocab_manager.set_level(self.vocab_level)
                            self._save_current_profile()
                            self.sound.play("coin")
                            break

                elif self.state == STATE_GARAGE:
                    for card_rect, key, idx in getattr(self.ui, 'garage_cards', []):
                        if card_rect.collidepoint(mx, my):
                            self.selected_car_idx = idx
                            self.selected_car_id = key
                            self.player = PlayerCar(self.selected_car_id)
                            self.player.player_name = self.player_name
                            self.player.coins = self.coins
                            self._save_current_profile()
                            break
                    start_btn = getattr(self.ui, 'garage_start_btn', None)
                    if start_btn and start_btn.collidepoint(mx, my):
                        self.start_new_game()

                elif self.state == STATE_GAMEOVER:
                    self.start_new_game()

            elif event.type == pygame.KEYDOWN:
                if self.state == STATE_NAME_INPUT:
                    if event.key == pygame.K_RETURN:
                        name = self.input_name_text.strip() or "Khansa"
                        self.player_name = name
                        self.player.player_name = name
                        self._save_current_profile()
                        self.state = STATE_MENU
                        self.sound.play("coin")
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_name_text = self.input_name_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        if self.player_name:
                            self.state = STATE_MENU
                    else:
                        if len(self.input_name_text) < 15 and event.unicode.isprintable() and event.unicode not in ('\r', '\n', '\t'):
                            self.input_name_text += event.unicode

                elif self.state == STATE_CONFIRM_DELETE:
                    if event.key in (pygame.K_y, pygame.K_SPACE, pygame.K_RETURN):
                        delete_profile()
                        self.player_name = ""
                        self.input_name_text = ""
                        self.highscore = 0
                        self.coins = 0
                        self.player.coins = 0
                        self.state = STATE_NAME_INPUT
                        self.sound.play("horn")
                    elif event.key in (pygame.K_n, pygame.K_ESCAPE):
                        self.state = STATE_MENU

                elif self.state == STATE_MENU:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.start_new_game()
                    elif event.key == pygame.K_n:
                        self.input_name_text = self.player_name
                        self.state = STATE_NAME_INPUT
                        self.sound.play("coin")
                    elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                        self.state = STATE_CONFIRM_DELETE
                        self.sound.play("horn")
                    elif event.key == pygame.K_LEFT:
                        self.selected_car_idx = (self.selected_car_idx - 1) % len(self.car_keys)
                        self.selected_car_id = self.car_keys[self.selected_car_idx]
                        self.player = PlayerCar(self.selected_car_id)
                        self.player.player_name = self.player_name
                        self.player.coins = self.coins
                        self._save_current_profile()
                    elif event.key == pygame.K_RIGHT:
                        self.selected_car_idx = (self.selected_car_idx + 1) % len(self.car_keys)
                        self.selected_car_id = self.car_keys[self.selected_car_idx]
                        self.player = PlayerCar(self.selected_car_id)
                        self.player.player_name = self.player_name
                        self.player.coins = self.coins
                        self._save_current_profile()
                    elif event.key == pygame.K_e:
                        self.edu_mode = EDU_MODE_VOCAB if (self.edu_mode == EDU_MODE_MATH) else EDU_MODE_MATH
                        self._save_current_profile()
                        self.sound.play("coin")
                    elif event.key in (pygame.K_1, pygame.K_KP1):
                        if self.edu_mode == EDU_MODE_MATH:
                            self.grade_level = 1
                            self.math_manager.set_grade(self.grade_level)
                        else:
                            self.vocab_level = 1
                            self.vocab_manager.set_level(self.vocab_level)
                        self._save_current_profile()
                        self.sound.play("coin")
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        if self.edu_mode == EDU_MODE_MATH:
                            self.grade_level = 2
                            self.math_manager.set_grade(self.grade_level)
                        else:
                            self.vocab_level = 2
                            self.vocab_manager.set_level(self.vocab_level)
                        self._save_current_profile()
                        self.sound.play("coin")
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        if self.edu_mode == EDU_MODE_MATH:
                            self.grade_level = 3
                            self.math_manager.set_grade(self.grade_level)
                        else:
                            self.vocab_level = 3
                            self.vocab_manager.set_level(self.vocab_level)
                        self._save_current_profile()
                        self.sound.play("coin")
                    elif event.key == pygame.K_t:
                        # Lompat langsung ke Tank
                        for idx, k in enumerate(self.car_keys):
                            if CARS_DATA[k].get("type") == "tank":
                                self.selected_car_idx = idx
                                self.selected_car_id = k
                                self.player = PlayerCar(self.selected_car_id)
                                self.player.player_name = self.player_name
                                self.player.coins = self.coins
                                self._save_current_profile()
                                break
                    elif event.key == pygame.K_c:
                        # Lompat langsung ke Mobil
                        for idx, k in enumerate(self.car_keys):
                            if CARS_DATA[k].get("type") == "car":
                                self.selected_car_idx = idx
                                self.selected_car_id = k
                                self.player = PlayerCar(self.selected_car_id)
                                self.player.player_name = self.player_name
                                self.player.coins = self.coins
                                self._save_current_profile()
                                break
                    elif event.key == pygame.K_g:
                        self.state = STATE_GARAGE
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

                elif self.state == STATE_GARAGE:
                    if event.key == pygame.K_LEFT:
                        self.selected_car_idx = (self.selected_car_idx - 1) % len(self.car_keys)
                        self.selected_car_id = self.car_keys[self.selected_car_idx]
                        self.player = PlayerCar(self.selected_car_id)
                        self.player.player_name = self.player_name
                        self.player.coins = self.coins
                        self._save_current_profile()
                    elif event.key == pygame.K_RIGHT:
                        self.selected_car_idx = (self.selected_car_idx + 1) % len(self.car_keys)
                        self.selected_car_id = self.car_keys[self.selected_car_idx]
                        self.player = PlayerCar(self.selected_car_id)
                        self.player.player_name = self.player_name
                        self.player.coins = self.coins
                        self._save_current_profile()
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.start_new_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_MENU

                elif self.state == STATE_PLAYING:
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.state = STATE_PAUSED
                        self.sound.stop_all_continuous()
                    elif event.key == pygame.K_b:
                        self.sound.toggle_bgm()

                elif self.state == STATE_PAUSED:
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.state = STATE_PLAYING
                    elif event.key == pygame.K_m:
                        self.sound.stop_bgm()
                        self.sound.stop_all_continuous()
                        self.state = STATE_MENU

                elif self.state == STATE_GAMEOVER:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_r):
                        self.start_new_game()
                    elif event.key == pygame.K_m:
                        self.sound.stop_bgm()
                        self.sound.stop_all_continuous()
                        self.state = STATE_MENU
                    elif event.key == pygame.K_g:
                        self.sound.stop_bgm()
                        self.sound.stop_all_continuous()
                        self.state = STATE_GARAGE

    def _update(self):
        self.cursor_timer += 1
        if self.state != STATE_PLAYING:
            return

        keys = pygame.key.get_pressed()
        fired_cannon = self.player.update(keys)
        if fired_cannon:
            self.sound.play("cannon")

        is_gas = keys[pygame.K_UP] or keys[pygame.K_w]
        is_brake = keys[pygame.K_DOWN] or keys[pygame.K_s]

        # 1. Update Suara Raungan Mesin Mobil / Tank Dinamis
        self.sound.update_engine(
            self.player.speed,
            self.player.base_max_speed,
            self.player.is_nitro_active,
            is_gas,
            is_brake,
            vehicle_type=self.player.vehicle_type
        )

        # 2. Suara Turbo Nitro Berkelanjutan (khusus Mobil)
        if self.player.vehicle_type != "tank":
            self.sound.update_nitro(self.player.is_nitro_active and self.player.nitro > 0)
        else:
            self.sound.update_nitro(False)

        # 3. Suara Decitan Ban Saat Belok Tajam (Drift)
        if abs(self.player.angle) > 6.0 and self.player.speed > 5.0:
            self.sound.play_screech()

        # Perbarui Jalan
        distance = self.player.distance
        self.road.update(self.player.speed, distance)

        # Tambah Skor Dasar Berdasarkan Kecepatan
        if self.player.speed > 0.5:
            speed_mult = 1.8 if self.player.is_nitro_active else 1.0
            self.score += int(self.player.speed * 0.8 * speed_mult)

        # Spawner Objek
        self._spawn_world_elements()

        # Update Mobil Lalu Lintas
        player_rect = self.player.get_rect()
        for t_car in self.traffic_cars:
            t_car.update(self.player.speed)

            # Deteksi Near Miss (Lewat mobil sangat dekat tanpa tabrakan)
            if not t_car.passed and t_car.y > self.player.y:
                t_car.passed = True
                if abs(t_car.x - self.player.x) < 55:
                    # Bonus "Close Pass"
                    self.score += 50

            # Deteksi Tabrakan Mobil Pemain dengan Mobil Lalu Lintas
            if player_rect.colliderect(t_car.get_rect()):
                if self.player.super_shield_timer > 0:
                    # SUPER SMASH! Hancurkan mobil musuh seketika saat perisai bintang kebal aktif!
                    if t_car in self.traffic_cars:
                        self.traffic_cars.remove(t_car)
                    self.explosions.append(Explosion(t_car.x, t_car.y, size=1.6))
                    self.sound.play("explosion")
                    self.score += 250
                    self.player.coins += 2
                else:
                    damaged = self.player.take_damage(25)
                    if damaged:
                        self.sound.play("crash")
                        # Efek mobil musuh terdorong ke depan
                        t_car.y -= 30

        # Magnet Koin saat Super Shield aktif
        if self.player.super_shield_timer > 0:
            for item in self.items:
                dist = math.hypot(item.x - self.player.x, item.y - self.player.y)
                if 5 < dist < 280:
                    item.x += (self.player.x - item.x) * 0.16
                    item.y += (self.player.y - item.y) * 0.16

        # Update Item (Koin, Nitro, P3K)
        for item in self.items:
            item.update(self.player.speed)
            if player_rect.colliderect(item.get_rect()):
                if isinstance(item, Coin):
                    item.collected = True
                    self.player.coins += 1
                    self.score += 100
                    self.sound.play("coin")
                elif isinstance(item, NitroBottle):
                    item.collected = True
                    self.player.add_nitro(75)
                    self.sound.play("nitro")
                elif isinstance(item, RepairKit):
                    item.collected = True
                    self.player.add_hp(35)
                    self.sound.play("repair")

        # Update Rintangan (Oli, Pembatas)
        for hazard in list(self.hazards):
            hazard.update(self.player.speed)
            if player_rect.colliderect(hazard.get_rect()):
                if self.player.super_shield_timer > 0:
                    if isinstance(hazard, RoadBlock) and hazard in self.hazards:
                        self.hazards.remove(hazard)
                        self.explosions.append(Explosion(hazard.x, hazard.y, size=1.2))
                        self.sound.play("explosion")
                        self.score += 100
                else:
                    if isinstance(hazard, OilSlick):
                        self.player.hit_oil()
                    elif isinstance(hazard, RoadBlock):
                        damaged = self.player.take_damage(35)
                        if damaged:
                            self.sound.play("crash")

        # Update Modul Edukasi (Matematika SD atau English Vocab)
        if self.edu_mode == EDU_MODE_VOCAB:
            edu_result = self.vocab_manager.update(self.player.speed, self.player)
        else:
            edu_result = self.math_manager.update(self.player.speed, self.player)

        if edu_result == "correct":
            self.sound.play("victory_fanfare")
            self.sound.play("coin_cascade")
            self.sound.play("math_correct")
            self.score += 500
            # Semburan Konfeti & Kembang Api Perayaan
            for _ in range(50):
                self.confetti_particles.append(ConfettiParticle())
            self.explosions.append(Explosion(self.player.x - 70, self.player.y - 70, size=1.4))
            self.explosions.append(Explosion(self.player.x + 70, self.player.y - 70, size=1.4))
            self.celebration_banner_timer = 360
            self._save_current_profile()
        elif edu_result == "wrong_blocked":
            self.sound.play("barrier_block")
            # Percikan partikel tolak listrik merah di bemper depan
            for _ in range(16):
                self.player.particles.append(Particle(
                    self.player.x + random.uniform(-20, 20),
                    self.player.y - self.player.height // 2,
                    random.uniform(-4.0, 4.0),
                    random.uniform(1.0, 5.0),
                    random.choice([(255, 40, 40), (255, 120, 40), (255, 255, 255)]),
                    random.uniform(3.0, 6.0),
                    18
                ))

        # Deteksi Tembakan Meriam Tank Menghancurkan Musuh & Barikade
        for shell in list(self.player.shells):
            shell_rect = shell.get_rect()
            hit = False

            # Tabrakan dengan mobil lalu lintas
            for t_car in list(self.traffic_cars):
                if shell_rect.colliderect(t_car.get_rect()):
                    hit = True
                    self.traffic_cars.remove(t_car)
                    self.explosions.append(Explosion(t_car.x, t_car.y, size=1.4))
                    self.sound.play("explosion")
                    self.score += 150  # Bonus Skor Ledakkan Musuh!
                    break

            # Tabrakan dengan barikade rintangan jalan
            if not hit:
                for hazard in list(self.hazards):
                    if isinstance(hazard, RoadBlock) and shell_rect.colliderect(hazard.get_rect()):
                        hit = True
                        self.hazards.remove(hazard)
                        self.explosions.append(Explosion(hazard.x, hazard.y, size=1.1))
                        self.sound.play("explosion")
                        self.score += 100
                        break

            if hit and shell in self.player.shells:
                self.player.shells.remove(shell)

        # Update Animasi Partikel Ledakan
        for exp in self.explosions:
            exp.update(self.player.speed)
        self.explosions = [exp for exp in self.explosions if exp.lifetime > 0]

        # Bersihkan Objek Keluar Layar
        self.traffic_cars = [c for c in self.traffic_cars if not c.is_offscreen()]
        self.items = [i for i in self.items if not i.is_offscreen() and not getattr(i, 'collected', False)]
        self.hazards = [h for h in self.hazards if not h.is_offscreen()]

        # Update Konfeti & Banner Selebrasi Hadiah
        for cp in self.confetti_particles:
            cp.update()
        self.confetti_particles = [cp for cp in self.confetti_particles if cp.lifetime > 0]
        if self.celebration_banner_timer > 0:
            self.celebration_banner_timer -= 1
            active_edu = self.vocab_manager if (self.edu_mode == EDU_MODE_VOCAB) else self.math_manager
            if active_edu and active_edu.active_gate and active_edu.active_gate.y >= 20:
                self.celebration_banner_timer = min(self.celebration_banner_timer, 15)

        # Cek Game Over
        if self.player.hp <= 0:
            self.sound.stop_all_continuous()
            self.sound.stop_bgm()
            self.sound.play("gameover")
            if self.score > self.highscore:
                self.highscore = self.score
                self.is_new_record = True
            self.coins = self.player.coins
            self._save_current_profile()
            self.state = STATE_GAMEOVER

    def _spawn_world_elements(self):
        # 1. Spawner Lalu Lintas (Traffic)
        self.spawn_traffic_timer += 1
        traffic_interval = max(45, int(85 - (self.player.distance / 1500)))
        if self.spawn_traffic_timer >= traffic_interval:
            self.spawn_traffic_timer = 0
            
            # Pilih lane yang aman (jangan blokir semua lane)
            occupied_lanes = [c.lane_idx for c in self.traffic_cars if c.y < 120]
            available_lanes = [l for l in range(NUM_LANES) if l not in occupied_lanes]
            
            if available_lanes:
                chosen_lane = random.choice(available_lanes)
                self.traffic_cars.append(TrafficCar(chosen_lane, -110))

        # 2. Spawner Item (Koin beruntun atau power-up)
        self.spawn_item_timer += 1
        if self.spawn_item_timer >= 60:
            self.spawn_item_timer = 0
            lane = random.choice(range(NUM_LANES))
            lane_x = LANE_CENTERS[lane]

            item_type = random.random()
            if item_type < 0.65:
                # Spawn deretan 3 koin
                for i in range(3):
                    self.items.append(Coin(lane_x, -50 - (i * 38)))
            elif item_type < 0.85:
                # Spawn botol Nitro
                self.items.append(NitroBottle(lane_x, -60))
            else:
                # Spawn kotak reparasi HP
                self.items.append(RepairKit(lane_x, -60))

        # 3. Spawner Rintangan (Oli dan Pembatas)
        self.spawn_hazard_timer += 1
        if self.spawn_hazard_timer >= 110:
            self.spawn_hazard_timer = 0
            lane = random.choice(range(NUM_LANES))
            lane_x = LANE_CENTERS[lane]

            if random.random() < 0.6:
                self.hazards.append(OilSlick(lane_x, -70))
            else:
                self.hazards.append(RoadBlock(lane_x, -70))

    def _draw(self):
        distance = self.player.distance if self.state == STATE_PLAYING else 0
        biome = self.road.get_biome(distance)

        if self.state == STATE_PLAYING:
            # 1. Gambar Jalan & Latar
            self.road.draw(self.screen, distance)

            # 2. Gambar Rintangan & Item di Atas Aspal
            for hazard in self.hazards:
                hazard.draw(self.screen)
            for item in self.items:
                item.draw(self.screen)

            # 2b. Gambar Gerbang Jawaban Edukasi (Matematika / Vocab)
            self.ui.draw_math_gates(self.screen, self.math_manager, self.vocab_manager, self.edu_mode)

            # 3. Gambar Mobil Lalu Lintas
            for t_car in self.traffic_cars:
                t_car.draw(self.screen)

            # 4. Gambar Kendaraan Pemain (Mobil / Tank)
            self.player.draw(self.screen)

            # 5. Gambar Efek Ledakan
            for exp in self.explosions:
                exp.draw(self.screen)

            # 5b. Gambar Partikel Konfeti Selebrasi
            for cp in self.confetti_particles:
                cp.draw(self.screen)

            # 6. Gambar HUD (Termasuk Banner Soal & Feedback Edukasi)
            self.ui.draw_hud(self.screen, self.player, self.score, self.highscore, biome, self.math_manager, self.vocab_manager, self.edu_mode)

            # 7. Gambar Banner Pop-up Hadiah Spesial jika aktif
            if self.celebration_banner_timer > 0:
                self._draw_celebration_banner()

        elif self.state == STATE_PAUSED:
            # Tetap render tampilan balapan di belakang overlay pause
            self.road.draw(self.screen, distance)
            for hazard in self.hazards:
                hazard.draw(self.screen)
            for item in self.items:
                item.draw(self.screen)
            self.ui.draw_math_gates(self.screen, self.math_manager, self.vocab_manager, self.edu_mode)
            for t_car in self.traffic_cars:
                t_car.draw(self.screen)
            self.player.draw(self.screen)
            self.ui.draw_hud(self.screen, self.player, self.score, self.highscore, biome, self.math_manager, self.vocab_manager, self.edu_mode)
            self.ui.draw_pause(self.screen)

        elif self.state == STATE_NAME_INPUT:
            self.road.update(2.0, 100)
            self.road.draw(self.screen, 100)
            self.ui.draw_name_input(self.screen, self.input_name_text, self.cursor_timer)

        elif self.state == STATE_CONFIRM_DELETE:
            self.road.draw(self.screen, distance)
            self.ui.draw_confirm_delete(self.screen, self.player_name or "Khansa")

        elif self.state == STATE_MENU:
            # Demo animasi jalan pelan di background menu
            self.road.update(4.0, 100)
            self.road.draw(self.screen, 100)
            m_cnt = len(getattr(self.vocab_manager, 'words_learned', set()))
            self.ui.draw_menu(
                self.screen, self.selected_car_id, self.highscore,
                self.grade_level, self.edu_mode, self.vocab_level,
                player_name=self.player_name, coins=self.player.coins,
                mastered_words_count=m_cnt
            )

        elif self.state == STATE_GARAGE:
            self.ui.draw_garage(self.screen, self.selected_car_idx, self.car_keys)

        elif self.state == STATE_GAMEOVER:
            self.road.draw(self.screen, distance)
            self.ui.draw_game_over(
                self.screen, self.score, self.highscore,
                self.player.coins, self.player.distance, self.is_new_record,
                self.math_manager, self.vocab_manager, self.edu_mode
            )

        pygame.display.flip()

    def _draw_celebration_banner(self):
        """Menampilkan banner perayaan dan kata motivasi dari tokoh-tokoh hebat dunia (Bilingual: ID & EN)."""
        banner_w, banner_h = 620, 114
        bx = (SCREEN_WIDTH - banner_w) // 2
        by = SCREEN_HEIGHT // 2 - 148

        surf = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (15, 20, 36, 245), (0, 0, banner_w, banner_h), border_radius=14)
        pygame.draw.rect(surf, (255, 215, 0), (0, 0, banner_w, banner_h), width=3, border_radius=14)
        self.screen.blit(surf, (bx, by))

        # Baris 1: Header Nama Pemain & Kosa Kata Dikuasai
        p_name = (self.player_name or "Khansa").upper()
        m_cnt = len(getattr(self.vocab_manager, 'words_learned', set()))
        h_text = f"🎁 JAWABAN TEPAT! HEBAT, {p_name}! 🌟 (📚 {m_cnt}/3000 KATA)"
        t1 = self.ui.font_med.render(h_text, True, (255, 225, 50))
        r1 = t1.get_rect(center=(SCREEN_WIDTH // 2, by + 18))
        self.screen.blit(t1, r1)

        # Baris 2 & 3: Kata Mutiara Tokoh Dunia (Indonesia & Inggris)
        active_edu = self.vocab_manager if (self.edu_mode == EDU_MODE_VOCAB) else self.math_manager
        quote_obj = getattr(active_edu, 'last_quote', None)
        if quote_obj:
            id_txt = f"🇮🇩 \"{quote_obj['id']}\""
            en_txt = f"🇬🇧 \"{quote_obj['en']}\" — {quote_obj['author']}"
        else:
            motiv = getattr(active_edu, 'last_motivation', '') or f"Hebat sekali {self.player_name}! Terus melaju juara!"
            id_txt = f"💬 \"{motiv}\""
            en_txt = "🌟 Keep learning, keep shining!"

        t2 = self.ui.font_tiny.render(id_txt, True, (80, 255, 140))
        r2 = t2.get_rect(center=(SCREEN_WIDTH // 2, by + 44))
        self.screen.blit(t2, r2)

        t3 = self.ui.font_tiny.render(en_txt, True, (210, 235, 255))
        r3 = t3.get_rect(center=(SCREEN_WIDTH // 2, by + 66))
        self.screen.blit(t3, r3)

        # Baris 4: Hadiah yang didapatkan
        t4 = self.ui.font_tiny.render("🛡️ SHIELD BINTANG KEBAL + 💰 HUJAN 35 KOIN + ⚡ MEGA BOOST!", True, (0, 240, 255))
        r4 = t4.get_rect(center=(SCREEN_WIDTH // 2, by + 90))
        self.screen.blit(t4, r4)


def main():
    game = MobilLegendGame()
    game.run()

if __name__ == "__main__":
    main()
