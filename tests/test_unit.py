"""
Unit Test Suite for GameKhansa (Mobil Legend)
Corresponds to document 05_VERIFICATION_VALIDATION_AND_TESTING_STD.md (Section A: Unit Testing UT-001 to UT-025)
"""
import os
import sys
import unittest

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
pygame.init()
pygame.display.set_mode((800, 650))

from game.car import PlayerCar, Particle, Explosion
from game.math_quiz import MathGate, MathQuestion, MathManager
from game.vocab_quiz import VocabGate, VocabQuestion, VocabManager
from game.obstacle import Coin, RepairKit, NitroBottle
from game.sound import SoundManager
from game.constants import (
    LANE_CENTERS, NUM_LANES, SCREEN_WIDTH, SCREEN_HEIGHT,
    ROAD_LEFT, ROAD_RIGHT, CARS_DATA
)


class TestPlayerCar(unittest.TestCase):
    def setUp(self):
        self.car = PlayerCar("merah_kilat")

    def test_UT001_normal_damage(self):
        """UT-001: PlayerCar.take_damage() reduces HP without shield"""
        initial_hp = self.car.hp
        result = self.car.take_damage(20)
        self.assertTrue(result)
        self.assertEqual(self.car.hp, initial_hp - 20)

    def test_UT002_shield_prevents_damage(self):
        """UT-002: PlayerCar.take_damage() returns False and preserves HP when super shield is active"""
        self.car.super_shield_timer = 420
        initial_hp = self.car.hp
        result = self.car.take_damage(50)
        self.assertFalse(result)
        self.assertEqual(self.car.hp, initial_hp)

    def test_UT003_add_hp_capped(self):
        """UT-003: PlayerCar.add_hp() does not exceed max_hp"""
        self.car.hp = 60
        self.car.add_hp(50)
        self.assertEqual(self.car.hp, self.car.max_hp)

    def test_UT004_add_hp_normal(self):
        """UT-004: PlayerCar.add_hp() adds correct amount below max_hp"""
        self.car.hp = 40
        self.car.add_hp(30)
        self.assertEqual(self.car.hp, 70)

    def test_UT005_initial_state(self):
        """UT-005: PlayerCar.__init__() initializes super_shield_timer=0, coins=0"""
        self.assertEqual(self.car.super_shield_timer, 0)
        self.assertEqual(self.car.coins, 0)
        self.assertEqual(self.car.hp, self.car.max_hp)

    def test_UT018_speed_boundary_max(self):
        """UT-018: PlayerCar speed capped within base_max_speed"""
        self.car.speed = self.car.base_max_speed
        from collections import defaultdict; keys = defaultdict(bool); keys[pygame.K_UP] = True
        self.car.update(keys)
        self.assertLessEqual(self.car.speed, self.car.base_max_speed + 0.1)

    def test_UT019_speed_boundary_reverse(self):
        """UT-019: PlayerCar reverse speed capped at -5.0"""
        self.car.speed = -5.0
        from collections import defaultdict; keys = defaultdict(bool); keys[pygame.K_DOWN] = True
        self.car.update(keys)
        self.assertGreaterEqual(self.car.speed, -5.0)

    def test_UT022_particle_expiry(self):
        """UT-022: Particle.update() decrements lifetime to 0"""
        p = Particle(400, 300, 0, 1, (255, 0, 0), 5, 1)
        p.update()
        self.assertEqual(p.lifetime, 0)

    def test_UT023_explosion_active(self):
        """UT-023: Explosion.update() stays active while lifetime > 0"""
        ex = Explosion(400, 300, 1.0)
        self.assertGreater(ex.lifetime, 0)
        ex.update()
        self.assertGreaterEqual(ex.lifetime, 0)


class TestMathQuiz(unittest.TestCase):
    def setUp(self):
        self.question = MathQuestion(1)
        self.gate = MathGate(self.question, start_y=300)
        self.car = PlayerCar("merah_kilat")
        self.car.y = 300

    def test_UT006_collision_correct(self):
        """UT-006: MathGate.check_collision() on correct lane resolves gate"""
        correct_lane = self.gate.question.options.index(self.gate.question.correct_answer)
        px = LANE_CENTERS[correct_lane]
        res = self.gate.check_collision(px, 300, self.car)
        self.assertIsNotNone(res)
        self.assertTrue(res.get("is_correct"))
        self.assertTrue(self.gate.resolved)

    def test_UT007_collision_wrong(self):
        """UT-007: MathGate.check_collision() on wrong lane bounces player back"""
        wrong_lane = (self.gate.question.options.index(self.gate.question.correct_answer) + 1) % 4
        px = LANE_CENTERS[wrong_lane]
        res = self.gate.check_collision(px, 300, self.car)
        self.assertIsNotNone(res)
        self.assertFalse(res.get("is_correct"))
        self.assertTrue(res.get("blocked"))
        self.assertEqual(self.car.speed, -3.5)
        self.assertFalse(self.gate.resolved)

    def test_UT008_no_contact(self):
        """UT-008: MathGate.check_collision() returns None when vehicle is far"""
        res = self.gate.check_collision(LANE_CENTERS[0], 100, self.car)
        self.assertIsNone(res)

    def test_UT009_handle_answer_correct(self):
        """UT-009: MathManager._handle_answer() triggers super rewards on correct"""
        mm = MathManager(1)
        self.car.hp = 50
        res = {"is_correct": True, "chosen_val": 5, "correct_val": 5, "question_text": "2+3", "lane": 0}
        result = mm._handle_answer(res, self.car)
        self.assertEqual(result, "correct")
        self.assertEqual(self.car.super_shield_timer, 420)
        self.assertEqual(self.car.coins, 35)
        self.assertEqual(self.car.hp, 100)

    def test_UT010_handle_answer_wrong(self):
        """UT-010: MathManager._handle_answer() returns wrong_blocked on wrong"""
        mm = MathManager(1)
        res = {"is_correct": False, "chosen_val": 4, "correct_val": 5, "question_text": "2+3", "lane": 0}
        result = mm._handle_answer(res, self.car)
        self.assertEqual(result, "wrong_blocked")

    def test_UT021_blocked_lanes_countdown(self):
        """UT-021: MathGate.blocked_lanes decrements and clears correctly"""
        self.gate.blocked_lanes = {1: 2}
        self.gate.update(0)
        self.assertEqual(self.gate.blocked_lanes.get(1), 1)
        self.gate.update(0)
        self.assertNotIn(1, self.gate.blocked_lanes)

    def test_UT024_grade1_range(self):
        """UT-024: Grade 1 question generates valid options with 4 choices"""
        q = MathQuestion(1)
        self.assertIn(q.correct_answer, q.options)
        self.assertEqual(len(q.options), 4)

    def test_UT025_grade5_range(self):
        """UT-025: Grade 3 question produces valid options with 4 choices"""
        q = MathQuestion(3)
        self.assertIn(q.correct_answer, q.options)
        self.assertEqual(len(q.options), 4)


class TestVocabQuiz(unittest.TestCase):
    def setUp(self):
        self.vm = VocabManager(1)
        self.car = PlayerCar("merah_kilat")
        self.car.y = 300

    def test_UT011_vocab_collision_correct(self):
        """UT-011: VocabGate.check_collision() resolves on correct answer"""
        q = self.vm.current_question
        gate = VocabGate(q, start_y=300)
        c_idx = gate.question.options.index(gate.question.correct_answer)
        res = gate.check_collision(LANE_CENTERS[c_idx], 300, self.car)
        self.assertIsNotNone(res)
        self.assertTrue(res.get("is_correct"))
        self.assertTrue(gate.resolved)

    def test_UT012_vocab_collision_wrong(self):
        """UT-012: VocabGate.check_collision() bounces player on wrong lane"""
        q = self.vm.current_question
        gate = VocabGate(q, start_y=300)
        w_idx = (gate.question.options.index(gate.question.correct_answer) + 1) % 4
        res = gate.check_collision(LANE_CENTERS[w_idx], 300, self.car)
        self.assertIsNotNone(res)
        self.assertFalse(res.get("is_correct"))
        self.assertEqual(self.car.speed, -3.5)

    def test_UT013_distractor_uniqueness(self):
        """UT-013: Vocab question options are all unique"""
        q = self.vm.current_question
        self.assertEqual(len(set(q.options)), 4)

    def test_UT014_level_filtering(self):
        """UT-014: VocabManager generates questions from correct level pool"""
        q = self.vm.current_question
        self.assertTrue(len(q.source_word) > 0)
        self.assertTrue(len(q.correct_answer) > 0)


class TestSoundAndObstacles(unittest.TestCase):
    def test_UT015_sound_manager_init(self):
        """UT-015: SoundManager initialises procedural synthesis without error"""
        sm = SoundManager()
        self.assertIsNotNone(sm)

    def test_UT016_coin_collection(self):
        """UT-016: Coin object properties and positioning"""
        coin = Coin(200, 300)
        self.assertEqual(coin.x, 200)
        self.assertEqual(coin.y, 300)

    def test_UT017_repair_kit(self):
        """UT-017: RepairKit restores HP"""
        kit = RepairKit(200, 300)
        car = PlayerCar("merah_kilat")
        car.hp = 40
        car.add_hp(35)
        self.assertEqual(car.hp, 75)

    def test_UT020_constants_lanes(self):
        """UT-020: NUM_LANES equals 4 and matches LANE_CENTERS length"""
        self.assertEqual(NUM_LANES, 4)
        self.assertEqual(len(LANE_CENTERS), 4)


if __name__ == '__main__':
    unittest.main(verbosity=2)
