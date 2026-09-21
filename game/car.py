"""
Modul Kendaraan untuk game Mobil Legend (GameKhansa).
Mendukung Mobil Balap Super Cepat (dengan Turbo Nitro)
dan Tank Tempur Lapis Baja (dengan Roda Rantai & Meriam Tembak Peledak).
"""

import math
import random
import pygame
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ROAD_LEFT, ROAD_RIGHT,
    CARS_DATA, TRAFFIC_TYPES, COLOR_WHITE, COLOR_NITRO_CYAN
)

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.max_lifetime = lifetime
        self.lifetime = lifetime

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(0.5, self.size * 0.94)

    def draw(self, surface):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            p_surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            col = (*self.color[:3], alpha)
            pygame.draw.circle(p_surf, col, (int(self.size), int(self.size)), int(self.size))
            surface.blit(p_surf, (self.x - self.size, self.y - self.size))


class SkidMark:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.lifetime = 45

    def update(self, scroll_speed):
        self.y1 += scroll_speed
        self.y2 += scroll_speed
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            min_x = int(min(self.x1, self.x2)) - 3
            min_y = int(min(self.y1, self.y2)) - 3
            max_x = int(max(self.x1, self.x2)) + 3
            max_y = int(max(self.y1, self.y2)) + 3
            w = max(4, max_x - min_x)
            h = max(4, max_y - min_y)
            if -w < min_x < SCREEN_WIDTH and -h < min_y < SCREEN_HEIGHT:
                alpha = min(120, int(120 * (self.lifetime / 45)))
                skid_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                pygame.draw.line(skid_surf, (25, 25, 30, alpha), (self.x1 - min_x, self.y1 - min_y), (self.x2 - min_x, self.y2 - min_y), 4)
                surface.blit(skid_surf, (min_x, min_y))


class TankShell:
    """Proyektil Peluru Meriam yang ditembakkan oleh Tank Tempur."""
    def __init__(self, x, y, vy=-18.0, is_plasma=False):
        self.x = x
        self.y = y
        self.vy = vy
        self.is_plasma = is_plasma
        self.radius = 5
        self.lifetime = 50
        self.particles = []

    def update(self):
        self.y += self.vy
        self.lifetime -= 1
        # Asap roket & percikan api di belakang peluru
        col = (0, 240, 255) if self.is_plasma else random.choice([(255, 180, 40), (255, 100, 20), (240, 240, 240)])
        self.particles.append(Particle(
            self.x + random.uniform(-1.5, 1.5), self.y + 6,
            random.uniform(-0.4, 0.4), random.uniform(2, 5),
            col, random.uniform(2.5, 4.5), 10
        ))
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def is_offscreen(self):
        return self.y < -50 or self.lifetime <= 0

    def get_rect(self):
        return pygame.Rect(self.x - 7, self.y - 10, 14, 20)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

        col = (0, 230, 255) if self.is_plasma else (255, 210, 50)
        # Glow peluru
        glow = pygame.Surface((20, 26), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (*col, 110), (0, 0, 20, 26))
        surface.blit(glow, (int(self.x - 10), int(self.y - 13)))

        # Kepala peluru
        pygame.draw.circle(surface, col, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius - 2)


class Explosion:
    """Efek Ledakan saat mobil musuh atau rintangan hancur tertembak meriam."""
    def __init__(self, x, y, size=1.0):
        self.x = x
        self.y = y
        self.lifetime = 24
        self.particles = []
        num_parts = int(22 * size)
        for _ in range(num_parts):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2.0, 7.0) * size
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            col = random.choice([(255, 240, 60), (255, 130, 20), (230, 40, 20), (70, 70, 75)])
            self.particles.append(Particle(x, y, vx, vy, col, random.uniform(4, 9) * size, random.randint(14, 24)))

    def update(self, scroll_speed=0):
        self.y += scroll_speed
        self.lifetime -= 1
        for p in self.particles:
            p.y += scroll_speed
            p.update()
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class PlayerCar:
    """Kelas Kendaraan Pemain (bisa berupa Mobil Balap atau Tank Tempur)."""
    def __init__(self, car_id="merah_kilat"):
        self.car_id = car_id
        self.data = CARS_DATA.get(car_id, CARS_DATA["merah_kilat"])
        self.vehicle_type = self.data.get("type", "car")

        # Dimensi Kendaraan (Tank lebih lebar dan kekar)
        if self.vehicle_type == "tank":
            self.width = 48
            self.height = 76
        else:
            self.width = 42
            self.height = 76

        # Posisi & Fisika
        self.x = (ROAD_LEFT + ROAD_RIGHT) // 2
        self.default_y = SCREEN_HEIGHT - 135
        self.y = self.default_y
        self.prev_x = self.x
        self.prev_y = self.y
        self.player_name = "Khansa"


        self.speed = 0.0
        self.base_max_speed = self.data["max_speed"]
        self.accel = self.data["accel"]
        self.handling = self.data["handling"]

        # HP & Kekuatan
        self.max_hp = self.data["max_hp"]
        self.hp = self.max_hp

        # Khusus Mobil: Nitro
        self.max_nitro = self.data.get("nitro_duration", 150)
        self.nitro = self.max_nitro
        self.is_nitro_active = False

        # Khusus Tank: Meriam & Rantai
        self.cannon_cooldown = self.data.get("cannon_cooldown", 22)
        self.shoot_timer = 0
        self.muzzle_flash_timer = 0
        self.tread_scroll = 0.0
        self.shells = []

        # Efek & Status
        self.invulnerable_timer = 0
        self.super_shield_timer = 0
        self.super_shield_anim = 0.0
        self.slip_timer = 0
        self.slip_direction = 1
        self.angle = 0.0

        # Partikel & Jejak
        self.particles = []
        self.skid_marks = []

        # Jarak & Skor
        self.distance = 0.0
        self.coins = 0

    def set_car(self, car_id):
        self.car_id = car_id
        self.data = CARS_DATA.get(car_id, CARS_DATA["merah_kilat"])
        self.vehicle_type = self.data.get("type", "car")
        if self.vehicle_type == "tank":
            self.width = 48
            self.height = 76
        else:
            self.width = 42
            self.height = 76

        self.base_max_speed = self.data["max_speed"]
        self.accel = self.data["accel"]
        self.handling = self.data["handling"]
        self.max_hp = self.data["max_hp"]
        self.hp = self.max_hp
        self.max_nitro = self.data.get("nitro_duration", 150)
        self.nitro = self.max_nitro
        self.cannon_cooldown = self.data.get("cannon_cooldown", 22)
        self.shoot_timer = 0
        self.muzzle_flash_timer = 0
        self.shells.clear()

    def update(self, keys):
        self.prev_x = self.x
        self.prev_y = self.y
        fired_cannon = False

        # 1. Kontrol Spesial: Tembak Meriam (Tank) ATAU Turbo Nitro (Mobil)
        if self.vehicle_type == "tank":
            # Tank menembak meriam saat tombol SPACE ditekan
            if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
                is_plasma = (self.car_id == "titan_khansa")
                # Munculkan peluru dari ujung moncong laras meriam
                cannon_tip_y = self.y - self.height // 2 - 16
                self.shells.append(TankShell(self.x, cannon_tip_y, is_plasma=is_plasma))
                self.shoot_timer = self.cannon_cooldown
                self.muzzle_flash_timer = 6
                self.y += 2.5  # Efek dorongan hentakan balik (recoil)
                fired_cannon = True

            if self.shoot_timer > 0:
                self.shoot_timer -= 1
            if self.muzzle_flash_timer > 0:
                self.muzzle_flash_timer -= 1

            current_max_speed = self.base_max_speed
            current_accel = self.accel
            self.is_nitro_active = False

        else:
            # Mobil Balap: Turbo Nitro
            if (keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]) and self.nitro > 0 and self.speed > 3.0:
                self.is_nitro_active = True
                self.nitro = max(0, self.nitro - 1.2)
                current_max_speed = self.base_max_speed * 1.35
                current_accel = self.accel * 1.8
            else:
                self.is_nitro_active = False
                current_max_speed = self.base_max_speed
                current_accel = self.accel
                if self.nitro < self.max_nitro and self.speed > 5.0:
                    self.nitro = min(self.max_nitro, self.nitro + 0.1)

        # 2. Akselerasi / Pengereman & Melaju Mundur (Reverse)
        if self.slip_timer > 0:
            self.slip_timer -= 1
            self.x += self.slip_direction * (2.2 if self.vehicle_type == "tank" else 3.5)
            self.angle = math.sin(self.slip_timer * 0.4) * (14.0 if self.vehicle_type == "tank" else 25.0)
            self.speed = max(3.0, self.speed * 0.98)
        else:
            is_gas = keys[pygame.K_UP] or keys[pygame.K_w]
            is_brake = keys[pygame.K_DOWN] or keys[pygame.K_s]
            max_reverse_speed = -4.0 if self.vehicle_type == "tank" else -5.0

            if is_gas:
                if self.speed < 0:
                    # Sedang mundur lalu tekan gas -> rem mundur cepat menuju 0
                    self.speed = min(current_max_speed, self.speed + current_accel * 2.5)
                else:
                    self.speed = min(current_max_speed, self.speed + current_accel)
            elif is_brake:
                if self.speed > 0:
                    # Sedang maju lalu tekan rem -> rem cepat menuju 0
                    self.speed = max(0.0, self.speed - current_accel * 2.5)
                else:
                    # Sudah berhenti atau sedang mundur -> melaju mundur!
                    self.speed = max(max_reverse_speed, self.speed - current_accel * 1.3)
            else:
                # Gesekan alami meluncur kembali ke diam
                if self.speed > 0:
                    self.speed = max(0.0, self.speed - 0.08)
                elif self.speed < 0:
                    self.speed = min(0.0, self.speed + 0.12)

            # Kemudi Kiri / Kanan (Bisa belok kapan saja, TIDAK PERLU sambil ngegas!)
            is_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
            is_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
            target_angle = 0.0

            # Kemudi responsif penuh kapan saja (bahkan saat diam atau melambat)
            abs_speed = abs(self.speed)
            steer_factor = max(0.85, min(1.0, abs_speed / 4.0))

            if is_left:
                self.x -= self.handling * steer_factor
                target_angle = -7.0 if self.vehicle_type == "tank" else -12.0
            elif is_right:
                self.x += self.handling * steer_factor
                target_angle = 7.0 if self.vehicle_type == "tank" else 12.0

            # Jika sedang mundur, balik kemiringan visual setir agar realistis
            if self.speed < -0.5:
                target_angle = -target_angle * 0.7

            self.angle += (target_angle - self.angle) * 0.28

        # 3. Batasan Tepi Jalan & Kembalikan Posisi Vertikal secara Halus
        half_w = self.width / 2
        min_x = ROAD_LEFT + half_w + 4
        max_x = ROAD_RIGHT - half_w - 4
        if self.x < min_x:
            self.x = min_x
            if self.speed > 0:
                self.speed = max(2.0, self.speed * 0.9)
            elif self.speed < 0:
                self.speed = min(-1.5, self.speed * 0.9)
        elif self.x > max_x:
            self.x = max_x
            if self.speed > 0:
                self.speed = max(2.0, self.speed * 0.9)
            elif self.speed < 0:
                self.speed = min(-1.5, self.speed * 0.9)

        # Kembalikan posisi Y secara mulus ke posisi default balap
        if abs(self.y - self.default_y) > 0.5:
            self.y += (self.default_y - self.y) * 0.08

        # Pastikan kendaraan selalu terlihat utuh penuh di layar (tidak tenggelam di bawah layar)
        min_y = 120 + self.height // 2
        max_y = SCREEN_HEIGHT - self.height // 2 - 24
        self.y = max(min_y, min(max_y, self.y))

        # 4. Jarak Tempuh & Rantai Tank
        self.distance = max(0.0, self.distance + self.speed * 0.45)
        self.tread_scroll = (self.tread_scroll + self.speed * 0.8) % 14


        # 5. Timer Kebal Sementara & Super Shield Bintang
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        if self.super_shield_timer > 0:
            self.super_shield_timer -= 1
            self.super_shield_anim += 0.12
            if random.random() < 0.6:
                spark_cols = [(255, 215, 0), (0, 235, 255), (255, 80, 200), (50, 255, 120), (255, 160, 50)]
                self.particles.append(Particle(
                    self.x + random.uniform(-20, 20),
                    self.y + random.uniform(-25, 25),
                    random.uniform(-1.0, 1.0),
                    random.uniform(1.0, 4.0),
                    random.choice(spark_cols),
                    random.uniform(3.0, 5.5),
                    20
                ))

        # 6. Update Peluru Tank
        for s in self.shells:
            s.update()
        self.shells = [s for s in self.shells if not s.is_offscreen()]

        # 7. Efek Partikel
        self._update_effects()

        return fired_cannon

    def hit_oil(self):
        if self.slip_timer <= 0:
            self.slip_timer = 28 if self.vehicle_type == "tank" else 40
            self.slip_direction = random.choice([-1, 1])

    def take_damage(self, amount):
        if self.super_shield_timer > 0:
            # Kebal total saat Super Shield aktif!
            return False
        if self.invulnerable_timer <= 0:
            # Tank memiliki ketahanan benturan alami 30% lebih tangguh
            actual_dmg = int(amount * 0.7) if self.vehicle_type == "tank" else amount
            self.hp = max(0, self.hp - actual_dmg)
            self.invulnerable_timer = 55
            self.speed = max(2.0, self.speed * (0.75 if self.vehicle_type == "tank" else 0.5))
            return True
        return False

    def add_hp(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def add_nitro(self, amount):
        self.nitro = min(self.max_nitro, self.nitro + amount)

    def _update_effects(self):
        # Partikel Knalpot Mobil / Asap Diesel Tank
        if self.speed > 1.5:
            back_y = self.y + self.height // 2
            if self.vehicle_type == "tank":
                # Asap knalpot diesel hitam kelabu pekat
                if random.random() < 0.45:
                    self.particles.append(Particle(
                        self.x + random.uniform(-10, 10), back_y + 2,
                        random.uniform(-0.4, 0.4), random.uniform(2, 4),
                        (55, 55, 60), random.uniform(3.0, 5.5), random.randint(12, 18)
                    ))
            else:
                # Knalpot mobil sport
                for ex in (self.x - 12, self.x + 12):
                    if self.is_nitro_active:
                        col = random.choice([COLOR_NITRO_CYAN, (255, 140, 0), (255, 230, 50), (255, 255, 255)])
                        self.particles.append(Particle(
                            ex + random.uniform(-2, 2), back_y + random.uniform(2, 6),
                            random.uniform(-0.6, 0.6), random.uniform(3, 7),
                            col, random.uniform(3.5, 6.0), random.randint(10, 18)
                        ))
                    elif random.random() < 0.35:
                        self.particles.append(Particle(
                            ex + random.uniform(-1, 1), back_y + 4,
                            random.uniform(-0.3, 0.3), random.uniform(2, 4),
                            (160, 160, 165), random.uniform(2.0, 3.5), random.randint(8, 14)
                        ))

        # Jejak Roda / Ban
        if abs(self.angle) > 5.0 and self.speed > 5.0:
            rear_y = self.y + self.height // 2 - 4
            self.skid_marks.append(SkidMark(self.prev_x - 14, rear_y, self.x - 14, rear_y))
            self.skid_marks.append(SkidMark(self.prev_x + 14, rear_y, self.x + 14, rear_y))

        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.lifetime > 0]

        for sm in self.skid_marks:
            sm.update(self.speed * 0.6)
        self.skid_marks = [sm for sm in self.skid_marks if sm.lifetime > 0]
        if len(self.skid_marks) > 30:
            self.skid_marks = self.skid_marks[-30:]

    def get_rect(self):
        margin_x = 4
        margin_y = 6
        return pygame.Rect(
            self.x - self.width // 2 + margin_x,
            self.y - self.height // 2 + margin_y,
            self.width - margin_x * 2,
            self.height - margin_y * 2
        )

    def draw(self, surface):
        # Gambar Jejak Skid Marks
        for sm in self.skid_marks:
            sm.draw(surface)

        # Gambar Partikel
        for p in self.particles:
            p.draw(surface)

        # Gambar Peluru Tank yang sedang meluncur
        for s in self.shells:
            s.draw(surface)

        # Kedipan Kebal
        if self.invulnerable_timer > 0 and (self.invulnerable_timer // 6) % 2 == 1:
            return

        # Sorot Lampu Depan
        self._draw_headlights(surface)

        # Gambar Kendaraan (Tank vs Mobil)
        if self.vehicle_type == "tank":
            self._draw_tank(surface)
        else:
            self._draw_car(surface)

        # Gambar Super Shield Bintang Pelangi jika aktif
        if self.super_shield_timer > 0:
            self._draw_super_shield(surface)

    def _draw_super_shield(self, surface):
        """Menggambar Perisai Bintang Pelangi Bercahaya dan Bintang Berputar Mengorbit Kendaraan."""
        cx = int(self.x)
        cy = int(self.y)
        radius = max(self.width, self.height) // 2 + 14

        # Warna pelangi dinamis
        hue_deg = (self.super_shield_anim * 45) % 360
        r = int(127 + 127 * math.sin(math.radians(hue_deg)))
        g = int(127 + 127 * math.sin(math.radians(hue_deg + 120)))
        b = int(127 + 127 * math.sin(math.radians(hue_deg + 240)))
        shield_color = (r, g, b)

        # Lingkaran aura perisai transparan
        shield_surf = pygame.Surface((radius * 2 + 24, radius * 2 + 24), pygame.SRCALPHA)
        center_surf = (radius + 12, radius + 12)
        pygame.draw.circle(shield_surf, (*shield_color, 65), center_surf, radius + 6)
        pygame.draw.circle(shield_surf, (*shield_color, 150), center_surf, radius, width=4)
        pygame.draw.circle(shield_surf, (255, 255, 255, 210), center_surf, radius - 2, width=2)
        surface.blit(shield_surf, (cx - radius - 12, cy - radius - 12))

        # 3 Bintang Emas Berputar Mengelilingi Kendaraan
        num_stars = 3
        orbit_radius = radius + 8
        for i in range(num_stars):
            angle = self.super_shield_anim + i * (2.0 * math.pi / num_stars)
            sx = cx + int(math.cos(angle) * orbit_radius)
            sy = cy + int(math.sin(angle) * orbit_radius)

            star_pts = [
                (sx, sy - 8),
                (sx + 2, sy - 2),
                (sx + 8, sy),
                (sx + 2, sy + 2),
                (sx, sy + 8),
                (sx - 2, sy + 2),
                (sx - 8, sy),
                (sx - 2, sy - 2),
            ]
            pygame.draw.polygon(surface, (255, 225, 40), star_pts)
            pygame.draw.circle(surface, (255, 255, 255), (sx, sy), 2)

    def _draw_tank(self, surface):
        """Merender Tank Tempur Lapis Baja dengan Roda Rantai dan Meriam."""
        tank_surf = pygame.Surface((self.width + 30, self.height + 40), pygame.SRCALPHA)
        cx = (self.width + 30) // 2
        cy = (self.height + 40) // 2 + 6
        hw = self.width // 2
        hh = self.height // 2

        prim_col = self.data["primary_color"]
        camo_col = self.data["stripe_color"]

        # Bayangan Tank
        shadow_rect = pygame.Rect(cx - hw - 3, cy - hh + 4, self.width + 6, self.height + 4)
        pygame.draw.rect(tank_surf, (10, 12, 15, 110), shadow_rect, border_radius=6)

        # Roda Rantai Kiri & Kanan (Caterpillar Treads)
        tread_w = 11
        for tx in (cx - hw - 1, cx + hw - tread_w + 1):
            # Latar rantai hitam
            pygame.draw.rect(tank_surf, (28, 30, 32), (tx, cy - hh, tread_w, self.height), border_radius=4)
            # Bergerigi / link rantai yang berputar
            for ty in range(int(cy - hh - self.tread_scroll), int(cy + hh + 14), 10):
                if cy - hh <= ty <= cy + hh - 3:
                    pygame.draw.line(tank_surf, (55, 60, 65), (tx + 1, ty), (tx + tread_w - 2, ty), 2)
            # Roda pemutar di dalam rantai
            for wy in (-24, -8, 8, 24):
                pygame.draw.circle(tank_surf, (70, 75, 80), (tx + tread_w // 2, cy + wy), 3)

        # Bodi Lapis Baja Utama (Armored Hull)
        hull_rect = pygame.Rect(cx - hw + 8, cy - hh + 4, self.width - 16, self.height - 8)
        pygame.draw.rect(tank_surf, prim_col, hull_rect, border_radius=6)
        
        # Pola Loreng Kamuflase / Armor Plate
        pygame.draw.rect(tank_surf, camo_col, (cx - hw + 10, cy - hh + 8, 14, 20), border_radius=3)
        pygame.draw.rect(tank_surf, camo_col, (cx + 2, cy + 2, 12, 22), border_radius=3)

        # Pelat Depan Bersudut (Glacis Plate)
        pygame.draw.polygon(tank_surf, tuple(max(0, c - 20) for c in prim_col), [
            (cx - hw + 8, cy - hh + 4),
            (cx + hw - 8, cy - hh + 4),
            (cx + hw - 11, cy - hh + 16),
            (cx - hw + 11, cy - hh + 16)
        ])

        # Laras Meriam Panjang (Cannon Barrel)
        barrel_w = 6 if self.car_id != "titan_khansa" else 8
        barrel_len = 34
        barrel_rect = pygame.Rect(cx - barrel_w // 2, cy - hh - barrel_len + 12, barrel_w, barrel_len)
        barrel_col = (50, 55, 60) if self.car_id != "titan_khansa" else (30, 80, 110)
        pygame.draw.rect(tank_surf, barrel_col, barrel_rect, border_radius=2)
        
        # Moncong Meriam (Muzzle Brake)
        pygame.draw.rect(tank_surf, (80, 85, 90), (cx - barrel_w // 2 - 2, cy - hh - barrel_len + 8, barrel_w + 4, 6), border_radius=2)

        # Kubah Meriam Tengah (Turret)
        turret_w = 26
        turret_h = 30
        turret_rect = pygame.Rect(cx - turret_w // 2, cy - turret_h // 2, turret_w, turret_h)
        pygame.draw.rect(tank_surf, prim_col, turret_rect, border_radius=8)
        pygame.draw.rect(tank_surf, (30, 35, 40), turret_rect, width=2, border_radius=8)

        # Pintu Palka Komandan (Commander Hatch)
        pygame.draw.circle(tank_surf, (20, 25, 30), (cx, cy + 3), 6)
        pygame.draw.circle(tank_surf, (70, 75, 80), (cx, cy + 3), 3)

        # Lampu Depan Tank (Dual Armor Headlights)
        pygame.draw.rect(tank_surf, (255, 255, 200), (cx - hw + 7, cy - hh + 4, 6, 3), border_radius=1)
        pygame.draw.rect(tank_surf, (255, 255, 200), (cx + hw - 13, cy - hh + 4, 6, 3), border_radius=1)

        # Muzzle Flash saat menembak meriam
        if self.muzzle_flash_timer > 0:
            flash_col = (0, 240, 255) if self.car_id == "titan_khansa" else (255, 200, 40)
            flash_y = cy - hh - barrel_len + 8
            pygame.draw.circle(tank_surf, flash_col, (cx, flash_y), 14)
            pygame.draw.circle(tank_surf, (255, 255, 255), (cx, flash_y), 7)

        # Rotasi Tank
        rot_surf = pygame.transform.rotate(tank_surf, -self.angle)
        rot_rect = rot_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rot_surf, rot_rect)

    def _draw_car(self, surface):
        """Merender Mobil Balap Sport."""
        car_surf = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
        cx = (self.width + 20) // 2
        cy = (self.height + 20) // 2
        hw = self.width // 2
        hh = self.height // 2
        half_w = hw
        half_h = hh

        # Bayangan Mobil
        shadow_rect = pygame.Rect(cx - hw - 2, cy - hh + 4, self.width + 4, self.height + 2)
        pygame.draw.rect(car_surf, (10, 10, 15, 100), shadow_rect, border_radius=8)

        # Roda / Ban Mobil
        wheel_w, wheel_h = 7, 15
        for wx in (cx - hw - 2, cx + hw - wheel_w + 2):
            for wy in (cy - hh + 8, cy + hh - 22):
                pygame.draw.rect(car_surf, (25, 25, 30), (wx, wy, wheel_w, wheel_h), border_radius=3)

        # Bodi Utama Mobil
        body_rect = pygame.Rect(cx - hw, cy - hh, self.width, self.height)
        pygame.draw.rect(car_surf, self.data["primary_color"], body_rect, border_radius=9)

        # Striping Balap
        stripe_col = self.data["stripe_color"]
        pygame.draw.rect(car_surf, stripe_col, (cx - 4, cy - hh + 2, 8, self.height - 4))

        # Kaca Depan & Belakang
        pygame.draw.rect(car_surf, (28, 40, 55), (cx - hw + 5, cy - hh + 18, self.width - 10, 14), border_radius=3)
        pygame.draw.rect(car_surf, (20, 30, 42), (cx - hw + 6, cy + hh - 24, self.width - 12, 10), border_radius=3)

        # Atap Mobil
        pygame.draw.rect(car_surf, self.data["primary_color"], (cx - hw + 4, cy - hh + 30, self.width - 8, 20))

        # Spoiler Belakang
        spoiler_rect = pygame.Rect(cx - hw + 2, cy + hh - 6, self.width - 4, 5)
        pygame.draw.rect(car_surf, (30, 30, 35), spoiler_rect, border_radius=2)

        # Lampu Belakang (Merah saat maju/rem, Putih terang saat mundur) & Depan
        tail_col = (255, 255, 255) if self.speed < -0.2 else (255, 30, 30)
        pygame.draw.rect(car_surf, tail_col, (cx - half_w + 2, cy + half_h - 4, 8, 3))
        pygame.draw.rect(car_surf, tail_col, (cx + half_w - 10, cy + half_h - 4, 8, 3))
        pygame.draw.rect(car_surf, (255, 255, 210), (cx - half_w + 3, cy - half_h + 2, 8, 4), border_radius=2)
        pygame.draw.rect(car_surf, (255, 255, 210), (cx + half_w - 11, cy - half_h + 2, 8, 4), border_radius=2)

        rot_surf = pygame.transform.rotate(car_surf, -self.angle)
        rot_rect = rot_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rot_surf, rot_rect)

    def _draw_headlights(self, surface):
        cone_len = 140
        cone_w = 200
        hw = cone_w // 2
        light_surf = pygame.Surface((cone_w, cone_len + 10), pygame.SRCALPHA)
        left_poly = [(hw - 14, cone_len), (hw - 46, 0), (hw - 6, 0)]
        right_poly = [(hw + 14, cone_len), (hw + 6, 0), (hw + 46, 0)]
        pygame.draw.polygon(light_surf, (255, 255, 220, 22), left_poly)
        pygame.draw.polygon(light_surf, (255, 255, 220, 22), right_poly)
        surface.blit(light_surf, (int(self.x - hw), int(self.y - self.height // 2 - cone_len)))


class TrafficCar:
    """Mobil Lalu Lintas."""
    def __init__(self, lane_idx, start_y):
        self.type_data = random.choice(TRAFFIC_TYPES)
        self.width = self.type_data["width"]
        self.height = self.type_data["height"]

        from .constants import LANE_CENTERS
        self.lane_idx = lane_idx
        self.x = LANE_CENTERS[lane_idx]
        self.y = start_y

        self.base_speed = self.type_data["speed"] + random.uniform(-0.5, 0.8)
        self.passed = False

    def update(self, player_speed):
        rel_speed = player_speed - self.base_speed
        self.y += rel_speed

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 150 or self.y < -350

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2 + 2,
            self.y - self.height // 2 + 3,
            self.width - 4,
            self.height - 6
        )

    def draw(self, surface):
        half_w = self.width // 2
        half_h = self.height // 2

        # Jangan gambar jika kendaraan sudah lewat atau di luar layar penuh
        if self.y - half_h >= SCREEN_HEIGHT or self.y + half_h <= -10:
            return

        cx = int(self.x)
        cy = int(self.y)
        col = self.type_data["color"]
        roof_col = self.type_data["roof_color"]


        # Bayangan
        shadow = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (15, 15, 20, 95), (0, 0, self.width + 4, self.height + 4), border_radius=6)
        surface.blit(shadow, (cx - half_w - 2, cy - half_h + 3))

        # Ban
        wheel_w, wheel_h = 6, 14
        for wx in (cx - half_w - 2, cx + half_w - wheel_w + 2):
            for wy in (cy - half_h + 8, cy + half_h - 20):
                pygame.draw.rect(surface, (25, 25, 30), (wx, wy, wheel_w, wheel_h), border_radius=2)

        # Bodi
        pygame.draw.rect(surface, col, (cx - half_w, cy - half_h, self.width, self.height), border_radius=7)

        # Detail Truk vs Mobil
        if self.type_data["type"] == "truck":
            pygame.draw.rect(surface, (50, 50, 60), (cx - half_w + 3, cy + half_h - 32, self.width - 6, 28), border_radius=3)
            pygame.draw.rect(surface, (40, 70, 95), (cx - half_w + 5, cy + half_h - 28, self.width - 10, 10), border_radius=2)
            pygame.draw.rect(surface, roof_col, (cx - half_w + 2, cy - half_h + 3, self.width - 4, self.height - 38), border_radius=4)
            for gy in range(cy - half_h + 10, cy + half_h - 35, 12):
                pygame.draw.line(surface, (60, 40, 20), (cx - half_w + 4, gy), (cx + half_w - 4, gy), 1)
        else:
            pygame.draw.rect(surface, (35, 55, 75), (cx - half_w + 4, cy - half_h + 16, self.width - 8, 12), border_radius=3)
            pygame.draw.rect(surface, (30, 45, 65), (cx - half_w + 5, cy + half_h - 22, self.width - 10, 9), border_radius=2)
            pygame.draw.rect(surface, roof_col, (cx - half_w + 3, cy - half_h + 29, self.width - 6, 16), border_radius=3)

            if self.type_data["type"] == "taxi":
                pygame.draw.rect(surface, (255, 255, 255), (cx - 7, cy - 3, 14, 6), border_radius=2)
                pygame.draw.rect(surface, (20, 20, 20), (cx - 5, cy - 1, 10, 2))

        # Lampu Depan & Belakang
        pygame.draw.rect(surface, (255, 255, 200), (cx - half_w + 3, cy - half_h + 1, 6, 3), border_radius=1)
        pygame.draw.rect(surface, (255, 255, 200), (cx + half_w - 9, cy - half_h + 1, 6, 3), border_radius=1)
        pygame.draw.rect(surface, (240, 40, 40), (cx - half_w + 3, cy + half_h - 3, 6, 2))
        pygame.draw.rect(surface, (240, 40, 40), (cx + half_w - 9, cy + half_h - 3, 6, 2))
