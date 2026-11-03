# Progress

Read `MASTER_PLAN.md` first. Then continue from **Next up**.

## Next up

**Part 1, Chapter 9 — Simulation or real hardware: what you need (and what is optional).**
File: `part-01-welcome-to-robots/ch009-simulation-or-real-hardware.md`, code and `figures.py` in `code/ch009/`, figures in `images/ch009/`.
Promised by Ch 8 "Next chapter": plan the reader's path; what you can do with only a computer (every chapter has a
simulation track), what a first hardware kit for Rover contains and roughly what it costs (use ROBOTS.md shopping list
and prices; Rover's parts from Ch 5: 6 × AA NiMH, switch, 4 A slow fuse (Ch 7), e-stop, 5 V regulator, TB6612,
Arduino, bumpers, line sensor, distance sensor, 2 gearmotors with encoders, caster; Pi + camera at stage 7), how to
choose parts safely and cheaply (Ch 7 safety: no mains, low voltage, NiMH before LiPo). Good program idea: a shopping
/ budget calculator over a parts list. Keep it shorter (~7,000–8,000 words).

## Chapters done

| Ch | File | Words | Code / figures |
|---|---|---|---|
| 1 | part-01-welcome-to-robots/ch001-how-to-use-this-book.md | 8,570 | code/ch001/first_look.py, robot_trip.py, figures.py → images/ch001/fig01–fig06 |
| 2 | part-01-welcome-to-robots/ch002-what-is-a-robot.md | 10,580 | code/ch002/wall_stop.py, cliff_check.py, stop_distance.py, figures.py → images/ch002/fig01–fig06 |
| 3 | part-01-welcome-to-robots/ch003-a-short-history-of-robots.md | 11,380 | code/ch003/governor.py, tortoise.py, figures.py → images/ch003/fig01–fig06 |
| 4 | part-01-welcome-to-robots/ch004-kinds-of-robots.md | 10,590 | code/ch004/choose_robot.py, robot_range.py, figures.py → images/ch004/fig01–fig07 |
| 5 | part-01-welcome-to-robots/ch005-parts-of-a-robot.md | 9,150 | code/ch005/power_budget.py, centre_of_mass.py, figures.py → images/ch005/fig01–fig06 |
| 6 | part-01-welcome-to-robots/ch006-how-a-robot-thinks.md | 9,420 | code/ch006/catch.py, wall_proportional.py, follow.py, figures.py → images/ch006/fig01–fig07 |
| 7 | part-01-welcome-to-robots/ch007-safety-first.md | 13,650 | code/ch007/watchdog.py, e_stop_distance.py, prop_tip.py, figures.py → images/ch007/fig01–fig08 |
| 8 | part-01-welcome-to-robots/ch008-setting-up-your-computer.md | 9,230 | code/ch008/hello_robot.py, hello_error.py, hello_syntax.py, check_setup.py, plot_catch.py, figures.py → images/ch008/fig01–fig06 (fig05 = real output of plot_catch.py) |

## Notes for writers

- Ch 1 set these reader expectations: 📖 word list at the back of the notebook; folders `robotics/my-code/chNNN/`;
  5 safety rules (simulation first, a way to stop, start slow, no propellers on the table, respect batteries);
  colour meanings (setpoint black dashed, output blue, error red, control green, robot orange, obstacles grey).
- Ch 1 forward references to keep true: Ch 54 (float rounding, `0.4 * 3 = 1.2000000000000002`), Ch 63 (a ≤ μ·g, load
  sliding on a warehouse robot), Ch 7 and Ch 89 (battery safety).
- Ch 2 defined: the **robot test** (4 questions: senses? thinks by itself? acts by moving? loops?); tool / automatic
  machine / robot; a thermostat is a *controller*, not a robot; open loop vs closed loop (feedback); setpoint;
  autonomy vs teleoperation; "blind distance" between loops = speed × loop time; loop-rate figure (thermostat 0.2/s,
  vacuum ~50, warehouse ~100, arm ~1,000, drone ~2,000). Room model used: new T = T + heat − 0.05 × (T − outside).
  Forward refs to keep: Ch 59 (braking distance grows with speed², warehouse table 0.50/1.13/2.00 m), Ch 52 (log scale),
  Ch 208 (on-off zigzag), Ch 250 (loop rate maths), Ch 641–643 (drone tilt loop), Ch 744 (safety fields).
- Ch 3 used: S/T/A tags for milestones; governor model `speed += 10 × (2.0 × valve − load × speed / 100)` with
  valve = 0.5 + 0.02 × (100 − speed) → settles at 90.9 (open loop 66.7) — Ch 211 must explain this steady-state error,
  Ch 212 removes it. Tortoise model: brightness = 1/(1 + d²), sensors ±30° at 0.2 m, turn = 400 × (left − right);
  start C (facing away) gets lost; gain 50 → passes the lamp and leaves (4.4 m away after 100 steps); gain −400 → flees
  (11 m). Lab 3.3 left an open challenge: `turn_gain = 4000` (test it once Python is installed, Ch 8+).
  Forward refs: Ch 93 Moth, Ch 292–295 line/wall following, Ch 454 A*, Ch 744 safety, Ch 745 ethics.
- Ch 4 introduced: DOF (6 free in space, 3 on a floor, 1 per simple joint; arm ≈ 7 for a human arm); link, joint,
  end effector, cobot, multirotor, tether, centre of mass, support polygon (static stability rule); differential drive
  forward speed = (left + right) ÷ 2; W and Wh with time = energy ÷ power (example values 1 kg robots: wheeled 10 W
  1 m/s, legged 40 W 1 m/s, flying 150 W 10 m/s, 50 Wh → 300/75/20 min, 18/4.5/12 km); weighted score table
  (decision matrix) with the "forgot 'sees from above'" lesson; drone survey 50 Wh, 75% usable, 150 W, 8 m/s, 40 m strip
  → 28.8 ha. No dedicated underwater part: underwater ideas live in 🌊 applications.
  Forward refs: Ch 70, 67, 122, 146, 150, 270 (MPC), 284, 285, 301–309, 334, 344, 348–349, 368, 370, 390, 476,
  594, 615, 624, 630, 668, 671, 687–690, 740–743, 749.
- Ch 5 fixed Rover's design (stage 3): 6 × AA NiMH 7.2 V 2.0 Ah = 14.4 Wh (80% usable = 11.52 Wh), switch + fuse,
  5 V regulator (brain + sensors), TB6612 driver fed 7.2 V direct, Arduino, bumpers, line sensor, distance sensor,
  2 gearmotors with encoders, caster at −9 cm behind the axle. Typical watts: Arduino 0.25, driver 0.3, motors 3.0,
  line 0.15, distance 0.08 → 3.78 W → 3.05 h; stage 7 adds Pi 4.0 + camera 1.0 → 8.78 W → 79 min.
  Masses: chassis 150 g (−3), motors+wheels 160 (0), Arduino+driver 35 (−4), sensors 30 (+7), battery 165 (−5 back)
  → CoM −2.23 cm (battery front +5 → +0.82, tips). Rover loop 50 Hz = 20 ms (sense 2, think 1, send 0.5 ms).
  Taught: signal vs power wires, common ground, digital/analog/PWM, two-level brains, Wh = V × Ah (trust until Ch 89),
  CoM = Σ m·x ÷ Σ m (Ch 70 full), "moment" word (Ch 65). Diagram colours here: power = thick black, signal = blue,
  motor power = green.
- Ch 6 defined the control-loop vocabulary (setpoint, measurement, error = setpoint − measurement, controller,
  command, actuator, system/plant, output, disturbance, gain, overshoot, delay, steady-state error) and proportional
  control (command = gain × error) as a PREVIEW of Ch 210. Key rule taught: for x += gain·(sp − x)·dt the "fraction per
  loop" gain·dt should be well below 1 and must be < 2. Results to stay consistent with: catch gain 4, dt 0.05 → 1.186 m
  at 1 s; gains 1/30/45 → 0.77 / settles / unstable (2.7, −0.675, 3.544); 0.2 s delay with gain 4 → peak 1.68, dip 1.02;
  gain 8 + delay unstable; follower error = v ÷ gain (gain 2 → 1.5 m, gain 5 → 1.2 m); feedforward removes the gap
  (Ch 227); chase vs aim: 0.90 vs 1.19 m. Rover wall with P (gain 1, dt 0.5, limit 0.25) → 0.301 m, no overshoot.
  Ruler-drop table (Ch 59 formula): 5/10/15/20/25/30 cm → 0.10/0.14/0.18/0.20/0.23/0.25 s.
  Forward refs: 103, 210–216, 212, 218–219, 227, 228, 270, 298, 306, 310–312, 385, 416, 637.
- Ch 7 defined hazard, risk = how likely × how bad (1–3 each; 1–2 low, 3–4 medium, 6–9 high), mains vs low voltage
  (water picture: voltage = how hard the pump pushes, current = how much flows; dry skin = narrow pipe), short circuit,
  fuse rules (near battery on +, above peak and below wire limit, never replace with bigger/wire), lithium types table,
  thermal runaway as a GROWING loop (×1.5 per round picture), LiPo 4.2 V full / 3.8 V storage per cell, coin-cell
  swallowing danger, pinch points, fail-safe brakes, propeller rules, tools table, e-stop 6 properties (red on yellow,
  reachable, mushroom, latching, cuts MOTOR power with a real switch while brain stays on, release does not restart),
  two stop kinds (cut at once / brake then cut = stop cat. 0 / 1, Ch 744), drone arm/disarm + failsafe + kill switch,
  "safe state depends on the robot", watchdog/heartbeat ("if I hear nothing, I stop"), 5 safety layers (design,
  software, sensors, hardware, people), 8-item pre-power checklist incl. "wheels up". Rover now has an e-stop in the
  MOTOR power path (after the regulator split; 2nd contact to an Arduino pin) and a 4 A slow fuse (normal 0.53 A,
  start peak 3.1 A = 2 × 1.5 A + 0.1, wires ~5 A, current = power ÷ voltage preview of Ch 76).
  Results: watchdog (0.5 m/s, dt 0.1, link lost step 20, 3 silent loops) → STOP at 2.2 s, 0.1 m vs 1.55 m without;
  e-stop totals at 1.5 m/s: 1.535 / 2.66 / 5.66 m (human 0.25/1.0/3.0 s, circuit 0.02 s) vs own sensor 1.355 m;
  prop tips: toy 62.8, racing 199.5 (500 turns/s), camera 88.0, farm 119.4 m/s; saw ~55, motorway 33 m/s;
  cobot zone 1.6 m/s × 0.6 s + 0.2 + 0.1 ≈ 1.3 m (simplified; real rule Ch 744); battery room 40 × 100 Wh, 6S
  25.2 / 22.8 V. Introduced π = 3.14159 and circumference = π × d (Ch 48 full), rpm ÷ 60, m/s × 3.6 = km/h.
  Forward refs: 26, 48, 59, 67, 68, 73–93, 76, 80, 81, 87–88, 89, 92, 129, 151, 385, 523, 544, 615, 618, 621, 640,
  718, 729, 743, 744. Ch 7 ran long (~13,650 words): Part 1 chapters keep growing; aim shorter for Ch 8–12.
- Ch 8 set up: Python ≥ 3.12 (tested 3.14), Thonny (beginners) or VS Code + Python extension; `python` on Windows
  (`py` also), `python3` on macOS/Linux; `python -m pip install numpy matplotlib`; Linux "externally-managed-
  environment" → venv `~/robotics-venv` (source …/activate each terminal). Terminal commands taught: pwd, dir/ls, cd,
  cd .., mkdir (mkdir -p), python file.py, Tab, ↑, Ctrl+C ("software e-stop", not enough on a real robot). Rules for
  file names (lowercase, _, no spaces, not a library name, start with a letter). Four steps to read an error (last
  line, line number, ^^^, fix/save/run); error table (SyntaxError, NameError, IndentationError, TypeError,
  ModuleNotFoundError, ZeroDivisionError). Introduced (lightly): comment, print, variable, import, `as plt`, list
  `.append`, indexing from 0, `str()`, `**`, plt.plot/axhline/xlabel/ylabel/title/legend/savefig/show.
  Results: plot_catch gains 1/4/30 at 1.0 s → 0.77 / 1.186 / 1.2 m (Ch 6 table fixed from 0.79 to 0.77);
  gain 20 → 1.2 in one loop; 39 swings (0.77 at 1 s); 45 unstable (−102.9 at 1 s); watchdog max_silent 10 → STOP
  2.9 s, 0.45 m; max_silent 1 → 2.0 s, 0.0 m. Application 1: requirements.txt, version comparison (3.10 > 3.9).
  Forward refs: 11, 12, 13, 14, 15, 18, 21, 25, 26, 27, 33, 34–35, 96, 111, 112, 214, 549, 554, 639, Part 27/28.
- Chapter length: theory chapters with the full 🏭 applications section come out at ~10,000 words (Ch 2: 10,580).
  That matches MASTER_PLAN §2 (base + 2,000–3,000 for applications) only loosely; it is on the long side, not short.
- Figures: the matplotlib default font has no emoji, so do not put emoji inside figures (only in the Markdown text).
- Ch 1 is 8,570 words, above the 5,500–6,500 target for normal chapters. That is fine for an introduction chapter, but
  keep later Part 1 chapters nearer the target.

## Status

- 2026-11-03: Chapter 8 written (setup, terminal, errors, first plot; 6 figures, 5 programs). Ch 6 gain-1 value corrected 0.79 → 0.77.
- 2026-11-03: Chapter 7 written (safety, e-stop, watchdog; 8 figures, 3 programs).
- 2026-11-03: Chapter 1 written. `matplotlib` 3.11 and `numpy` 2.5 installed (Python 3.14).
- 2026-11-03: Every theory chapter gets a 🏭 Real robot applications section (MASTER_PLAN §5.2): at least 5 applications from at least 3 fields, 2 worked in full. Catalogue in `APPLICATIONS.md`. Estimate now about 21,000 pages.
- 2026-11-03: Full tutorials added: Part 30 Drones (53 ch), Part 31 Legged robots (24 ch), Part 32 Humanoids (48 ch), all under the lecture and figure rules. Robots Hero and Buddy added to `ROBOTS.md`. The course now has 33 parts, 749 chapters, about 16,500 pages.
- 2026-11-03: More practice: 24 project chapters added (now 631 chapters, about 13,500 pages), `ROBOTS.md` lists the 26 robots, and every chapter gets a 🔧 hands-on lab (MASTER_PLAN §5.1).
- 2026-11-03: Control split into 3 parts (PID; classical analysis; state-space, LQR, MPC, nonlinear). Mobile robots, frames, arms, IK, dynamics, trajectories and planning expanded. Lecture and figure rules added (MASTER_PLAN §6). The course had 30 parts, 607 chapters.
- 2026-11-03: Parts 24–28 added (real-time and protocols with CAN, ROS 2, four simulators, ROS 2 in practice).
- 2026-11-03: Syllabus (`README.md`), rules (`MASTER_PLAN.md`) and this file were written.
