# Progress

Read `MASTER_PLAN.md` first. Then continue from **Next up**.

## Next up

**Part 1, Chapter 5 — The parts of a robot: body, sensors, brain, actuators, power.**
File: `part-01-welcome-to-robots/ch005-parts-of-a-robot.md`, code and `figures.py` in `code/ch005/`, figures in `images/ch005/`.
Promised by Ch 4 "Next chapter": open a robot and look inside; the five main parts every robot has (body, sensors,
brain, actuators, power); how they connect with wires and signals; the reader draws the complete **block diagram of
Rover**. Good applications: a power budget (W, Wh, time = energy ÷ power from Ch 4), weight budget, signal paths.

## Chapters done

| Ch | File | Words | Code / figures |
|---|---|---|---|
| 1 | part-01-welcome-to-robots/ch001-how-to-use-this-book.md | 8,570 | code/ch001/first_look.py, robot_trip.py, figures.py → images/ch001/fig01–fig06 |
| 2 | part-01-welcome-to-robots/ch002-what-is-a-robot.md | 10,580 | code/ch002/wall_stop.py, cliff_check.py, stop_distance.py, figures.py → images/ch002/fig01–fig06 |
| 3 | part-01-welcome-to-robots/ch003-a-short-history-of-robots.md | 11,380 | code/ch003/governor.py, tortoise.py, figures.py → images/ch003/fig01–fig06 |
| 4 | part-01-welcome-to-robots/ch004-kinds-of-robots.md | 10,590 | code/ch004/choose_robot.py, robot_range.py, figures.py → images/ch004/fig01–fig07 |

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
- Chapter length: theory chapters with the full 🏭 applications section come out at ~10,000 words (Ch 2: 10,580).
  That matches MASTER_PLAN §2 (base + 2,000–3,000 for applications) only loosely; it is on the long side, not short.
- Figures: the matplotlib default font has no emoji, so do not put emoji inside figures (only in the Markdown text).
- Ch 1 is 8,570 words, above the 5,500–6,500 target for normal chapters. That is fine for an introduction chapter, but
  keep later Part 1 chapters nearer the target.

## Status

- 2026-11-03: Chapter 1 written. `matplotlib` 3.11 and `numpy` 2.5 installed (Python 3.14).
- 2026-11-03: Every theory chapter gets a 🏭 Real robot applications section (MASTER_PLAN §5.2): at least 5 applications from at least 3 fields, 2 worked in full. Catalogue in `APPLICATIONS.md`. Estimate now about 21,000 pages.
- 2026-11-03: Full tutorials added: Part 30 Drones (53 ch), Part 31 Legged robots (24 ch), Part 32 Humanoids (48 ch), all under the lecture and figure rules. Robots Hero and Buddy added to `ROBOTS.md`. The course now has 33 parts, 749 chapters, about 16,500 pages.
- 2026-11-03: More practice: 24 project chapters added (now 631 chapters, about 13,500 pages), `ROBOTS.md` lists the 26 robots, and every chapter gets a 🔧 hands-on lab (MASTER_PLAN §5.1).
- 2026-11-03: Control split into 3 parts (PID; classical analysis; state-space, LQR, MPC, nonlinear). Mobile robots, frames, arms, IK, dynamics, trajectories and planning expanded. Lecture and figure rules added (MASTER_PLAN §6). The course had 30 parts, 607 chapters.
- 2026-11-03: Parts 24–28 added (real-time and protocols with CAN, ROS 2, four simulators, ROS 2 in practice).
- 2026-11-03: Syllabus (`README.md`), rules (`MASTER_PLAN.md`) and this file were written.
