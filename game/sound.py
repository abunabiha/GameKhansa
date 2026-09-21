"""
Sistem Efek Suara Prosedural untuk game Mobil Legend.
Dibuat secara mandiri menggunakan modul wave bawaan Python tanpa memerlukan file audio eksternal.
Mencakup suara raungan mesin dinamis, turbo nitro berkelanjutan, decitan ban (drift),
efek koin/tabrakan, dan musik balap arcade retro (BGM).
"""

import math
import struct
import io
import random
import pygame

class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sample_rate = 22050
        self.sounds = {}
        self.current_engine_tier = None
        self.bgm_enabled = True

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2, buffer=512)
            pygame.mixer.set_num_channels(16)
            
            # Kanal Suara Khusus
            self.engine_channel = pygame.mixer.Channel(0)
            self.screech_channel = pygame.mixer.Channel(1)
            self.nitro_channel = pygame.mixer.Channel(2)
            self.bgm_channel = pygame.mixer.Channel(3)

            self.enabled = True
            self._generate_all_sounds()
        except Exception as e:
            self.enabled = False
            print(f"[SoundManager] Audio tidak dapat diinisialisasi ({e}), suara dinonaktifkan.")

    def _create_wav_bytes(self, samples, nchannels=1):
        """Mengubah list sample float (-1.0 s/d 1.0) menjadi file WAV byte stream."""
        byte_io = io.BytesIO()
        import wave
        with wave.open(byte_io, 'wb') as wav_file:
            wav_file.setnchannels(nchannels)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            
            raw_frames = bytearray()
            for s in samples:
                val = max(-1.0, min(1.0, s))
                int_sample = int(val * 32767.0)
                raw_frames.extend(struct.pack('<h', int_sample))
            wav_file.writeframes(raw_frames)
            
        byte_io.seek(0)
        return byte_io

    def _make_engine_loop(self, base_freq, duration=1.0, grit=0.45):
        """Membuat loop suara mesin dengan frekuensi dan harmonik silinder stabil tanpa klik."""
        total_len = int(self.sample_rate * duration)
        samples = []
        for i in range(total_len):
            t = i / self.sample_rate
            # Fundamental + harmonik genap & ganjil khas knalpot mesin
            val = math.sin(2.0 * math.pi * base_freq * t)
            val += 0.55 * math.sin(4.0 * math.pi * base_freq * t)
            val += 0.35 * math.sin(6.0 * math.pi * base_freq * t)
            val += 0.20 * math.sin(8.0 * math.pi * base_freq * t)
            val += (random.random() * 2.0 - 1.0) * 0.08  # Sedikit desis gesekan knalpot
            
            # Saturasi agresif agar terdengar garang/menderu
            val = math.tanh(val * (1.0 + grit)) * 0.6
            samples.append(val)
        return pygame.mixer.Sound(self._create_wav_bytes(samples))

    def _generate_all_sounds(self):
        """Membuat seluruh suara mesin, SFX, dan musik prosedural."""
        # 1. Variasi Suara Mesin Mobil (Idle -> Low -> Mid -> High -> Nitro)
        self.sounds["engine_idle"] = self._make_engine_loop(52.0, duration=1.0, grit=0.35)
        self.sounds["engine_idle"].set_volume(0.35)

        self.sounds["engine_low"] = self._make_engine_loop(88.0, duration=1.0, grit=0.45)
        self.sounds["engine_low"].set_volume(0.50)

        self.sounds["engine_mid"] = self._make_engine_loop(145.0, duration=1.0, grit=0.55)
        self.sounds["engine_mid"].set_volume(0.60)

        self.sounds["engine_high"] = self._make_engine_loop(225.0, duration=1.0, grit=0.65)
        self.sounds["engine_high"].set_volume(0.70)

        self.sounds["engine_nitro"] = self._make_engine_loop(310.0, duration=1.0, grit=0.85)
        self.sounds["engine_nitro"].set_volume(0.85)

        # Suara Mesin Diesel Berat Khusus Tank Tempur
        self.sounds["engine_tank_idle"] = self._make_engine_loop(42.0, duration=1.0, grit=0.75)
        self.sounds["engine_tank_idle"].set_volume(0.55)

        self.sounds["engine_tank_drive"] = self._make_engine_loop(78.0, duration=1.0, grit=0.85)
        self.sounds["engine_tank_drive"].set_volume(0.75)

        # Suara Dentuman Meriam Tank (Cannon Shot)
        cannon_samples = []
        dur_cannon = 0.55
        len_cannon = int(self.sample_rate * dur_cannon)
        for i in range(len_cannon):
            t = i / self.sample_rate
            env = math.exp(-t * 12.0)
            f = 190.0 * math.exp(-t * 18.0) + 38.0
            sub_boom = math.sin(2.0 * math.pi * f * t)
            noise = (random.random() * 2.0 - 1.0) * math.exp(-t * 22.0)
            sample = (noise * 0.55 + sub_boom * 0.45) * env * 0.95
            cannon_samples.append(sample)
        self.sounds["cannon"] = pygame.mixer.Sound(self._create_wav_bytes(cannon_samples))
        self.sounds["cannon"].set_volume(0.95)

        # Suara Ledakan Kendaraan Hancur (Explosion)
        expl_samples = []
        dur_expl = 0.70
        len_expl = int(self.sample_rate * dur_expl)
        for i in range(len_expl):
            t = i / self.sample_rate
            decay = (1.0 - (i / len_expl)) ** 1.8
            rumble = math.sin(2.0 * math.pi * (85.0 - 55.0 * (i / len_expl)) * t)
            crack = (random.random() * 2.0 - 1.0)
            sample = (crack * 0.7 + rumble * 0.3) * decay * 0.9
            expl_samples.append(sample)
        self.sounds["explosion"] = pygame.mixer.Sound(self._create_wav_bytes(expl_samples))
        self.sounds["explosion"].set_volume(0.90)

        # 2. Suara Decitan Ban (Tire Screech saat drift/belok tajam)
        screech_samples = []
        dur_screech = 0.35
        len_screech = int(self.sample_rate * dur_screech)
        for i in range(len_screech):
            t = i / self.sample_rate
            env = math.sin(math.pi * (i / len_screech))
            # Gesekan frekuensi tinggi modulasi
            f = 950 + 250 * math.sin(2.0 * math.pi * 35.0 * t)
            tone = math.sin(2.0 * math.pi * f * t)
            noise = (random.random() * 2.0 - 1.0)
            sample = (tone * 0.4 + noise * 0.6) * env * 0.45
            screech_samples.append(sample)
        self.sounds["screech"] = pygame.mixer.Sound(self._create_wav_bytes(screech_samples))
        self.sounds["screech"].set_volume(0.65)

        # 3. Suara Nitro Berkelanjutan (Roaring Rocket Jet)
        nitro_samples = []
        dur_nitro = 0.8
        len_nitro = int(self.sample_rate * dur_nitro)
        for i in range(len_nitro):
            t = i / self.sample_rate
            noise = (random.random() * 2.0 - 1.0)
            jet_whistle = math.sin(2.0 * math.pi * (450 + 80 * math.sin(15 * t)) * t)
            sample = (noise * 0.7 + jet_whistle * 0.3) * 0.55
            nitro_samples.append(sample)
        self.sounds["nitro_loop"] = pygame.mixer.Sound(self._create_wav_bytes(nitro_samples))
        self.sounds["nitro_loop"].set_volume(0.75)

        # 4. Koin (Two-tone high arpeggio)
        coin_samples = []
        dur_coin = 0.16
        len_coin = int(self.sample_rate * dur_coin)
        for i in range(len_coin):
            t = i / self.sample_rate
            freq = 987.77 if i < len_coin // 2 else 1318.51
            decay = 1.0 - (i / len_coin)
            sample = math.sin(2.0 * math.pi * freq * t) * decay * 0.45
            coin_samples.append(sample)
        self.sounds["coin"] = pygame.mixer.Sound(self._create_wav_bytes(coin_samples))
        self.sounds["coin"].set_volume(0.65)

        # 5. Tabrakan / Crash (Low rumble + noisy crunch)
        crash_samples = []
        dur_crash = 0.45
        len_crash = int(self.sample_rate * dur_crash)
        for i in range(len_crash):
            t = i / self.sample_rate
            decay = (1.0 - (i / len_crash)) ** 2
            noise = (random.random() * 2.0 - 1.0)
            low_rumble = math.sin(2.0 * math.pi * (110 - 70 * (i / len_crash)) * t)
            sample = (noise * 0.65 + low_rumble * 0.35) * decay * 0.75
            crash_samples.append(sample)
        self.sounds["crash"] = pygame.mixer.Sound(self._create_wav_bytes(crash_samples))
        self.sounds["crash"].set_volume(0.85)

        # 6. Reparasi / Repair Kit
        repair_samples = []
        dur_rep = 0.25
        len_rep = int(self.sample_rate * dur_rep)
        for i in range(len_rep):
            t = i / self.sample_rate
            phase = i / len_rep
            freq = 523.25 + 350 * phase
            decay = 1.0 - phase
            sample = math.sin(2.0 * math.pi * freq * t) * decay * 0.5
            repair_samples.append(sample)
        self.sounds["repair"] = pygame.mixer.Sound(self._create_wav_bytes(repair_samples))
        self.sounds["repair"].set_volume(0.65)

        # 7. Game Over
        go_samples = []
        dur_go = 0.9
        len_go = int(self.sample_rate * dur_go)
        notes = [440, 392, 349, 293]
        for i in range(len_go):
            t = i / self.sample_rate
            note_idx = min(len(notes) - 1, int((i / len_go) * len(notes)))
            freq = notes[note_idx]
            decay = 1.0 - ((i % (len_go // len(notes))) / (len_go // len(notes)))
            sample = math.sin(2.0 * math.pi * freq * t) * decay * 0.5
            go_samples.append(sample)
        self.sounds["gameover"] = pygame.mixer.Sound(self._create_wav_bytes(go_samples))
        self.sounds["gameover"].set_volume(0.75)

        # 8. Edukasi Matematika: Jawaban Benar (Sparkle Chime C-E-G-C)
        correct_samples = []
        dur_corr = 0.36
        len_corr = int(self.sample_rate * dur_corr)
        chime_notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
        note_chunk = len_corr // len(chime_notes)
        for i in range(len_corr):
            t = i / self.sample_rate
            n_idx = min(len(chime_notes) - 1, i // note_chunk)
            freq = chime_notes[n_idx]
            local_i = i % note_chunk
            decay = 1.0 - (local_i / note_chunk) * 0.7
            sample = (math.sin(2.0 * math.pi * freq * t) * 0.7 + math.sin(4.0 * math.pi * freq * t) * 0.3) * decay * 0.55
            correct_samples.append(sample)
        self.sounds["math_correct"] = pygame.mixer.Sound(self._create_wav_bytes(correct_samples))
        self.sounds["math_correct"].set_volume(0.85)

        # 9. Edukasi Matematika: Jawaban Kurang Tepat (Gentle Friendly Bump)
        wrong_samples = []
        dur_wrong = 0.28
        len_wrong = int(self.sample_rate * dur_wrong)
        wrong_notes = [220.0, 174.61]
        w_chunk = len_wrong // 2
        for i in range(len_wrong):
            t = i / self.sample_rate
            n_idx = min(1, i // w_chunk)
            freq = wrong_notes[n_idx]
            decay = 1.0 - (i / len_wrong)
            sample = math.sin(2.0 * math.pi * freq * t) * decay * 0.45
            wrong_samples.append(sample)
        self.sounds["math_wrong"] = pygame.mixer.Sound(self._create_wav_bytes(wrong_samples))
        self.sounds["math_wrong"].set_volume(0.65)

        # 9b. Tolakan Perisai Gerbang Salah (Barrier Forcefield Zap / Deflection)
        block_samples = []
        dur_block = 0.24
        len_block = int(self.sample_rate * dur_block)
        for i in range(len_block):
            t = i / self.sample_rate
            decay = (1.0 - (i / len_block)) ** 1.5
            zap_noise = (random.random() * 2.0 - 1.0) * 0.4
            zap_freq = 320.0 - 220.0 * (i / len_block)
            sample = (math.sin(2.0 * math.pi * zap_freq * t) * 0.5 + zap_noise) * decay * 0.75
            block_samples.append(sample)
        self.sounds["barrier_block"] = pygame.mixer.Sound(self._create_wav_bytes(block_samples))
        self.sounds["barrier_block"].set_volume(0.85)

        # 9c. Fanfare Kemenangan Hadiah Super (Grand Victory Celebration Fanfare)
        fanfare_samples = []
        dur_fanfare = 0.55
        len_fanfare = int(self.sample_rate * dur_fanfare)
        fanfare_notes = [523.25, 659.25, 783.99, 1046.50, 1318.51]  # C5, E5, G5, C6, E6
        f_chunk = len_fanfare // len(fanfare_notes)
        for i in range(len_fanfare):
            t = i / self.sample_rate
            n_idx = min(len(fanfare_notes) - 1, i // f_chunk)
            freq = fanfare_notes[n_idx]
            sub_i = i % f_chunk
            decay = 1.0 - (sub_i / f_chunk) * 0.5
            s = (math.sin(2.0 * math.pi * freq * t) * 0.6 +
                 math.sin(4.0 * math.pi * freq * t) * 0.25 +
                 math.sin(6.0 * math.pi * freq * t) * 0.15) * decay * 0.6
            fanfare_samples.append(s)
        self.sounds["victory_fanfare"] = pygame.mixer.Sound(self._create_wav_bytes(fanfare_samples))
        self.sounds["victory_fanfare"].set_volume(0.9)

        # 9d. Rentetan Hujan Koin (Coin Cascade Shower)
        cascade_samples = []
        dur_cascade = 0.48
        len_cascade = int(self.sample_rate * dur_cascade)
        cascade_notes = [987.77, 1318.51, 1567.98, 1760.00, 2093.00, 2637.02]
        c_chunk = len_cascade // len(cascade_notes)
        for i in range(len_cascade):
            t = i / self.sample_rate
            n_idx = min(len(cascade_notes) - 1, i // c_chunk)
            freq = cascade_notes[n_idx]
            local_i = i % c_chunk
            decay = (1.0 - (local_i / c_chunk)) ** 2
            s = math.sin(2.0 * math.pi * freq * t) * decay * 0.45
            cascade_samples.append(s)
        self.sounds["coin_cascade"] = pygame.mixer.Sound(self._create_wav_bytes(cascade_samples))
        self.sounds["coin_cascade"].set_volume(0.85)

        # 10. Musik Balap Retro Arcade (Energetic Synthwave Racing Beat)
        bpm = 132
        beat_dur = 60.0 / bpm
        total_beats = 16  # 4 bar per loop
        total_dur = total_beats * beat_dur
        total_bgm_samples = int(self.sample_rate * total_dur)
        bgm_raw = [0.0] * total_bgm_samples

        for b in range(total_beats):
            start_s = int(b * beat_dur * self.sample_rate)
            # Bass Drum (Kick)
            kick_len = int(0.18 * self.sample_rate)
            for i in range(min(kick_len, total_bgm_samples - start_s)):
                t = i / self.sample_rate
                f = 130 * math.exp(-t * 26)
                env = max(0.0, 1.0 - t / 0.18)
                bgm_raw[start_s + i] += math.sin(2 * math.pi * f * t) * env * 0.5

            # Snare Drum pada beat ke-2 dan ke-4
            if b % 2 == 1:
                snare_len = int(0.15 * self.sample_rate)
                for i in range(min(snare_len, total_bgm_samples - start_s)):
                    t = i / self.sample_rate
                    env = max(0.0, 1.0 - t / 0.15)
                    noise = (random.random() * 2.0 - 1.0)
                    tone = math.sin(2 * math.pi * 200 * t)
                    bgm_raw[start_s + i] += (noise * 0.4 + tone * 0.15) * env * 0.35

        # Bassline Synth 16th notes
        bass_notes = [110.0, 110.0, 130.81, 146.83, 110.0, 110.0, 164.81, 146.83]
        sixteenth_dur = beat_dur / 4.0
        for step in range(total_beats * 4):
            start_s = int(step * sixteenth_dur * self.sample_rate)
            note_freq = bass_notes[step % len(bass_notes)]
            note_len = int(sixteenth_dur * 0.85 * self.sample_rate)
            for i in range(min(note_len, total_bgm_samples - start_s)):
                t = i / self.sample_rate
                env = max(0.0, 1.0 - (i / note_len))
                val = math.sin(2 * math.pi * note_freq * t) + 0.5 * math.sin(4 * math.pi * note_freq * t)
                bgm_raw[start_s + i] += val * env * 0.20

        # Normalisasi BGM
        max_v = max(abs(s) for s in bgm_raw) or 1.0
        bgm_norm = [s / max_v * 0.65 for s in bgm_raw]
        self.sounds["bgm"] = pygame.mixer.Sound(self._create_wav_bytes(bgm_norm))
        self.sounds["bgm"].set_volume(0.35)

    def update_engine(self, speed, max_speed, is_nitro, is_accelerating, is_braking, vehicle_type="car"):
        """Memperbarui suara raungan mesin mobil atau tank secara real-time sesuai kecepatan dan input."""
        if not self.enabled:
            return

        ratio = min(1.0, max(0.0, abs(speed) / max_speed))

        if vehicle_type == "tank":
            # Suara Mesin Diesel Berat untuk Tank
            if ratio > 0.15:
                target_tier = "engine_tank_drive"
                base_vol = 0.75 if is_accelerating else 0.55
            else:
                target_tier = "engine_tank_idle"
                base_vol = 0.50
        else:
            # Tentukan tier suara mesin Mobil Balap
            if is_nitro and speed > 2.0:
                target_tier = "engine_nitro"
                base_vol = 0.85
            elif ratio > 0.70:
                target_tier = "engine_high"
                base_vol = 0.75 if is_accelerating else 0.55
            elif ratio > 0.35:
                target_tier = "engine_mid"
                base_vol = 0.65 if is_accelerating else 0.45
            elif ratio > 0.08:
                target_tier = "engine_low"
                base_vol = 0.55 if is_accelerating else 0.35
            else:
                target_tier = "engine_idle"
                base_vol = 0.40

        if is_braking:
            base_vol *= 0.7

        # Ganti sampel suara mesin jika tier berubah atau channel berhenti
        if target_tier != self.current_engine_tier or not self.engine_channel.get_busy():
            self.current_engine_tier = target_tier
            snd = self.sounds.get(target_tier)
            if snd:
                self.engine_channel.play(snd, loops=-1)

        self.engine_channel.set_volume(base_vol)

    def play_screech(self):
        """Suara decitan ban mobil saat menikung tajam."""
        if not self.enabled:
            return
        if not self.screech_channel.get_busy():
            snd = self.sounds.get("screech")
            if snd:
                self.screech_channel.play(snd)

    def update_nitro(self, is_active):
        """Suara turbo roket menyala saat tombol nitro ditekan."""
        if not self.enabled:
            return
        if is_active:
            if not self.nitro_channel.get_busy():
                snd = self.sounds.get("nitro_loop")
                if snd:
                    self.nitro_channel.play(snd, loops=-1)
        else:
            if self.nitro_channel.get_busy():
                self.nitro_channel.stop()

    def start_bgm(self):
        """Memulai musik arcade balapan pengiring."""
        if not self.enabled or not self.bgm_enabled:
            return
        if not self.bgm_channel.get_busy():
            snd = self.sounds.get("bgm")
            if snd:
                self.bgm_channel.play(snd, loops=-1)

    def stop_bgm(self):
        if self.enabled and self.bgm_channel.get_busy():
            self.bgm_channel.stop()

    def toggle_bgm(self):
        self.bgm_enabled = not self.bgm_enabled
        if self.bgm_enabled:
            self.start_bgm()
        else:
            self.stop_bgm()
        return self.bgm_enabled

    def stop_all_continuous(self):
        """Menghentikan semua loop suara kontinu (saat pause atau game over)."""
        if not self.enabled:
            return
        self.engine_channel.stop()
        self.screech_channel.stop()
        self.nitro_channel.stop()
        self.current_engine_tier = None

    def play(self, sound_name):
        """Memutar efek suara sekali pakai (koin, crash, dll)."""
        if not self.enabled:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            try:
                # Cari channel bebas di atas channel 4 agar tidak mengganggu mesin/BGM
                free_chan = pygame.mixer.find_channel()
                if free_chan:
                    free_chan.play(snd)
                else:
                    snd.play()
            except Exception:
                pass
