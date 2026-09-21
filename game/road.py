"""
Modul Jalan & Lingkungan (Road & Scenery) untuk game Mobil Legend.
Mengatur animasi scrolling aspal, marka jalan, pembatas (curbs),
dan pemandangan di sisi jalan (pohon, lampu jalan, transisi tema).
"""

import math
import random
import pygame
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ROAD_WIDTH, ROAD_LEFT, ROAD_RIGHT,
    NUM_LANES, LANE_WIDTH, COLOR_ASPHALT, COLOR_ASPHALT_LINE,
    COLOR_CURB_RED, COLOR_CURB_WHITE
)

class RoadSideObject:
    def __init__(self, side, y, obj_type):
        self.side = side  # "left" or "right"
        self.y = y
        self.type = obj_type
        
        # Posisi X
        if side == "left":
            self.x = ROAD_LEFT - random.randint(35, 95)
        else:
            self.x = ROAD_RIGHT + random.randint(35, 95)

    def update(self, scroll_speed):
        self.y += scroll_speed

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 100 or self.y < -150

    def draw(self, surface, biome):
        cx = int(self.x)
        cy = int(self.y)

        if self.type == "tree":
            # Gambar Pohon sesuai Biome
            if biome == "desert":
                # Kaktus gurun
                pygame.draw.rect(surface, (45, 125, 60), (cx - 4, cy - 25, 8, 35), border_radius=3)
                pygame.draw.rect(surface, (45, 125, 60), (cx - 14, cy - 18, 12, 6), border_radius=2)
                pygame.draw.rect(surface, (45, 125, 60), (cx - 14, cy - 26, 6, 12), border_radius=2)
                pygame.draw.rect(surface, (45, 125, 60), (cx + 4, cy - 12, 12, 6), border_radius=2)
                pygame.draw.rect(surface, (45, 125, 60), (cx + 10, cy - 20, 6, 12), border_radius=2)
            elif biome == "cyber":
                # Tiang Neon Cyber
                pygame.draw.line(surface, (50, 60, 90), (cx, cy + 10), (cx, cy - 30), 4)
                glow = pygame.Surface((24, 24), pygame.SRCALPHA)
                pygame.draw.circle(glow, (0, 240, 255, 120), (12, 12), 10)
                surface.blit(glow, (cx - 12, cy - 38))
                pygame.draw.circle(surface, (230, 255, 255), (cx, cy - 26), 4)
            else:
                # Pohon Hijau Alami
                # Bayangan
                pygame.draw.ellipse(surface, (15, 60, 20, 100), (cx - 18, cy + 8, 36, 12))
                # Batang pohon
                pygame.draw.rect(surface, (100, 65, 35), (cx - 4, cy - 8, 8, 20), border_radius=2)
                # Daun berlapis
                pygame.draw.circle(surface, (30, 120, 45), (cx, cy - 12), 22)
                pygame.draw.circle(surface, (45, 155, 60), (cx - 4, cy - 16), 18)
                pygame.draw.circle(surface, (70, 185, 80), (cx - 2, cy - 20), 12)

        elif self.type == "lamp":
            # Lampu Jalan
            pole_color = (130, 140, 155) if biome != "cyber" else (70, 80, 120)
            pygame.draw.line(surface, pole_color, (cx, cy + 15), (cx, cy - 25), 3)
            # Kepala lampu mengarah ke jalan
            arm_dir = 1 if self.side == "left" else -1
            pygame.draw.line(surface, pole_color, (cx, cy - 25), (cx + arm_dir * 16, cy - 28), 3)
            # Bohlam lampu
            bulb_col = (255, 250, 180) if biome != "cyber" else (255, 80, 210)
            pygame.draw.circle(surface, bulb_col, (cx + arm_dir * 16, cy - 27), 4)


class Road:
    def __init__(self):
        self.scroll_y = 0.0
        self.curb_height = 36
        self.curb_width = 12
        self.dash_height = 42
        self.dash_gap = 32
        
        # Objek di pinggir jalan
        self.side_objects = []
        self._init_side_objects()

    def _init_side_objects(self):
        for y in range(-100, SCREEN_HEIGHT + 100, 80):
            for side in ("left", "right"):
                obj_type = "tree" if random.random() < 0.7 else "lamp"
                self.side_objects.append(RoadSideObject(side, y + random.randint(-15, 15), obj_type))

    def get_biome(self, distance):
        """Menentukan tema pemandangan berdasarkan jarak tempuh."""
        cycle = int(distance // 1500) % 3
        if cycle == 0:
            return "green"    # Lembah Hijau
        elif cycle == 1:
            return "desert"   # Gurun Senja
        else:
            return "cyber"    # Kota Neon Cyber

    def update(self, player_speed, distance):
        self.scroll_y = (self.scroll_y + player_speed) % (self.dash_height + self.dash_gap)
        
        # Update objek tepi jalan
        for obj in self.side_objects:
            obj.update(player_speed)
        
        # Hapus objek keluar layar
        self.side_objects = [obj for obj in self.side_objects if not obj.is_offscreen()]
        
        # Spawn objek baru di atas layar (maju) atau di bawah layar (mundur)
        if player_speed >= 0:
            min_y = min((obj.y for obj in self.side_objects), default=0)
            if min_y > -60:
                biome = self.get_biome(distance)
                for side in ("left", "right"):
                    obj_type = "tree" if random.random() < 0.75 else "lamp"
                    self.side_objects.append(RoadSideObject(side, min_y - random.randint(70, 100), obj_type))
        else:
            max_y = max((obj.y for obj in self.side_objects), default=SCREEN_HEIGHT)
            if max_y < SCREEN_HEIGHT + 60:
                biome = self.get_biome(distance)
                for side in ("left", "right"):
                    obj_type = "tree" if random.random() < 0.75 else "lamp"
                    self.side_objects.append(RoadSideObject(side, max_y + random.randint(70, 100), obj_type))

    def draw(self, surface, distance):
        biome = self.get_biome(distance)

        # 1. Warna Dasar Rumput / Tanah Sisi Jalan Sesuai Biome
        if biome == "desert":
            grass_col = (215, 160, 95)
            grass_grid = (195, 140, 80)
            road_asphalt = (60, 50, 48)
        elif biome == "cyber":
            grass_col = (18, 14, 32)
            grass_grid = (40, 28, 68)
            road_asphalt = (28, 25, 40)
        else:
            grass_col = (42, 145, 52)
            grass_grid = (34, 125, 42)
            road_asphalt = COLOR_ASPHALT

        surface.fill(grass_col)

        # Tekstur garis lembut di rumput/gurun
        for gy in range(0, SCREEN_HEIGHT, 40):
            offset_gy = (gy + int(self.scroll_y * 0.8)) % SCREEN_HEIGHT
            pygame.draw.line(surface, grass_grid, (0, offset_gy), (ROAD_LEFT, offset_gy), 1)
            pygame.draw.line(surface, grass_grid, (ROAD_RIGHT, offset_gy), (SCREEN_WIDTH, offset_gy), 1)

        # 2. Gambar Objek Tepi Jalan (di bawah pembatas)
        for obj in self.side_objects:
            obj.draw(surface, biome)

        # 3. Aspal Jalan Raya Utama
        pygame.draw.rect(surface, road_asphalt, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        # 4. Pembatas Jalan Merah-Putih (Curbs / Rumble Strips)
        curb_cycle = self.curb_height * 2
        offset_curb = int(self.scroll_y * 1.5) % curb_cycle
        
        for y in range(-curb_cycle, SCREEN_HEIGHT + curb_cycle, self.curb_height):
            actual_y = y + offset_curb
            idx = int(actual_y // self.curb_height)
            curb_col = COLOR_CURB_RED if idx % 2 == 0 else COLOR_CURB_WHITE
            if biome == "cyber" and curb_col == COLOR_CURB_RED:
                curb_col = (255, 0, 110)
            elif biome == "cyber" and curb_col == COLOR_CURB_WHITE:
                curb_col = (0, 240, 255)

            # Curb Kiri
            pygame.draw.rect(surface, curb_col, (ROAD_LEFT - self.curb_width, actual_y, self.curb_width, self.curb_height))
            # Curb Kanan
            pygame.draw.rect(surface, curb_col, (ROAD_RIGHT, actual_y, self.curb_width, self.curb_height))

        # Garis Solid Tepi Jalan
        edge_line_col = (255, 255, 255) if biome != "cyber" else (0, 255, 220)
        pygame.draw.line(surface, edge_line_col, (ROAD_LEFT + 2, 0), (ROAD_LEFT + 2, SCREEN_HEIGHT), 3)
        pygame.draw.line(surface, edge_line_col, (ROAD_RIGHT - 3, 0), (ROAD_RIGHT - 3, SCREEN_HEIGHT), 3)

        # 5. Marka Garis Putus-Putus Tiap Jalur (Lane Dividers)
        lane_step = self.dash_height + self.dash_gap
        offset_dash = int(self.scroll_y) % lane_step
        
        for lane in range(1, NUM_LANES):
            lane_x = ROAD_LEFT + lane * LANE_WIDTH
            for y in range(-lane_step, SCREEN_HEIGHT + lane_step, lane_step):
                dash_y = y + offset_dash
                line_col = COLOR_ASPHALT_LINE if biome != "cyber" else (0, 230, 255)
                pygame.draw.rect(surface, line_col, (lane_x - 2, dash_y, 4, self.dash_height), border_radius=2)
