# 04 — Algorithms and Mathematical Formulations
## GameKhansa (Mobil Legend) — Educational Racing Game

**Document Version:** 1.0 | **Date:** September 2026

> All formulas use KaTeX-compatible LaTeX notation.

---

## 1. Vehicle Physics Algorithm

### 1.1 Acceleration Model

Player vehicle speed is governed by a discrete-time Euler integration with separate acceleration/deceleration rates:

$$v_{t+1} = \begin{cases}
\min(v_t + a_{accel}, v_{max}) & \text{if throttle pressed} \\
\max(v_t - a_{decel}, 0) & \text{if no input, } v_t > 0 \\
\max(v_t + a_{reverse}, -v_{reverse\_max}) & \text{if reverse pressed, } v_t \leq 0
\end{cases}$$

Where:
- $v_t$ = speed at frame $t$ (px/frame)
- $a_{accel} = 0.18$ px/frame² (car) | $0.12$ (tank)
- $a_{decel} = 0.09$ px/frame²
- $v_{max}$ = base max speed (car: 7.5, tank: 5.0) × boost multiplier
- $a_{reverse} = 0.15$ px/frame²
- $v_{reverse\_max} = 5.0$ (car) | $4.0$ (tank)

### 1.2 Lateral (Lane-Change) Steering

$$x_{t+1} = x_t + \Delta x_{steer} \cdot \text{steer\_factor}$$

Where:
- $\Delta x_{steer} = \pm 4.2$ px/frame (car) | $\pm 3.5$ (tank) when directional key held
- $\text{steer\_factor} = \max(0.85, \min(1.0, |v_t| / 2.0))$

**Key design decision:** `steer_factor ≥ 0.85` ensures steering remains responsive even at zero speed (vehicle can reposition to correct gate lane without accelerating).

### 1.3 Road Boundary Clamping

$$x_{t+1} = \text{clamp}(x_{t+1},\ R_L + w/2,\ R_R - w/2)$$

Where $R_L = 160$ (ROAD_LEFT), $R_R = 640$ (ROAD_RIGHT), $w$ = vehicle width.

### 1.4 Nitro Boost

$$v_{max, nitro} = v_{max, base} \times 1.65$$

Nitro depletes at $\Delta n = -0.018$ per frame; fills at $+0.004$ per frame when inactive.

---

## 2. Gate Collision Detection Algorithm

### 2.1 Proximity Detection

A gate at position $G_y$ interacts with the player at position $(P_x, P_y)$ when:

$$|P_y - G_y| < \delta_{gate} = 22 \text{ px}$$

### 2.2 Lane Assignment

The closest lane $\ell^*$ to the player is:

$$\ell^* = \arg\min_{\ell \in \{0,1,2,3\}} |P_x - C_\ell|$$

Where $C_\ell \in \{200, 320, 440, 560\}$ are the lane centre x-coordinates.

### 2.3 Correct Lane Test

$$\text{correct} = (\text{options}[\ell^*] == \text{correct\_answer})$$

### 2.4 Full Collision Decision Tree

```
if |P_y - G_y| < 22:
    ℓ* = argmin|P_x - C_ℓ|
    if options[ℓ*] == correct_answer:
        → RESOLVE gate → Super Celebration Reward
    else if ℓ* not in blocked_lanes:
        blocked_lanes[ℓ*] = 35
        → BOUNCE player (Algorithm 3.1)
        → SFX barrier_block
```

---

## 3. Wrong-Gate Bounce Algorithm

### 3.1 Bounce-Back Mechanics

When an incorrect lane is entered:

$$v_{t+1} = -3.5 \text{ px/frame (reverse)}$$

$$P_y = \max(P_y,\ G_y + 42) \text{ (prevent penetration)}$$

The gate lane is marked blocked for $T_{block} = 35$ frames:

$$\text{blocked\_lanes}[\ell^*] \leftarrow T_{block}$$

Each frame: $\text{blocked\_lanes}[\ell^*] -= 1$; delete when $\leq 0$.

### 3.2 Visual Barrier Rendering (HTML5)

For blocked lane $\ell$, two diagonal lines form an ⛔ cross:

$$\text{Line 1: } (p_x + 8,\ p_y + 8) \to (p_x + pw - 8,\ p_y + ph - 8)$$
$$\text{Line 2: } (p_x + pw - 8,\ p_y + 8) \to (p_x + 8,\ p_y + ph - 8)$$

Where $pw = W_{lane} - 14$, $ph = 44$.

---

## 4. Super Shield — Rainbow Star Shield

### 4.1 Shield Timer

On correct gate:
$$\text{shield\_timer} = 420 \text{ frames} = 7.0 \text{ seconds at 60 FPS}$$

Decrement: $\text{shield\_timer} -= 1$ per frame.

Immunity condition: `take_damage()` returns `False` when $\text{shield\_timer} > 0$.

### 4.2 Rainbow Aura Color Cycling

The aura HSL hue cycles as:

$$H(t) = (t \times 3.0) \mod 360$$

where $t = \text{super\_shield\_anim}$ increments each frame.

Three concentric aura circles:

$$r_k = 28 + k \times 6,\quad k \in \{0, 1, 2\}$$

$$\alpha_k = 0.55 - k \times 0.15$$

### 4.3 Orbiting Gold Stars

Three gold star-shaped polygons orbit the vehicle:

$$x_{star,k}(t) = P_x + r_{orbit} \cdot \cos\!\left(\frac{t}{18} + \frac{2\pi k}{3}\right)$$

$$y_{star,k}(t) = P_y + r_{orbit} \cdot \sin\!\left(\frac{t}{18} + \frac{2\pi k}{3}\right)$$

Where $r_{orbit} = 38$ px, $k \in \{0, 1, 2\}$.

Each star is a 5-pointed polygon with outer radius $r_o = 8$ and inner radius $r_i = 4$:

$$P_{star}^{(j)} = \left(r_j \cdot \cos\!\left(\frac{2\pi j}{10} - \frac{\pi}{2}\right),\ r_j \cdot \sin\!\left(\frac{2\pi j}{10} - \frac{\pi}{2}\right)\right)$$

where $r_j = r_o$ for even $j$, $r_i$ for odd $j$.

---

## 5. Confetti Particle Physics

### 5.1 Particle Spawn (Correct Gate Event)

50 particles spawned uniformly across road width:

$$x_0 \sim \mathcal{U}(R_L,\ R_R)$$
$$y_0 \sim \mathcal{U}(-30,\ 0)$$

Velocity components:
$$v_x \sim \mathcal{U}(-2.5,\ 2.5) \text{ px/frame}$$
$$v_y \sim \mathcal{U}(2.5,\ 5.5) \text{ px/frame (downward)}$$

### 5.2 Particle Update Per Frame

$$x_{t+1} = x_t + v_x$$
$$y_{t+1} = y_t + v_y$$
$$\theta_{t+1} = \theta_t + \omega,\quad \omega \sim \mathcal{U}(0.04, 0.12) \text{ rad/frame}$$
$$\text{life}_{t+1} = \text{life}_t - 1$$

Particle removed when $\text{life} \leq 0$.

Life range: $\text{life}_0 \sim \mathcal{U}(75, 130)$ frames.

### 5.3 Transparency Fade-Out (HTML5)

$$\alpha(t) = \min\!\left(1,\ \frac{\text{life}_t}{20}\right)$$

The particle becomes transparent over its final 20 frames.

---

## 6. Coin Magnet Algorithm

When `super_shield_timer > 0`, coins within magnet radius $r_m = 200$ px are attracted:

$$\vec{d} = (P_x - c_x,\ P_y - c_y)$$
$$|\vec{d}| = \sqrt{d_x^2 + d_y^2}$$

If $|\vec{d}| < r_m$:
$$c_x += d_x \times s_{magnet},\quad c_y += d_y \times s_{magnet}$$

Where $s_{magnet} = 0.12$ (attraction speed factor).

If $|\vec{d}| < 16$ px: coin collected, $\text{coins} += 1$.

---

## 7. Math Question Generation

### 7.1 Grade-Adaptive Operations

| Grade Level | Operations | Number Range | Example |
|------------|-----------|-------------|---------|
| Kelas 1–2 | +, − | 1–20 | 7 + 5 = ? |
| Kelas 3–4 | +, −, ×, ÷ | 1–100 | 24 ÷ 6 = ? |
| Kelas 5–6 | ×, ÷, fractions, % | 1–1000 | 15% of 80 = ? |

### 7.2 Distractor Generation

Distractors are generated by perturbing the correct answer:

$$d_i = c + \epsilon_i,\quad \epsilon_i \sim \mathcal{U}(\{-5,-3,-2,-1,1,2,3,5\}),\quad d_i \neq c$$

Distractors are shuffled with the correct answer to produce 4 options.

### 7.3 Answer Validation

For division questions, only integer-divisible pairs are generated:
$$a \times b = c,\quad a,b \in [2, 12],\quad b \mid a$$

---

## 8. Vocabulary Question Generation

### 8.1 Distractor Sampling

For a target word $w_{en}$ with correct translation $w_{id}$, distractors $D$ are sampled from the same level without replacement:

$$D = \text{sample}(\text{VOCAB\_LEVEL}[k] \setminus \{w_{id}\},\ n=3)$$

where $k \in \{1, 2, 3\}$ is the selected level.

### 8.2 Level Vocabulary Coverage

| Level | Count | CEFR Equivalent | Sample Words |
|-------|-------|----------------|-------------|
| Level 1 | 1,000 words | A1–A2 | water, school, happy, run |
| Level 2 | 1,000 words | B1–B2 | scientist, compass, journey |
| Level 3 | 1,000 words | C1–C2 | perseverance, philosophy, harmony |

---

## 9. Scoring Algorithm

$$\text{score}_{t+1} = \text{score}_t + \Delta s$$

Where $\Delta s$ is:

| Event | $\Delta s$ |
|-------|-----------|
| Distance traveled (per frame) | $+\lfloor v_t / 3 \rfloor$ |
| Correct gate answer | $+500$ |
| Super Smash (traffic during shield) | $+250$ |
| Coin collected | $+10$ |
| Destroying RoadBlock (shield) | $+100$ |

---

## 10. Procedural Audio Synthesis

### 10.1 Sine Wave Generation

$$y(t) = A \cdot \sin(2\pi f t)$$

Where $A$ = amplitude (0–1), $f$ = frequency (Hz), $t$ = sample index / sample_rate.

### 10.2 Victory Fanfare (C5 → E6)

Ascending fanfare: frequencies = [523, 587, 659, 784, 880, 988, 1047, 1175, 1319] Hz  
Duration per note: 60 ms  
Waveform: triangle wave $y(t) = A \cdot |\text{sawtooth}(t)|$

### 10.3 Coin Cascade (B5 → E7)

Rapid coin chime sequence: frequencies = [988, 1047, 1175, 1319, 1568, 1760, 1976, 2093, 2349, 2637] Hz  
Duration per note: 30 ms  
Waveform: sine wave with exponential decay envelope $e(t) = e^{-5t}$

### 10.4 Barrier Block (Zap Effect)

Sawtooth sweep from $f_{start} = 880$ Hz to $f_{end} = 110$ Hz over 200 ms:

$$f(t) = f_{start} - (f_{start} - f_{end}) \cdot \frac{t}{T}$$

---

## 11. Performance Optimisation

| Technique | Description | Impact |
|-----------|-------------|--------|
| Particle pooling | Confetti/sparks removed when `life ≤ 0` | Prevents unbounded list growth |
| Traffic culling | Traffic off-screen (y > SCREEN_H + 80) removed | O(n) bounded at ~12 vehicles |
| Gate proximity guard | Collision only checked when `|P_y - G_y| < 22` | Skips 95% of frames |
| Shadow caching | Shadow surfaces pre-rendered | Avoids per-frame shadow render |
| FPS cap | `clock.tick(60)` / `requestAnimationFrame` | Consistent 60 FPS target |
| Canvas state batching | `ctx.save/restore` grouped per draw pass | Reduces state change overhead |

---

*Document version: 1.0 | September 2026*
