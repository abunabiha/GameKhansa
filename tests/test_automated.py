"""
Automated Regression Test Suite for GameKhansa (Mobil Legend)
Corresponds to document 05_VERIFICATION_VALIDATION_AND_TESTING_STD.md (Section B: Automated Testing AT-001 to AT-010)
"""
import os
import sys
import time

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
pygame.init()
pygame.display.set_mode((800, 650))

from game.car import PlayerCar, Particle
from game.math_quiz import MathGate, MathQuestion, MathManager
from game.vocab_quiz import VocabGate, VocabQuestion, VocabManager
from game.constants import LANE_CENTERS, NUM_LANES

def run_automated_suite():
    passed = 0
    failed = 0
    results = []

    def check(test_id, name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  ✅ [{test_id}] {name}")
            passed += 1
            results.append((test_id, name, "PASS", detail))
        else:
            print(f"  ❌ [{test_id}] FAIL: {name} — {detail}")
            failed += 1
            results.append((test_id, name, "FAIL", detail))

    print("\n" + "="*50)
    print("🚀 MEMULAI GAMEKHANSA AUTOMATED TEST SUITE")
    print("="*50)
    start_time = time.time()

    # AT-001: Wrong gate barrier bounce
    car = PlayerCar("merah_kilat")
    car.y = 300
    q = MathQuestion(2)
    gate = MathGate(q, start_y=300)
    wrong_idx = (gate.question.options.index(gate.question.correct_answer) + 1) % 4
    gate.check_collision(LANE_CENTERS[wrong_idx], 300, car)
    check("AT-001", "Wrong gate barrier bounce reverses speed to -3.5", car.speed == -3.5, f"speed={car.speed}")

    # AT-002: Super shield on correct answer
    car2 = PlayerCar("merah_kilat")
    car2.y = 300
    q2 = MathQuestion(2)
    gate2 = MathGate(q2, start_y=300)
    manager = MathManager(2)
    manager.active_gate = gate2
    correct_idx = gate2.question.options.index(gate2.question.correct_answer)
    col_res = gate2.check_collision(LANE_CENTERS[correct_idx], 300, car2)
    manager._handle_answer(col_res, car2)
    check("AT-002", "Super shield timer set to 420 frames & +35 coins", car2.super_shield_timer == 420 and car2.coins == 35, f"timer={car2.super_shield_timer}, coins={car2.coins}")

    # AT-003: Shield invincibility
    car3 = PlayerCar("merah_kilat")
    car3.super_shield_timer = 420
    car3.hp = 100
    res_dmg = car3.take_damage(100)
    check("AT-003", "Super shield grants full damage immunity", res_dmg is False and car3.hp == 100, f"res={res_dmg}, hp={car3.hp}")

    # AT-004: blocked_lanes countdown
    q3 = MathQuestion(1)
    gate3 = MathGate(q3, start_y=300)
    gate3.blocked_lanes = {0: 3}
    gate3.update(0)
    gate3.update(0)
    gate3.update(0)
    check("AT-004", "blocked_lanes decrements and clears after timeout", 0 not in gate3.blocked_lanes, f"lanes={gate3.blocked_lanes}")

    # AT-005: HP capping
    car4 = PlayerCar("merah_kilat")
    car4.hp = 90
    car4.add_hp(50)
    check("AT-005", "Player HP capped at max_hp (100)", car4.hp == 100, f"hp={car4.hp}")

    # AT-006: Vocab distractor uniqueness
    vm = VocabManager(1)
    vq = vm.current_question
    check("AT-006", "Vocab question options are 4 unique choices with correct answer", len(vq.options) == 4 and len(set(vq.options)) == 4 and vq.correct_answer in vq.options)

    # AT-007: Particle lifecycle
    p = Particle(400, 300, 0, 1, (255, 0, 0), 5, 1)
    p.update()
    check("AT-007", "Particle lifecycle expires when lifetime reaches 0", p.lifetime == 0)

    # AT-008: Constants consistency
    check("AT-008", "Road lane geometry consistency (4 lanes with ordered coordinates)", NUM_LANES == 4 and len(LANE_CENTERS) == 4 and LANE_CENTERS[0] < LANE_CENTERS[3])

    # AT-009: Gate persists after multiple wrong attempts
    car5 = PlayerCar("merah_kilat")
    car5.y = 300
    q4 = MathQuestion(2)
    gate4 = MathGate(q4, start_y=300)
    c_idx = gate4.question.options.index(gate4.question.correct_answer)
    wrong_idxs = [i for i in range(4) if i != c_idx]
    for wi in wrong_idxs[:2]:
        gate4.blocked_lanes = {}
        gate4.check_collision(LANE_CENTERS[wi], 300, car5)
    check("AT-009", "Gate persists (resolved=False) after multiple wrong lane attempts", not gate4.resolved)

    # AT-010: Full reward chain on correct answer
    car6 = PlayerCar("merah_kilat")
    car6.hp = 50
    mm = MathManager(1)
    col = {"is_correct": True, "chosen_val": 10, "correct_val": 10, "question_text": "5+5", "lane": 0}
    res_str = mm._handle_answer(col, car6)
    check("AT-010", "Full reward chain: 'correct' status, shield 420, HP +50, coins +35", res_str == "correct" and car6.super_shield_timer == 420 and car6.hp == 100 and car6.coins == 35)

    elapsed = (time.time() - start_time) * 1000
    print("-" * 50)
    print(f"📊 SUMMARY: {passed} PASSED, {failed} FAILED (Durasi: {elapsed:.2f} ms)")
    print("=" * 50 + "\n")
    return failed == 0

if __name__ == '__main__':
    success = run_automated_suite()
    sys.exit(0 if success else 1)
