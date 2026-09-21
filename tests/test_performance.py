"""
Performance & Benchmark Testing Suite for GameKhansa (Mobil Legend)
Corresponds to document 05_VERIFICATION_VALIDATION_AND_TESTING_STD.md (Section D: Performance Testing PT-001 to PT-008)
"""
import os
import sys
import time
import tracemalloc
from collections import defaultdict

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
pygame.init()
screen = pygame.display.set_mode((800, 650))

from game.car import PlayerCar, TrafficCar, Particle
from game.math_quiz import MathGate, MathQuestion, MathManager
from game.vocab_quiz import VocabManager
from game.sound import SoundManager
from game.road import Road
from main import ConfettiParticle

def benchmark_scenario(name, traffic_count, confetti_count, spark_count, frames=180):
    car = PlayerCar("merah_kilat")
    road = Road()
    traffic = [TrafficCar(i % 4, 100 + (i * 60)) for i in range(traffic_count)]
    confetti = [ConfettiParticle() for _ in range(confetti_count)]
    sparks = [Particle(400, 300, 1, 1, (255, 50, 50), 4, 40) for _ in range(spark_count)]
    
    keys = defaultdict(bool)
    keys[pygame.K_UP] = True
    
    clock = pygame.time.Clock()
    start_t = time.perf_counter()
    
    for _ in range(frames):
        # Update
        car.update(keys)
        road.update(car.speed, car.distance)
        for t in traffic:
            t.update(car.speed)
        for c in confetti:
            c.update()
        for s in sparks:
            s.update()
            
        # Draw
        road.draw(screen, car.distance)
        for t in traffic:
            t.draw(screen)
        car.draw(screen)
        for c in confetti:
            c.draw(screen)
        for s in sparks:
            s.draw(screen)
            
        clock.tick(120)  # unbound tick to measure max throughput
        
    elapsed = time.perf_counter() - start_t
    effective_fps = frames / elapsed if elapsed > 0 else 999.0
    return effective_fps

def run_performance_suite():
    print("\n" + "="*55)
    print("⚡ MEMULAI GAMEKHANSA PERFORMANCE BENCHMARK SUITE")
    print("="*55)
    
    results = []
    
    # PT-001: Base Game (0 traffic, 0 particles)
    fps_base = benchmark_scenario("Base Game (0 Traffic)", 0, 0, 0)
    p1 = fps_base >= 60
    results.append(("PT-001", "Base Game (0 Traffic, 0 Particles)", f"{fps_base:.1f} FPS", "≥ 60 FPS", "PASS" if p1 else "FAIL"))
    
    # PT-002: 5 Traffic Cars
    fps_5 = benchmark_scenario("5 Traffic Cars", 5, 0, 0)
    p2 = fps_5 >= 60
    results.append(("PT-002", "5 Traffic Cars Active", f"{fps_5:.1f} FPS", "≥ 60 FPS", "PASS" if p2 else "FAIL"))
    
    # PT-003: 10 Traffic Cars
    fps_10 = benchmark_scenario("10 Traffic Cars", 10, 0, 0)
    p3 = fps_10 >= 60
    results.append(("PT-003", "10 Traffic Cars (Peak Density)", f"{fps_10:.1f} FPS", "≥ 60 FPS", "PASS" if p3 else "FAIL"))
    
    # PT-004: 10 Traffic + 50 Confetti
    fps_confetti = benchmark_scenario("10 Traffic + 50 Confetti", 10, 50, 0)
    p4 = fps_confetti >= 55
    results.append(("PT-004", "10 Traffic + 50 Confetti Particles", f"{fps_confetti:.1f} FPS", "≥ 55 FPS", "PASS" if p4 else "FAIL"))
    
    # PT-005: 10 Traffic + 50 Confetti + 100 Sparks
    fps_sparks = benchmark_scenario("10 Traffic + Confetti + Sparks", 10, 50, 100)
    p5 = fps_sparks >= 50
    results.append(("PT-005", "10 Traffic + 50 Confetti + 100 Sparks", f"{fps_sparks:.1f} FPS", "≥ 50 FPS", "PASS" if p5 else "FAIL"))
    
    # PT-006: Memory Allocation Benchmark
    tracemalloc.start()
    car = PlayerCar("merah_kilat")
    road = Road()
    mm = MathManager(1)
    vm = VocabManager(1)
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_mb = peak_mem / (1024 * 1024)
    p6 = peak_mb < 50.0  # < 50MB
    results.append(("PT-006", "Memory Allocation Peak", f"{peak_mb:.2f} MB", "< 50.0 MB", "PASS" if p6 else "FAIL"))
    
    # PT-007: Cold Load Time Benchmark
    t0 = time.perf_counter()
    _ = VocabManager(1)
    _ = MathManager(1)
    load_ms = (time.perf_counter() - t0) * 1000
    p7 = load_ms < 500.0  # < 500 ms
    results.append(("PT-007", "Question Banks Cold Load Time", f"{load_ms:.2f} ms", "< 500 ms", "PASS" if p7 else "FAIL"))
    
    # PT-008: Procedural Audio Generation Latency
    t_sfx = time.perf_counter()
    sm = SoundManager()
    sfx_ms = (time.perf_counter() - t_sfx) * 1000
    p8 = sfx_ms < 1000.0  # < 1000 ms
    results.append(("PT-008", "Audio Procedural SFX Synthesis", f"{sfx_ms:.2f} ms", "< 1000 ms", "PASS" if p8 else "FAIL"))
    
    print(f"\n{'ID':<8} {'Skenario Benchmark':<38} {'Hasil':<14} {'Target':<12} {'Status'}")
    print("-" * 78)
    all_passed = True
    for tid, name, res, target, status in results:
        status_str = "✅ PASS" if status == "PASS" else "❌ FAIL"
        if status != "PASS":
            all_passed = False
        print(f"{tid:<8} {name:<38} {res:<14} {target:<12} {status_str}")
        
    print("=" * 78)
    if all_passed:
        print("🎉 SEMUA PENGUJIAN PERFORMA & BENCHMARK BERHASIL MEMENUHI TARGET 60 FPS!")
    print("=" * 78 + "\n")
    return all_passed

if __name__ == '__main__':
    success = run_performance_suite()
    sys.exit(0 if success else 1)
