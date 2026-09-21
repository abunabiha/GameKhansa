"""
Modul Rintangan & Item Koleksi untuk game Mobil Legend.
Berisi Coin, NitroBottle, RepairKit, OilSlick, dan RoadBlock.
"""

import math
import random
import pygame
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GOLD, COLOR_NITRO_CYAN,
    COLOR_HEALTH_GREEN
)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.anim_timer = random.randint(0, 100)
        self.collected = False

    def update(self, scroll_speed):
        self.y += scroll_speed
        self.anim_timer += 1

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 50

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self, surface):
        self.anim_timer += 0.08
        # Efek koin berputar 3D (skala horizontal sin)
        scale_x = abs(math.cos(self.anim_timer))
        w = max(3, int(self.radius * 2 * scale_x))
        h = self.radius * 2
        
        # Bayangan koin
        shadow = pygame.Surface((w, 6), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (20, 20, 25, 80), (0, 0, w, 6))
        surface.blit(shadow, (self.x - w // 2, self.y + self.radius - 2))

        # Badan koin
        coin_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(coin_surf, COLOR_GOLD, (0, 0, w, h))
        pygame.draw.ellipse(coin_surf, (255, 245, 120), (2, 2, max(1, w - 4), h - 4))
        
        # Tanda $ atau garis tengah jika cukup lebar
        if w > 10:
            pygame.draw.line(coin_surf, (200, 150, 0), (w // 2, 4), (w // 2, h - 4), 2)
            
        surface.blit(coin_surf, (self.x - w // 2, self.y - h // 2))


class NitroBottle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 22
        self.height = 36
        self.pulse = random.random() * math.pi

    def update(self, scroll_speed):
        self.y += scroll_speed
        self.pulse += 0.08

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 50

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, surface):
        glow_size = int(math.sin(self.pulse) * 3)
        cx = int(self.x)
        cy = int(self.y)
        hw = self.width // 2
        hh = self.height // 2

        # Efek Cahaya / Glow di sekitar botol
        glow_surf = pygame.Surface((self.width + 16, self.height + 16), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*COLOR_NITRO_CYAN, 45 + glow_size * 5),
                         (0, 0, self.width + 16, self.height + 16), border_radius=8)
        surface.blit(glow_surf, (cx - hw - 8, cy - hh - 8))

        # Tabung Nitro (Silinder Cyan)
        bottle_rect = pygame.Rect(cx - hw, cy - hh + 6, self.width, self.height - 6)
        pygame.draw.rect(surface, (0, 170, 210), bottle_rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_NITRO_CYAN, (cx - hw + 3, cy - hh + 8, self.width - 6, self.height - 10), border_radius=4)
        
        # Leher botol & tutup
        pygame.draw.rect(surface, (180, 190, 200), (cx - 5, cy - hh + 1, 10, 6), border_radius=2)
        pygame.draw.rect(surface, (230, 240, 250), (cx - 3, cy - hh - 2, 6, 4), border_radius=1)

        # Label N2O
        label_rect = pygame.Rect(cx - hw + 2, cy - 4, self.width - 4, 8)
        pygame.draw.rect(surface, (20, 25, 35), label_rect)
        pygame.draw.line(surface, (255, 255, 255), (cx - 4, cy), (cx + 4, cy), 2)


class RepairKit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 28
        self.float_offset = random.random() * math.pi

    def update(self, scroll_speed):
        self.y += scroll_speed
        self.float_offset += 0.06

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 50

    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def draw(self, surface):
        offset_y = math.sin(self.float_offset) * 3
        cx = int(self.x)
        cy = int(self.y + offset_y)
        hs = self.size // 2

        # Kotak P3K / Reparasi
        box_rect = pygame.Rect(cx - hs, cy - hs, self.size, self.size)
        pygame.draw.rect(surface, (245, 245, 250), box_rect, border_radius=6)
        pygame.draw.rect(surface, (200, 200, 210), box_rect, width=2, border_radius=6)

        # Palang Hijau / Merah Kesehatan
        cross_w = 6
        cross_l = 16
        pygame.draw.rect(surface, COLOR_HEALTH_GREEN, (cx - cross_w // 2, cy - cross_l // 2, cross_w, cross_l), border_radius=2)
        pygame.draw.rect(surface, COLOR_HEALTH_GREEN, (cx - cross_l // 2, cy - cross_w // 2, cross_l, cross_w), border_radius=2)


class OilSlick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = random.randint(46, 58)
        self.height = random.randint(30, 42)

    def update(self, scroll_speed):
        self.y += scroll_speed

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 50

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2 + 6, self.y - self.height // 2 + 4, self.width - 12, self.height - 8)

    def draw(self, surface):
        cx = int(self.x)
        cy = int(self.y)
        slick_surf = pygame.Surface((self.width + 8, self.height + 8), pygame.SRCALPHA)
        # Genangan oli hitam pekat mengkilat
        pygame.draw.ellipse(slick_surf, (20, 22, 28, 200), (4, 4, self.width, self.height))
        pygame.draw.ellipse(slick_surf, (40, 45, 55, 170), (8, 7, self.width - 12, self.height - 10))
        # Kilauan minyak ungu/kebiruan
        pygame.draw.arc(slick_surf, (100, 70, 140, 130), (12, 10, self.width - 24, self.height - 16), 0.2, 2.6, 3)
        surface.blit(slick_surf, (cx - self.width // 2 - 4, cy - self.height // 2 - 4))


class RoadBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 24

    def update(self, scroll_speed):
        self.y += scroll_speed

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 50

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, surface):
        cx = int(self.x)
        cy = int(self.y)
        hw = self.width // 2
        hh = self.height // 2

        # Kaki pembatas
        pygame.draw.rect(surface, (60, 60, 70), (cx - hw + 6, cy + hh - 4, 8, 8))
        pygame.draw.rect(surface, (60, 60, 70), (cx + hw - 14, cy + hh - 4, 8, 8))

        # Papan utama
        bar_rect = pygame.Rect(cx - hw, cy - hh, self.width, self.height)
        pygame.draw.rect(surface, (230, 230, 230), bar_rect, border_radius=4)

        # Garis loreng oranye bahaya (Hazard Stripes)
        stripe_w = 10
        for i in range(-2, self.width // stripe_w + 2):
            pts = [
                (cx - hw + i * stripe_w, cy - hh),
                (cx - hw + i * stripe_w + 6, cy - hh),
                (cx - hw + i * stripe_w - 4, cy + hh),
                (cx - hw + i * stripe_w - 10, cy + hh)
            ]
            # Clip polygon ke batas bar_rect
            poly_clipped = [(max(cx - hw, min(cx + hw, p[0])), p[1]) for p in pts]
            pygame.draw.polygon(surface, (235, 95, 20), poly_clipped)

        pygame.draw.rect(surface, (70, 70, 80), bar_rect, width=2, border_radius=4)
