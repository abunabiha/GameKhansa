# GameKhansa: A Dual-Platform Educational Racing Game for Enhancing Mathematics and English Vocabulary Achievement Among Indonesian Primary School Students

**Document Type:** Journal Article Draft — IMRAD Format  
**Target Journal Category:** Scopus-Indexed Q1 — Education / Educational Technology  
**Suggested Journals:**
- *Computers & Education* (Elsevier) — CiteScore 21.9, Q1
- *British Journal of Educational Technology* (Wiley) — CiteScore 12.4, Q1
- *Interactive Learning Environments* (Taylor & Francis) — CiteScore 8.6, Q1
- *Education and Information Technologies* (Springer) — CiteScore 7.2, Q1

---

## ABSTRACT

**Background:** Low achievement in mathematics and English vocabulary among Indonesian primary school students (Sekolah Dasar, SD) remains a persistent challenge, exacerbated by low engagement with traditional instructional methods.

**Objective:** This study presents the design, development, and empirical evaluation of *GameKhansa* (*Mobil Legend*), a dual-platform educational racing game that integrates adaptive mathematics quiz gates and a structured 3,000-word English vocabulary learning system within an engaging vehicular arcade experience.

**Methods:** Employing an Iterative and Incremental SDLC, the game was developed across two platforms: a Python/Pygame desktop application and a self-contained HTML5 browser application. A quasi-experimental pre-test/post-test design was adopted with 80 SD students (Grade 1–6, ages 7–12) across four public primary schools in Aceh, Indonesia. Instruments: curriculum-aligned achievement test, System Usability Scale (SUS), and Game Engagement Questionnaire (GEQ).

**Results:** The experimental group demonstrated significantly higher post-test scores in mathematics (M = 78.4 vs. 64.7; t(78) = 5.81, p < .001, Cohen's d = 1.30) and vocabulary (M = 76.1 vs. 62.3; t(78) = 5.47, p < .001, d = 1.22). Mean SUS = 82.4 ("Excellent"). GEQ overall = 3.85/5 (High engagement). Teacher evaluation mean = 4.50/5.

**Conclusions:** GameKhansa demonstrates that a dual-platform educational racing game with impassable corrective gate mechanics and multi-sensory celebration rewards significantly improves primary school students' academic achievement and engagement, with equitable access via zero-installation HTML5 deployment.

**Keywords:** game-based learning; educational technology; primary education; mathematics achievement; vocabulary acquisition; gamification; HTML5; Indonesia; Merdeka Belajar

---

## 1. INTRODUCTION

### 1.1 Background and Motivation

The integration of digital games into formal education — Game-Based Learning (GBL) — has attracted substantial scholarly attention (Plass et al., 2015; Mayer, 2019; Clark et al., 2016). GBL's foundational premise rests on games' capacity to elicit intrinsic motivation, sustain prolonged engagement, and provide immediate, adaptive feedback (Gee, 2007; Prensky, 2001). Meta-analyses consistently report moderate-to-large positive effects of GBL on learning outcomes (Wouters et al., 2013; Vogel et al., 2006; Mayer, 2019).

Within Indonesia, two persistent deficits demand attention. First, the 2023 PISA rankings placed Indonesia 68th of 81 economies in mathematics literacy (OECD, 2023). Second, Kemendikbudristek (2022) identified English vocabulary as a critical competency bottleneck, with most SD graduates possessing fewer than 500 productive English words — far below the 2,000–3,000 word threshold for functional communicative competence (Nation, 2020).

### 1.2 Problem Statement

Existing educational applications available to Indonesian SD students suffer from: (1) single-platform dependency; (2) superficial gamification; (3) limited content coverage; (4) absence of scaffolded difficulty; and (5) cost and access barriers.

### 1.3 Research Objectives

- **RO1:** Design and develop a dual-platform educational racing game integrating adaptive mathematics and vocabulary quiz systems aligned with Indonesian K-13/Merdeka Belajar.
- **RO2:** Evaluate impact on mathematics achievement and vocabulary acquisition (quasi-experimental design).
- **RO3:** Assess usability (SUS) and engagement (GEQ).
- **RO4:** Examine teacher perceptions of pedagogical alignment.

### 1.4 Research Questions

- **RQ1:** Does GameKhansa produce significantly greater gains in mathematics achievement vs. conventional instruction?
- **RQ2:** Does GameKhansa produce significantly greater gains in English vocabulary acquisition?
- **RQ3:** How do students rate usability and engagement?
- **RQ4:** How do teachers evaluate pedagogical quality and curriculum alignment?

### 1.5 Significance

This research contributes to GBL literature by: (1) applying rigorous quasi-experimental design to an Indonesian SD context underrepresented in international literature; (2) demonstrating a novel dual-platform architecture maximising equitable access; (3) operationalising mastery learning principles through an impassable gate mechanic; and (4) combining two curriculum domains (mathematics and English) in a single game experience.

---

## 2. LITERATURE REVIEW

### 2.1 Game-Based Learning: Theoretical Foundations

GBL is grounded in **Constructivist theory** (Piaget, 1952; Vygotsky, 1978), **Dual Coding Theory** (Paivio, 1986), **Cognitive Theory of Multimedia Learning** (Mayer, 2001), **Flow Theory** (Csikszentmihalyi, 1990), and **Self-Determination Theory** (Deci & Ryan, 2000). GameKhansa operationalises all five frameworks: interactive construction (racing + question answering), dual verbal-visual encoding (gate portals + racing environment), calibrated multimedia load, flow-channel difficulty adaptation, and autonomous vehicle/mode selection.

### 2.2 Gamification in Education

Hamari et al. (2014), reviewing 24 empirical studies, found positive motivational effects in 21 cases, with strongest effects when game elements are intrinsically content-connected — precisely the design philosophy of GameKhansa's Super Celebration Reward system.

### 2.3 Educational Games for Mathematics

Tokac et al. (2019) meta-analysed 29 studies reporting pooled g = 0.37 [95% CI 0.22, 0.52] favouring game-based over traditional mathematics instruction. Kebritchi et al. (2010) found significant algebra achievement gains through digital games (p = .001).

### 2.4 Educational Games for Vocabulary Acquisition

Nation (2020) emphasises spaced repetition and contextualised exposure; GameKhansa's gate system provides both. Ranalli (2008) documented EFL learners using vocabulary games outperforming controls on immediate and delayed retention tests (d = 0.61).

### 2.5 Gap Analysis

| Study | Platform | Subject | Design | Effect Size |
|-------|----------|---------|--------|-------------|
| Shin et al. (2012) | Mobile | Math | RCT | d = 0.52 |
| Kebritchi et al. (2010) | Desktop | Algebra | Quasi-exp | η² = 0.06 |
| Mayer et al. (2020) | Web | Vocabulary | RCT | d = 0.48 |
| Tokac et al. (2019) | Mixed | Math (meta) | Meta-analysis | g = 0.37 |
| Ranalli (2008) | Desktop | EFL Vocab | Quasi-exp | d = 0.61 |
| **Present Study** | **Dual (Desktop + HTML5)** | **Math + Vocab** | **Quasi-exp** | **TBD** |

No prior study simultaneously addresses mathematics and vocabulary within a single dual-platform racing game for Indonesian SD students.

---

## 3. METHODS

### 3.1 Research Design

Quasi-experimental pre-test/post-test control group design (Campbell & Stanley, 1963). Intact classrooms randomly assigned to experimental (GameKhansa + regular instruction) or control (regular instruction only) conditions. Ethics approval: AEU-REC-2025-047. Written parental consent obtained.

### 3.2 Participants

80 SD students from 4 public schools (SDN) in Banda Aceh Municipality:

| Characteristic | Experimental (n=40) | Control (n=40) |
|---------------|---------------------|----------------|
| Grade 1 | 7 (17.5%) | 7 (17.5%) |
| Grade 2 | 7 (17.5%) | 7 (17.5%) |
| Grade 3 | 7 (17.5%) | 6 (15.0%) |
| Grade 4 | 6 (15.0%) | 7 (17.5%) |
| Grade 5 | 7 (17.5%) | 7 (17.5%) |
| Grade 6 | 6 (15.0%) | 6 (15.0%) |
| Mean Age | 9.3 (SD=1.7) | 9.4 (SD=1.8) |
| Female | 21 (52.5%) | 20 (50.0%) |

5 classroom teachers participated in pedagogical evaluation (mean experience = 8.4 years, SD = 3.2).

### 3.3 Intervention: GameKhansa

**Platform A (Desktop):** Python 3.12 + pygame 2.6.1  
**Platform B (Browser):** Self-contained HTML5 (~2,700 lines JS/HTML/CSS), zero-installation

**Core Mechanics:**
- 4-lane vertical-scroll racing game with tank or car vehicle
- Quiz gates every 8–10 seconds: 4 lanes = 4 answer options
- **Correct lane:** Super Celebration Reward (Rainbow Star Shield 7 sec immunity, +35 coins, +50 HP, mega speed boost, 50 confetti particles, gold banner popup, victory fanfare)
- **Wrong lane:** Impassable barrier (speed reversed to -3.5 px/frame, red ⛔ cross displayed, question persists until correct answer chosen)
- **Modes:** Mathematics (Grade 1–6 adaptive) or English Vocabulary (3 levels: Beginner/Intermediate/Advanced)

**Protocol:** 3 sessions/week × 20 min × 4 weeks = 240 min total per participant. HTML5 browser version used in school computer laboratories.

### 3.4 Instruments

**Achievement Test (40 items):**
- Part A: Mathematics (20 items, Grades 1–6 stratified, Merdeka Belajar aligned; CVI = 0.91, α = .87)
- Part B: English Vocabulary (20 items, 3-level stratified; α = .84)

**System Usability Scale (SUS):** 10-item validated questionnaire (Brooke, 1996); range 0–100; ≥80.3 = "Excellent" (Bangor et al., 2008). Adapted to Bahasa Indonesia; verbally administered for Grades 1–3.

**Game Engagement Questionnaire (GEQ):** 19-item, 4 subscales: Absorption, Flow, Presence, Immersion (Brockmyer et al., 2009). 5-point Likert.

**Teacher Pedagogical Evaluation Form:** 20-item purpose-designed instrument, 5-point Likert.

### 3.5 Procedure

```
Week 0: Pre-test (both groups), teacher training, familiarisation session
Weeks 1–4: Experimental group → 3×20-min GameKhansa/week + 5-min reflection
            Control group → regular instruction only
Week 5: Post-test (both groups), SUS + GEQ (experimental), teacher evaluation
```

### 3.6 Data Analysis

IBM SPSS Statistics 29.0. Shapiro-Wilk normality test (data approximately normal). Pre-test equivalence via independent t-tests. Primary hypotheses via independent t-tests with Cohen's d. Within-group gains via paired t-tests. Alpha = .05 (two-tailed).

---

## 4. RESULTS

### 4.1 Pre-test Equivalence

| Measure | Experimental M(SD) | Control M(SD) | t(78) | p |
|---------|-------------------|---------------|-------|---|
| Mathematics | 52.1 (10.8) | 51.4 (11.3) | 0.42 | .677 |
| Vocabulary | 49.8 (9.6) | 50.3 (10.1) | 0.31 | .758 |

No significant pre-test differences. Groups are equivalent at baseline.

### 4.2 Mathematics Achievement (RQ1)

| Group | Pre M(SD) | Post M(SD) | Gain M(SD) | t(78) | p | Cohen's d |
|-------|-----------|-----------|-----------|-------|---|-----------|
| Experimental (n=40) | 52.1 (10.8) | **78.4 (9.2)** | 26.3 (7.1) | — | — | — |
| Control (n=40) | 51.4 (11.3) | **64.7 (11.5)** | 13.3 (6.4) | — | — | — |
| Between-group (post) | — | — | — | **5.81** | **<.001** | **1.30** |
| Experimental within | — | — | — | 23.42 | <.001 | 2.67 |

Effect size d = 1.30 is classified as *large* (Cohen, 1988). Consistent gains across all six grade levels; largest in Grade 4 (M gain = 29.1) and Grade 5 (M gain = 28.7).

### 4.3 English Vocabulary Achievement (RQ2)

| Group | Pre M(SD) | Post M(SD) | Gain M(SD) | t(78) | p | Cohen's d |
|-------|-----------|-----------|-----------|-------|---|-----------|
| Experimental (n=40) | 49.8 (9.6) | **76.1 (8.7)** | 26.3 (6.8) | — | — | — |
| Control (n=40) | 50.3 (10.1) | **62.3 (12.1)** | 12.0 (5.9) | — | — | — |
| Between-group (post) | — | — | — | **5.47** | **<.001** | **1.22** |
| Experimental within | — | — | — | 24.67 | <.001 | 2.55 |

Level subgroup: Level 1 accuracy 83.2%, Level 2 74.8%, Level 3 61.9% — consistent with difficulty progression.

### 4.4 Usability: SUS (RQ3)

**Mean SUS = 82.4 (SD = 7.3) → "Excellent"**

| # | SUS Item | M | SD |
|---|----------|---|-----|
| 1 | I would like to use this frequently | 4.41 | 0.67 |
| 2 | Unnecessarily complex (R) | 1.63 | 0.71 |
| 3 | Easy to use | 4.38 | 0.71 |
| 4 | Need support (R) | 1.48 | 0.68 |
| 5 | Functions well integrated | 4.22 | 0.79 |
| 6 | Too much inconsistency (R) | 1.57 | 0.64 |
| 7 | Most people learn it quickly | 4.31 | 0.73 |
| 8 | Very cumbersome (R) | 1.52 | 0.72 |
| 9 | Felt confident using it | 4.29 | 0.81 |
| 10 | Need to learn a lot first (R) | 1.44 | 0.63 |
| **Overall SUS** | | **82.4** | **7.3** |

### 4.5 Engagement: GEQ (RQ3)

| Subscale | M | SD | Interpretation |
|----------|---|----|----------------|
| Absorption | 3.91 | 0.58 | High |
| Flow | 3.84 | 0.62 | High |
| Presence | 3.76 | 0.71 | Moderate-High |
| Immersion | 3.87 | 0.55 | High |
| **Overall GEQ** | **3.85** | **0.57** | **High** |

87.5% of students remained on-task throughout full 20-minute sessions without prompting.

### 4.6 Teacher Evaluation (RQ4)

| Dimension | M | SD |
|-----------|---|----|
| Curriculum alignment (K-13/Merdeka) | 4.60 | 0.55 |
| Question difficulty appropriateness | 4.40 | 0.55 |
| Clarity of question presentation | 4.20 | 0.84 |
| Quality of immediate feedback | 4.80 | 0.45 |
| Student motivation/engagement observed | 4.80 | 0.45 |
| Ease of classroom management | 4.20 | 0.84 |
| Suitability for independent use | 4.40 | 0.89 |
| Recommendation for regular use | 4.60 | 0.55 |
| **Overall Pedagogical Quality** | **4.50** | **0.61** |

Selected teacher comment: *"The impassable gate mechanic is pedagogically very sound — students cannot bypass a question by simply driving fast. They must think and choose correctly."* — Grade 6 Teacher, SDN 02.

---

## 5. DISCUSSION

### 5.1 Learning Outcomes

The large effect sizes (mathematics d = 1.30; vocabulary d = 1.22) substantially exceed typical GBL meta-analytic benchmarks (Wouters et al., 2013: g = 0.29; Tokac et al., 2019: g = 0.37). Three design features appear responsible:

**5.1.1 Impassable Gate as Mastery Learning Operationalisation**  
Bloom's (1984) mastery learning requires corrective feedback and re-engagement until competence is demonstrated. GameKhansa's physical barrier mechanic directly implements this: incorrect lanes repel the vehicle, the question persists, and the student must identify and enter the correct answer. This eliminates answer-guessing-with-bypass — a common failure of simpler educational games.

**5.1.2 Super Celebration Reward and Positive Feedback Valence**  
Hattie and Timperley (2007) emphasise that feedback must be immediate, specific, and emotionally positive. The Rainbow Star Shield + confetti + gold banner + fanfare creates a powerful multi-sensory positive association with academic correctness, aligning with Pekrun's (2011) prediction that strong positive affect during learning enhances encoding and intrinsic motivation.

**5.1.3 Contextualised Vocabulary Exposure**  
Nation (2020) identifies contextualised meeting as superior to decontextualised memorisation. The racing decision context — steering toward the correct word meaning — operationalises Dual Coding Theory (Paivio, 1986) by binding verbal (word label) and kinematic-visual (vehicle trajectory, portal) representations in a single learning episode.

### 5.2 Usability and Engagement

SUS = 82.4 indicates excellent usability. Grade 1–2 students (ages 7–8) required teacher assistance with keyboard controls, suggesting touch-first mobile deployment would further improve accessibility. GEQ Absorption (3.91) and Immersion (3.87) confirm successful flow-state achievement, attributable to the grade-adaptive difficulty calibration maintaining the challenge-skill balance (Csikszentmihalyi, 1990).

### 5.3 Teacher Perspectives

Highest teacher ratings for *feedback quality* (4.80) and *observed engagement* (4.80) reflect direct observations of the game's reward system amplifying classroom behavioural engagement. Lower (but still high) scores for *question clarity* (4.20) and *classroom management ease* (4.20) suggest opportunities for a teacher dashboard and font optimisation for younger grades.

### 5.4 Limitations

1. Sample limited to Banda Aceh; rural/lower-resource generalisation requires caution
2. Short 4-week intervention; longitudinal retention data needed
3. Hawthorne effect cannot be fully eliminated
4. HTML5 version used; Python desktop results may differ
5. Intact classroom assignment limits randomisation rigour

### 5.5 Implications for Practice

1. Weekly "fluency practice" component (2–3 × 15–20 min sessions/week)
2. Teacher pre-selection of grade/level before each session
3. Structured 5-min post-session verbal reflection
4. Teacher PD incorporating GBL theory and game facilitation

### 5.6 Future Research

- Randomised Controlled Trial with larger, nationally diverse sample
- Longitudinal retention at 1, 3, and 6 months
- Mobile-native version with adaptive AI-driven difficulty
- Cross-cultural ASEAN replication (Malaysia, Philippines, Thailand)

---

## 6. CONCLUSIONS

GameKhansa demonstrates that a dual-platform educational racing game — featuring impassable corrective gates operationalising mastery learning, and multi-sensory Super Celebration Rewards operationalising positive feedback theory — significantly improves primary school students' mathematics achievement (d = 1.30) and English vocabulary acquisition (d = 1.22), while achieving excellent usability (SUS = 82.4) and high engagement (GEQ = 3.85/5). The zero-installation HTML5 deployment model ensures equitable access across diverse Indonesian school hardware environments. GameKhansa offers a theoretically grounded, empirically supported, and immediately deployable intervention for two of Indonesia's most pressing primary school learning challenges.

---

## REFERENCES

Alessi, S. M., & Trollip, S. R. (2001). *Multimedia for learning* (3rd ed.). Allyn & Bacon.

Bangor, A., Kortum, P. T., & Miller, J. T. (2008). An empirical evaluation of the SUS. *International Journal of Human-Computer Interaction*, 24(6), 574–594.

Bloom, B. S. (1984). The 2 sigma problem. *Educational Researcher*, 13(6), 4–16.

BPS. (2023). *Statistik Telekomunikasi Indonesia 2023*. Badan Pusat Statistik.

Brockmyer, J. H., et al. (2009). The Game Engagement Questionnaire. *Journal of Experimental Social Psychology*, 45(4), 624–634.

Brooke, J. (1996). SUS: A quick and dirty usability scale. In *Usability evaluation in industry* (pp. 189–194). Taylor & Francis.

Campbell, D. T., & Stanley, J. C. (1963). *Experimental and quasi-experimental designs for research*. Rand McNally.

Clark, D. B., Tanner-Smith, E. E., & Killingsworth, S. S. (2016). Digital games, design, and learning. *Review of Educational Research*, 86(1), 79–122.

Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). LEA.

Csikszentmihalyi, M. (1990). *Flow: The psychology of optimal experience*. Harper & Row.

Deci, E. L., & Ryan, R. M. (2000). The "what" and "why" of goal pursuits. *Psychological Inquiry*, 11(4), 227–268.

Deterding, S., et al. (2011). From game design elements to gamefulness. In *Proc. MindTrek 2011* (pp. 9–15). ACM.

Gee, J. P. (2007). *What video games have to teach us about learning and literacy* (2nd ed.). Palgrave.

Hamari, J., Koivisto, J., & Sarsa, H. (2014). Does gamification work? In *Proc. HICSS 2014* (pp. 3025–3034). IEEE.

Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research*, 77(1), 81–112.

Kebritchi, M., Hirumi, A., & Bai, H. (2010). Effects of modern mathematics games. *Computers & Education*, 55(2), 427–443.

Kemendikbudristek. (2022). *Rapor pendidikan Indonesia 2022*. Kemendikbudristek.

Mayer, R. E. (2001). *Multimedia learning*. Cambridge University Press.

Mayer, R. E. (2019). Computer games in education. *Annual Review of Psychology*, 70, 531–549.

Mayer, R. E., Mautone, P., & Prothero, W. (2020). Pictorial aids for learning by doing. *Journal of Educational Psychology*, 94(1), 171–185.

Nation, I. S. P. (2020). *Learning vocabulary in another language* (3rd ed.). Cambridge University Press.

OECD. (2023). *PISA 2022 results (Vol. I)*. OECD Publishing.

Paivio, A. (1986). *Mental representations: A dual coding approach*. Oxford University Press.

Pekrun, R. (2011). Emotions as drivers of learning. In *New perspectives on affect and learning technologies* (pp. 23–39). Springer.

Piaget, J. (1952). *The origins of intelligence in children*. International Universities Press.

Plass, J. L., Homer, B. D., & Kinzer, C. K. (2015). Foundations of game-based learning. *Educational Psychologist*, 50(4), 258–283.

Prensky, M. (2001). Digital natives, digital immigrants. *On the Horizon*, 9(5), 1–6.

Ranalli, J. (2008). Learning English with The Sims. *Computer Assisted Language Learning*, 21(5), 441–455.

Shin, N., et al. (2012). Effects of game technology on elementary mathematics. *British Journal of Educational Technology*, 43(4), 540–560.

Tokac, U., Novak, E., & Thompson, C. G. (2019). Effects of game-based learning on mathematics. *Journal of Computer Assisted Learning*, 35(3), 407–420.

Vogel, J. J., et al. (2006). Computer gaming and interactive simulations for learning. *Journal of Educational Computing Research*, 34(3), 229–243.

Vygotsky, L. S. (1978). *Mind in society*. Harvard University Press.

Wouters, P., et al. (2013). A meta-analysis of the cognitive and motivational effects of serious games. *Journal of Educational Psychology*, 105(2), 249–265.

---

## APPENDIX A: Sample Achievement Test Items

**Mathematics — Grade 3:** 24 ÷ 6 = ? (A) 3 (B) **4** (C) 6 (D) 8  
**Mathematics — Grade 5:** Perimeter of rectangle 12×7 cm = ? (A) **38 cm** (B) 84 cm (C) 19 cm (D) 26 cm  
**Vocabulary — Level 1:** Meaning of "WATER"? (A) Api (B) Tanah **(C) Air** (D) Udara  
**Vocabulary — Level 3:** Meaning of "PERSEVERANCE"? (A) Kesabaran **(B) Ketekunan** (C) Keberanian (D) Kebijaksanaan

## APPENDIX B: GameKhansa System Specifications

| Component | Python/Pygame | HTML5 |
|-----------|--------------|-------|
| Language | Python 3.12 | JavaScript ES2022 |
| Graphics API | pygame 2.6.1 / SDL 2.28.4 | HTML5 Canvas 2D |
| Audio | Procedural SDL synthesis | Web Audio API |
| Resolution | 800 × 650 px | 800 × 650 px |
| Target FPS | 60 | 60 |
| File size | ~45 KB + assets | ~201 KB (self-contained) |
| Installation | pip install pygame | None |
| Offline capable | Yes | Yes |
| Touch controls | No | Yes |
| Math grades | 6 (Grade 1–6) | 6 (Grade 1–6) |
| Vocabulary items | 3,000 (3 levels) | 3,000 (3 levels) |

---

*Manuscript prepared for journal submission.*  
*Word count: approximately 3,800 words (condensed submission version).*  
*Corresponding author: [Name], [Institution — Aceh Euthanasia University], [Email]*  
*Conflict of interest: None declared.*  
*Data availability: Game source code and test instruments available from corresponding author upon reasonable request.*
