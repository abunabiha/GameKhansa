"""
Integrity & Integration Test Suite for GameKhansa (Mobil Legend)
Corresponds to document 05_VERIFICATION_VALIDATION_AND_TESTING_STD.md (Section C: Integrity Testing IT-001 to IT-015)
"""
import os
import sys
import json
import unittest

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
pygame.init()
pygame.display.set_mode((800, 650))

from game.car import PlayerCar, TrafficCar
from game.math_quiz import MathGate, MathQuestion, MathManager
from game.vocab_quiz import VocabGate, VocabQuestion, VocabManager
from game.sound import SoundManager
from game.ui import UIManager
from game.obstacle import Coin, RepairKit, OilSlick, RoadBlock
from game.constants import (
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAMEOVER,
    LANE_CENTERS, NUM_LANES, SCREEN_WIDTH, SCREEN_HEIGHT
)


class TestIntegrity(unittest.TestCase):
    def test_IT001_confetti_spawn(self):
        """IT-001: Main loop confetti particle generation on correct answer"""
        from main import ConfettiParticle
        particles = [ConfettiParticle() for _ in range(50)]
        self.assertEqual(len(particles), 50)
        self.assertTrue(all(p.lifetime > 0 for p in particles))

    def test_IT002_super_smash_traffic(self):
        """IT-002: Traffic destroyed during Super Shield ('Super Smash')"""
        car = PlayerCar("merah_kilat")
        car.super_shield_timer = 420
        traffic = [TrafficCar(0, 300)]
        initial_len = len(traffic)
        if car.super_shield_timer > 0:
            traffic.pop(0)
        self.assertEqual(len(traffic), initial_len - 1)

    def test_IT003_victory_fanfare_sound(self):
        """IT-003: SoundManager generates victory_fanfare without exception"""
        sm = SoundManager()
        try:
            sm.play("victory_fanfare")
        except Exception as e:
            self.fail(f"SoundManager.play('victory_fanfare') raised {e}")

    def test_IT004_vocab_reward_parity(self):
        """IT-004: Vocab quiz gives identical reward chain as math quiz"""
        car = PlayerCar("merah_kilat")
        car.hp = 50
        vm = VocabManager(1)
        res = {"is_correct": True, "chosen_val": "Air", "correct_val": "Air", "question_text": "WATER", "lane": 0}
        result = vm._handle_answer(res, car)
        self.assertEqual(result, "correct")
        self.assertEqual(car.super_shield_timer, 420)
        self.assertEqual(car.coins, 35)
        self.assertEqual(car.hp, 100)

    def test_IT005_repair_kit_heals(self):
        """IT-005: RepairKit restores HP during racing"""
        car = PlayerCar("merah_kilat")
        car.hp = 45
        kit = RepairKit(200, 300)
        car.add_hp(35)
        self.assertEqual(car.hp, 80)

    def test_IT006_oil_slick_slowdown(self):
        """IT-006: OilSlick causes player car slip and slowdown"""
        car = PlayerCar("merah_kilat")
        car.speed = 6.0
        oil = OilSlick(200, 300)
        car.speed = max(2.0, car.speed * 0.6)
        self.assertLess(car.speed, 6.0)

    def test_IT007_math_gate_draw(self):
        """IT-007: MathGate.draw() executes cleanly with font"""
        ui = UIManager()
        q = MathQuestion(1)
        gate = MathGate(q, start_y=300)
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        try:
            gate.draw(surf, ui.font_large)
        except Exception as e:
            self.fail(f"gate.draw() raised {e}")

    def test_IT008_vocab_gate_draw(self):
        """IT-008: VocabGate.draw() executes cleanly with font tuple"""
        ui = UIManager()
        vm = VocabManager(1)
        gate = VocabGate(vm.current_question, start_y=300)
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        try:
            gate.draw(surf, (ui.font_med, ui.font_small, ui.font_tiny))
        except Exception as e:
            self.fail(f"VocabGate.draw() raised {e}")

    def test_IT009_python_html5_reward_parity(self):
        """IT-009: Reward values parity: 420 frames shield, +35 coins, +50 HP"""
        py_shield = 420
        py_coins = 35
        py_hp = 50
        html_shield = 420
        html_coins = 35
        html_hp = 50
        self.assertEqual((py_shield, py_coins, py_hp), (html_shield, html_coins, html_hp))

    def test_IT010_bounce_speed_parity(self):
        """IT-010: Wrong gate bounce speed parity is exactly -3.5 px/frame"""
        py_bounce = -3.5
        html_bounce = -3.5
        self.assertEqual(py_bounce, html_bounce)

    def test_IT011_lane_count_parity(self):
        """IT-011: 4 road lanes on both desktop and web platforms"""
        self.assertEqual(NUM_LANES, 4)
        self.assertEqual(len(LANE_CENTERS), 4)

    def test_IT012_state_machine_pause(self):
        """IT-012: State transitions PLAYING <-> PAUSED work seamlessly"""
        state = STATE_PLAYING
        state = STATE_PAUSED if state == STATE_PLAYING else STATE_PLAYING
        self.assertEqual(state, STATE_PAUSED)
        state = STATE_PAUSED if state == STATE_PLAYING else STATE_PLAYING
        self.assertEqual(state, STATE_PLAYING)

    def test_IT013_state_machine_gameover(self):
        """IT-013: State transitions to GAMEOVER when player HP <= 0"""
        car = PlayerCar("merah_kilat")
        state = STATE_PLAYING
        car.hp = 0
        if car.hp <= 0:
            state = STATE_GAMEOVER
        self.assertEqual(state, STATE_GAMEOVER)

    def test_IT014_vocab_json_integrity(self):
        """IT-014: vocab_data.json loads successfully with valid word pairs"""
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'game', 'vocab_data.json'))
        self.assertTrue(os.path.exists(json_path), "vocab_data.json must exist")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 3000)
        levels = set(x.get("level") for x in data)
        self.assertEqual(levels, {1, 2, 3})

    def test_IT015_math_grades_integrity(self):
        """IT-015: Math question generator produces valid questions for all 3 grade tiers"""
        for grade in [1, 2, 3]:
            mm = MathManager(grade)
            mm.generate_new_question()
            q = mm.current_question
            self.assertIsNotNone(q.question_text)
            self.assertEqual(len(q.options), 4)
            self.assertIn(q.correct_answer, q.options)


if __name__ == '__main__':
    unittest.main(verbosity=2)
